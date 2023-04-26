from datetime import datetime as dt
from functools import partial
from itertools import chain
from typing import Annotated, Union, Optional, List
from uuid import uuid4
import json


import fastapi
from fastapi import Body, FastAPI, Response, Request, middleware, exceptions
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .api_models import ChatCompletionInput, CompletionInput, EmbeddingInput, InstructionInput
from .dummy import dummy_chat, dummy_complete, dummy_edit, dummy_embedding, dummy_engine
from .models import get_model, get_model_infos, list_models
from .utils import (
    add_instructions,
    format_autocompletion_response,
    format_autocompletion_stream_response,
    format_chat_delta_response,
    format_chat_response,
    format_edits_response,
    format_embeddings_results,
)

from pydantic import BaseModel

import logging

logger = logging.getLogger("fastapi")


app = FastAPI(
    title="Leapfrog AI",
    description="A self-hosted alternative API to the not so Open one",
    version="0.0.1",
    contact={
        "name": "TOMMY",
        "url": "https://github.com/defenseunicorns",
    },  

)

# @app.middleware("http")
# async def log_stuff(request: Request, call_next):
#     logger.error(f"{request.method} {request.url}")
#     logger.error(f"{ request }")
#     logger.error(f"Headers: { request.headers }")
#     b = await request.body()
#     logger.error(f"Request Body: { b }")
#     response = await call_next(request)
#     # logger.error(response)
#     # logger.error(response.status_code)
#     return response

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    print(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

async def http422_error_handler(
    _: Request, exc: Union[exceptions.RequestValidationError, ValidationError]
) -> JSONResponse:
    await print(_.json())
    return JSONResponse(
        {"errors": exc.errors()}, status_code=exceptions.HTTP_422_UNPROCESSABLE_ENTITY
    )

app.add_exception_handler(ValidationError, http422_error_handler)
app.add_exception_handler(exceptions.RequestValidationError, http422_error_handler)
app.debug = True

# Models
@app.get("/models/")
async def show_models():
    return list_models()


@app.get("/models/{model_id}")
async def show_model(model_id: str):
    return get_model_infos(model_id)


# Completions
@app.post("/completions")
async def complete(
    body: Annotated[CompletionInput, Body(example=dummy_complete)],
    background_tasks: fastapi.background.BackgroundTasks,
):
    assert body.logprobs <= 5

    prompt = body.prompt
    if isinstance(prompt, list):
        assert len(body.prompt) == 1, "unsupported, at most 1 prompt allowed"
        prompt = body.prompt[0]

    llm = get_model(model_id=body.model)
    if not body.stream:
        predictions = llm.complete(
            prompt=prompt,
            suffix=body.suffix,
            max_tokens=body.max_tokens,
            temperature=body.temperature,
            top_p=body.top_p,
            n=body.n,
            stream=body.stream,
            logprobs=body.logprobs,
            echo=body.echo,
            stop=body.stop,
            presence_penalty=body.presence_penalty,
            frequence_penalty=body.frequence_penalty,
            best_of=body.best_of,
            logit_bias=body.logit_bias,
        )
        output = format_autocompletion_response(model_name=llm.name, predictions=predictions)
        return output

    predictions_stream = llm.stream_complete(
        prompt=prompt,
        suffix=body.suffix,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        top_p=body.top_p,
        n=body.n,
        stream=body.stream,
        logprobs=body.logprobs,
        echo=body.echo,
        stop=body.stop,
        presence_penalty=body.presence_penalty,
        frequence_penalty=body.frequence_penalty,
        best_of=body.best_of,
        logit_bias=body.logit_bias,
    )
    background_tasks.add_task(lambda f: f.close(), predictions_stream)

    uuid = uuid4().hex
    current_timestamp = int(dt.now().timestamp())
    postprocessed = map(
        partial(format_autocompletion_stream_response, current_timestamp, uuid, body.model),
        predictions_stream,
    )
    with_finaliser = chain(postprocessed, ("data: [DONE]\n",))
    return StreamingResponse(with_finaliser, media_type="text/event-stream")


# Chat / completions
@app.post("/chat/completions")
async def chat_complete(
    body: Annotated[ChatCompletionInput, Body(example=dummy_chat)],
    response: Response,
    background_tasks: fastapi.background.BackgroundTasks,
):
    llm = get_model(model_id=body.model, task="chat")
    messages = [[message.get("role", ""), message.get("content", "")] for message in body.messages]
    if not body.stream:
        predictions = llm.chat(
            messages=messages,
            temperature=body.temperature,
            top_p=body.top_p,
            n=body.n,
            stream=body.stream,
            max_tokens=body.max_tokens,
            stop=body.stop,
            presence_penalty=body.presence_penalty,
            frequence_penalty=body.frequence_penalty,
            logit_bias=body.logit_bias,
        )

        output = format_chat_response(model_name=llm.name, predictions=predictions)
        return output

    predictions_stream = llm.stream(
        messages=messages,
        temperature=body.temperature,
        top_p=body.top_p,
        n=body.n,
        stream=body.stream,
        max_tokens=body.max_tokens,
        stop=body.stop,
        presence_penalty=body.presence_penalty,
        frequence_penalty=body.frequence_penalty,
        logit_bias=body.logit_bias,
    )

    background_tasks.add_task(lambda f: f.close(), predictions_stream)

    uuid = uuid4().hex
    current_timestamp = int(dt.now().timestamp())
    postprocessed = map(
        partial(format_chat_delta_response, current_timestamp, uuid, body.model), predictions_stream
    )

    with_finaliser = chain(postprocessed, ("data: [DONE]\n",))
    return StreamingResponse(with_finaliser, media_type="text/event-stream")


# Edits
@app.post("/edits/")
async def edit(body: Annotated[InstructionInput, Body(example=dummy_edit)]):
    llm = get_model(model_id=body.model)
    input_text = add_instructions(instructions=body.instruction, text=body.input)

    predictions = llm.complete(
        prompt=input_text,
        temperature=body.temperature,
        top_p=body.top_p,
        n=body.n,
        max_tokens=body.max_tokens,
    )
    output = format_edits_response(model_name=llm.name, predictions=predictions)
    return output

# Models
@app.get("/embeddings")
async def show_models():
    return list_models()

# Embeddings
@app.post("/embeddings")
async def embed(body: Annotated[EmbeddingInput, Body(example=dummy_embedding)]):
    llm = get_model(model_id=body.model, task="embed")
    if isinstance(body.input, str):
        body.input = [body.input]

    results = llm.embed(inputs=body.input)

    output = format_embeddings_results(model_name=llm.name, embeddings=results)
    return output


class EngineEmbedding(BaseModel):
    encoding_format: Optional[str]
    input:  Union[List[List[int]], list]
    prompt: Optional[List[str]]


import tiktoken

@app.post("/engines/{model_id}/embeddings")
async def embed2(model_id: str, body: Annotated[EngineEmbedding, Body(example=dummy_engine)]):
# async def embed2(model_id: str, body: Annotated[EngineEmbedding, Body(example=dummy_embedding)]):
    logger.error(f"Request for model: { model_id} with body { body }")
    # return "WOOHOO"
    llm = get_model(model_id=model_id, task="embed")
    encoding = tiktoken.model.encoding_for_model(model_id)
    
    body.prompt = [ encoding.decode(input) for input in body.input]
    logger.error(f"Decoded: { body.prompt}")
    

    # results = [llm.embed(inputs=prompt) for prompt in body.prompt]
    results = llm.embed(inputs=body.prompt)
    output = format_embeddings_results(model_name=llm.name, embeddings=results)
    return output

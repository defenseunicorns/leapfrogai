from itertools import chain
from typing import Annotated

from fastapi import Depends, HTTPException
import leapfrogai_sdk as lfai
from leapfrogai_api.backends.openai import router
from leapfrogai_api.backends.openai.grpc_client import (
    chat_completion,
    completion,
    create_embeddings,
    create_transcription,
    stream_chat_completion,
    stream_completion,
)
from leapfrogai_api.backends.openai.helpers import grpc_chat_role, read_chunks
from leapfrogai_api.backends.openai.types import (
    ChatCompletionRequest,
    CompletionRequest,
    CreateEmbeddingRequest,
    CreateEmbeddingResponse,
    CreateTranscriptionRequest,
    CreateTranscriptionResponse,
    ModelResponse,
    ModelResponseModel,
)
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.utils.config import Config


@router.post("/completions")
async def complete(
    req: CompletionRequest, model_config: Annotated[Config, Depends(get_model_config)]
):
    # Get the model backend configuration
    model = model_config.get_model_backend(req.model)
    if model is None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    request = lfai.CompletionRequest(
        prompt=req.prompt,  # type: ignore
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_completion(model, request)
    else:
        return await completion(model, request)


@router.post("/chat/completions")
async def chat_complete(
    req: ChatCompletionRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
):
    # Get the model backend configuration
    model = model_config.get_model_backend(req.model)
    if model is None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    chat_items: list[lfai.ChatItem] = []
    for m in req.messages:
        chat_items.append(lfai.ChatItem(role=grpc_chat_role(m.role), content=m.content))
    request = lfai.ChatCompletionRequest(
        chat_items=chat_items,
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_chat_completion(model, request)
    else:
        return await chat_completion(model, request)


@router.get("/models")
async def models(
    model_config: Annotated[Config, Depends(get_model_config)],
) -> ModelResponse:
    res = ModelResponse()
    for model in model_config.models:
        m = ModelResponseModel(id=model)
        res.data.append(m)
    return res


@router.post("/embeddings")
async def embeddings(
    req: CreateEmbeddingRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
) -> CreateEmbeddingResponse:
    # Get the model backend configuration
    model = model_config.get_model_backend(req.model)
    if model is None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    if isinstance(req.input, str):
        request = lfai.EmbeddingRequest(inputs=[req.input])
    # elif isinstance(req.input, list) and all(isinstance(i, str) for i in req.input):
    # request = lfai.EmbeddingRequest(inputs=req.input)
    else:
        raise HTTPException(
            status_code=405,
            detail=f"Invalid input type {type(req.input)}. Currently supported types are str and list[str]",
        )

    return await create_embeddings(model, request)


@router.post("/audio/transcriptions")
async def transcribe(
    model_config: Annotated[Config, Depends(get_model_config)],
    req: CreateTranscriptionRequest = Depends(CreateTranscriptionRequest.as_form),
) -> CreateTranscriptionResponse:
    # Get the model backend configuration
    model = model_config.get_model_backend(req.model)
    if model is None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    # Create a request that contains the metadata for the AudioRequest
    audio_metadata = lfai.AudioMetadata(
        prompt=req.prompt, temperature=req.temperature, inputlanguage=req.language
    )
    audio_metadata_request = lfai.AudioRequest(metadata=audio_metadata)

    # Read the file and get an iterator of all the data chunks
    chunk_iterator = read_chunks(req.file.file, 1024)

    # combine our metadata and chunk_data iterators
    request_iterator = chain((audio_metadata_request,), chunk_iterator)

    return await create_transcription(model, request_iterator)

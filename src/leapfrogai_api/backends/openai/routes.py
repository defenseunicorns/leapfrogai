from itertools import chain
from typing import Annotated

from fastapi import Depends, HTTPException
from leapfrogai_api import types
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
    DeleteFileRequest,
    DeleteFileResponse,
    ListFilesRequest,
    ListFilesResponse,
    ModelResponse,
    ModelResponseModel,
    RetrieveFileContentRequest,
    RetrieveFileContentResponse,
    RetrieveFileRequest,
    RetrieveFileResponse,
    UploadFileRequest,
    UploadFileResponse,
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

    request = types.CompletionRequest(
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

    chat_items: list[types.ChatItem] = []
    for m in req.messages:
        chat_items.append(
            types.ChatItem(role=grpc_chat_role(m.role), content=m.content)
        )
    request = types.ChatCompletionRequest(
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
        request = types.EmbeddingRequest(inputs=[req.input])
    # elif isinstance(req.input, list) and all(isinstance(i, str) for i in req.input):
    # request = types.EmbeddingRequest(inputs=req.input)
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
    audio_metadata = types.AudioMetadata(
        prompt=req.prompt, temperature=req.temperature, inputlanguage=req.language
    )
    audio_metadata_request = types.AudioRequest(metadata=audio_metadata)

    # Read the file and get an iterator of all the data chunks
    chunk_iterator = read_chunks(req.file.file, 1024)

    # combine our metadata and chunk_data iterators
    request_iterator = chain((audio_metadata_request,), chunk_iterator)

    return await create_transcription(model, request_iterator)

@router.post("/files")
async def files(request: UploadFileRequest = Depends(UploadFileRequest.as_form)) -> UploadFileResponse:
    # TODO: https://github.com/defenseunicorns/leapfrogai/issues/286
    raise HTTPException(
        status_code=501,
        detail=f"POST {request.file.filename}: This endpoint is not implemented yet."
    )

@router.get("/files")
async def files(request: ListFilesRequest = Depends(ListFilesRequest.as_form)) -> ListFilesResponse:
    # TODO: https://github.com/defenseunicorns/leapfrogai/issues/287
    raise HTTPException(
        status_code=501,
        detail=f"GET {request.purpose} Files: This endpoint is not implemented yet."
    )

@router.get("/files/{file_id}")
async def files(request: RetrieveFileRequest) -> RetrieveFileResponse:
    # TODO: https://github.com/defenseunicorns/leapfrogai/issues/338
    raise HTTPException(
        status_code=501,
        detail=f"GET {request.file_id} File: This endpoint is not implemented yet."
    )

@router.delete("/files/{file_id}")
async def files(request: DeleteFileRequest) -> DeleteFileResponse:
    # TODO: https://github.com/defenseunicorns/leapfrogai/issues/339
    raise HTTPException(
        status_code=501,
        detail=f"DELETE {request.file_id} File: This endpoint is not implemented yet."
    )

@router.get("/files/{file_id}/content")
async def files(request: RetrieveFileContentRequest) -> RetrieveFileContentResponse:
    # TODO: https://github.com/defenseunicorns/leapfrogai/issues/289
    raise HTTPException(
        status_code=501,
        detail=f"GET {request.file_id} File Content: This endpoint is not implemented yet."
    )

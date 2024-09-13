"""This module contains the audio router for the OpenAI API."""

from itertools import chain
from typing import Annotated
from fastapi import HTTPException, APIRouter, Depends

from leapfrogai_api.backend.grpc_client import create_transcription, create_translation
from leapfrogai_api.backend.helpers import read_chunks
from leapfrogai_api.typedef.audio import (
    CreateTranscriptionRequest,
    CreateTranscriptionResponse,
    CreateTranslationRequest,
)
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.utils.config import Config
import leapfrogai_sdk as lfai

router = APIRouter(prefix="/openai/v1/audio", tags=["openai/audio"])


@router.post("/transcriptions")
async def transcribe(
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
    model_config: Annotated[Config, Depends(get_model_config)],
    req: CreateTranscriptionRequest = Depends(CreateTranscriptionRequest.as_form),
) -> CreateTranscriptionResponse:
    """Create a transcription from the given audio file."""
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


@router.post("/translations")
async def translate(
    session: Session,
    model_config: Annotated[Config, Depends(get_model_config)],
    req: CreateTranslationRequest = Depends(CreateTranslationRequest.as_form),
) -> CreateTranscriptionResponse:
    """Create a translation to english from the given audio file."""
    model = model_config.get_model_backend(req.model)
    if model is None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    # Create a request that contains the metadata for the AudioRequest
    audio_metadata = lfai.AudioMetadata(prompt=req.prompt, temperature=req.temperature)
    audio_metadata_request = lfai.AudioRequest(metadata=audio_metadata)

    # Read the file and get an iterator of all the data chunks
    chunk_iterator = read_chunks(req.file.file, 1024)

    # combine our metadata and chunk_data iterators
    request_iterator = chain((audio_metadata_request,), chunk_iterator)

    return await create_translation(model, request_iterator)

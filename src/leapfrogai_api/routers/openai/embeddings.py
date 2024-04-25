"""FastAPI router for OpenAI embeddings API."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from leapfrogai_api.backend.grpc_client import create_embeddings
from leapfrogai_api.backend.types import (
    CreateEmbeddingRequest,
    CreateEmbeddingResponse,
)
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.utils.config import Config
import leapfrogai_sdk as lfai


router = APIRouter(prefix="/openai/v1/embeddings", tags=["openai/embeddings"])


@router.post("")
async def embeddings(
    req: CreateEmbeddingRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
) -> CreateEmbeddingResponse:
    """Create embeddings from the given input."""
    model = model_config.get_model_backend(req.model)
    if model is None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    if isinstance(req.input, str):
        request = lfai.EmbeddingRequest(inputs=[req.input])
    else:
        raise HTTPException(
            status_code=405,
            detail=f"Invalid input type {type(req.input)}. Currently supported types are str and list[str]",
        )

    return await create_embeddings(model, request)

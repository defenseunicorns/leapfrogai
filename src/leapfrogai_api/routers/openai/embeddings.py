"""FastAPI router for OpenAI embeddings API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
import leapfrogai_sdk as lfai
from leapfrogai_api.backend.grpc_client import create_embeddings
from leapfrogai_api.backend.types import CreateEmbeddingRequest, CreateEmbeddingResponse
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.__init__ import config as global_config
from leapfrogai_api.utils.config import Config

import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/openai/v1/embeddings", tags=["openai/embeddings"])


@router.post("")
async def embeddings(
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
    req: CreateEmbeddingRequest,
    model_config: Annotated[Config, Depends(global_config.create)],
) -> CreateEmbeddingResponse:
    """Create embeddings from the given input."""
    model = model_config.get_model_backend(model=req.model)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    if isinstance(req.input, str):
        request = lfai.EmbeddingRequest(inputs=[req.input])
    elif list_str := _to_list_of_strs(req.input):
        request = lfai.EmbeddingRequest(inputs=list_str)
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Invalid input type {type(req.input)}. Currently supported types are str and list[str]",
        )

    return await create_embeddings(model, request)


def _to_list_of_strs(v: list) -> list[str]:
    new_list: list[str] = []
    for item in v:
        if not isinstance(item, str):
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail=f"Invalid input type {type(item)}. Currently supported types are str and list[str]",
            )

        new_list.append(item)
    return new_list

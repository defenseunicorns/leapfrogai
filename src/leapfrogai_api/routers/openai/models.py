"""OpenAI models router."""

from typing import Annotated
from fastapi import APIRouter, Depends
from leapfrogai_api.routers.openai.types import (
    ModelResponse,
    ModelResponseModel,
)
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.utils.config import Config

router = APIRouter(prefix="/openai/v1/models", tags=["openai/models"])


@router.get("")
async def models(
    model_config: Annotated[Config, Depends(get_model_config)],
) -> ModelResponse:
    """List all available models."""
    res = ModelResponse()
    for model in model_config.models:
        m = ModelResponseModel(id=model)
        res.data.append(m)
    return res

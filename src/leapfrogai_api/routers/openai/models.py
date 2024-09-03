"""OpenAI compliant models router."""

from fastapi import APIRouter
from leapfrogai_api.typedef.models import (
    ModelResponse,
    ModelResponseModel,
)
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.utils.config import Config

router = APIRouter(prefix="/openai/v1/models", tags=["openai/models"])


@router.get("")
async def models(
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
) -> ModelResponse:
    """List all available models."""
    res = ModelResponse(data=[])
    model_config: Config = get_model_config()
    for model in model_config.models:
        m = ModelResponseModel(id=model)
        res.data.append(m)
    return res

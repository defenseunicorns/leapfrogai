"""OpenAI compliant models router."""

from fastapi import APIRouter
from leapfrogai_api.backend.types import (
    ModelResponse,
    ModelResponseModel,
    ModelMetadataResponse,
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
    for model_name, model_data in model_config.models.items():
        meta = ModelMetadataResponse(
            type=model_data.metadata.type,
            dimensions=model_data.metadata.dimensions,
            precision=model_data.metadata.precision,
            capabilities=model_data.metadata.capabilities,
        )
        m = ModelResponseModel(
            id=model_name,
            metadata=meta,
        )
        res.data.append(m)
    return res

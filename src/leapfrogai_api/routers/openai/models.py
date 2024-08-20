"""OpenAI compliant models router."""

from fastapi import APIRouter
from leapfrogai_api.backend.types import (
    ModelResponse,
    ModelResponseModel,
    ModelMetadataResponse,
)
from typing import TYPE_CHECKING
from leapfrogai_api.routers.supabase_session import Session

import logging

logger = logging.getLogger(__file__)
if TYPE_CHECKING:
    from leapfrogai_api.utils.config import Config

router = APIRouter(prefix="/openai/v1/models", tags=["openai/models"])


@router.get("")
async def models(
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
) -> ModelResponse:
    """List all available models."""
    res = ModelResponse(data=[])
    # shared config object from the app
    model_config: "Config" = session.app.state.config

    for model_name, model_data in model_config.models.items():
        meta = ModelMetadataResponse(**dict(model_data.metadata))
        m = ModelResponseModel(
            id=model_name,
            metadata=meta,
        )
        res.data.append(m)
    return res

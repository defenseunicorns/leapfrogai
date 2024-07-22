from fastapi import APIRouter
from leapfrogai_api.utils import get_model_config

router = APIRouter(prefix="/leapfrogai/v1/models", tags=["leapfrogai/models"])


@router.get("/")
async def models():
    """List all the models."""
    return get_model_config()

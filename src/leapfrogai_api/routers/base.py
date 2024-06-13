"""Base router for the API."""

from fastapi import APIRouter
from leapfrogai_api.utils import get_model_config

router = APIRouter(tags=["/"])


@router.get("/healthz")
async def healthz():
    """Health check endpoint."""
    return {"status": "ok"}


@router.get("/models")
async def models():
    """List all the models."""
    return get_model_config()

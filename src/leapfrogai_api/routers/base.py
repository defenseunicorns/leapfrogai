"""Base router for the API."""

from fastapi import APIRouter
from fastapi.security import HTTPBearer
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(tags=["/"])
security = HTTPBearer()


@router.get("/test-api-key-auth")
async def test_api_key_auth(session: Session):
    # TODO: Delete me once api auth is added to the rest of the API
    return {"status": "That's a fine auth you have there."}


@router.get("/healthz")
async def healthz():
    """Health check endpoint."""
    return {"status": "ok"}


@router.get("/models")
async def models():
    """List all the models."""
    return get_model_config()

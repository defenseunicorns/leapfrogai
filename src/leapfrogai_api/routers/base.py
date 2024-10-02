"""Base router for the API."""

from fastapi import APIRouter


router = APIRouter(tags=["/"])


@router.get("/healthz")
async def healthz():
    """Health check endpoint."""
    return {"status": "ok"}

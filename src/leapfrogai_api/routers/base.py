"""Base router for the API."""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["/"])


@router.get("")
async def root():
    """Intercepts the root path and redirects to the API documentation."""
    return RedirectResponse(url="/redoc")


@router.get("/healthz")
async def healthz():
    """Health check endpoint."""
    return {"status": "ok"}

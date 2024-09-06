from typing import Any

from fastapi import APIRouter, Request
import logging


router = APIRouter(prefix="/leapfrogai/v1/models", tags=["leapfrogai/models"])


@router.get("")
async def models(
    request: Request,
) -> dict[str, dict[str, Any]]:
    """List all the models."""
    config = request.app.state.config
    logging.debug(f"CONFIG IN models.py: {config}")
    return config.to_dict()

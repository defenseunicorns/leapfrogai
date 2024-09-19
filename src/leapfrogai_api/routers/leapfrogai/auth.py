"""LeapfrogAI endpoints for Auth."""

import time
from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from pydantic import Field

from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.data.crud_api_key import APIKeyItem, CRUDAPIKey
from leapfrogai_api.typedef.auth import CreateAPIKeyRequest, ModifyAPIKeyRequest


router = APIRouter(prefix="/leapfrogai/v1/auth", tags=["leapfrogai/auth"])


@router.post("/api-keys")
async def create_api_key(
    session: Session,
    request: CreateAPIKeyRequest,
) -> APIKeyItem:
    """
    Create an API key.

    Accessible only with a valid JWT, not an API key.

    WARNING: The API key is only returned once. Store it securely.
    """

    if request.expires_at <= int(time.time()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expiration time."
        )

    new_api_key = APIKeyItem(
        name=request.name,
        id="",  # This is set by the database
        api_key="",  # This is generated during the create operation
        created_at=0,  # This is set by the database
        expires_at=request.expires_at,
    )

    crud_api_key = CRUDAPIKey(session)

    return await crud_api_key.create(new_api_key)


@router.get("/api-keys")
async def list_api_keys(
    session: Session,
) -> list[APIKeyItem]:
    """
    List all API keys.

    Accessible only with a valid JWT, not an API key.
    """

    crud_api_key = CRUDAPIKey(session)

    return await crud_api_key.list()


@router.patch("/api-keys/{api_key_id}")
async def update_api_key(
    session: Session,
    api_key_id: Annotated[str, Field(description="The UUID of the API key.")],
    request: ModifyAPIKeyRequest,
) -> APIKeyItem:
    """
    Update an API key.

    Accessible only with a valid JWT, not an API key.
    """

    crud_api_key = CRUDAPIKey(session)

    api_key = await crud_api_key.get(filters={"id": api_key_id})

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found.",
        )

    if request.expires_at and (
        request.expires_at > api_key.expires_at
        or request.expires_at <= int(time.time())
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid expiration time. New expiration must be in the future but less than the current expiration.",
        )

    updated_api_key = APIKeyItem(
        name=request.name if request.name else api_key.name,
        id=api_key_id,
        api_key="",  # This can't be changed
        created_at=0,  # This can't be changed
        expires_at=request.expires_at if request.expires_at else api_key.expires_at,
    )

    crud_api_key = CRUDAPIKey(session)

    return await crud_api_key.update(api_key_id, updated_api_key)


@router.delete("/api-keys/{api_key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    session: Session,
    api_key_id: Annotated[str, Field(description="The UUID of the API key.")],
):
    """
    Revoke an API key.

    Accessible only with a valid JWT, not an API key.
    """

    crud_api_key = CRUDAPIKey(session)

    if not await crud_api_key.delete(filters={"id": api_key_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found.",
        )

"""LeapfrogAI endpoints for Auth."""

import logging

import time
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from leapfrogai_api.routers.supabase_session import Session
import leapfrogai_api.backend.security.api_key as security

router = APIRouter(prefix="/leapfrogai/v1/auth", tags=["leapfrogai/auth"])

KEY_PREFIX = "lfai"


class CreateAPIKeyRequest(BaseModel):
    """Request body for creating an API key."""

    expires_at: int = Field(
        default=int(time.time()) + 60 * 60 * 24 * 30,
        description="The time at which the API key expires, in seconds since the Unix epoch.",
        examples=[int(time.time()) + 60 * 60 * 24 * 30],  # default to 30 days
    )


@router.post("/create-api-key")
async def create_api_key(
    session: Session,
    request: CreateAPIKeyRequest,
) -> dict[str, str]:
    """Create an API key."""

    user_id: str = (await session.auth.get_user()).user.id
    
    if request.expires_at < time.time():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expiration time.")

    api_key = await generate_and_store_api_key(session, user_id, request.expires_at)

    if not api_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create API key.")
    return {"api_key": api_key}


@router.post("/validate-api-key")
async def validate_api_key(
    session: Session,
    api_key: str,
) -> dict:
    """Validate an API key."""

    prefix, unique_key, checksum = security.parse(api_key)

    if not prefix == KEY_PREFIX:
        logging.warning("Received API key with incorrect prefix")
        return {"valid": False, "details": "Invalid prefix"}
    if not security.validate_checksum(unique_key=unique_key, checksum=checksum):
        logging.warning("Received API key with incorrect checksum")
        return {"valid": False, "details": "Invalid checksum"}

    data, _ = (
        await session.table("api_keys")
        .select("*")
        .eq("api_key", security.encode_unique_key(unique_key=unique_key))
        .execute()
    )
    _, response = data

    if not response:
        return {"valid": False, "details": "API key not found"}
    if response[0]["expires_at"] < time.time():
        return {"valid": False, "details": "API key expired"}
    return {"valid": True}


@router.post("/revoke-api-key")
async def revoke_api_key(
    session: Session,
    api_key: str,
) -> dict[str, str]:
    """Revoke an API key."""

    _, key, _ = security.parse(api_key)

    stored_key = security.encode_unique_key(unique_key=key)

    response = (
        await session.table("api_keys").delete().eq("api_key", stored_key).execute()
    )
    if not response:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to revoke API key.")
    return {"message": "API key revoked."}


@router.get("/list-api-keys")
async def list_api_keys(
    session: Session,
) -> dict[str, list[dict]]:
    """List all API keys."""
    user_id: str = (await session.auth.get_user()).user.id

    data, _ = (
        await session.table("api_keys").select("*").eq("user_id", user_id).execute()
    )
    _, response = data

    return {"api_keys": response}


async def generate_and_store_api_key(
    session: Session, user_id: str, expires_at: int
) -> str:
    """Generate and store an API key."""
    read_once_token, hashed_token = security.generate_api_key()

    data, _ = (
        await session.table("api_keys")
        .insert(
            {
                "user_id": user_id,
                "api_key": hashed_token,
                "expires_at": expires_at,
            }
        )
        .execute()
    )
    _, response = data

    if response:
        return read_once_token

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create API key.")

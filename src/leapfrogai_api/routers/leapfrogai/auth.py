"""LeapfrogAI endpoints for Auth."""

import logging
import time
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from leapfrogai_api.routers.supabase_session_api_key import Session
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


class CreateAPIKeyResponse(BaseModel):
    """Response body for creating an API key."""

    api_key: str = Field(
        description="The API key.",
        examples=["lfai_1234567890abcdef1234567890abcdef_1234"],
    )
    created_at: int = Field(
        description="The time at which the API key was created, in seconds since the Unix epoch.",
        examples=[int(time.time())],
    )
    expires_at: int = Field(
        description="The time at which the API key expires, in seconds since the Unix epoch.",
        examples=[int(time.time()) + 60 * 60 * 24 * 30],  # default to 30 days
    )


@router.post("/create-api-key")
async def create_api_key(
    session: Session,
    request: CreateAPIKeyRequest,
) -> CreateAPIKeyResponse:
    """Create an API key."""

    user_id: str = (await session.auth.get_user()).user.id

    if request.expires_at < time.time():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expiration time."
        )

    response = await _generate_and_store_api_key(session, user_id, request.expires_at)

    api_key = response["api_key"]
    created_at = response["created_at"]
    expires_at = response["expires_at"]

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create API key.",
        )

    return CreateAPIKeyResponse(
        api_key=api_key, created_at=created_at, expires_at=expires_at
    )


@router.post("/validate-api-key")
async def validate_api_key(
    session: Session,
    api_key: str,
) -> dict:
    """Validate an API key."""

    try:
        encoded_key = security.validate_and_encode_api_key(api_key)
    except ValueError:
        logging.warning("Received API key with incorrect format")
        return {"valid": False, "details": "Invalid format"}

    data, _ = (
        await session.table("api_keys").select("*").eq("api_key", encoded_key).execute()
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

    try:
        encoded_key = security.validate_and_encode_api_key(api_key)
    except ValueError as exc:
        logging.warning("Received API key with incorrect format")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid API key format."
        ) from exc

    response = (
        await session.table("api_keys").delete().eq("api_key", encoded_key).execute()
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke API key.",
        )
    return {"message": "API key revoked."}


@router.get("/list-api-keys")
async def list_api_keys(
    session: Session,
):
    """List all API keys."""
    user_id: str = (await session.auth.get_user()).user.id

    data, _ = (
        await session.table("api_keys").select("*").eq("user_id", user_id).execute()
    )
    _, db_response = data

    endpoint_response = []

    for entry in db_response:
        prefix, _, checksum = security.parse_api_key(entry["api_key"])
        endpoint_response.append(
            {
                "api_key": f"{prefix}_****_{checksum}",
                "created_at": entry["created_at"],
                "expires_at": entry["expires_at"],
            }
        )

    return endpoint_response


async def _generate_and_store_api_key(session: Session, user_id: str, expires_at: int):
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
        return {
            "api_key": read_once_token,
            "created_at": response[0]["created_at"],
            "expires_at": response[0]["expires_at"],
        }

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create API key.",
    )

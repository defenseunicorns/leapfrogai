"""LeapfrogAI endpoints for Auth."""

import time
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from leapfrogai_api.routers.supabase_session_api_key import Session
import leapfrogai_api.backend.security.api_key as security

router = APIRouter(prefix="/leapfrogai/v1/auth", tags=["leapfrogai/auth"])

KEY_PREFIX = "lfai"
THIRTY_DAYS = 60 * 60 * 24 * 30  # in seconds


class CreateAPIKeyRequest(BaseModel):
    """Request body for creating an API key."""

    expires_at: int = Field(
        default=int(time.time()) + THIRTY_DAYS,
        description="The time at which the API key expires, in seconds since the Unix epoch.",
        examples=[int(time.time()) + THIRTY_DAYS],
    )


class APIKeyItem(BaseModel):
    """Response body for an API key."""

    id: str
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
        examples=[int(time.time()) + THIRTY_DAYS],
    )


class RevokeAPIKey(BaseModel):
    """Request body for revoking an API key."""

    id: str
    revoked: bool
    message: str


@router.post("/create-api-key")
async def create_api_key(
    session: Session,
    request: CreateAPIKeyRequest,
) -> APIKeyItem:
    """Create an API key."""

    user_id: str = (await session.auth.get_user()).user.id

    if request.expires_at <= int(time.time()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expiration time."
        )

    try:
        api_key_item = await _generate_and_store_api_key(
            session, user_id, request.expires_at
        )
    except HTTPException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create API key.",
        ) from exc

    return api_key_item


@router.post("/revoke-api-key")
async def revoke_api_key(
    session: Session,
    id_: str,
) -> RevokeAPIKey:
    """Revoke an API key."""

    data, _count = await session.table("api_keys").delete().eq("id", id_).execute()

    if not data[1]:
        return RevokeAPIKey(id=id_, revoked=False, message="API key not found.")

    return RevokeAPIKey(id=id_, revoked=True, message="API key revoked.")


@router.get("/list-api-keys")
async def list_api_keys(
    session: Session,
) -> list[APIKeyItem]:
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
            APIKeyItem(
                id=entry["id"],
                api_key=f"{prefix}_****_{checksum}",
                created_at=entry["created_at"],
                expires_at=entry["expires_at"],
            )
        )

    return endpoint_response


async def _generate_and_store_api_key(
    session: Session, user_id: str, expires_at: int
) -> APIKeyItem:
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
        return APIKeyItem(
            id=response[0]["id"],  # This is set by the database
            api_key=read_once_token,
            created_at=response[0]["created_at"],
            expires_at=response[0]["expires_at"],
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create API key.",
    )

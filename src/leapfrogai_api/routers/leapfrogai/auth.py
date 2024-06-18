"""LeapfrogAI endpoints for Auth."""

import hashlib
import secrets
from fastapi import APIRouter, HTTPException
from openai import BaseModel
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/leapfrogai/v1/auth", tags=["leapfrogai/auth"])


class CreateAPIKeyRequest(BaseModel):
    """Request body for creating an API key."""

    expires_at: int


@router.post("/create-api-key")
async def create_api_key(
    session: Session,
    request: CreateAPIKeyRequest,
) -> dict[str, str]:
    """Create an API key."""
    # TODO: Generate a more secure API key
    api_key = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

    user_id: str = (await session.auth.get_user()).user.id

    response = (
        await session.table("api_keys")
        .insert(
            {
                "user_id": user_id,
                "api_key": api_key,
                "expires_at": request.expires_at,
            }
        )
        .execute()
    )

    if not response:
        raise HTTPException(status_code=500, detail="Failed to create API key.")
    return {"api_key": api_key}


@router.post("/revoke-api-key")
async def revoke_api_key(
    session: Session,
    api_key: str,
) -> dict[str, str]:
    """Revoke an API key."""
    response = await session.table("api_keys").delete().eq("api_key", api_key).execute()
    if not response:
        raise HTTPException(status_code=500, detail="Failed to revoke API key.")
    return {"message": "API key revoked."}

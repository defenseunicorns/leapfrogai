"""CRUD Operations for API Keys."""

import time
from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase
import leapfrogai_api.backend.security.api_key as security

THIRTY_DAYS = 60 * 60 * 24 * 30  # in seconds


class APIKeyItem(BaseModel):
    """Response body for an API key."""

    name: str | None = Field(
        description="The name of the API key.",
        examples=["API Key 1"],
    )
    id: str = Field(
        description="The UUID of the API key.",
        examples=["12345678-1234-1234-1234-1234567890ab"],
    )
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


class CRUDAPIKey(CRUDBase[APIKeyItem]):
    """CRUD Operations for API Key"""

    def __init__(self, db: AsyncClient):
        super().__init__(db=db, model=APIKeyItem, table_name="api_keys")

    async def create(self, object_: APIKeyItem) -> APIKeyItem:
        """Create new API key."""

        user_id = await self._get_user_id()

        read_once_token = security.generate_new_api_key()

        # We only care about the unique key for the database
        api_key = security.parse_api_key(read_once_token)

        params = {
            "p_api_key": api_key.unique_key,
            "p_user_id": user_id,
            "p_expires_at": object_.expires_at,
            "p_name": object_.name,
            "p_checksum": api_key.checksum,
        }

        result = await self.db.rpc("insert_api_key", params=params).execute()

        response = result.data

        if response:
            return APIKeyItem(
                name=response[0]["name"],
                id=response[0]["id"],  # This is set by the database
                api_key=read_once_token,
                created_at=response[0]["created_at"],  # This is set by the database
                expires_at=response[0]["expires_at"],
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create API key.",
        )

    async def list(self, filters: dict | None = None) -> list[APIKeyItem]:
        """List API keys."""

        query = self.db.table(self.table_name).select("*")

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        result = await query.execute()

        response = result.data

        try:
            return [
                APIKeyItem(
                    name=item["name"],
                    id=item["id"],
                    api_key=f"{security.KEY_PREFIX}_****_{item['checksum']}",
                    created_at=item["created_at"],
                    expires_at=item["expires_at"],
                )
                for item in response
            ]
        except Exception as exc:
            raise exc

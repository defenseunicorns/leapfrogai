from pydantic import BaseModel, Field
import time

from leapfrogai_api.backend.constants import THIRTY_DAYS_SECONDS


class CreateAPIKeyRequest(BaseModel):
    """Request body for creating an API key."""

    name: str | None = Field(
        default=None,
        description="The name of the API key.",
        examples=["API Key 1"],
    )

    expires_at: int = Field(
        default=int(time.time()) + THIRTY_DAYS_SECONDS,
        description="The time at which the API key expires, in seconds since the Unix epoch.",
        examples=[int(time.time()) + THIRTY_DAYS_SECONDS],
    )


class ModifyAPIKeyRequest(BaseModel):
    """Request body for modifying an API key."""

    name: str | None = Field(
        default=None,
        description="The name of the API key. If not provided, the name will not be changed.",
        examples=["API Key 1"],
    )

    expires_at: int | None = Field(
        default=None,
        description="The time at which the API key expires, in seconds since the Unix epoch. If not provided, the expiration time will not be changed.",
        examples=[int(time.time()) + THIRTY_DAYS_SECONDS],
    )

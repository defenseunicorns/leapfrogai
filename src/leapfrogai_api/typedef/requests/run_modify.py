from pydantic import BaseModel, Field


class ModifyRunRequest(BaseModel):
    """Request object for modifying a run."""

    metadata: dict[str, str] | None = Field(default=None, examples=[{}])

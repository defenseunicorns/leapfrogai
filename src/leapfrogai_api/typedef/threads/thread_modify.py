from openai.types.beta.thread import ToolResources as BetaThreadToolResources
from pydantic import BaseModel, Field


class ModifyThreadRequest(BaseModel):
    """Request object for modifying a thread."""

    tool_resources: BetaThreadToolResources | None = Field(
        default=None, examples=[None]
    )
    metadata: dict | None = Field(default=None, examples=[{}])

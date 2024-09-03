from typing import Literal
from pydantic import BaseModel, Field
from openai.types.beta import Assistant


class ListAssistantsResponse(BaseModel):
    """Response object for listing assistants."""

    object: Literal["list"] = Field(
        default="list",
        description="The type of object. Always 'list' for this response.",
    )
    data: list[Assistant] = Field(description="A list of Assistant objects.")

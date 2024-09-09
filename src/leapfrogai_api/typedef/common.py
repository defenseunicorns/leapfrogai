from pydantic import BaseModel, Field
from leapfrogai_api.typedef.constants import DEFAULT_MAX_COMPLETION_TOKENS


class Usage(BaseModel):
    """Usage object."""

    prompt_tokens: int = Field(
        ..., description="The number of tokens used in the prompt."
    )
    completion_tokens: int | None = Field(
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        description="The number of tokens generated in the completion.",
    )
    total_tokens: int = Field(
        ..., description="The total number of tokens used (prompt + completion)."
    )

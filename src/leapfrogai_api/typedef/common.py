from pydantic import BaseModel, Field
from leapfrogai_api.backend.constants import DEFAULT_MAX_COMPLETION_TOKENS


class MetadataObject:
    """A metadata object that can be serialized back to a dict."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, key):
        return self.__dict__.get(key)


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

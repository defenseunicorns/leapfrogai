from pydantic import BaseModel, Field
from typing import Literal

from ..common import Usage
from ..constants import DEFAULT_MAX_COMPLETION_TOKENS


class CompletionChoice(BaseModel):
    """Choice object for completion."""

    index: int = Field(..., description="The index of this completion choice.")
    text: str = Field(..., description="The generated text for this completion choice.")
    logprobs: object | None = Field(
        None,
        description="Log probabilities for the generated tokens. Only returned if requested.",
    )
    finish_reason: str = Field(
        "", description="The reason why the completion finished.", example="length"
    )


class CompletionRequest(BaseModel):
    """Request object for completion."""

    model: str = Field(
        ...,
        description="The ID of the model to use for completion.",
        example="llama-cpp-python",
    )
    prompt: str | list[int] = Field(
        ...,
        description="The prompt to generate completions for. Can be a string or a list of integers representing token IDs.",
        examples=["Once upon a time,"],
    )
    stream: bool = Field(
        False, description="Whether to stream the results as they become available."
    )
    max_tokens: int | None = Field(
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        description="The maximum number of tokens to generate.",
        ge=1,
    )
    temperature: float | None = Field(
        1.0,
        description="Sampling temperature to use. Higher values mean more random completions. Use lower values for more deterministic completions. The upper limit may vary depending on the backend used.",
        ge=0.0,
    )


class CompletionResponse(BaseModel):
    """Response object for completion."""

    id: str = Field("", description="A unique identifier for this completion response.")
    object: Literal["completion"] = Field(
        "completion",
        description="The object type, which is always 'completion' for this response.",
    )
    created: int = Field(
        0,
        description="The Unix timestamp (in seconds) of when the completion was created.",
    )
    model: str = Field("", description="The ID of the model used for the completion.")
    choices: list[CompletionChoice] = Field(
        ..., description="A list of generated completions."
    )
    usage: Usage | None = Field(
        None, description="Usage statistics for the completion request."
    )

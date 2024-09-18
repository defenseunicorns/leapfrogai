from pydantic import BaseModel, Field

class TokenCountResponse(BaseModel):
    """Response object for token count."""

    token_count: int = Field(..., description="The number of tokens in the text.")


class TokenCountRequest(BaseModel):
    """Request object for token count."""

    model: str = Field(
        ...,
        examples=["llama-cpp-python", "vllm"],
        description="The ID of the model to use for token count.",
    )
    text: str = Field(
        ...,
        examples=["Once upon a time,"],
        description="The text to count the tokens of.",
    )
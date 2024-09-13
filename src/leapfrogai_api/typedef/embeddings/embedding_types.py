from pydantic import BaseModel, Field

from ..common import Usage


class EmbeddingResponseData(BaseModel):
    """Response object for embeddings."""

    embedding: list[float] = Field(
        default=[],
        description="The embedding vector representing the input text.",
    )
    index: int = Field(
        default=0,
        description="The index of the embedding in the list of generated embeddings.",
    )
    object: str = Field(
        default="embedding",
        description="The object type, which is always 'embedding'.",
    )


class CreateEmbeddingRequest(BaseModel):
    """Request object for creating embeddings."""

    model: str = Field(
        description="The ID of the model to use for generating embeddings.",
        examples=["text-embeddings"],
    )
    input: str | list[str] | list[int] | list[list[int]] = Field(
        description="The text to generate embeddings for. Can be a string, array of strings, array of tokens, or array of token arrays.",
        examples=["The quick brown fox jumps over the lazy dog", ["Hello", "World"]],
    )


class CreateEmbeddingResponse(BaseModel):
    """Response object for embeddings."""

    data: list[EmbeddingResponseData] = Field(
        default=[],
        description="A list of embedding objects.",
    )
    model: str = Field(
        default="",
        examples=["text-embeddings"],
        description="The ID of the model used for generating the embeddings.",
    )
    object: str = Field(
        default="list",
        description="The object type, which is always 'list' for embedding responses.",
    )
    usage: Usage | None = Field(
        default=None,
        description="Usage statistics for the API call.",
    )

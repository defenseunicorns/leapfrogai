from typing import Optional

from pydantic import BaseModel, Field


class SearchItem(BaseModel):
    """Object representing a single item in a search result."""

    id: str = Field(..., description="Unique identifier for the search item.")
    vector_store_id: str = Field(
        ..., description="ID of the vector store containing this item."
    )
    file_id: str = Field(..., description="ID of the file associated with this item.")
    content: str = Field(..., description="The actual content of the item.")
    metadata: dict = Field(
        ..., description="Additional metadata associated with the item."
    )
    similarity: float = Field(
        ..., description="Similarity score of this item to the query."
    )
    rank: Optional[int] = Field(
        default=None,
        description="The rank of this search item after ranking has occurred.",
    )
    score: Optional[float] = Field(
        default=None,
        description="The score of this search item after ranking has occurred.",
    )


class SearchResponse(BaseModel):
    """Response object for RAG queries."""

    data: list[SearchItem] = Field(
        ...,
        description="List of RAG items returned as a result of the query.",
        min_length=0,
    )

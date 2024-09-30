from pydantic import BaseModel, Field


class Vector(BaseModel):
    id: str = ""
    vector_store_id: str
    file_id: str
    content: str
    metadata: dict
    embedding: list[float]


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


class SearchResponse(BaseModel):
    """Response object for RAG queries."""

    data: list[SearchItem] = Field(
        ...,
        description="List of RAG items returned as a result of the query.",
        min_length=0,
    )

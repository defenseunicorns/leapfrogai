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


class SearchResponse(BaseModel):
    """Response object for RAG queries."""

    data: list[SearchItem] = Field(
        ...,
        description="List of RAG items returned as a result of the query.",
        min_length=0,
    )

    def get_response_without_content(self):
        response_without_content: SearchResponse = SearchResponse(
            data=[
                SearchItem(
                    id=item.id,
                    vector_store_id=item.vector_store_id,
                    file_id=item.file_id,
                    content="",
                    metadata=item.metadata,
                    similarity=item.similarity,
                )
                for item in self.data
            ]
        )
        return response_without_content

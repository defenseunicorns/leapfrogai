"""Service for querying the RAG model."""

from supabase_py_async import AsyncClient
from leapfrogai_api.backend.rag.index import IndexingService


class QueryService:
    """Service for querying the RAG model."""

    def __init__(self, db: AsyncClient) -> None:
        """Initializes the QueryService."""
        self.db = db

    async def query_rag(self, query: str, vector_store_id: str, k: int = 5):
        """
        Query the Vector Store.

        Args:
            query (str): The query string.
            vector_store_id (str): The ID of the vector store.
            k (int, optional): The number of results to retrieve. Defaults to 5.

        Returns:
            dict: The response from the RAG model.
        """
        vector_store = IndexingService(db=self.db)

        response = await vector_store.asimilarity_search(
            query=query,
            vector_store_id=vector_store_id,
            k=k,
        )

        return response

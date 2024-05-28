from supabase_py_async import AsyncClient
from leapfrogai_api.data.async_supabase_vector_store import AsyncSupabaseVectorStore
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings


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
        vector_store = AsyncSupabaseVectorStore(
            db=self.db,
            embedding=LeapfrogAIEmbeddings(),
        )

        response = await vector_store.asimilarity_search(
            query=query,
            vector_store_id=vector_store_id,
            k=k,
        )

        return response

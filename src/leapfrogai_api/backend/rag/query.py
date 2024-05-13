from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.data.supabase_vector_store import AsyncSupabaseVectorStore
from leapfrogai_api.backend.leapfrogai_embeddings import LeapfrogAIEmbeddings


class QueryService:
    """Service for querying the RAG model."""

    def __init__(self, session: Session):
        """
        Initialize the QueryService.

        Args:
            session (Session): The session object used for making requests to Supabase.
        """
        self.session = session

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
            client=self.session,
            embedding=LeapfrogAIEmbeddings(),
        )

        response = await vector_store.asimilarity_search(
            query=query,
            vector_store_id=vector_store_id,
            k=k,
        )

        return response

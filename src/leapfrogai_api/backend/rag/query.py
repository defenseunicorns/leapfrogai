"""Service for querying the RAG model."""

from supabase import AClient as AsyncClient
from langchain_core.embeddings import Embeddings
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings
from leapfrogai_api.data.crud_vector_content import CRUDVectorContent
from leapfrogai_api.typedef.vectorstores.search_types import SearchResponse

# Allows for overwriting type of embeddings that will be instantiated
embeddings_type: type[Embeddings] | type[LeapfrogAIEmbeddings] | None = (
    LeapfrogAIEmbeddings
)


class QueryService:
    """Service for querying the RAG model."""

    def __init__(self, db: AsyncClient) -> None:
        """Initializes the QueryService."""
        self.db = db
        self.embeddings = embeddings_type()

    async def query_rag(
        self, query: str, vector_store_id: str, k: int = 5
    ) -> SearchResponse:
        """
        Query the Vector Store.

        Args:
            query (str): The input query string.
            vector_store_id (str): The ID of the vector store.
            k (int, optional): The number of results to retrieve. Defaults to 5.

        Returns:
            SearchResponse: The search response from the vector store.
        """

        # 1. Embed query
        vector = await self.embeddings.aembed_query(query)

        # 2. Perform similarity search
        crud_vector_content = CRUDVectorContent(db=self.db)
        return await crud_vector_content.similarity_search(
            query=vector, vector_store_id=vector_store_id, k=k
        )

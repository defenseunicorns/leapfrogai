from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.backend.rag.supabase_vector_store import AsyncSupabaseVectorStore
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings


class QueryService:
    def __init__(self, session: Session):
        self.session = session

    async def query_rag(self, query: str, vector_store_id: str, k: int = 5):
        """Query the RAG model."""

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

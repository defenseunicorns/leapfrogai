"""LeapfrogAI endpoints for RAG."""

from fastapi import APIRouter
from leapfrogai_api.backend.rag.query import QueryService
from leapfrogai_api.typedef.vectorstores import SearchResponse
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.backend.constants import TOP_K

router = APIRouter(
    prefix="/leapfrogai/v1/vector_stores", tags=["leapfrogai/vector_stores"]
)


@router.post("/search")
async def search(
    session: Session,
    query: str,
    vector_store_id: str,
    k: int = TOP_K,
) -> SearchResponse:
    """
    Performs a similarity search of the vector store.

    Args:
        session (Session): The database session.
        query (str): The input query string.
        vector_store_id (str): The ID of the vector store.
        k (int, optional): The number of results to retrieve.

    Returns:
        SearchResponse: The search response from the vector store.
    """
    query_service = QueryService(db=session)
    return await query_service.query_rag(
        query=query, vector_store_id=vector_store_id, k=k
    )

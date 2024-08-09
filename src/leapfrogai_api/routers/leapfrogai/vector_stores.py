"""LeapfrogAI endpoints for RAG."""

from fastapi import APIRouter
from postgrest.base_request_builder import SingleAPIResponse
from leapfrogai_api.backend.rag.query import QueryService
from leapfrogai_api.backend.types import SearchResponse
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(
    prefix="/leapfrogai/v1/vector_stores", tags=["leapfrogai/vector_stores"]
)


@router.post("/search")
async def search(
    session: Session,
    query: str,
    vector_store_id: str,
    k: int = 5,
) -> SearchResponse:
    """
    Performs a similarity search of the vector store.

    Args:
        session (Session): The database session.
        query (str): The input query string.
        vector_store_id (str): The ID of the vector store.
        k (int, optional): The number of results to retrieve. Defaults to 5.

    Returns:
        SearchResponse: The search response from the vector store.
    """
    query_service = QueryService(db=session)
    result: SingleAPIResponse[SearchResponse] = await query_service.query_rag(
        query=query,
        vector_store_id=vector_store_id,
        k=k,
    )

    return SearchResponse(data=result.data)

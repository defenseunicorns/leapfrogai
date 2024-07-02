"""LeapfrogAI endpoints for RAG."""

from fastapi import APIRouter
from fastapi.security import HTTPBearer
from postgrest.base_request_builder import SingleAPIResponse
from leapfrogai_api.backend.rag.query import QueryService
from leapfrogai_api.backend.types import RAGResponse
from leapfrogai_api.routers.supabase_session_api_key import Session

router = APIRouter(prefix="/leapfrogai/v1/rag", tags=["leapfrogai/rag"])
security = HTTPBearer()


@router.post("")
async def query_rag(
    session: Session,
    query: str,
    vector_store_id: str,
    k: int = 5,
) -> RAGResponse:
    """
    Query the RAG (Retrieval-Augmented Generation).

    Args:
        session (Session): The database session.
        query (str): The input query string.
        vector_store_id (str): The ID of the vector store.
        k (int, optional): The number of results to retrieve. Defaults to 5.

    Returns:
        RAGResponse: The response from the RAG.
    """
    query_service = QueryService(db=session)
    result: SingleAPIResponse[RAGResponse] = await query_service.query_rag(
        query=query,
        vector_store_id=vector_store_id,
        k=k,
    )

    return RAGResponse(data=result.data)

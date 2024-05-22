"""LeapfrogAI endpoints for RAG."""

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from leapfrogai_api.backend.rag.query import QueryService
from leapfrogai_api.backend.types import RAGResponse

router = APIRouter(prefix="/leapfrogai/v1/rag", tags=["leapfrogai/rag"])

security = HTTPBearer()


@router.post("")
async def query_rag(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
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
    query_service = QueryService(auth_creds.credentials)

    return await query_service.query_rag(
        query=query,
        vector_store_id=vector_store_id,
        k=k,
    )

"""OpenAI Compliant Assistants API Router."""

from fastapi import APIRouter
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.backend.rag.query import QueryService

router = APIRouter(prefix="/leapfrogai/v1/rag", tags=["leapfrogai/rag"])


@router.post("")
async def query_rag(session: Session, query: str, vector_store_id: str, k: int = 5):
    query_service = QueryService(session)

    return await query_service.query_rag(
        query=query, vector_store_id=vector_store_id, k=k
    )

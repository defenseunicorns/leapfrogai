"""OpenAI Compliant Vector Store API Router."""

from fastapi import HTTPException, APIRouter
from fastapi.security import HTTPBearer
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_stores import VectorStoreFile, VectorStoreFileDeleted

from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/openai/v1/vector_store", tags=["openai/vector_store"])
security = HTTPBearer()


@router.post("")
async def create_vector_store(session: Session) -> VectorStore:
    """Create a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("")
async def list_vector_stores(session: Session) -> list[VectorStore]:
    """List all the vector stores."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{vector_store_id}")
async def retrieve_vector_store(vector_store_id: str, session: Session) -> VectorStore:
    """Retrieve a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{vector_store_id}")
async def modify_vector_store(vector_store_id: str, session: Session) -> VectorStore:
    """Modify a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{vector_store_id}")
async def delete_vector_store(
    vector_store_id: str, session: Session
) -> VectorStoreDeleted:
    """Delete a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{vector_store_id}/files")
async def create_vector_store_file(
    vector_store_id: str, session: Session
) -> VectorStoreFile:
    """Create a file in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{vector_store_id}/files")
async def list_vector_store_files(
    vector_store_id: str, session: Session
) -> list[VectorStoreFile]:
    """List all the files in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{vector_store_id}/files/{file_id}")
async def delete_vector_store_file(
    vector_store_id: str, file_id: str, session: Session
) -> VectorStoreFileDeleted:
    """Delete a file in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

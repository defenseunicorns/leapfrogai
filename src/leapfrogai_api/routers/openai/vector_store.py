"""OpenAI Compliant Vector Store API Router."""

from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_stores import VectorStoreFile, VectorStoreFileDeleted

router = APIRouter(prefix="/openai/v1/vector_store", tags=["openai/vector_store"])
security = HTTPBearer()


@router.post("")
async def create_vector_store(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> VectorStore:
    """Create a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("")
async def list_vector_stores(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> list[VectorStore]:
    """List all the vector stores."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{vector_store_id}")
async def retrieve_vector_store(
    vector_store_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> VectorStore:
    """Retrieve a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{vector_store_id}")
async def modify_vector_store(
    vector_store_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> VectorStore:
    """Modify a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{vector_store_id}")
async def delete_vector_store(
    vector_store_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> VectorStoreDeleted:
    """Delete a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{vector_store_id}/files")
async def create_vector_store_file(
    vector_store_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> VectorStoreFile:
    """Create a file in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{vector_store_id}/files")
async def list_vector_store_files(
    vector_store_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> list[VectorStoreFile]:
    """List all the files in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{vector_store_id}/files/{file_id}")
async def delete_vector_store_file(
    vector_store_id: str,
    file_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> VectorStoreFileDeleted:
    """Delete a file in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

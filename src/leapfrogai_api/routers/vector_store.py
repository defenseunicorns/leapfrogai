"""OpenAI Compliant Vector Store API Router."""

from typing import List
from fastapi import HTTPException, APIRouter
from openai.types.beta import VectorStore


router = APIRouter(prefix="/openai/v1/vector_store", tags=["openai/vector_store"])


@router.post("/")
def create_vector_store() -> VectorStore:
    """Create a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/")
def list_vector_stores() -> List[VectorStore]:
    """List all the vector stores."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{vector_store_id}")
def retrieve_vector_store(vector_store_id: str) -> VectorStore:
    """Retrieve a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{vector_store_id}")
def modify_vector_store(vector_store_id: str) -> VectorStore:
    """Modify a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{vector_store_id}")
def delete_vector_store(vector_store_id: str) -> VectorStore:
    """Delete a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

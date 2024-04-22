"""OpenAI Compliant Threads API Router."""

from fastapi import HTTPException, APIRouter
from openai.types.beta import Thread, ThreadDeleted


router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads"])


@router.post("/")
def create_thread() -> Thread:
    """Create a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}")
def retrieve_thread(thread_id: str) -> Thread:
    """Retrieve a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}")
def modify_thread(thread_id: str) -> Thread:
    """Modify a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{thread_id}")
def delete_thread(thread_id: str) -> ThreadDeleted:
    """Delete a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

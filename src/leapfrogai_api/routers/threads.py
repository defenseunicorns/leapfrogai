"""OpenAI Compliant Threads API Router."""

from typing import List
from fastapi import HTTPException, APIRouter
from openai.types.beta import Thread, ThreadDeleted, Message


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


@router.post("/{thread_id}/messages")
def create_message(thread_id: str) -> Message:
    """Create a message."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/messages")
def list_messages(thread_id: str) -> List[Message]:
    """List all the messages in a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/messages/{message_id}")
def retrieve_message(thread_id: str, message_id: str) -> Message:
    """Retrieve a message."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}/messages/{message_id}")
def modify_message(thread_id: str, message_id: str) -> Message:
    """Modify a message."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

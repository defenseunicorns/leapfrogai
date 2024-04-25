"""OpenAI Compliant Assistants API Router."""

from typing import List
from fastapi import HTTPException, APIRouter
from openai.types.beta import Assistant, AssistantDeleted
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ModifyAssistantRequest,
)

router = APIRouter(prefix="/openai/v1/assistants", tags=["openai/assistants"])


@router.post("")
async def create_assistant(request: CreateAssistantRequest) -> Assistant:
    """Create an assistant."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("")
async def list_assistants() -> List[Assistant]:
    """List all the assistants."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{assistant_id}")
async def retrieve_assistant(assistant_id: str) -> Assistant:
    """Retrieve an assistant."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{assistant_id}")
async def modify_assistant(
    assistant_id: str, request: ModifyAssistantRequest
) -> Assistant:
    """Modify an assistant."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{assistant_id}")
async def delete_assistant(assistant_id: str) -> AssistantDeleted:
    """Delete an assistant."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

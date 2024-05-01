"""OpenAI Compliant Assistants API Router."""

import time
from typing import List
from fastapi import HTTPException, APIRouter
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.assistant import ToolResources
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ModifyAssistantRequest,
)
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.openai_util import validate_tools_typed_dict
from leapfrogai_api.data.crud_assistant_object import CRUDAssistant

router = APIRouter(prefix="/openai/v1/assistants", tags=["openai/assistants"])


@router.post("")
async def create_assistant(
    session: Session, request: CreateAssistantRequest
) -> Assistant:
    """Create an assistant."""

    try:
        assistant = Assistant(
            id="",
            created_at=int(time.time()),
            name=request.name,
            description=request.description,
            instructions=request.instructions,
            model=request.model,
            object="assistant",
            tools=validate_tools_typed_dict(request.tools),
            tool_resources=ToolResources.model_validate(request.tool_resources),
            temperature=request.temperature,
            top_p=request.top_p,
            metadata=request.metadata,
            response_format=request.response_format,
        )

        crud_assistant = CRUDAssistant(model=Assistant)
        return await crud_assistant.create(assistant=assistant, client=session)

    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to create assistant"
        ) from exc


@router.get("")
async def list_assistants(session: Session) -> List[Assistant] | None:
    """List all the assistants."""
    try:
        crud_assistant = CRUDAssistant(model=Assistant)
        return await crud_assistant.list(client=session)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="No assistants found") from exc


@router.get("/{assistant_id}")
async def retrieve_assistant(session: Session, assistant_id: str) -> Assistant:
    """Retrieve an assistant."""
    try:
        crud_assistant = CRUDAssistant(model=Assistant)
        return await crud_assistant.get(assistant_id=assistant_id, client=session)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Assistant not found") from exc


@router.post("/{assistant_id}")
async def modify_assistant(
    session: Session, assistant_id: str, request: ModifyAssistantRequest
) -> Assistant:
    """Modify an assistant."""
    # TODO: Implement this function
    raise HTTPException(status_code=405, detail="Not Implemented")


@router.delete("/{assistant_id}")
async def delete_assistant(session: Session, assistant_id: str) -> AssistantDeleted:
    """Delete an assistant."""
    try:
        crud_assistant = CRUDAssistant(model=Assistant)
        return await crud_assistant.delete(assistant_id=assistant_id, client=session)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Assistant not found") from exc

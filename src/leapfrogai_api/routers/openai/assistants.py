"""OpenAI Compliant Assistants API Router."""

import time
from fastapi import HTTPException, APIRouter
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.assistant import ToolResources
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ListAssistantsResponse,
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
            id="",  # Leave blank to have Postgres generate a UUID
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
    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to parse assistant request"
        ) from exc

    try:
        crud_assistant = CRUDAssistant(model=Assistant)
        return await crud_assistant.create(assistant=assistant, client=session)
    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to create assistant"
        ) from exc


@router.get("")
async def list_assistants(session: Session) -> ListAssistantsResponse | None:
    """List all the assistants."""
    try:
        crud_assistant = CRUDAssistant(model=Assistant)
        crud_response = await crud_assistant.list(client=session)
        response = {
            "object": "list",
            "data": crud_response,
        }
        return response
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="No assistants found") from exc


@router.get("/{assistant_id}")
async def retrieve_assistant(session: Session, assistant_id: str) -> Assistant | None:
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

    old_assistant = await retrieve_assistant(session, assistant_id)
    if old_assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")

    try:
        assistant = Assistant(
            id=assistant_id,
            created_at=old_assistant.created_at,
            name=request.name or old_assistant.name,
            description=request.description or old_assistant.description,
            instructions=request.instructions or old_assistant.instructions,
            model=request.model or old_assistant.model,
            object="assistant",
            tools=validate_tools_typed_dict(request.tools) or old_assistant.tools,
            tool_resources=ToolResources.model_validate(request.tool_resources)
            or old_assistant.tool_resources,
            temperature=request.temperature or old_assistant.temperature,
            top_p=request.top_p or old_assistant.top_p,
            metadata=request.metadata or old_assistant.metadata,
            response_format=request.response_format or old_assistant.response_format,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to parse assistant request"
        ) from exc

    try:
        crud_assistant = CRUDAssistant(model=Assistant)
        return await crud_assistant.update(
            assistant_id=assistant_id, assistant=assistant, client=session
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Assistant not found") from exc


@router.delete("/{assistant_id}")
async def delete_assistant(session: Session, assistant_id: str) -> AssistantDeleted:
    """Delete an assistant."""
    try:
        crud_assistant = CRUDAssistant(model=Assistant)
        return await crud_assistant.delete(assistant_id=assistant_id, client=session)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Assistant not found") from exc

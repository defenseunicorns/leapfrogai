"""OpenAI Compliant Assistants API Router."""

import time
from typing import List
from uuid import uuid4
from fastapi import HTTPException, APIRouter
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.assistant import ToolResources
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ModifyAssistantRequest,
)
from leapfrogai_api.data.supabase_client import SupabaseWrapper
from leapfrogai_api.utils.openai_util import validate_tools_typed_dict

router = APIRouter(prefix="/openai/v1/assistants", tags=["openai/assistants"])


@router.post("/")
async def create_assistant(request: CreateAssistantRequest) -> Assistant:
    """Create an assistant."""

    try:
        created_at = int(time.time())
        assistant_id = str(uuid4())

        assistant = Assistant(
            id=assistant_id,
            created_at=created_at,
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

        supabase_wrapper = SupabaseWrapper()
        await supabase_wrapper.upsert_assistant(assistant)
        return assistant

    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to create assistant"
        ) from exc


@router.get("/")
async def list_assistants() -> List[Assistant]:
    """List all the assistants."""
    try:
        supabase_wrapper = SupabaseWrapper()
        assistants: List[Assistant] = await supabase_wrapper.list_assistants()
        return assistants
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="No assistants found") from exc


@router.get("/{assistant_id}")
async def retrieve_assistant(assistant_id: str) -> Assistant:
    """Retrieve an assistant."""
    try:
        supabase_wrapper = SupabaseWrapper()
        assistant: Assistant = await supabase_wrapper.retrieve_assistant(assistant_id)
        return assistant
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Assistant not found") from exc


@router.post("/{assistant_id}")
async def modify_assistant(
    assistant_id: str, request: ModifyAssistantRequest
) -> Assistant:
    """Modify an assistant."""

    try:
        supabase_wrapper = SupabaseWrapper()
        assistant: Assistant = await supabase_wrapper.retrieve_assistant(assistant_id)

        assistant.model = request.model or assistant.model
        assistant.name = request.name or assistant.name
        assistant.description = request.description or assistant.description
        assistant.instructions = request.instructions or assistant.instructions
        if request.tools:
            assistant.tools = validate_tools_typed_dict(request.tools)

        if request.tool_resources:
            assistant.tool_resources = ToolResources.model_validate_json(
                request.tool_resources
            )

        assistant.metadata = request.metadata or assistant.metadata
        assistant.temperature = request.temperature or assistant.temperature
        assistant.top_p = request.top_p or assistant.top_p
        assistant.response_format = request.response_format or assistant.response_format
        await supabase_wrapper.upsert_assistant(assistant)
        return assistant
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Assistant not found") from exc


@router.delete("/{assistant_id}")
async def delete_assistant(assistant_id: str) -> AssistantDeleted:
    """Delete an assistant."""
    try:
        supabase_wrapper = SupabaseWrapper()
        return await supabase_wrapper.delete_assistant(assistant_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Assistant not found") from exc

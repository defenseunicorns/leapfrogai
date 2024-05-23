"""OpenAI Compliant Assistants API Router."""

import logging

from fastapi import HTTPException, APIRouter, status
from fastapi.security import HTTPBearer
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.assistant import ToolResources, ToolResourcesCodeInterpreter
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ListAssistantsResponse,
    ModifyAssistantRequest,
)
from leapfrogai_api.data.crud_assistant_object import CRUDAssistant
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/openai/v1/assistants", tags=["openai/assistants"])
security = HTTPBearer()

supported_tools = ["file_search"]


@router.post("")
async def create_assistant(
    session: Session,
    request: CreateAssistantRequest,
) -> Assistant:
    """Create an assistant."""

    if request.tools and (
        unsupported_tool := next(
            (tool for tool in request.tools if tool.type not in supported_tools), None
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool type: {unsupported_tool.type}",
        )

    if request.tool_resources and any(
        isinstance(tool_resource, ToolResourcesCodeInterpreter)
        and tool_resource.get("file_ids")
        for tool_resource in request.tool_resources
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code interpreter tool is not supported",
        )

    try:
        assistant = Assistant(
            id="",  # This is set by the database to prevent conflicts
            created_at=0,  # This is set by the database
            name=request.name,
            description=request.description,
            instructions=request.instructions,
            model=request.model,
            object="assistant",
            tools=request.tools,
            tool_resources=request.tool_resources,
            temperature=request.temperature,
            top_p=request.top_p,
            metadata=request.metadata,
            response_format=request.response_format,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse assistant request",
        ) from exc

    try:
        crud_assistant = CRUDAssistant(session)
        return await crud_assistant.create(object_=assistant)
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        logging.debug(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create assistant",
        ) from exc


@router.get("")
async def list_assistants(
    session: Session,
) -> ListAssistantsResponse:
    """List all the assistants."""
    crud_assistant = CRUDAssistant(session)
    crud_response = await crud_assistant.list()

    return ListAssistantsResponse(
        object="list",
        data=crud_response or [],
    )


@router.get("/{assistant_id}")
async def retrieve_assistant(
    session: Session,
    assistant_id: str,
) -> Assistant | None:
    """Retrieve an assistant."""

    crud_assistant = CRUDAssistant(session)
    return await crud_assistant.get(id_=assistant_id)


@router.post("/{assistant_id}")
async def modify_assistant(
    session: Session,
    assistant_id: str,
    request: ModifyAssistantRequest,
) -> Assistant:
    """
    Modify an assistant.

    Args:
        session (Session): An authenticated client for the current session.
        assistant_id (str): The ID of the assistant to modify.
        request (ModifyAssistantRequest): The request object containing the updated assistant information.
        auth_creds (HTTPAuthorizationCredentials): The authorization header that contains the user's API key.

    Returns:
        Assistant: The modified assistant.

    Raises:
        HTTPException: If the assistant is not found or if there is an error parsing the request.

    Note:
        The following attributes of the assistant can be updated:
        - name
        - description
        - instructions
        - model
        - tools
        - tool_resources
        - temperature
        - top_p
        - metadata
        - response_format
    """

    if request.tools and (
        unsupported_tool := next(
            (tool for tool in request.tools if tool.type not in supported_tools), None
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool type: {unsupported_tool.type}",
        )

    if request.tool_resources and any(
        isinstance(tool_resource, ToolResourcesCodeInterpreter)
        and tool_resource.get("file_ids")
        for tool_resource in request.tool_resources
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code interpreter tool is not supported",
        )

    crud_assistant = CRUDAssistant(session)

    if not (old_assistant := await crud_assistant.get(id_=assistant_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Assistant not found"
        )

    try:
        new_assistant = Assistant(
            id=assistant_id,
            created_at=old_assistant.created_at,
            name=getattr(request, "name", old_assistant.name),
            description=getattr(request, "description", old_assistant.description),
            instructions=getattr(request, "instructions", old_assistant.instructions),
            model=getattr(request, "model", old_assistant.model),
            object="assistant",
            tools=getattr(request, "tools", old_assistant.tools),
            tool_resources=ToolResources.model_validate(
                getattr(request, "tool_resources", None)
            )
            or old_assistant.tool_resources,
            temperature=float(
                getattr(request, "temperature", old_assistant.temperature)
            ),
            top_p=getattr(request, "top_p", old_assistant.top_p),
            metadata=getattr(request, "metadata", old_assistant.metadata),
            response_format=getattr(
                request, "response_format", old_assistant.response_format
            ),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse assistant request",
        ) from exc

    try:
        return await crud_assistant.update(
            object_=new_assistant,
            id_=assistant_id,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update assistant",
        ) from exc


@router.delete("/{assistant_id}")
async def delete_assistant(
    session: Session,
    assistant_id: str,
) -> AssistantDeleted:
    """Delete an assistant."""
    crud_assistant = CRUDAssistant(session)
    assistant_deleted = await crud_assistant.delete(id_=assistant_id)
    return AssistantDeleted(
        id=assistant_id,
        deleted=bool(assistant_deleted),
        object="assistant.deleted",
    )

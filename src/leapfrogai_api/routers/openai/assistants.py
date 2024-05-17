"""OpenAI Compliant Assistants API Router."""

from fastapi import HTTPException, APIRouter, status, Header
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.assistant import ToolResources
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ListAssistantsResponse,
    ModifyAssistantRequest,
)
from leapfrogai_api.routers.supabase_session import Session, get_user_session
from leapfrogai_api.utils.openai_util import validate_tools_typed_dict
from leapfrogai_api.data.crud_assistant_object import CRUDAssistant

router = APIRouter(prefix="/openai/v1/assistants", tags=["openai/assistants"])


@router.post("")
async def create_assistant(
    session: Session,
    request: CreateAssistantRequest,
    authorization: str | None = Header(default=None),
) -> Assistant:
    """Create an assistant."""

    try:
        assistant = Assistant(
            id="",  # This is set by the database to prevent conflicts
            created_at=0,  # This is set by the database
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse assistant request",
        ) from exc

    try:
        crud_assistant = CRUDAssistant(model=Assistant)
        return await crud_assistant.create(
            db=await get_user_session(session, authorization), object_=assistant
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create assistant",
        ) from exc


@router.get("")
async def list_assistants(
    session: Session, authorization: str | None = Header(default=None)
) -> ListAssistantsResponse:
    """List all the assistants."""
    crud_assistant = CRUDAssistant(model=Assistant)
    crud_response = await crud_assistant.list(
        db=await get_user_session(session, authorization)
    )

    return ListAssistantsResponse(
        object="list",
        data=crud_response or [],
    )


@router.get("/{assistant_id}")
async def retrieve_assistant(
    session: Session,
    assistant_id: str,
    authorization: str | None = Header(default=None),
) -> Assistant | None:
    """Retrieve an assistant."""

    crud_assistant = CRUDAssistant(model=Assistant)
    return await crud_assistant.get(
        db=await get_user_session(session, authorization), id_=assistant_id
    )


@router.post("/{assistant_id}")
async def modify_assistant(
    session: Session,
    assistant_id: str,
    request: ModifyAssistantRequest,
    authorization: str | None = Header(default=None),
) -> Assistant:
    """
    Modify an assistant.

    Args:
        session (Session): The database session.
        assistant_id (str): The ID of the assistant to modify.
        request (ModifyAssistantRequest): The request object containing the updated assistant information.
        authorization (str): The authorization header that contains the user's API key.

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
    crud_assistant = CRUDAssistant(model=Assistant)

    old_assistant = await crud_assistant.get(
        db=await get_user_session(session, authorization), id_=assistant_id
    )
    if old_assistant is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Assistant not found"
        )

    try:
        new_assistant = Assistant(
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse assistant request",
        ) from exc

    try:
        return await crud_assistant.update(
            db=await get_user_session(session, authorization),
            object_=new_assistant,
            id_=assistant_id,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Assistant not found"
        ) from exc


@router.delete("/{assistant_id}")
async def delete_assistant(
    session: Session,
    assistant_id: str,
    authorization: str | None = Header(default=None),
) -> AssistantDeleted:
    """Delete an assistant."""
    crud_assistant = CRUDAssistant(model=Assistant)
    assistant_deleted = await crud_assistant.delete(
        db=await get_user_session(session, authorization), id_=assistant_id
    )
    return AssistantDeleted(
        id=assistant_id,
        deleted=bool(assistant_deleted),
        object="assistant.deleted",
    )

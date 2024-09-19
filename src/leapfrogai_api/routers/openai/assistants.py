"""OpenAI Compliant Assistants API Router."""

from fastapi import HTTPException, APIRouter, status
from openai.types.beta import Assistant, AssistantDeleted

from leapfrogai_api.backend.helpers import object_or_default
from leapfrogai_api.typedef.assistants import ListAssistantsResponse
from leapfrogai_api.typedef.assistants import (
    CreateAssistantRequest,
    ModifyAssistantRequest,
)
from leapfrogai_api.data.crud_assistant import CRUDAssistant, FilterAssistant
from leapfrogai_api.routers.supabase_session import Session


router = APIRouter(prefix="/openai/v1/assistants", tags=["openai/assistants"])

supported_tools = ["file_search"]


@router.post("")
async def create_assistant(
    session: Session,
    request: CreateAssistantRequest,
) -> Assistant:
    """Create an assistant."""

    # perform checks for unsupported tools and new vector stores
    await request.request_checks_and_modifications(session)

    try:
        assistant = Assistant(
            id="",  # This is set by the database to prevent conflicts
            created_at=0,  # This is set by the database
            name=request.name,
            description=request.description,
            instructions=request.instructions,
            model=request.model,
            object="assistant",
            tools=request.tools or [],
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

    crud_assistant = CRUDAssistant(session)

    if not (response := await crud_assistant.create(object_=assistant)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create assistant",
        )
    return response


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
    return await crud_assistant.get(filters=FilterAssistant(id=assistant_id))


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

    crud_assistant = CRUDAssistant(session)

    # check assistant id is valid
    if not (
        old_assistant := await crud_assistant.get(
            filters=FilterAssistant(id=assistant_id)
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Assistant not found"
        )

    # perform checks for unsupported tools and new vector stores
    await request.request_checks_and_modifications(session)

    try:
        new_assistant = Assistant(
            id=assistant_id,
            created_at=old_assistant.created_at,
            name=object_or_default(request.name, old_assistant.name),
            description=object_or_default(
                request.description, old_assistant.description
            ),
            instructions=object_or_default(
                request.instructions, old_assistant.instructions
            ),
            model=object_or_default(request.model, old_assistant.model),
            object="assistant",
            tools=object_or_default(request.tools, old_assistant.tools),
            tool_resources=object_or_default(
                request.tool_resources, old_assistant.tool_resources
            ),
            temperature=object_or_default(
                request.temperature, old_assistant.temperature
            ),
            top_p=object_or_default(request.top_p, old_assistant.top_p),
            metadata=object_or_default(request.metadata, old_assistant.metadata),
            response_format=object_or_default(
                request.response_format, old_assistant.response_format
            ),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse assistant request",
        ) from exc

    if not (
        response := await crud_assistant.update(object_=new_assistant, id_=assistant_id)
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update assistant",
        )
    return response


@router.delete("/{assistant_id}")
async def delete_assistant(
    session: Session,
    assistant_id: str,
) -> AssistantDeleted:
    """Delete an assistant."""
    crud_assistant = CRUDAssistant(session)
    assistant_deleted = await crud_assistant.delete(
        filters=FilterAssistant(id=assistant_id)
    )
    return AssistantDeleted(
        id=assistant_id,
        deleted=bool(assistant_deleted),
        object="assistant.deleted",
    )

"""OpenAI Compliant Assistants API Router."""

import logging
from contextlib import suppress

from fastapi import HTTPException, APIRouter, status
from fastapi.security import HTTPBearer
from openai.types.beta import Assistant, AssistantDeleted
from leapfrogai_api.backend.helpers import object_or_default
from leapfrogai_api.backend.rag.index import IndexingService
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ListAssistantsResponse,
    ModifyAssistantRequest,
    CreateVectorStoreRequest,
)
from leapfrogai_api.data.crud_assistant import CRUDAssistant, FilterAssistant
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore, FilterVectorStore
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.validate_tools import (
    validate_assistant_tool,
    validate_tool_resources,
)

router = APIRouter(prefix="/openai/v1/assistants", tags=["openai/assistants"])
security = HTTPBearer()

supported_tools = ["file_search"]


@router.post("")
async def create_assistant(
    session: Session,
    request: CreateAssistantRequest,
) -> Assistant:
    """Create an assistant."""

    # perform checks for unsupported tools and new vector stores
    request = await _assistant_request_checks_and_modifications(request, session)

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
    request = await _assistant_request_checks_and_modifications(request, session)

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


# helper function to check for unsupported tools/tool resources, and if a new vector store needs to be added
async def _assistant_request_checks_and_modifications(
    request: CreateAssistantRequest | ModifyAssistantRequest, session: Session
) -> CreateAssistantRequest | ModifyAssistantRequest:
    """
    Performs checks and modifications that occur in both create and modify requests

    Checks performed:
    - unsupported tools
    - unsupported tool resources

    Modifications performed:
    - vector store creation
    """

    async def new_vector_store_from_file_ids():
        logging.debug("Creating vector store for new assistant")
        indexing_service = IndexingService(db=session)
        vector_store_params_dict = vector_stores[0]

        if "file_ids" not in vector_store_params_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ToolResourcesFileSearchVectorStores found but no file ids were provided",
            )

        if not indexing_service.file_ids_are_valid(
            vector_store_params_dict["file_ids"]
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file ids attached to assistants request",
            )

        vector_store_request = CreateVectorStoreRequest(
            file_ids=vector_store_params_dict["file_ids"],
            name="{}_vector_store".format(request.name),
            expires_after=None,
            metadata={},
        )

        vector_store = await indexing_service.create_new_vector_store(
            vector_store_request
        )

        request.tool_resources.file_search.vector_store_ids = [vector_store.id]

    async def attach_existing_vector_store_from_id():
        logging.debug(
            "Attaching vector store with id: {} to new assistant".format(ids[0])
        )
        crud_vector_store = CRUDVectorStore(db=session)
        try:
            existing_vector_store = await crud_vector_store.get(
                filters=FilterVectorStore(id=ids[0])
            )
            if existing_vector_store is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Provided vector store id was not found",
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid vector store id was provided",
            )

    # check for unsupported tools
    if request.tools:
        for tool in request.tools:
            if not validate_assistant_tool(tool):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported tool type: {tool.type}",
                )

    # check for unsupported tool resources
    if request.tool_resources and not validate_tool_resources(request.tool_resources):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool resource: {request.tool_resources}",
        )

    # check if a vector store needs to be built or added to this assistant
    if request.tool_resources and request.tool_resources.file_search is not None:
        ids = request.tool_resources.file_search.vector_store_ids or []
        vector_stores = (
            getattr(request.tool_resources.file_search, "vector_stores", []) or []
        )

        ids_len = len(ids)
        vector_stores_len = len(list(vector_stores))

        # too many ids or vector_stores provided
        if (ids_len + vector_stores_len) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There can be a maximum of 1 vector store attached to the assistant",
            )

        # new vector store requested from file ids
        elif vector_stores_len == 1:
            await new_vector_store_from_file_ids()

        # attach already existing vector store from its id
        elif ids_len == 1:
            await attach_existing_vector_store_from_id()

        # nothing provided, no changes made
        else:
            logging.debug(
                "No files or vector store id found; assistant will be created with no vector store"
            )

        # ensure the vector_stores field is removed regardless, if it exists
        with suppress(AttributeError):
            request.tool_resources.file_search.vector_stores = None

    return request

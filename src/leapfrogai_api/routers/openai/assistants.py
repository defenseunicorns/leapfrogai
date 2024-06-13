"""OpenAI Compliant Assistants API Router."""

import logging

from contextlib import suppress
from fastapi import HTTPException, APIRouter, status
from fastapi.security import HTTPBearer
from leapfrogai_api.backend.rag.index import IndexingService
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.assistant import ToolResources
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ListAssistantsResponse,
    ModifyAssistantRequest,
    CreateVectorStoreRequest,
)
from leapfrogai_api.data.crud_assistant import CRUDAssistant, FilterAssistant
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore, FilterVectorStore
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

    # check for unsupported tools
    if request.tools and (
        unsupported_tool := next(
            (tool for tool in request.tools if tool.type not in supported_tools), None
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool type: {unsupported_tool.type}",
        )

    # check if the request includes a code interpreter
    if request.tool_resources and request.tool_resources.code_interpreter is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code interpreter tool is not supported",
        )

    # check if a vector store needs to be built or added to this assistant
    if request.tool_resources and request.tool_resources.file_search is not None:
        ids = request.tool_resources.file_search.vector_store_ids
        vector_stores = (
            request.tool_resources.file_search.vector_stores
            if hasattr(request.tool_resources.file_search, "vector_stores")
            else None
        )

        ids_len = len(ids) if ids is not None else 0
        vector_stores_len = len(list(vector_stores)) if vector_stores is not None else 0

        if (ids_len + vector_stores_len) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There can be a maximum of 1 vector store attached to the assistant",
            )
        elif vector_stores_len == 1:
            logging.debug("Creating vector store for new assistant")

            vector_store_request = CreateVectorStoreRequest(
                file_ids=vector_stores[0]["file_ids"],
                name="{}_vector_store".format(request.name),
                expires_after=None,
                metadata={},
            )

            indexing_service = IndexingService(db=session)
            vector_store = await indexing_service.create_new_vector_store(
                vector_store_request
            )

            request.tool_resources.file_search.vector_store_ids = [vector_store.id]
        elif ids_len == 1:
            logging.debug(
                "Attaching vector store with id: {} to new assistant".format(ids[0])
            )
            # How do we check to make sure the supplied vector_store_id is valid?
            crud_vector_store = CRUDVectorStore(db=session)

            try:
                await crud_vector_store.get(filters=FilterVectorStore(id=ids[0]))
            except Exception as e:
                raise e
        else:
            logging.debug(
                "No files or vector store id found; assistant will be created with no vector store"
            )

        with suppress(AttributeError):
            request.tool_resources.file_search.vector_stores = (
                None  # remove vector_stores if it's there
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

    if request.tools and (
        unsupported_tool := next(
            (tool for tool in request.tools if tool.type not in supported_tools), None
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool type: {unsupported_tool.type}",
        )

    if request.tool_resources and request.tool_resources.code_interpreter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code interpreter tool is not supported",
        )

    crud_assistant = CRUDAssistant(session)

    if not (
        old_assistant := await crud_assistant.get(
            filters=FilterAssistant(id=assistant_id)
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Assistant not found"
        )

    # check if a vector store needs to be built or added to this assistant
    if request.tool_resources and request.tool_resources.file_search is not None:
        ids = request.tool_resources.file_search.vector_store_ids
        vector_stores = (
            request.tool_resources.file_search.vector_stores
            if hasattr(request.tool_resources.file_search, "vector_stores")
            else None
        )

        ids_len = len(ids) if ids is not None else 0
        vector_stores_len = len(list(vector_stores)) if vector_stores is not None else 0

        if (ids_len + vector_stores_len) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There can be a maximum of 1 vector store attached to the assistant",
            )
        elif vector_stores_len == 1:
            logging.debug("Creating vector store for new assistant")
            indexing_service = IndexingService(db=session)

            if not indexing_service.file_ids_are_valid(vector_stores[0]["file_ids"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid file ids attached to assistants request",
                )

            vector_store_request = CreateVectorStoreRequest(
                file_ids=vector_stores[0]["file_ids"],
                name="{}_vector_store".format(request.name),
                expires_after=None,
                metadata={},
            )

            vector_store = await indexing_service.create_new_vector_store(
                vector_store_request
            )

            request.tool_resources.file_search.vector_store_ids = [vector_store.id]
        elif ids_len == 1:
            logging.debug(
                "Attaching vector store with id: {} to new assistant".format(ids[0])
            )
            # How do we check to make sure the supplied vector_store_id is valid?
            crud_vector_store = CRUDVectorStore(db=session)

            try:
                await crud_vector_store.get(filters=FilterVectorStore(id=ids[0]))
            except Exception as e:
                raise e
        else:
            logging.debug(
                "No files or vector store id found; assistant will be created with no vector store"
            )

        with suppress(AttributeError):
            request.tool_resources.file_search.vector_stores = (
                None  # remove vector_stores if it's there
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
    assistant_deleted = await crud_assistant.delete(
        filters=FilterAssistant(id=assistant_id)
    )
    return AssistantDeleted(
        id=assistant_id,
        deleted=bool(assistant_deleted),
        object="assistant.deleted",
    )

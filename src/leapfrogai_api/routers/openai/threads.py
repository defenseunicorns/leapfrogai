"""OpenAI Compliant Threads API Router."""

from fastapi import HTTPException, APIRouter, status
from openai.types.beta import Thread, ThreadDeleted

from leapfrogai_api.typedef.threads import ModifyThreadRequest, CreateThreadRequest
from leapfrogai_api.data.crud_thread import CRUDThread
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.validate_tools import (
    validate_tool_resources,
)

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads"])


@router.post("")
async def create_thread(request: CreateThreadRequest, session: Session) -> Thread:
    """Create a thread."""
    if request.tool_resources and not validate_tool_resources(request.tool_resources):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool resource: {request.tool_resources}",
        )

    new_thread: Thread | None = await request.create_thread(session)

    if new_thread:
        # Once the thread has been created, add all the request's messages to the DB
        await request.create_messages(new_thread, session)

        return new_thread

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unable to create thread",
    )


@router.get("/{thread_id}")
async def retrieve_thread(thread_id: str, session: Session) -> Thread:
    """Retrieve a thread."""
    crud_thread = CRUDThread(db=session)

    if not (thread := await crud_thread.get(filters={"id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found",
        )

    return thread


@router.post("/{thread_id}")
async def modify_thread(
    thread_id: str, request: ModifyThreadRequest, session: Session
) -> Thread:
    """Modify a thread."""

    if request.tool_resources and not validate_tool_resources(request.tool_resources):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool resource: {request.tool_resources}",
        )

    crud_thread = CRUDThread(db=session)

    if not (thread := await crud_thread.get(filters={"id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found",
        )

    try:
        thread.metadata = getattr(request, "metadata", thread.metadata)
        thread.tool_resources = getattr(
            request, "tool_resources", thread.tool_resources
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse thread request",
        ) from exc

    if not (response := await crud_thread.update(id_=thread_id, object_=thread)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update thread",
        )

    return response


@router.delete("/{thread_id}")
async def delete_thread(thread_id: str, session: Session) -> ThreadDeleted:
    """Delete a thread."""
    try:
        crud_thread = CRUDThread(db=session)

        thread_deleted = await crud_thread.delete(filters={"id": thread_id})
        return ThreadDeleted(
            id=thread_id,
            object="thread.deleted",
            deleted=bool(thread_deleted),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to delete thread",
        ) from exc

"""OpenAI Compliant Threads API Router."""

import traceback
from fastapi import HTTPException, APIRouter, status
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer
from openai.types.beta import Thread, ThreadDeleted
from openai.types.beta.threads import Message, MessageDeleted, Run
from openai.types.beta.threads.runs import RunStep
from openai.pagination import SyncCursorPage
from leapfrogai_api.backend.types import (
    ModifyThreadRequest,
    ModifyMessageRequest,
    ModifyRunRequest,
)
from leapfrogai_api.routers.openai.requests.create_message_request import (
    CreateMessageRequest,
)
from leapfrogai_api.routers.openai.requests.thread_run_create_params_request import (
    ThreadRunCreateParamsRequestBaseRequest,
)
from leapfrogai_api.routers.openai.requests.run_create_params_request import (
    RunCreateParamsRequestBaseRequest,
)
from leapfrogai_api.routers.openai.requests.create_thread_request import (
    CreateThreadRequest,
)
from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.data.crud_run import CRUDRun
from leapfrogai_api.data.crud_thread import CRUDThread
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.validate_tools import (
    validate_tool_resources,
    validate_assistant_tool_choice_option,
)

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads"])
security = HTTPBearer()


@router.post("")
async def create_thread(request: CreateThreadRequest, session: Session) -> Thread:
    """Create a thread."""
    if request.tool_resources and not validate_tool_resources(request.tool_resources):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool resource: {request.tool_resources}",
        )
    try:
        new_thread: Thread | None = await request.create_thread(session)

        if new_thread:
            # Once the thread has been created, add all the request's messages to the DB
            await request.create_messages(new_thread, session)

            return new_thread
        else:
            raise Exception("Thread creation failed!")
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create thread",
        ) from exc


@router.post("/{thread_id}/runs", response_model=None)
async def create_run(
    thread_id: str, session: Session, request: RunCreateParamsRequestBaseRequest
) -> Run | StreamingResponse:
    """Create a run."""

    if request.tools and not validate_tool_resources(request.tools):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool resource: {request.tools}",
        )

    if request.tool_choice and not validate_assistant_tool_choice_option(
        request.tool_choice
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool choice option: {request.tool_choice}",
        )

    try:
        new_run = await request.create_run(session, thread_id)

        if not new_run:
            raise Exception("The DB failed to create the run")

        existing_thread: Thread = await retrieve_thread(
            thread_id,
            session,
        )

        return await request.generate_response(existing_thread, new_run, session)
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create run",
        ) from exc


@router.post("/runs", response_model=None)
async def create_thread_and_run(
    session: Session, request: ThreadRunCreateParamsRequestBaseRequest
) -> Run | StreamingResponse:
    """Create a thread and run."""

    try:
        new_run, new_thread = await request.create_run_and_thread(session)

        if not new_run:
            raise Exception("The DB failed to create the run")

        return await request.generate_response(new_run, new_thread, session)
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create run",
        ) from exc


@router.get("/{thread_id}/runs")
async def list_runs(thread_id: str, session: Session) -> SyncCursorPage[Run]:
    """List all the runs in a thread."""
    try:
        crud_run = CRUDRun(db=session)
        runs = await crud_run.list(filters={"thread_id": thread_id})

        if runs is None:
            return SyncCursorPage(object="list", data=[])

        return SyncCursorPage(object="list", data=runs)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list runs for thread {thread_id}",
        ) from exc


@router.get("/{thread_id}/runs/{run_id}")
async def retrieve_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Retrieve a run."""
    crud_run = CRUDRun(db=session)

    if not (run := await crud_run.get(filters={"id": run_id, "thread_id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run {run_id} not found for thread {thread_id}.",
        )
    return run


@router.post("/{thread_id}/runs/{run_id}")
async def modify_run(
    thread_id: str, run_id: str, request: ModifyRunRequest, session: Session
) -> Run:
    """Modify a run."""
    crud_run = CRUDRun(db=session)

    if not (run := await crud_run.get(filters={"id": run_id, "thread_id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found",
        )

    try:
        run.metadata = getattr(request, "metadata", run.metadata)

        return await crud_run.update(
            id_=run_id,
            object_=run,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse run request",
        ) from exc


@router.post("/{thread_id}/runs/{run_id}/submit_tool_outputs")
async def submit_tool_outputs(thread_id: str, run_id: str, session: Session) -> Run:
    """Submit tool outputs for a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}/runs/{run_id}/cancel")
async def cancel_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Cancel a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/runs/{run_id}/steps")
async def list_run_steps(
    thread_id: str, run_id: str, session: Session
) -> list[RunStep]:
    """List all the steps in a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/runs/{run_id}/steps/{step_id}")
async def retrieve_run_step(
    thread_id: str, run_id: str, step_id: str, session: Session
) -> RunStep:
    """Retrieve a step."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


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

        return await crud_thread.update(
            id_=thread_id,
            object_=thread,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse thread request",
        ) from exc


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


@router.post("/{thread_id}/messages")
async def create_message(
    thread_id: str, request: CreateMessageRequest, session: Session
) -> Message:
    """Create a message."""
    try:
        crud_message = CRUDMessage(db=session)

        message_content = await request.get_message_content()

        message = Message(
            id="",  # Leave blank to have Postgres generate a UUID
            attachments=request.attachments,
            content=message_content,
            created_at=0,  # Leave blank to have Postgres generate a timestamp
            metadata=request.metadata,
            object="thread.message",
            role=request.role,
            status="completed",
            thread_id=thread_id,
        )
        return await crud_message.create(object_=message)
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create message",
        ) from exc


@router.get("/{thread_id}/messages")
async def list_messages(thread_id: str, session: Session) -> SyncCursorPage[Message]:
    """List all the messages in a thread."""
    try:
        crud_message = CRUDMessage(db=session)
        messages: list[Message] | None = await crud_message.list(
            filters={"thread_id": thread_id}
        )

        if messages is None:
            return SyncCursorPage(object="list", data=[])

        return SyncCursorPage(object="list", data=messages)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list messages",
        ) from exc


@router.get("/{thread_id}/messages/{message_id}")
async def retrieve_message(
    thread_id: str, message_id: str, session: Session
) -> Message | None:
    """Retrieve a message."""
    crud_message = CRUDMessage(db=session)
    return await crud_message.get(filters={"id": message_id, "thread_id": thread_id})


@router.post("/{thread_id}/messages/{message_id}")
async def modify_message(
    thread_id: str, message_id: str, request: ModifyMessageRequest, session: Session
) -> Message:
    """Modify a message."""
    crud_message = CRUDMessage(db=session)

    if not (
        message := await crud_message.get(
            filters={"id": message_id, "thread_id": thread_id}
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    try:
        message.metadata = getattr(request, "metadata", message.metadata)

        return await crud_message.update(
            id_=message_id,
            object_=message,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse message request",
        ) from exc


@router.delete("/{thread_id}/messages/{message_id}")
async def delete_message(
    thread_id: str, message_id: str, session: Session
) -> MessageDeleted:
    """Delete message from a thread."""

    crud_message = CRUDMessage(db=session)
    message_deleted = await crud_message.delete(
        filters={"id": message_id, "thread_id": thread_id}
    )
    return MessageDeleted(
        id=message_id,
        deleted=bool(message_deleted),
        object="thread.message.deleted",
    )

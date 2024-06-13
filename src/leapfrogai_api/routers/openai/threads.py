"""OpenAI Compliant Threads API Router."""

import traceback

from fastapi import HTTPException, APIRouter, status
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer
from openai.types.beta import Thread, ThreadDeleted
from openai.types.beta.threads import Message, MessageDeleted, Run
from openai.types.beta.threads.runs import RunStep

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

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads"])
security = HTTPBearer()


@router.post("")
async def create_thread(request: CreateThreadRequest, session: Session) -> Thread:
    """Create a thread."""
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
async def list_runs(thread_id: str, session: Session) -> list[Run]:
    """List all the runs in a thread."""
    try:
        crud_run = CRUDRun(db=session)
        runs = await crud_run.list(filters={"thread_id": thread_id})

        return runs
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list runs for thread {thread_id}",
        ) from exc


@router.get("/{thread_id}/runs/{run_id}")
async def retrieve_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Retrieve a run."""
    crud_run = CRUDRun(db=session)
    return await crud_run.get(filters={"id": run_id, "thread_id": thread_id})


@router.post("/{thread_id}/runs/{run_id}")
async def modify_run(
    thread_id: str, run_id: str, request: ModifyRunRequest, session: Session
) -> Run:
    """Modify a run."""
    run = CRUDRun(db=session)

    if not (old_run := await run.get(filters={"id": run_id, "thread_id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found",
        )

    try:
        new_run = Run(
            id=run_id,
            thread_id=thread_id,
            created_at=old_run.created_at,
            metadata=getattr(request, "metadata", old_run.metadata),
            object="thread.run",
        )

        return await run.update(
            id_=run_id,
            object_=new_run,
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
    thread = CRUDThread(db=session)

    if not (old_thread := await thread.get(filters={"id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found",
        )

    try:
        new_thread = Thread(
            id=thread_id,
            created_at=old_thread.created_at,
            metadata=getattr(request, "metadata", old_thread.metadata),
            object="thread",
            tool_resources=getattr(
                request, "tool_resources", old_thread.tool_resources
            ),
        )

        return await thread.update(
            id_=thread_id,
            object_=new_thread,
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
async def list_messages(thread_id: str, session: Session) -> list[Message]:
    """List all the messages in a thread."""
    try:
        crud_message = CRUDMessage(db=session)
        messages: list[Message] | None = await crud_message.list(
            filters={"thread_id": thread_id}
        )

        if messages is None:
            return []

        return messages
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
    message = CRUDMessage(db=session)

    if not (
        old_message := await message.get(
            filters={"id": message_id, "thread_id": thread_id}
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    try:
        new_message = Message(
            id=message_id,
            created_at=old_message.created_at,
            content=old_message.content,
            metadata=getattr(request, "metadata", old_message.metadata),
            object="thread.message",
            attachments=old_message.attachments,
            role=old_message.role,
            status=old_message.status,
            thread_id=thread_id,
        )

        return await message.update(
            id_=message_id,
            object_=new_message,
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

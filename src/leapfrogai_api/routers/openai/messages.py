"""OpenAI Compliant Threads API Router."""

from fastapi import HTTPException, APIRouter, status
from openai.types.beta.threads import Message, MessageDeleted
from openai.pagination import SyncCursorPage
from leapfrogai_api.typedef.messages import CreateMessageRequest, ModifyMessageRequest
from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads/messages"])


@router.post("/{thread_id}/messages")
async def create_message(
    thread_id: str, request: CreateMessageRequest, session: Session
) -> Message:
    """Create a message."""

    crud_message = CRUDMessage(db=session)

    try:
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
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse message request.",
        ) from exc

    if not (response := await crud_message.create(object_=message)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create message.",
        )

    return response


@router.get("/{thread_id}/messages")
async def list_messages(thread_id: str, session: Session) -> SyncCursorPage[Message]:
    """List all the messages in a thread."""
    try:
        crud_message = CRUDMessage(db=session)
        messages: list[Message] | None = await crud_message.list(
            filters={"thread_id": thread_id}
        )

        if not messages:
            messages = []

        return SyncCursorPage(data=messages)
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

    message.metadata = getattr(request, "metadata", message.metadata)

    if not (response := await crud_message.update(id_=message_id, object_=message)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update message",
        )

    return response


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

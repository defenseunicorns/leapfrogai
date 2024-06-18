from __future__ import annotations
import traceback
from fastapi import HTTPException, status
from openai.types.beta import Thread
from openai.types.beta.thread import ToolResources as BetaThreadToolResources
from openai.types.beta.threads import Message, MessageDeleted, MessageContent
from pydantic import BaseModel, Field
from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.data.crud_thread import CRUDThread
from leapfrogai_api.routers.supabase_session import Session


class CreateThreadRequest(BaseModel):
    """Request object for creating a thread."""

    messages: list[Message] | None = Field(default=None, examples=[None])
    tool_resources: BetaThreadToolResources | None = Field(
        default=None, examples=[None]
    )
    metadata: dict | None = Field(default={}, examples=[{}])

    async def create_thread(self, session):
        crud_thread = CRUDThread(db=session)
        thread = Thread(
            id="",  # Leave blank to have Postgres generate a UUID
            created_at=0,  # Leave blank to have Postgres generate a timestamp
            metadata=self.metadata,
            object="thread",
            tool_resources=self.tool_resources,
        )
        new_thread = await crud_thread.create(object_=thread)
        return new_thread

    async def create_messages(self, new_thread, session):
        new_messages: list[Message] = []

        try:
            if self.messages:
                new_messages = [
                    await self.create_message(
                        message.content,
                        new_thread.id,
                        session,
                    )
                    for message in self.messages
                ]
        except Exception as exc:
            for message in new_messages:
                """Clean up any messages added prior to the error"""
                await self.delete_message(
                    thread_id=new_thread.id, message_id=message.id, session=session
                )
            raise exc

    async def create_message(
        self, message_content: list[MessageContent], thread_id: str, session: Session
    ) -> Message:
        """Create a message."""
        try:
            crud_message = CRUDMessage(db=session)

            message = Message(
                id="",  # Leave blank to have Postgres generate a UUID
                attachments=self.attachments,
                content=message_content,
                created_at=0,  # Leave blank to have Postgres generate a timestamp
                metadata=self.metadata,
                object="thread.message",
                role=self.role,
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

    async def delete_message(
        self, thread_id: str, message_id: str, session: Session
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

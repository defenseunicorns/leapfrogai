from __future__ import annotations

import traceback
from typing import Literal

from fastapi import HTTPException, status
from openai.types.beta.threads import MessageContent, TextContentBlock, Text, Message
from openai.types.beta.threads.message import Attachment
from pydantic import BaseModel, Field

from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.routers.supabase_session import Session


class CreateMessageRequest(BaseModel):
    """Request object for creating a message."""

    role: Literal["user", "assistant"] = Field(default="user")
    content: str | list[MessageContent] = Field(
        default=[TextContentBlock(text=Text(value="", annotations=[]), type="text")],
        examples=[[TextContentBlock(text=Text(value="", annotations=[]), type="text")]],
    )
    attachments: list[Attachment] | None = Field(default=None, examples=[None])
    metadata: dict | None = Field(default={}, examples=[{}])

    async def get_message_content(self):
        if isinstance(self.content, str):
            text_input: TextContentBlock = TextContentBlock(
                text=Text(value=self.content, annotations=[]), type="text"
            )
            message_content: list[MessageContent] = [text_input]
        else:
            message_content: list[MessageContent] = self.content
        return message_content

    async def create_message(
        self, session: Session, thread_id: str, run_id: str = None
    ) -> Message:
        """Create a message."""
        try:
            crud_message = CRUDMessage(db=session)

            message_content = await self.get_message_content()

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

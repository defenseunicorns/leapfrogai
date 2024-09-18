from __future__ import annotations

import time
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
    metadata: dict[str, str] | None = Field(default={}, examples=[{}])

    async def get_message_content(self) -> list[MessageContent]:
        """Get the message content."""
        if isinstance(self.content, str):
            text_input: TextContentBlock = TextContentBlock(
                text=Text(value=self.content, annotations=[]), type="text"
            )
            return [text_input]

        return self.content

    async def create_message(
        self,
        session: Session,
        thread_id: str,
        run_id: str | None = None,
        assistant_id: str | None = None,
    ) -> Message:
        """Create a message."""
        try:
            crud_message = CRUDMessage(db=session)

            message_content = await self.get_message_content()

            message = Message(
                id="",  # Leave blank to have Postgres generate a UUID
                attachments=self.attachments,
                content=message_content,
                created_at=int(
                    time.time()
                ),  # Leave blank to have Postgres generate a timestamp
                metadata=self.metadata,
                object="thread.message",
                role=self.role,
                status="completed",
                thread_id=thread_id,
                assistant_id=assistant_id,
                run_id=run_id,
            )

            if not (response := await crud_message.create(object_=message)):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unable to create message",
                )
            return response
        except Exception as exc:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create message",
            ) from exc


class ModifyMessageRequest(BaseModel):
    """Request object for modifying a message."""

    metadata: dict | None = Field(default=None, examples=[{}])

from __future__ import annotations

import logging
from openai.types.beta.threads import Run
from openai.types.beta.threads.run_create_params import (
    AdditionalMessage,
    AdditionalMessageAttachment,
    AdditionalMessageAttachmentToolFileSearch,
)
from pydantic import Field

from .run_create_base import (
    RunCreateParamsRequestBase,
)
from leapfrogai_api.typedef.messages import (
    CreateMessageRequest,
)
from leapfrogai_api.data.crud_run import CRUDRun
from leapfrogai_api.backend.converters import (
    from_content_param_to_content,
)
from leapfrogai_api.routers.supabase_session import Session


class RunCreateParamsRequest(RunCreateParamsRequestBase):
    additional_instructions: str | None = Field(
        default=None,
        examples=["Please provide a summary of the conversation so far."],
        description="Additional instructions to be considered during the run execution.",
    )
    additional_messages: list[AdditionalMessage] | None = Field(
        default=[],
        description="A list of additional messages to be added to the thread before the run starts.",
        examples=[
            [
                AdditionalMessage(
                    content="This is a test",
                    role="user",
                    attachments=[
                        AdditionalMessageAttachment(
                            file_id="",
                            tools=[
                                AdditionalMessageAttachmentToolFileSearch(
                                    type="file_search"
                                )
                            ],
                        )
                    ],
                    metadata={},
                )
            ]
        ],
    )
    stream: bool | None = Field(
        default=None,
        description="If set to true, the response will be streamed as it's generated.",
        examples=[False],
    )

    async def create_additional_messages(self, session: Session, thread_id: str):
        """If additional messages exist, create them in the DB as a part of this thread"""
        if not self.additional_messages:
            self.additional_messages = []

        for additional_message in self.additional_messages:
            # Convert the messages content into the correct format
            if content := additional_message.get("content"):
                message_content = from_content_param_to_content(
                    thread_message_content=content
                )
            else:
                logging.getLogger(__name__).warning(
                    "Found additional message without content"
                )
                continue

            create_message_request = CreateMessageRequest(
                role=additional_message["role"],
                content=[message_content],
                attachments=additional_message.get("attachments"),
                metadata=additional_message.get("metadata").__dict__,
            )

            await create_message_request.create_message(
                session=session, thread_id=thread_id
            )

    async def update_with_assistant_data(self, session: Session):
        await super().update_with_assistant_data(session=session)

    async def create_run(self, session, thread_id):
        """Create a run."""
        await self.update_with_assistant_data(session=session)

        await self.create_additional_messages(session=session, thread_id=thread_id)

        create_params = RunCreateParamsRequestBase.model_validate(self.__dict__)

        crud_run = CRUDRun(db=session)
        run = Run(
            id="",  # Leave blank to have Postgres generate a UUID
            created_at=0,  # Leave blank to have Postgres generate a timestamp
            thread_id=thread_id,
            object="thread.run",
            status="completed",
            **create_params.__dict__,
        )
        return await crud_run.create(object_=run)

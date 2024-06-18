from __future__ import annotations
from typing import AsyncGenerator, Any
from openai.types.beta.threads import Run
from openai.types.beta.threads.run_create_params import (
    AdditionalMessage,
    AdditionalMessageAttachment,
    AdditionalMessageAttachmentToolFileSearch,
)
from pydantic import Field
from starlette.responses import StreamingResponse
from leapfrogai_api.routers.openai.requests.run_create_params_request_base import (
    RunCreateParamsRequestBase,
)
from leapfrogai_api.routers.openai.requests.create_message_request import (
    CreateMessageRequest,
)
from leapfrogai_api.data.crud_run import CRUDRun
from leapfrogai_api.backend.converters import (
    from_content_param_to_content,
)
from leapfrogai_api.routers.supabase_session import Session


class RunCreateParamsRequestBaseRequest(RunCreateParamsRequestBase):
    additional_instructions: str | None = Field(default=None, examples=[""])
    additional_messages: list[AdditionalMessage] | None = Field(
        default=[],
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
    stream: bool | None = Field(default=None, examples=[False])

    async def create_additional_messages(self, session: Session, thread_id: str):
        """If additional messages exist, create them in the DB as a part of this thread"""
        if self.additional_messages:
            for additional_message in self.additional_messages:
                # Convert the messages content into the correct format
                if content := additional_message.get("content"):
                    message_content = from_content_param_to_content(
                        thread_message_content=content
                    )

                create_message_request = CreateMessageRequest(
                    role=additional_message["role"],
                    content=[message_content],
                    attachments=additional_message.get("attachments"),
                    metadata=additional_message.get("metadata"),
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

    async def generate_response(self, existing_thread, new_run: Run, session: Session):
        """Generate a new response based on the existing thread"""
        if self.stream:
            initial_messages: list[str] = (
                RunCreateParamsRequestBase.get_initial_messages_base(run=new_run)
            )
            ending_messages: list[str] = (
                RunCreateParamsRequestBase.get_ending_messages_base(run=new_run)
            )
            stream: AsyncGenerator[str, Any] = (
                super().stream_generate_message_for_thread(session=session, initial_messages=initial_messages, thread=existing_thread, ending_messages=ending_messages, run_id=new_run.id, additional_instructions=self.additional_instructions)
            )

            return StreamingResponse(stream, media_type="text/event-stream")
        else:
            await super().generate_message_for_thread(
                session=session,
                thread=existing_thread,
                run_id=new_run.id,
                additional_instructions=self.additional_instructions,
            )

            return new_run

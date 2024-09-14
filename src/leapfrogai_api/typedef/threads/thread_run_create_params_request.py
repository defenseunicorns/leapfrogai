from __future__ import annotations
import logging
from typing import Iterable
from pydantic import Field

from openai.types.beta.thread import (
    ToolResources as BetaThreadToolResources,
    ToolResourcesFileSearch as BetaThreadToolResourcesFileSearch,
)
from openai.types.beta.thread_create_and_run_params import (
    Thread as ThreadCreateAndRunsThread,
    ThreadToolResources,
    ThreadToolResourcesFileSearch,
    ThreadMessage,
    ThreadMessageAttachment,
    ThreadMessageAttachmentToolFileSearch,
)
from openai.types.beta.threads import MessageContent, Message, Run

from leapfrogai_api.typedef.messages import (
    CreateMessageRequest,
)
from leapfrogai_api.typedef.runs import (
    RunCreateParamsRequestBase,
)
from leapfrogai_api.data.crud_run import CRUDRun
from leapfrogai_api.backend.converters import (
    from_content_param_to_content,
)
from leapfrogai_api.typedef.threads import CreateThreadRequest

from leapfrogai_api.routers.supabase_session import Session


logger = logging.getLogger(__name__)


class ThreadRunCreateParamsRequest(RunCreateParamsRequestBase):
    thread: ThreadCreateAndRunsThread | None = Field(
        default=None,
        examples=[
            ThreadCreateAndRunsThread(
                tool_resources=ThreadToolResources(
                    file_search=ThreadToolResourcesFileSearch(vector_store_ids=[])
                ),
                messages=[
                    ThreadMessage(
                        content="This is a test",
                        role="user",
                        attachments=[
                            ThreadMessageAttachment(
                                file_id="",
                                tools=[
                                    ThreadMessageAttachmentToolFileSearch(
                                        type="file_search"
                                    )
                                ],
                            )
                        ],
                        metadata={},
                    )
                ],
            )
        ],
    )
    tool_resources: BetaThreadToolResources | None = Field(
        default=None, examples=[BetaThreadToolResourcesFileSearch(vector_store_ids=[])]
    )
    stream: bool | None = Field(default=None, examples=[False])

    async def update_with_assistant_data(self, session: Session):
        assistant = await super().update_with_assistant_data(session)

        if assistant and assistant.tool_resources:
            assistant_tool_resources = BetaThreadToolResources.model_validate(
                assistant.tool_resources.model_dump()
            )

            self.tool_resources = self.tool_resources or assistant_tool_resources

    async def create_thread_request(self) -> CreateThreadRequest:
        thread_request: CreateThreadRequest = CreateThreadRequest(
            messages=[],
            tool_resources=self.tool_resources,
            metadata=self.metadata,
        )
        if self.thread:
            # If the thread exists, convert all of its messages into a form that can be used by create_thread.
            thread_messages: Iterable[ThreadMessage] = self.thread.get("messages")
            for message in thread_messages:
                try:
                    # Convert the messages content into the correct format
                    message_content: MessageContent = from_content_param_to_content(
                        message.get("content")
                    )

                    new_message: Message = Message(
                        id="",
                        created_at=0,
                        object="thread.message",
                        status="in_progress",
                        thread_id="",
                        content=[message_content],
                        role=message.get("role"),
                        attachments=message.get("attachments"),
                        metadata=message.get("metadata"),
                    )

                    thread_request.messages.append(new_message)
                except ValueError as exc:
                    logger.error(f"\t{exc}")
                    continue
        return thread_request

    async def create_run_and_thread(self, session: Session):
        await self.update_with_assistant_data(session)
        new_thread_request: CreateThreadRequest = await self.create_thread_request()
        new_thread = await new_thread_request.create_thread(session)

        crud_run = CRUDRun(db=session)
        create_params: RunCreateParamsRequestBase = RunCreateParamsRequestBase(
            **self.__dict__
        )
        run = Run(
            id="",  # Leave blank to have Postgres generate a UUID
            created_at=0,  # Leave blank to have Postgres generate a timestamp
            thread_id=new_thread.id,
            object="thread.run",
            status="completed",  # This is always completed as the new message is already created by this point
            **create_params.__dict__,
        )
        new_run = await crud_run.create(object_=run)

        for message in new_thread_request.messages:
            create_message_request: CreateMessageRequest = CreateMessageRequest(
                role=message.role,
                content=message.content,
                attachments=message.attachments,
                metadata=message.metadata,
            )
            await create_message_request.create_message(
                session=session,
                thread_id=new_thread.id,
                run_id=new_run.id if new_run else None,
            )

        return new_run, new_thread

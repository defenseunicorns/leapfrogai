from __future__ import annotations

import logging
import traceback
import uuid
from typing import cast, AsyncGenerator, Any
from uuid import UUID

from fastapi import HTTPException, status
from openai.types.beta import (
    AssistantResponseFormatOptionParam,
    AssistantToolChoiceOptionParam,
    AssistantToolParam,
    FileSearchToolParam,
    Assistant,
    Thread,
)
from openai.types.beta.assistant_stream_event import (
    ThreadMessageCreated,
    ThreadMessageInProgress,
    ThreadMessageCompleted,
)
from openai.types.beta.assistant_stream_event import (
    ThreadRunCreated,
    ThreadRunQueued,
    ThreadRunInProgress,
    ThreadRunCompleted,
)
from openai.types.beta.thread import (
    ToolResources as BetaThreadToolResources,
    ToolResourcesFileSearch as BetaThreadToolResourcesFileSearch,
)
from openai.types.beta.threads import (
    Message,
)
from openai.types.beta.threads import Run
from openai.types.beta.threads.run_create_params import TruncationStrategy
from postgrest.base_request_builder import SingleAPIResponse
from pydantic import BaseModel, Field, ValidationError

from leapfrogai_api.backend.rag.query import QueryService
from leapfrogai_api.backend.types import (
    ChatMessage,
    RAGResponse,
    ChatCompletionResponse,
    ChatCompletionRequest,
    ChatChoice,
)
from leapfrogai_api.backend.validators import AssistantToolChoiceParamValidator
from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.routers.openai.assistants import retrieve_assistant
from leapfrogai_api.routers.openai.chat import chat_complete, chat_complete_stream_raw
from leapfrogai_api.backend.converters import (
    from_assistant_stream_event_to_str,
    from_text_to_message,
    from_chat_completion_choice_to_thread_message_delta,
)
from leapfrogai_api.routers.openai.requests.create_message_request import (
    CreateMessageRequest,
)
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils import get_model_config
from leapfrogai_sdk.chat.chat_pb2 import (
    ChatCompletionResponse as ProtobufChatCompletionResponse,
)


class RunCreateParamsRequestBase(BaseModel):
    assistant_id: str = Field(default="", examples=["123ab"])
    instructions: str = Field(default="", examples=["You are a helpful AI assistant."])
    max_completion_tokens: int | None = Field(default=None, examples=[4096])
    max_prompt_tokens: int | None = Field(default=None, examples=[32768])
    metadata: dict | None = Field(default=None, examples=[{}])
    model: str | None = Field(default=None, examples=["llama-cpp-python"])
    response_format: AssistantResponseFormatOptionParam | None = Field(
        default=None, examples=["auto"]
    )
    temperature: float | None = Field(default=None, examples=[1.0])
    tool_choice: AssistantToolChoiceOptionParam | None = Field(
        default=None, examples=["auto"]
    )
    tools: list[AssistantToolParam] = Field(
        default=[], examples=[[FileSearchToolParam(type="file_search")]]
    )
    top_p: float | None = Field(default=None, examples=[1.0])
    truncation_strategy: TruncationStrategy | None = Field(
        default=None, examples=[TruncationStrategy(type="auto", last_messages=None)]
    )
    parallel_tool_calls: bool | None = Field(default=None, examples=[False])

    @staticmethod
    def get_initial_messages_base(run: Run) -> list[str]:
        return [
            from_assistant_stream_event_to_str(
                ThreadRunCreated(data=run, event="thread.run.created")
            ),
            from_assistant_stream_event_to_str(
                ThreadRunQueued(data=run, event="thread.run.queued")
            ),
            from_assistant_stream_event_to_str(
                ThreadRunInProgress(data=run, event="thread.run.in_progress")
            ),
        ]

    @staticmethod
    def get_ending_messages_base(run: Run) -> list[str]:
        return [
            from_assistant_stream_event_to_str(
                ThreadRunCompleted(data=run, event="thread.run.completed")
            )
        ]

    async def update_with_assistant_data(self, session: Session) -> Assistant:
        assistant: Assistant | None = await retrieve_assistant(
            session=session, assistant_id=self.assistant_id
        )

        self.model = self.model or assistant.model
        self.temperature = self.temperature or assistant.temperature
        self.top_p = self.top_p or assistant.top_p
        self.instructions = self.instructions or assistant.instructions

        return assistant

    def can_use_rag(self, thread: Thread) -> bool:
        has_tool_choice: bool = self.tool_choice is not None
        has_tool_resources: bool = bool(
            thread.tool_resources
            and thread.tool_resources.file_search
            and thread.tool_resources.file_search.vector_store_ids
        )

        if has_tool_choice and has_tool_resources:
            if isinstance(self.tool_choice, str):
                return self.tool_choice == "auto" or self.tool_choice == "required"
            else:
                try:
                    if AssistantToolChoiceParamValidator.validate_python(
                        self.tool_choice
                    ):
                        return self.tool_choice.get("type") == "file_search"
                except ValidationError:
                    traceback.print_exc()
                    logging.error(
                        "Cannot use RAG for request, failed to validate tool for thread"
                    )
                    return False

        return False

    async def list_messages(self, thread_id: str, session: Session) -> list[Message]:
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

    async def create_chat_messages(
        self, session: Session, thread: Thread, additional_instructions: str | None
    ) -> list[ChatMessage]:
        # Get existing messages
        thread_messages: list[Message] = await self.list_messages(thread.id, session)
        # Holds the converted thread's messages
        chat_messages: list[ChatMessage] = []

        # 1 - Model instructions (system message)
        if self.instructions:
            chat_messages.append(ChatMessage(role="system", content=self.instructions))

        # 2 - Additional model instructions (system message)
        if additional_instructions:
            chat_messages.append(
                ChatMessage(role="system", content=additional_instructions)
            )

        chat_thread_messages = [
            ChatMessage(role=message.role, content=message.content[0].text.value)
            for message in thread_messages
        ]

        use_rag: bool = self.can_use_rag(thread)

        # 3 - RAG results
        if use_rag:
            query_service = QueryService(db=session)
            tool_resources: BetaThreadToolResources = cast(
                BetaThreadToolResources, thread.tool_resources
            )
            file_search: BetaThreadToolResourcesFileSearch = cast(
                BetaThreadToolResourcesFileSearch, tool_resources.file_search
            )
            vector_store_ids: list[str] = cast(list[str], file_search.vector_store_ids)

            for vector_store_id in vector_store_ids:
                rag_results_raw: SingleAPIResponse[
                    RAGResponse
                ] = await query_service.query_rag(
                    query=chat_thread_messages[0].content,
                    vector_store_id=vector_store_id,
                )
                rag_responses: RAGResponse = RAGResponse(data=rag_results_raw.data)

                for count, rag_response in enumerate(rag_responses.data):
                    """Insert the RAG response messages just before the user's query"""
                    response_with_instructions: str = (
                        f"<start attached file {count}'s content>\n"
                        f"{rag_response.content}"
                        f"\n<end attached file {count}'s content>"
                    )
                    chat_messages.append(
                        ChatMessage(
                            role="user", content=response_with_instructions
                        ),  # TODO: Should this go in user or something else like function?
                    )

        # 4 - Existing messages including the current user's message
        chat_messages.extend(chat_thread_messages)

        return chat_messages

    async def generate_message_for_thread(
        self,
        session: Session,
        thread: Thread,
        additional_instructions: str | None = None,
    ):
        chat_messages: list[ChatMessage] = await self.create_chat_messages(
            session, thread, additional_instructions
        )

        # Generate a new message and add it to the thread creation request
        chat_response: ChatCompletionResponse = await chat_complete(
            req=ChatCompletionRequest(
                model=str(self.model),
                messages=chat_messages,
                functions=None,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=self.stream,
                stop=None,
                max_tokens=self.max_completion_tokens,
            ),
            model_config=get_model_config(),
            session=session,
        )

        choice: ChatChoice = cast(ChatChoice, chat_response.choices[0])

        message = from_text_to_message(choice.message.content)

        create_message_request = CreateMessageRequest(
            role=message.role,
            content=message.content,
            attachments=message.attachments,
            metadata=message.metadata,
        )

        await create_message_request.create_message(
            thread_id=thread.id,
            session=session,
        )

    async def stream_generate_message_for_thread(
        self,
        session: Session,
        initial_messages: list[str],
        thread: Thread,
        ending_messages: list[str],
        additional_instructions: str | None = None,
    ) -> AsyncGenerator[str, Any]:
        chat_messages: list[ChatMessage] = await self.create_chat_messages(
            session, thread, additional_instructions
        )

        chat_response: AsyncGenerator[ProtobufChatCompletionResponse, Any] = (
            chat_complete_stream_raw(
                req=ChatCompletionRequest(
                    model=str(self.model),
                    messages=chat_messages,
                    functions=None,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    stream=self.stream,
                    stop=None,
                    max_tokens=self.max_completion_tokens,
                ),
                model_config=get_model_config(),
            )
        )

        for message in initial_messages:
            yield message
            yield "\n\n"

        # Create an empty message
        new_message: Message = from_text_to_message("")

        create_message_request = CreateMessageRequest(
            role=new_message.role,
            content=new_message.content,
            attachments=new_message.attachments,
            metadata=new_message.metadata,
        )

        new_message = await create_message_request.create_message(
            thread_id=thread.id,
            session=session,
        )

        yield from_assistant_stream_event_to_str(
            ThreadMessageCreated(data=new_message, event="thread.message.created")
        )
        yield "\n\n"

        yield from_assistant_stream_event_to_str(
            ThreadMessageInProgress(
                data=new_message, event="thread.message.in_progress"
            )
        )
        yield "\n\n"

        # The accumulated streaming response
        response: str = ""

        index: int = 0
        async for streaming_response in chat_response:
            random_uuid: UUID = uuid.uuid4()
            # Build up the llm response so that it can be committed to the db as a new message
            response += streaming_response.choices[0].chat_item.content
            thread_message_event = (
                await from_chat_completion_choice_to_thread_message_delta(
                    index, random_uuid, streaming_response
                )
            )
            yield from_assistant_stream_event_to_str(thread_message_event)
            yield "\n\n"
            index += 1

        new_message.content[0].text.value = response

        crud_message = CRUDMessage(db=session)

        updated_message: Message = await crud_message.update(
            id_=new_message.id,
            object_=new_message,
        )

        yield from_assistant_stream_event_to_str(
            ThreadMessageCompleted(
                data=updated_message, event="thread.message.completed"
            )
        )
        yield "\n\n"

        for message in ending_messages:
            yield message
            yield "\n\n"

        yield "event: done\ndata: [DONE]"

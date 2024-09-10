from __future__ import annotations

import logging
import time
import traceback
import uuid
from typing import cast, AsyncGenerator, Any
from uuid import UUID

from fastapi import HTTPException, status
from openai.types.beta.assistant import ToolResources as BetaAssistantToolResources
from openai.types.beta import (
    AssistantResponseFormatOption,
    FileSearchTool,
    Assistant,
    Thread,
    AssistantToolChoiceOption,
    AssistantTool,
    AssistantToolChoice,
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
    TextContentBlock,
)
from openai.types.beta.threads import Run
from openai.types.beta.threads.run_create_params import TruncationStrategy
from postgrest.base_request_builder import SingleAPIResponse
from pydantic import BaseModel, Field, ValidationError

from leapfrogai_api.backend.converters import (
    from_assistant_stream_event_to_str,
    from_text_to_message,
    from_chat_completion_choice_to_thread_message_delta,
)
from leapfrogai_api.backend.rag.query import QueryService
from leapfrogai_api.backend.types import (
    ChatMessage,
    SearchResponse,
    ChatCompletionResponse,
    ChatCompletionRequest,
    ChatChoice,
    DEFAULT_MAX_COMPLETION_TOKENS,
    DEFAULT_MAX_PROMPT_TOKENS,
)
from leapfrogai_api.data.crud_assistant import CRUDAssistant, FilterAssistant
from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.routers.openai.chat import chat_complete, chat_complete_stream_raw
from leapfrogai_api.routers.openai.requests.create_message_request import (
    CreateMessageRequest,
)
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils import get_model_config
from leapfrogai_sdk.chat.chat_pb2 import (
    ChatCompletionResponse as ProtobufChatCompletionResponse,
)

logger = logging.getLogger(__name__)


class RunCreateParamsRequestBase(BaseModel):
    assistant_id: str = Field(default="", examples=["123ab"])
    instructions: str = Field(default="", examples=["You are a helpful AI assistant."])
    max_completion_tokens: int | None = Field(
        default=DEFAULT_MAX_COMPLETION_TOKENS, examples=[DEFAULT_MAX_COMPLETION_TOKENS]
    )
    max_prompt_tokens: int | None = Field(
        default=DEFAULT_MAX_PROMPT_TOKENS, examples=[DEFAULT_MAX_PROMPT_TOKENS]
    )
    metadata: dict | None = Field(default={}, examples=[{}])
    model: str | None = Field(default=None, examples=["llama-cpp-python"])
    response_format: AssistantResponseFormatOption | None = Field(
        default=None, examples=["auto"]
    )
    temperature: float | None = Field(default=None, examples=[1.0])
    tool_choice: AssistantToolChoiceOption | None = Field(
        default="auto", examples=["auto"]
    )
    tools: list[AssistantTool] = Field(
        default=[], examples=[[FileSearchTool(type="file_search")]]
    )
    top_p: float | None = Field(default=None, examples=[1.0])
    truncation_strategy: TruncationStrategy | None = Field(
        default=None, examples=[TruncationStrategy(type="auto", last_messages=None)]
    )
    parallel_tool_calls: bool | None = Field(default=False, examples=[False])

    def __init__(self, **data):
        super().__init__(**data)
        # TODO: Temporary fix to ensure max_completion_tokens and max_prompt_tokens are set
        if self.max_completion_tokens is None or self.max_completion_tokens < 1:
            logger.warning(
                "max_completion_tokens is not set or is less than 1, setting to %s",
                DEFAULT_MAX_COMPLETION_TOKENS,
            )
            self.max_completion_tokens = DEFAULT_MAX_COMPLETION_TOKENS
        if self.max_prompt_tokens is None or self.max_prompt_tokens < 1:
            logger.warning(
                "max_prompt_tokens is not set or is less than 1, setting to %s",
                DEFAULT_MAX_PROMPT_TOKENS,
            )
            self.max_prompt_tokens = DEFAULT_MAX_PROMPT_TOKENS

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

    async def update_with_assistant_data(self, session: Session) -> Assistant | None:
        crud_assistant = CRUDAssistant(session)
        assistant = await crud_assistant.get(
            filters=FilterAssistant(id=self.assistant_id)
        )

        if assistant:
            self.model = self.model or assistant.model
            self.temperature = self.temperature or assistant.temperature
            self.top_p = self.top_p or assistant.top_p
            self.instructions = self.instructions or assistant.instructions or ""

        return assistant

    def can_use_rag(
        self,
        tool_resources: BetaThreadToolResources | None,
    ) -> bool:
        if not tool_resources:
            return False

        has_tool_choice: bool = self.tool_choice is not None
        has_tool_resources: bool = bool(
            tool_resources.file_search and tool_resources.file_search.vector_store_ids
        )

        if has_tool_choice and has_tool_resources:
            if isinstance(self.tool_choice, str):
                return self.tool_choice == "auto" or self.tool_choice == "required"
            else:
                try:
                    if isinstance(self.tool_choice, AssistantToolChoice):
                        return self.tool_choice.type == "file_search"
                except ValidationError:
                    traceback.print_exc()
                    logger.error(
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
        self,
        session: Session,
        thread: Thread,
        additional_instructions: str | None,
        tool_resources: BetaThreadToolResources | None = None,
    ) -> tuple[list[ChatMessage], list[str]]:
        # Get existing messages
        thread_messages: list[Message] = await self.list_messages(thread.id, session)

        if len(thread_messages) == 0:
            return [], []

        def sort_by_created_at(msg: Message):
            return msg.created_at

        # The messages are not guaranteed to come out of the DB sorted, so they are sorted here
        thread_messages.sort(key=sort_by_created_at)

        chat_thread_messages = []

        for message in thread_messages:
            if isinstance(message.content[0], TextContentBlock):
                for annotation in message.content[0].text.annotations:
                    # The LLM may hallucinate if we leave the annotations in when we pass them into the LLM, so they are removed
                    message.content[0].text.value = message.content[
                        0
                    ].text.value.replace(annotation.text, "")
                chat_thread_messages.append(
                    ChatMessage(
                        role=message.role, content=message.content[0].text.value
                    )
                )

        # Holds the converted thread's messages, this will be built up with a series of push operations
        chat_messages: list[ChatMessage] = []

        # 1 - Model instructions (system message)
        if self.instructions:
            chat_messages.append(ChatMessage(role="system", content=self.instructions))

        # 2 - Additional model instructions (system message)
        if additional_instructions:
            chat_messages.append(
                ChatMessage(role="system", content=additional_instructions)
            )

        # 3 - Add the existing messages to chat_messages
        chat_messages.extend(chat_thread_messages)

        # 4 - The RAG results are appended behind the user's query
        if self.can_use_rag(tool_resources):
            rag_message: str = "Here are relevant docs needed to reply:\n"

            if chat_thread_messages:
                query_message: ChatMessage = chat_thread_messages[-1]

                query_service = QueryService(db=session)
                file_search: BetaThreadToolResourcesFileSearch = cast(
                    BetaThreadToolResourcesFileSearch, tool_resources.file_search
                )

                # Ensure vector_store_ids is not empty or None
                vector_store_ids: list[str] = (
                    cast(list[str], file_search.vector_store_ids)
                    if file_search.vector_store_ids
                    else []
                )

                file_ids: set[str] = set()
                for vector_store_id in vector_store_ids:
                    rag_results_raw: SingleAPIResponse[
                        SearchResponse
                    ] = await query_service.query_rag(
                        query=query_message.content,
                        vector_store_id=vector_store_id,
                    )
                    rag_responses: SearchResponse = SearchResponse(
                        data=rag_results_raw.data
                    )

                    # Insert RAG response messages
                    for count, rag_response in enumerate(rag_responses.data):
                        if rag_response.file_id:  # Check if file_id exists
                            file_ids.add(rag_response.file_id)
                        response_with_instructions: str = f"{rag_response.content}"
                        rag_message += f"{response_with_instructions}\n"

                # Insert RAG message before the last user message
                chat_messages.insert(
                    len(chat_messages) - 1,
                    ChatMessage(role="user", content=rag_message),
                )

            # Return chat messages and list of file_ids
            return chat_messages, list(file_ids)

        # If no RAG is used, return the basic chat messages and empty file_ids
        return chat_messages, []

    async def generate_message_for_thread(
        self,
        session: Session,
        thread: Thread,
        run_id: str,
        additional_instructions: str | None = None,
        tool_resources: BetaThreadToolResources | None = None,
    ):
        # If no tools resources are passed in, try the tools in the assistant
        if not tool_resources:
            crud_assistant = CRUDAssistant(session)
            assistant = await crud_assistant.get(
                filters=FilterAssistant(id=self.assistant_id)
            )

            if (
                assistant
                and assistant.tool_resources
                and isinstance(assistant.tool_resources, BetaAssistantToolResources)
            ):
                tool_resources = BetaThreadToolResources.model_validate(
                    assistant.tool_resources.model_dump()
                )
            else:
                tool_resources = None

        chat_messages, file_ids = await self.create_chat_messages(
            session, thread, additional_instructions, tool_resources
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

        message = from_text_to_message(choice.message.content, file_ids)

        create_message_request = CreateMessageRequest(
            role=message.role,
            content=message.content,
            attachments=message.attachments,
            metadata=message.metadata.__dict__ if message.metadata else None,
        )

        await create_message_request.create_message(
            session=session,
            thread_id=thread.id,
            run_id=run_id,
            assistant_id=self.assistant_id,
        )

    async def stream_generate_message_for_thread(
        self,
        session: Session,
        initial_messages: list[str],
        thread: Thread,
        ending_messages: list[str],
        run_id: str,
        additional_instructions: str | None = None,
        tool_resources: BetaThreadToolResources | None = None,
    ) -> AsyncGenerator[str, Any]:
        # If no tools resources are passed in, try the tools in the assistant
        if not tool_resources:
            crud_assistant = CRUDAssistant(session)
            assistant = await crud_assistant.get(
                filters=FilterAssistant(id=self.assistant_id)
            )

            if (
                assistant
                and assistant.tool_resources
                and isinstance(assistant.tool_resources, BetaAssistantToolResources)
            ):
                tool_resources = BetaThreadToolResources.model_validate(
                    assistant.tool_resources.model_dump()
                )
            else:
                tool_resources = None

        chat_messages, file_ids = await self.create_chat_messages(
            session, thread, additional_instructions, tool_resources
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
        new_message: Message = from_text_to_message("", [])

        create_message_request = CreateMessageRequest(
            role=new_message.role,
            content=new_message.content,
            attachments=new_message.attachments,
            metadata=new_message.metadata.__dict__ if new_message.metadata else None,
        )

        new_message = await create_message_request.create_message(
            session=session,
            thread_id=thread.id,
            run_id=run_id,
            assistant_id=self.assistant_id,
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

        new_message.content = from_text_to_message(response, file_ids).content
        new_message.created_at = int(time.time())

        crud_message = CRUDMessage(db=session)

        if not (
            updated_message := await crud_message.update(
                id_=new_message.id, object_=new_message
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update message during streaming",
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

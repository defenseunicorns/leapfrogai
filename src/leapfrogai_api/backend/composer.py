from __future__ import annotations
import time
import uuid
from typing import cast, AsyncGenerator, Any
from uuid import UUID

from fastapi import HTTPException, status
from openai.types.beta.assistant import ToolResources as BetaAssistantToolResources
from openai.types.beta.threads import Run
from openai.types.beta import (
    Thread,
)
from openai.types.beta.assistant_stream_event import (
    ThreadMessageCreated,
    ThreadMessageInProgress,
    ThreadMessageCompleted,
)
from openai.types.beta.thread import (
    ToolResources as BetaThreadToolResources,
    ToolResourcesFileSearch as BetaThreadToolResourcesFileSearch,
)
from openai.types.beta.threads import (
    Message,
    TextContentBlock,
)
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from leapfrogai_api.backend.converters import (
    from_assistant_stream_event_to_str,
    from_text_to_message,
    from_chat_completion_choice_to_thread_message_delta,
)
from leapfrogai_api.backend.rag.query import QueryService
from leapfrogai_api.data.crud_assistant import CRUDAssistant, FilterAssistant
from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.routers.openai.chat import chat_complete, chat_complete_stream_raw
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils import get_model_config
from leapfrogai_sdk.chat.chat_pb2 import (
    ChatCompletionResponse as ProtobufChatCompletionResponse,
)
from leapfrogai_api.typedef.chat import (
    ChatMessage,
    ChatCompletionResponse,
    ChatCompletionRequest,
    ChatChoice,
)
from leapfrogai_api.typedef.runs import RunCreateParamsRequest
from leapfrogai_api.typedef.messages import CreateMessageRequest
from leapfrogai_api.typedef.vectorstores import SearchResponse


class Composer(BaseModel):
    @staticmethod
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

    async def create_chat_messages(
        self,
        request: RunCreateParamsRequest,
        session: Session,
        thread: Thread,
        additional_instructions: str | None,
        tool_resources: BetaThreadToolResources | None = None,
    ) -> tuple[list[ChatMessage], SearchResponse]:
        """Create chat message list for consumption by the LLM backend.

        Args:
            request (RunCreateParamsRequest): The request object.
            session (Session): The database session.
            thread (Thread): The thread object.
            additional_instructions (str | None): Additional instructions.
            tool_resources (BetaThreadToolResources | None): The tool resources.

        Returns:
            tuple[list[ChatMessage], SearchResponse]: The chat messages and any RAG responses.
        """
        # Get existing messages
        thread_messages: list[Message] = await self.list_messages(thread.id, session)
        rag_responses: SearchResponse = SearchResponse(data=[])

        if len(thread_messages) == 0:
            return [], rag_responses

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
        if request.instructions:
            chat_messages.append(
                ChatMessage(role="system", content=request.instructions)
            )

        # 2 - Additional model instructions (system message)
        if additional_instructions:
            chat_messages.append(
                ChatMessage(role="system", content=additional_instructions)
            )

        # 3 - The existing messages with everything after the first message
        chat_messages.extend(chat_thread_messages)

        # 4 - The RAG results are appended behind the user's query
        if request.can_use_rag(tool_resources) and chat_thread_messages:
            rag_message: str = "Here are relevant docs needed to reply:\n"

            query_message: ChatMessage = chat_thread_messages[-1]

            query_service = QueryService(db=session)
            file_search: BetaThreadToolResourcesFileSearch = cast(
                BetaThreadToolResourcesFileSearch, tool_resources.file_search
            )
            vector_store_ids: list[str] = cast(list[str], file_search.vector_store_ids)

            for vector_store_id in vector_store_ids:
                rag_responses = await query_service.query_rag(
                    query=query_message.content_as_str(),
                    vector_store_id=vector_store_id,
                )

                # Insert the RAG response messages just before the user's query
                for rag_response in rag_responses.data:
                    response_with_instructions: str = f"{rag_response.content}"
                    rag_message += f"{response_with_instructions}\n"

            chat_messages.insert(
                len(chat_messages) - 1,  # Insert right before the user message
                ChatMessage(role="user", content=rag_message),
            )

        return chat_messages, rag_responses

    async def generate_message_for_thread(
        self,
        request: RunCreateParamsRequest,
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
                filters=FilterAssistant(id=request.assistant_id)
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

        chat_messages, rag_responses = await self.create_chat_messages(
            request, session, thread, additional_instructions, tool_resources
        )

        # Generate a new message and add it to the thread creation request
        chat_response: ChatCompletionResponse = await chat_complete(
            req=ChatCompletionRequest(
                model=str(request.model),
                messages=chat_messages,
                functions=None,
                temperature=request.temperature,
                top_p=request.top_p,
                stream=request.stream,
                stop=None,
                max_tokens=request.max_completion_tokens,
            ),
            model_config=get_model_config(),
            session=session,
        )

        choice: ChatChoice = cast(ChatChoice, chat_response.choices[0])

        message: Message = from_text_to_message(
            text=choice.message.content_as_str(), search_responses=rag_responses
        )

        create_message_request = CreateMessageRequest(
            role=message.role,
            content=message.content,
            attachments=message.attachments,
            metadata=message.metadata.__dict__ if message.metadata else {},
        )

        await create_message_request.create_message(
            session=session,
            thread_id=thread.id,
            run_id=run_id,
            assistant_id=request.assistant_id,
        )

    async def stream_generate_message_for_thread(
        self,
        request: RunCreateParamsRequest,
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
                filters=FilterAssistant(id=request.assistant_id)
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

        chat_messages, rag_responses = await self.create_chat_messages(
            request, session, thread, additional_instructions, tool_resources
        )

        chat_response: AsyncGenerator[ProtobufChatCompletionResponse, Any] = (
            chat_complete_stream_raw(
                req=ChatCompletionRequest(
                    model=str(request.model),
                    messages=chat_messages,
                    functions=None,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    stream=request.stream,
                    stop=None,
                    max_tokens=request.max_completion_tokens,
                ),
                model_config=get_model_config(),
            )
        )

        for message in initial_messages:
            yield message
            yield "\n\n"

        # Create an empty message
        new_message: Message = from_text_to_message(
            text="", search_responses=SearchResponse(data=[])
        )

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
            assistant_id=request.assistant_id,
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

        new_message.content = from_text_to_message(
            text=response, search_responses=rag_responses
        ).content
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

    async def generate_response(
        self,
        request: RunCreateParamsRequest,
        new_thread: Thread,
        new_run: Run,
        session: Session,
    ):
        """Generate a new response based on the existing thread"""
        if request.stream:
            initial_messages: list[str] = (
                RunCreateParamsRequest.get_initial_messages_base(run=new_run)
            )
            ending_messages: list[str] = (
                RunCreateParamsRequest.get_ending_messages_base(run=new_run)
            )
            stream: AsyncGenerator[str, Any] = self.stream_generate_message_for_thread(
                request=request,
                session=session,
                initial_messages=initial_messages,
                thread=new_thread,
                ending_messages=ending_messages,
                run_id=new_run.id,
                additional_instructions=request.additional_instructions,
            )

            return StreamingResponse(stream, media_type="text/event-stream")
        else:
            await self.generate_message_for_thread(
                request=request,
                session=session,
                thread=new_thread,
                run_id=new_run.id,
                additional_instructions=request.additional_instructions,
            )

            return new_run

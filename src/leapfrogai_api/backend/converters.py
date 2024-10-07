"""Converters for the LeapfrogAI API"""

from typing import Iterable
from openai.types.beta import AssistantStreamEvent
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.file_citation_annotation import FileCitation
from openai.types.beta.threads.file_path_annotation import FilePathAnnotation
from openai.types.beta.threads import (
    MessageContentPartParam,
    MessageContent,
    TextContentBlock,
    Text,
    Message,
    MessageDeltaEvent,
    MessageDelta,
    TextDeltaBlock,
    TextDelta,
    FileCitationAnnotation,
)

from leapfrogai_api.typedef.vectorstores.search_types import SearchResponse
from leapfrogai_api.typedef.common import MetadataObject


def from_assistant_stream_event_to_str(stream_event: AssistantStreamEvent):
    return f"event: {stream_event.event}\ndata: {stream_event.data.model_dump_json()}"


def from_content_param_to_content(
    thread_message_content: str | Iterable[MessageContentPartParam],
) -> MessageContent:
    """Converts messages from MessageContentPartParam to MessageContent"""
    if isinstance(thread_message_content, str):
        return TextContentBlock(
            text=Text(annotations=[], value=thread_message_content),
            type="text",
        )
    else:
        result: str = ""

        for message_content_part in thread_message_content:
            if isinstance(text := message_content_part.get("text"), str):
                result += text

        return TextContentBlock(
            text=Text(annotations=[], value=result),
            type="text",
        )


def from_text_to_message(text: str, search_responses: SearchResponse | None) -> Message:
    """Loads text and RAG search responses into a Message object

    Args:
        text: The text to load into the message
        search_responses: The RAG search responses to load into the message

    Returns:
        The OpenAI compliant Message object
    """

    all_citations = ""
    all_vector_ids: list[str] = []
    annotations: list[FileCitationAnnotation | FilePathAnnotation] = []

    if search_responses:
        for search_response in search_responses.data:
            all_vector_ids.append(search_response.id)
            file_name = search_response.metadata.get("source", "source")
            replacement_text = f"【4:0†{file_name}】"  # TODO: What should these numbers be? https://github.com/defenseunicorns/leapfrogai/issues/1110
            annotations.append(
                FileCitationAnnotation(
                    text=replacement_text,
                    file_citation=FileCitation(
                        file_id=search_response.file_id, quote=search_response.content
                    ),
                    start_index=0,
                    end_index=0,
                    type="file_citation",
                )
            )

            all_citations += replacement_text

    message_content: TextContentBlock = TextContentBlock(
        text=Text(
            annotations=annotations,
            value=text + all_citations,  # TODO: Replace with find/replace test
        ),
        type="text",
    )

    new_message = Message(
        id="",
        created_at=0,
        object="thread.message",
        status="in_progress",
        thread_id="",
        content=[message_content],
        role="assistant",
        metadata=MetadataObject(
            vector_ids=all_vector_ids.__str__(),
        ),
    )

    return new_message


async def from_chat_completion_choice_to_thread_message_delta(
    index, random_uuid, streaming_response
) -> ThreadMessageDelta:
    thread_message_event: ThreadMessageDelta = ThreadMessageDelta(
        data=MessageDeltaEvent(
            id=str(random_uuid),
            delta=MessageDelta(
                content=[
                    TextDeltaBlock(
                        index=index,
                        type="text",
                        text=TextDelta(
                            annotations=[],
                            value=streaming_response.choices[0].chat_item.content,
                        ),
                    )
                ],
                role="assistant",
            ),
            object="thread.message.delta",
        ),
        event="thread.message.delta",
    )
    return thread_message_event

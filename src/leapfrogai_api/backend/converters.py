import logging
import traceback
from typing import Iterable
from openai.types.beta import AssistantStreamEvent
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.file_citation_annotation import FileCitation
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
from pydantic_core import ValidationError

from leapfrogai_api.backend.validators import TextContentBlockParamValidator


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
            try:
                if TextContentBlockParamValidator.validate_python(message_content_part):
                    result += message_content_part.get("text")
            except ValidationError:
                traceback.print_exc()
                logging.error("Failed to validate message content part")
                continue

        return TextContentBlock(
            text=Text(annotations=[], value=result),
            type="text",
        )


def from_text_to_message(text: str, file_ids: list[str]) -> Message:
    message_content: TextContentBlock = TextContentBlock(
        text=Text(
            annotations=[
                FileCitationAnnotation(
                    file_citation=FileCitation(file_id=file_id, text=f"[{file_id}]")
                )
                for file_id in file_ids
            ],
            value=text,
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
        metadata={},
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

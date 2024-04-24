"""Helper functions for the OpenAI backend."""

from typing import BinaryIO, Iterator, Union

import grpc
from openai.types import CompletionUsage as Usage
import leapfrogai_sdk as lfai
from leapfrogai_api.routers.openai.types import (
    ChatCompletionResponse,
    ChatDelta,
    ChatStreamChoice,
)


async def recv_chat(
    stream: grpc.aio.UnaryStreamCall[
        lfai.ChatCompletionRequest, lfai.ChatCompletionResponse
    ],
):
    """Generator that yields chat completion responses as Server-Sent Events."""
    async for c in stream:
        yield (
            "data: "
            + ChatCompletionResponse(
                id="foo",
                object="chat.completion.chunk",
                created=55,
                model="mpt-7b-8k-chat",
                choices=[
                    ChatStreamChoice(
                        index=0,
                        delta=ChatDelta(
                            role="assistant", content=c.choices[0].chat_item.content
                        ),
                        finish_reason=None,
                    )
                ],
                usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            ).model_dump_json()
        )
        yield "\n\n"

    yield "data: [DONE]\n\n"


def grpc_chat_role(role: str) -> Union[lfai.ChatRole, None]:
    """Converts a string to a ChatRole."""
    match role:
        case "user":
            return lfai.ChatRole.USER  # type: ignore
        case "system":
            return lfai.ChatRole.SYSTEM  # type: ignore
        case "function":
            return lfai.ChatRole.FUNCTION  # type: ignore
        case "assistant":
            return lfai.ChatRole.ASSISTANT  # type: ignore
        case _:
            return None


# read_chunks is a helper method that chunks the bytes of a file (audio file) into a iterator of AudioRequests
def read_chunks(file: BinaryIO, chunk_size: int) -> Iterator[lfai.AudioRequest]:
    """Reads a file in chunks and yields AudioRequests."""
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield lfai.AudioRequest(chunk_data=chunk)

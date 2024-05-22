"""Helper functions for the OpenAI backend."""

from typing import BinaryIO, Iterator
import grpc
import leapfrogai_sdk as lfai
from leapfrogai_api.backend.types import (
    ChatCompletionResponse,
    ChatDelta,
    ChatStreamChoice,
    CompletionChoice,
    CompletionResponse,
    Usage,
)


async def recv_completion(
    stream: grpc.aio.UnaryStreamCall[lfai.CompletionRequest, lfai.CompletionResponse],
):
    async for c in stream:
        yield (
            "data: "
            + CompletionResponse(
                id="foo",
                object="completion.chunk",
                created=55,
                model="mpt-7b-8k-chat",
                choices=[
                    CompletionChoice(
                        index=0,
                        text=c.choices[0].text,
                        logprobs=None,
                        finish_reason=c.choices[0].finish_reason,
                    )
                ],
                usage=Usage(
                    prompt_tokens=c.usage.prompt_tokens,
                    completion_tokens=c.usage.completion_tokens,
                    total_tokens=c.usage.total_tokens,
                ),
            ).model_dump_json()
        )
        yield "\n\n"

    yield "data: [DONE]"


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
                        finish_reason=c.choices[0].finish_reason,
                    )
                ],
                usage=Usage(
                    prompt_tokens=c.usage.prompt_tokens,
                    completion_tokens=c.usage.completion_tokens,
                    total_tokens=c.usage.total_tokens,
                ),
            ).model_dump_json()
        )
        yield "\n\n"

    yield "data: [DONE]\n\n"


def grpc_chat_role(role: str) -> lfai.ChatRole:
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

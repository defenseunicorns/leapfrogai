"""Helper functions for the OpenAI backend."""

import time
import uuid
from typing import BinaryIO, AsyncGenerator, Any
import aiofiles
from typing import AsyncIterator
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
    model: str,
):
    async for c in stream:
        yield (
            "data: "
            + CompletionResponse(
                id=str(uuid.uuid4()),
                object="completion.chunk",
                created=int(time.time()),
                model=model,
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
    model: str,
) -> AsyncGenerator[str, Any]:
    """Generator that yields chat completion responses as Server-Sent Events."""
    async for c in stream:
        yield (
            "data: "
            + ChatCompletionResponse(
                id=str(uuid.uuid4()),
                object="chat.completion.chunk",
                created=int(time.time()),
                model=model,
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
async def read_chunks(
    file: BinaryIO, chunk_size: int
) -> AsyncIterator[lfai.AudioRequest]:
    async with aiofiles.open(file.fileno(), mode="rb") as async_file:
        while True:
            chunk = await async_file.read(chunk_size)
            if not chunk:
                break
            yield lfai.AudioRequest(chunk_data=chunk)


def object_or_default(obj: Any | None, _default: Any) -> Any:
    if obj:
        return obj
    else:
        return _default

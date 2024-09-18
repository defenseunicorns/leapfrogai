"""Helper functions for the OpenAI backend."""

import time
import uuid
import grpc
from typing import BinaryIO, Iterator, AsyncGenerator, Any
import leapfrogai_sdk as lfai
from leapfrogai_api.typedef.chat import (
    ChatCompletionResponse,
    ChatDelta,
    ChatStreamChoice,
)
from leapfrogai_api.typedef.completion import (
    CompletionChoice,
    CompletionResponse,
    FinishReason,
)
from leapfrogai_api.typedef import (
    Usage,
)


async def recv_completion(
    stream: grpc.aio.UnaryStreamCall[lfai.CompletionRequest, lfai.CompletionResponse],
    model: str,
):
    async for c in stream:
        finish_reason_enum = FinishReason(c.choices[0].finish_reason)

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
                        finish_reason=finish_reason_enum.to_string(),
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
        finish_reason_enum = FinishReason(c.choices[0].finish_reason)

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
                        finish_reason=finish_reason_enum.to_string(),
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


# helper function used to modify objects unless certain fields are missing
def object_or_default(obj: Any | None, _default: Any) -> Any:
    """Returns the given object unless it is a None type, otherwise a given default is returned"""
    if obj is not None:
        return obj
    else:
        return _default

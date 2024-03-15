from typing import BinaryIO, Iterator, Union

import grpc
import leapfrogai_api.types as lfai_types
from leapfrogai_api.backends.openai.types import (
    ChatCompletionResponse,
    ChatDelta,
    ChatStreamChoice,
    CompletionChoice,
    CompletionResponse,
    Usage,
)


async def recv_completion(
    stream: grpc.aio.UnaryStreamCall[
        lfai_types.CompletionRequest, lfai_types.CompletionResponse
    ],
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
                        finish_reason="stop",
                    )
                ],
                usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            ).model_dump_json()
        )
        yield "\n\n"

    yield "data: [DONE]"


async def recv_chat(
    stream: grpc.aio.UnaryStreamCall[
        lfai_types.ChatCompletionRequest, lfai_types.ChatCompletionResponse
    ],
):
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


def grpc_chat_role(role: str) -> Union[lfai_types.ChatRole, None]:
    match role:
        case "user":
            return lfai_types.ChatRole.USER  # type: ignore
        case "system":
            return lfai_types.ChatRole.SYSTEM  # type: ignore
        case "function":
            return lfai_types.ChatRole.FUNCTION  # type: ignore
        case "assistant":
            return lfai_types.ChatRole.ASSISTANT  # type: ignore
        case _:
            return None


# read_chunks is a helper method that chunks the bytes of a file (audio file) into a iterator of AudioRequests
def read_chunks(file: BinaryIO, chunk_size: int) -> Iterator[lfai_types.AudioRequest]:
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield lfai_types.AudioRequest(chunk_data=chunk)

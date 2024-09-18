"""gRPC client for OpenAI models."""

from typing import Iterator, AsyncGenerator, Any, List
import grpc
from fastapi.responses import StreamingResponse

import leapfrogai_sdk as lfai
from leapfrogai_api.backend.helpers import recv_chat, recv_completion
from leapfrogai_api.backend.types import (
    ChatChoice,
    ChatCompletionResponse,
    ChatMessage,
    CompletionChoice,
    CompletionResponse,
    CreateEmbeddingResponse,
    CreateTranscriptionResponse,
    EmbeddingResponseData,
    FinishReason,
    Usage,
    CreateTranslationResponse,
)
from leapfrogai_sdk.chat.chat_pb2 import (
    ChatCompletionResponse as ProtobufChatCompletionResponse,
)
from leapfrogai_api.utils.config import Model


async def stream_completion(model: Model, request: lfai.CompletionRequest):
    """Stream completion using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.CompletionStreamServiceStub(channel)
        stream = stub.CompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(
            recv_completion(stream, model.name), media_type="text/event-stream"
        )


# TODO: Clean up completion() and stream_completion() to reduce code duplication
async def completion(model: Model, request: lfai.CompletionRequest):
    """Complete using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.CompletionServiceStub(channel)
        response: lfai.CompletionResponse = await stub.Complete(request)
        finish_reason_enum = FinishReason(response.choices[0].finish_reason)

        return CompletionResponse(
            model=model.name,
            choices=[
                CompletionChoice(
                    index=0,
                    text=response.choices[0].text,
                    finish_reason=finish_reason_enum.to_string(),
                    logprobs=None,
                )
            ],
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
        )


async def stream_chat_completion(model: Model, request: lfai.ChatCompletionRequest):
    """Stream chat completion using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.ChatCompletionStreamServiceStub(channel)
        stream = stub.ChatCompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(
            recv_chat(stream, model.name), media_type="text/event-stream"
        )


async def stream_chat_completion_raw(
    model: Model, request: lfai.ChatCompletionRequest
) -> AsyncGenerator[ProtobufChatCompletionResponse, Any]:
    """Stream chat completion using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.ChatCompletionStreamServiceStub(channel)
        stream: grpc.aio.UnaryStreamCall[
            lfai.ChatCompletionRequest, lfai.ChatCompletionResponse
        ] = stub.ChatCompleteStream(request)

        await stream.wait_for_connection()

        async for response in stream:
            yield response


# TODO: Clean up completion() and stream_completion() to reduce code duplication
async def chat_completion(model: Model, request: lfai.ChatCompletionRequest):
    """Complete chat using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.ChatCompletionServiceStub(channel)
        response: lfai.ChatCompletionResponse = await stub.ChatComplete(request)
        finish_reason_enum = FinishReason(response.choices[0].finish_reason)

        return ChatCompletionResponse(
            model=model.name,
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(
                        role=lfai.ChatRole.Name(
                            response.choices[0].chat_item.role
                        ).lower(),
                        content=response.choices[0].chat_item.content,
                    ),
                    finish_reason=finish_reason_enum.to_string(),
                )
            ],
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
        )


async def create_embeddings(model: Model, request: lfai.EmbeddingRequest):
    """Create embeddings using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.EmbeddingsServiceStub(channel)
        embeddings: List[EmbeddingResponseData] = []

        # Loop through inputs - 500 at a time
        for i in range(0, len(request.inputs), 500):
            request_embeddings = request.inputs[i : i + 500]

            range_request = lfai.EmbeddingRequest(inputs=request_embeddings)
            e: lfai.EmbeddingResponse = await stub.CreateEmbedding(range_request)
            if e and e.embeddings is not None:
                data = [
                    EmbeddingResponseData(
                        embedding=list(e.embeddings[i].embedding), index=i
                    )
                    for i in range(len(e.embeddings))
                ]
                embeddings.extend(data)

        return CreateEmbeddingResponse(
            data=embeddings,
            model=model.name,
            usage=Usage(prompt_tokens=0, total_tokens=0),
        )


async def create_transcription(model: Model, request: Iterator[lfai.AudioRequest]):
    """Transcribe audio using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.AudioStub(channel)
        response: lfai.AudioResponse = await stub.Transcribe(request)

        return CreateTranscriptionResponse(text=response.text)


async def create_translation(model: Model, request: Iterator[lfai.AudioRequest]):
    """Translate audio using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.AudioStub(channel)
        response: lfai.AudioResponse = await stub.Translate(request)

        return CreateTranslationResponse(text=response.text)

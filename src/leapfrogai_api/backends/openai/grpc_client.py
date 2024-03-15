from typing import Iterator

import grpc
import leapfrogai_api.types as lfai_types
from fastapi.responses import StreamingResponse
from leapfrogai_api.backends.openai.helpers import recv_chat, recv_completion
from leapfrogai_api.backends.openai.types import (
    ChatChoice,
    ChatCompletionResponse,
    ChatMessage,
    CompletionChoice,
    CompletionResponse,
    CreateEmbeddingResponse,
    CreateTranscriptionResponse,
    EmbeddingResponseData,
    Usage,
)
from leapfrogai_api.utils.config import Model


async def stream_completion(model: Model, request: lfai_types.CompletionRequest):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai_types.CompletionStreamServiceStub(channel)
        stream = stub.CompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(
            recv_completion(stream), media_type="text/event-stream"
        )


# TODO: Clean up completion() and stream_completion() to reduce code duplication
async def completion(model: Model, request: lfai_types.CompletionRequest):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai_types.CompletionServiceStub(channel)
        response: lfai_types.CompletionResponse = await stub.Complete(request)

        return CompletionResponse(
            model=model.name,
            choices=[
                CompletionChoice(
                    index=0,
                    text=response.choices[0].text,
                    finish_reason=str(response.choices[0].finish_reason),
                    logprobs=None,
                )
            ],
            usage=Usage(total_tokens=0, prompt_tokens=0),
        )


async def stream_chat_completion(
    model: Model, request: lfai_types.ChatCompletionRequest
):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai_types.ChatCompletionStreamServiceStub(channel)
        stream = stub.ChatCompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(recv_chat(stream), media_type="text/event-stream")


# TODO: Clean up completion() and stream_completion() to reduce code duplication
async def chat_completion(model: Model, request: lfai_types.ChatCompletionRequest):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai_types.ChatCompletionServiceStub(channel)
        response: lfai_types.ChatCompletionResponse = await stub.ChatComplete(request)
        return ChatCompletionResponse(
            model=model.name,
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(
                        role=lfai_types.ChatRole.Name(
                            response.choices[0].chat_item.role
                        ).lower(),
                        content=response.choices[0].chat_item.content,
                    ),
                    finish_reason="",
                )
            ],
            usage=Usage(total_tokens=0, prompt_tokens=0),
        )


async def create_embeddings(model: Model, request: lfai_types.EmbeddingRequest):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai_types.EmbeddingsServiceStub(channel)
        e: lfai_types.EmbeddingResponse = await stub.CreateEmbedding(request)
        return CreateEmbeddingResponse(
            data=[
                EmbeddingResponseData(
                    embedding=list(e.embeddings[i].embedding), index=i
                )
                for i in range(len(e.embeddings))
            ],
            model=model.name,
            usage=Usage(prompt_tokens=0, total_tokens=0),
        )


async def create_transcription(
    model: Model, request: Iterator[lfai_types.AudioRequest]
):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai_types.AudioStub(channel)
        response: lfai_types.AudioResponse = await stub.Transcribe(request)

        return CreateTranscriptionResponse(text=response.text)

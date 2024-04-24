from typing import Iterator

import grpc
from fastapi.responses import StreamingResponse
from openai.types import CompletionUsage as Usage

import leapfrogai_sdk as lfai
from leapfrogai_api.routers.openai.helpers import recv_chat
from leapfrogai_api.routers.openai.types import (
    ChatChoice,
    ChatMessage,
    ChatCompletionResponse,
    EmbeddingResponseData,
    CreateEmbeddingResponse,
    CreateTranscriptionResponse,
)
from leapfrogai_api.utils.config import Model


async def stream_chat_completion(model: Model, request: lfai.ChatCompletionRequest):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.ChatCompletionStreamServiceStub(channel)
        stream = stub.ChatCompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(recv_chat(stream), media_type="text/event-stream")


# TODO: Clean up completion() and stream_completion() to reduce code duplication
async def chat_completion(model: Model, request: lfai.ChatCompletionRequest):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.ChatCompletionServiceStub(channel)
        response: lfai.ChatCompletionResponse = await stub.ChatComplete(request)
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
                    finish_reason="",
                )
            ],
            usage=Usage(total_tokens=0, prompt_tokens=0),
        )


async def create_embeddings(model: Model, request: lfai.EmbeddingRequest):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.EmbeddingsServiceStub(channel)
        e: lfai.EmbeddingResponse = await stub.CreateEmbedding(request)
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


async def create_transcription(model: Model, request: Iterator[lfai.AudioRequest]):
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = lfai.AudioStub(channel)
        response: lfai.AudioResponse = await stub.Transcribe(request)

        return CreateTranscriptionResponse(text=response.text)

import logging

import leapfrogai_sdk
import asyncio

from leapfrogai_sdk import CompletionUsage
from leapfrogai_sdk.chat.chat_pb2 import Usage


class Repeater(
    leapfrogai_sdk.CompletionServiceServicer,
    leapfrogai_sdk.EmbeddingsServiceServicer,
    leapfrogai_sdk.ChatCompletionServiceServicer,
    leapfrogai_sdk.ChatCompletionStreamServiceServicer,
    leapfrogai_sdk.AudioServicer,
):
    async def Complete(
        self,
        request: leapfrogai_sdk.CompletionRequest,
        context: leapfrogai_sdk.GrpcContext,
    ) -> leapfrogai_sdk.CompletionResponse:
        result = request.prompt  # just returns what's provided
        print(f"Repeater.Complete:  { request }")
        completion = leapfrogai_sdk.CompletionChoice(
            text=result, index=0, finish_reason="stop"
        )
        return leapfrogai_sdk.CompletionResponse(
            choices=[completion],
            usage=CompletionUsage(prompt_tokens=1, completion_tokens=2, total_tokens=3),
        )

    async def CompleteStream(
        self,
        request: leapfrogai_sdk.CompletionRequest,
        context: leapfrogai_sdk.GrpcContext,
    ) -> leapfrogai_sdk.CompletionResponse:
        for _ in range(5):
            completion = leapfrogai_sdk.CompletionChoice(
                text=request.prompt, index=0, finish_reason="stop"
            )
            yield leapfrogai_sdk.CompletionResponse(
                choices=[completion],
                usage=CompletionUsage(
                    prompt_tokens=1, completion_tokens=2, total_tokens=3
                ),
            )

    async def CreateEmbedding(
        self,
        request: leapfrogai_sdk.EmbeddingRequest,
        context: leapfrogai_sdk.GrpcContext,
    ) -> leapfrogai_sdk.EmbeddingResponse:
        return leapfrogai_sdk.EmbeddingResponse(
            embeddings=[leapfrogai_sdk.Embedding(embedding=[0.0 for _ in range(10)])]
        )

    async def ChatComplete(
        self,
        request: leapfrogai_sdk.ChatCompletionRequest,
        context: leapfrogai_sdk.GrpcContext,
    ) -> leapfrogai_sdk.ChatCompletionResponse:
        completion = leapfrogai_sdk.ChatCompletionChoice(
            chat_item=request.chat_items[0], finish_reason="stop"
        )
        return leapfrogai_sdk.ChatCompletionResponse(
            choices=[completion],
            usage=Usage(prompt_tokens=1, completion_tokens=2, total_tokens=3),
        )

    async def ChatCompleteStream(
        self,
        request: leapfrogai_sdk.ChatCompletionRequest,
        context: leapfrogai_sdk.GrpcContext,
    ) -> leapfrogai_sdk.ChatCompletionResponse:
        for _ in range(5):
            completion = leapfrogai_sdk.ChatCompletionChoice(
                chat_item=request.chat_items[0], finish_reason="stop"
            )
            yield leapfrogai_sdk.ChatCompletionResponse(
                choices=[completion],
                usage=Usage(prompt_tokens=1, completion_tokens=2, total_tokens=3),
            )

    async def Transcribe(
        self, request: leapfrogai_sdk.AudioRequest, context: leapfrogai_sdk.GrpcContext
    ) -> leapfrogai_sdk.AudioResponse:
        return leapfrogai_sdk.AudioResponse(
            text="The repeater model received a transcribe request",
            duration=1,
            language="en",
        )

    async def Name(self, request, context):
        return leapfrogai_sdk.NameResponse(name="repeater")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(leapfrogai_sdk.serve(Repeater()))

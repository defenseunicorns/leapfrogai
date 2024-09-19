import logging
import os
from typing import Any, AsyncGenerator

from leapfrogai_sdk import (
    CompletionServiceServicer,
    EmbeddingsServiceServicer,
    ChatCompletionServiceServicer,
    ChatCompletionStreamServiceServicer,
    AudioServicer,
    TokenCountServiceServicer,
    GrpcContext,
    EmbeddingRequest,
    EmbeddingResponse,
    Embedding,
    AudioRequest,
    AudioResponse,
    NameResponse,
    serve,
)
from leapfrogai_sdk.llm import LLM, GenerationConfig

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)


@LLM
class Model(
    CompletionServiceServicer,
    EmbeddingsServiceServicer,
    ChatCompletionServiceServicer,
    ChatCompletionStreamServiceServicer,
    AudioServicer,
    TokenCountServiceServicer,
):
    async def generate(
        self, prompt: str, config: GenerationConfig
    ) -> AsyncGenerator[str, Any]:
        logger.info("Begin generating streamed response")
        for char in prompt:
            yield char  # type: ignore
        logger.info("Streamed response complete")

    async def count_tokens(self, raw_text: str) -> int:
        return len(raw_text)

    async def CreateEmbedding(
        self,
        request: EmbeddingRequest,
        context: GrpcContext,
    ) -> EmbeddingResponse:
        return EmbeddingResponse(
            embeddings=[Embedding(embedding=[0.0 for _ in range(10)])]
        )

    async def Transcribe(
        self, request: AudioRequest, context: GrpcContext
    ) -> AudioResponse:
        return AudioResponse(
            text="The repeater model received a transcribe request",
            duration=1,
            language="en",
        )

    async def Name(self, request, context):
        return NameResponse(name="repeater")


if __name__ == "__main__":
    serve(Model())

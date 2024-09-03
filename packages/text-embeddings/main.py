import asyncio
import logging
import os

from InstructorEmbedding import INSTRUCTOR
from leapfrogai_sdk import (
    Embedding,
    EmbeddingRequest,
    EmbeddingResponse,
    GrpcContext,
    serve,
)

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)


model_dir = os.environ.get("LFAI_MODEL_PATH", ".model")
model = INSTRUCTOR(model_dir)


class InstructorEmbedding:
    async def CreateEmbedding(self, request: EmbeddingRequest, context: GrpcContext):
        logger.info(
            f"processing CreateEmbedding request: char-length: {len(str(request.inputs))} word-count: {len(str(request.inputs).split())}"
        )

        embeddings = model.encode(request.inputs, show_progress_bar=True)

        embeddings = [Embedding(embedding=inner_list) for inner_list in embeddings]

        logger.info(
            f"finished processing CreateEmbedding request, created {len(embeddings)} embeddings"
        )
        return EmbeddingResponse(embeddings=embeddings)


if __name__ == "__main__":
    asyncio.run(serve(InstructorEmbedding()))

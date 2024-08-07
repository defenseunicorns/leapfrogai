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

model_dir = os.environ.get("LFAI_MODEL_PATH", ".model")
model = INSTRUCTOR(model_dir)


class InstructorEmbedding:
    async def CreateEmbedding(self, request: EmbeddingRequest, context: GrpcContext):
        embeddings = model.encode(request.inputs)

        embeddings = [Embedding(embedding=inner_list) for inner_list in embeddings]
        return EmbeddingResponse(embeddings=embeddings)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve(InstructorEmbedding()))

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

GPU_ENABLED = (
    False if os.environ.get("GPU_ENABLED", "False").lower() != "true" else True
)

model_dir = os.environ.get("LFAI_MODEL_PATH", ".model")
model = INSTRUCTOR(model_dir, device="cuda" if GPU_ENABLED else "cpu")


class InstructorEmbedding:
    async def CreateEmbedding(self, request: EmbeddingRequest, context: GrpcContext):
        # Run the CPU-intensive encoding in a separate thread
        embeddings = await asyncio.to_thread(
            model.encode, sentences=request.inputs, show_progress_bar=True
        )

        embeddings = [Embedding(embedding=inner_list) for inner_list in embeddings]
        return EmbeddingResponse(embeddings=embeddings)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve(InstructorEmbedding()))

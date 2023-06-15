import logging

from get_models import MODEL_ID
from sentence_transformers import SentenceTransformer

from leapfrog import (EmbeddingRequest, EmbeddingResponse,
                      EmbeddingsServiceServicer, GrpcContext, serve)


class AllMiniLML6V2(EmbeddingsServiceServicer):
    model = SentenceTransformer(MODEL_ID)

    def CreateEmbedding(self, request: EmbeddingRequest, context: GrpcContext):
        embeddings = self.model.encode(request.inputs)
        return EmbeddingResponse(embeddings=embeddings.tolist()[0])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(AllMiniLML6V2())

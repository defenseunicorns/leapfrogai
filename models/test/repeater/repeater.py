import leapfrog
import logging

class Repeater(leapfrog.CompletionServiceServicer):
    def Complete(self, request: leapfrog.CompletionRequest, context: leapfrog.GrpcContext) -> leapfrog.CompletionResponse:
        result = request.prompt+request.prompt # just returns what's provided
        print(f"Repeater.Complete:  { request }")
        return leapfrog.CompletionResponse(completion=[result for _ in range(request.n)])

    def CreateEmbedding(self, request, context):
        return leapfrog.EmbeddingResponse(
            embeddings=[leapfrog.Embedding(embedding=[ 0.0 for _ in range(10)])]
        )

    def Name(self, request, context):
        return leapfrog.NameResponse ( name = "repeater" )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    leapfrog.serve(Repeater())
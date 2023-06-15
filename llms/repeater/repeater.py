import leapfrog
import logging

class Repeater(leapfrog.CompletionServiceServicer):
    def Complete(self, request, context):

        result = request.prompt # just returns what's provided
        print(f"Repeater.Complete:  { request }")
        return leapfrog.CompletionResponse(completion=result)

    def CreateEmbedding(self, request, context):
        return leapfrog.EmbeddingResponse(
            embeddings=["a;fdlkajd;fakjdf;lakdjf"]
        )

    def Name(self, request, context):
        return leapfrog.NameResponse ( name = "repeater" )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    leapfrog.serve(Repeater())
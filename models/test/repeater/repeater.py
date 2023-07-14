import logging

import leapfrogai


class Repeater(leapfrogai.CompletionServiceServicer):
    def Complete(
        self, request: leapfrogai.CompletionRequest, context: leapfrogai.GrpcContext
    ) -> leapfrogai.CompletionResponse:
        result = request.prompt  # just returns what's provided
        print(f"Repeater.Complete:  { request }")
        completion = leapfrogai.CompletionChoice(text=result, index=0)
        return leapfrogai.CompletionResponse(choices=[completion])

    def CreateEmbedding(self, request, context):
        return leapfrogai.EmbeddingResponse(
            embeddings=[leapfrogai.Embedding(embedding=[0.0 for _ in range(10)])]
        )

    def Name(self, request, context):
        return leapfrogai.NameResponse(name="repeater")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    leapfrogai.serve(Repeater())

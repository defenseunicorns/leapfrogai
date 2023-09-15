import logging

import leapfrogai
import asyncio


class Repeater(leapfrogai.CompletionServiceServicer):
    async def Complete(
        self, request: leapfrogai.CompletionRequest, context: leapfrogai.GrpcContext
    ) -> leapfrogai.CompletionResponse:
        result = request.prompt  # just returns what's provided
        print(f"Repeater.Complete:  { request }")
        completion = leapfrogai.CompletionChoice(text=result, index=0)
        return leapfrogai.CompletionResponse(choices=[completion])

    async def CreateEmbedding(self, request, context):
        return leapfrogai.EmbeddingResponse(
            embeddings=[leapfrogai.Embedding(embedding=[0.0 for _ in range(10)])]
        )

    async def Name(self, request, context):
        return leapfrogai.NameResponse(name="repeater")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(leapfrogai.serve(Repeater()))

import logging

import leapfrogai
import asyncio


class Repeater(leapfrogai.CompletionServiceServicer,
               leapfrogai.EmbeddingsServiceServicer,
               leapfrogai.ChatCompletionServiceServicer,
               leapfrogai.ChatCompletionStreamServiceServicer,
               leapfrogai.AudioServicer):


    async def Complete(self,
                       request: leapfrogai.CompletionRequest,
                       context: leapfrogai.GrpcContext
                       ) -> leapfrogai.CompletionResponse:
        result = request.prompt  # just returns what's provided
        print(f"Repeater.Complete:  { request }")
        completion = leapfrogai.CompletionChoice(text=result, index=0)
        return leapfrogai.CompletionResponse(choices=[completion])


    async def CompleteStream(self,
                             request: leapfrogai.CompletionRequest,
                             context: leapfrogai.GrpcContext
                             ) -> leapfrogai.CompletionResponse:
        for _ in range(5):
            completion = leapfrogai.CompletionChoice(text=request.prompt, index=0)
            yield leapfrogai.CompletionResponse(choices=[completion])


    async def CreateEmbedding(self,
                              request: leapfrogai.EmbeddingRequest,
                              context: leapfrogai.GrpcContext
                              ) -> leapfrogai.EmbeddingResponse:
        return leapfrogai.EmbeddingResponse(
            embeddings=[leapfrogai.Embedding(embedding=[0.0 for _ in range(10)])]
        )


    async def ChatComplete(self,
                           request: leapfrogai.ChatCompletionRequest,
                           context: leapfrogai.GrpcContext
                           ) -> leapfrogai.ChatCompletionResponse:
        completion = leapfrogai.ChatCompletionChoice(chat_item=request.chat_items[0])
        return leapfrogai.ChatCompletionResponse(choices=[completion])


    async def ChatCompleteStream(self,
                                 request: leapfrogai.ChatCompletionRequest,
                                 context: leapfrogai.GrpcContext
                                 ) -> leapfrogai.ChatCompletionResponse:
        for _ in range(5):
            completion = leapfrogai.ChatCompletionChoice(chat_item=request.chat_items[0])
            yield leapfrogai.ChatCompletionResponse(choices=[completion])


    async def Transcribe(self,
                         request: leapfrogai.AudioRequest,
                         context: leapfrogai.GrpcContext
                         ) -> leapfrogai.AudioResponse:
        return leapfrogai.AudioResponse(
            text="The repeater model received a transcribe request",
            duration=1,
            language="en"
        )


    async def Name(self, request, context):
        return leapfrogai.NameResponse(name="repeater")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(leapfrogai.serve(Repeater()))

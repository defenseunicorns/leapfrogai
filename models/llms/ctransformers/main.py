import asyncio
import logging
from typing import Any, Generator

from ctransformers import AutoModelForCausalLM

from leapfrogai import (
    CompletionChoice,
    CompletionRequest,
    CompletionResponse,
    GrpcContext,
    serve,
)


class CTransformers:
    llm = AutoModelForCausalLM.from_pretrained(
        "Sidharthkr/MPT-7b-chat-GGML", model_type="mpt"
    )

    def Complete(
        self, request: CompletionRequest, context: GrpcContext
    ) -> CompletionResponse:
        text = self.llm(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            stop=["<|im_end|>"],
        )
        completion = CompletionChoice(text=text, index=0)
        print("COMPLETE:\n---")
        print(request.prompt)
        print(completion)
        print("COMPLETE END")
        return CompletionResponse(choices=[completion])

    def CompleteStream(
        self, request: CompletionRequest, context: GrpcContext
    ) -> Generator[CompletionResponse, Any, Any]:
        print("COMPLETESTREAM:\n---")
        print(request.prompt, end="", flush=True)
        for text in self.llm(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            stream=True,
            stop=["<|im_end|>"],
        ):
            print(text)
            completion = CompletionChoice(text=text, index=0)
            yield CompletionResponse(choices=[completion])
        print("COMPLETESTREAM END")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve(CTransformers()))

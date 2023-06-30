import logging
import time
from typing import Any, Generator

from ctransformers import AutoModelForCausalLM

from leapfrogai import (
    CompletionRequest,
    CompletionChoice,
    CompletionUsage,
    CompletionFinishReason,
    CompletionResponse,
    GrpcContext,
    serve
)


class CTransformers:
    llm = AutoModelForCausalLM.from_pretrained("Sidharthkr/MPT-7b-chat-GGML", model_type="mpt")

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
        return CompletionResponse(choices=[completion])

    def CompleteStream(
        self, request: CompletionRequest, context: GrpcContext
    ) -> Generator[CompletionResponse, Any, Any]:
        for text in self.llm(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            stream=True,
            stop=["<|im_end|>"],
        ):
            completion = CompletionChoice(text=text, index=0)
            yield CompletionResponse(choices=[completion])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(CTransformers())

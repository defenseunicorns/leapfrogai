import logging
import time
from typing import Any, Generator

from ctransformers import AutoModelForCausalLM

from leapfrogai import CompletionRequest, CompletionResponse, GrpcContext, serve


class CTransformers:
    llm = AutoModelForCausalLM.from_pretrained("TheBloke/mpt-30B-chat-GGML")

    def CompleteStream(
        self, request: CompletionRequest, context: GrpcContext
    ) -> Generator[CompletionResponse, Any, Any]:
        for text in self.llm(
            request.prompt,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=True,
            stop=["<|im_end|>"],
        ):
            yield CompletionResponse(completion=text)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(CTransformers())

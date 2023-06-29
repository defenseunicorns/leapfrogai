import logging
import time

from leapfrogai import CompletionRequest, CompletionResponse, GrpcContext, serve

from ctransformers import AutoModelForCausalLM


class CTransformers:
    # llm = AutoModelForCausalLM.from_pretrained("TheBloke/mpt-30B-chat-GGML")
    # llm = AutoModelForCausalLM.from_pretrained("TheBloke/MPT-30B-Instruct-GGML")
    llm = AutoModelForCausalLM.from_pretrained(
        "Sidharthkr/MPT-7b-chat-GGML", model_type="mpt"
    )

    def CompleteStream(self, request: CompletionRequest, context: GrpcContext):
        start_time = time.time()
        printed_time = False
        for text in self.llm(
            request.prompt,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=True,
            stop=["<|im_end|>"],
            batch_size=24,
            threads=8,
        ):
            if printed_time is False:
                response_time = time.time() - start_time
                print(f"Took {response_time} seconds to start generating tokens")
                printed_time = True
            print(text)
            yield CompletionResponse(completion=text)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(CTransformers())

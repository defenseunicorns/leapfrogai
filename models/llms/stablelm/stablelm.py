import logging
from threading import Thread
from typing import List

import torch
from get_models import MODEL_ID, TOKENIZER_ID
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)

from leapfrogai import (
    CompletionChoice,
    CompletionRequest,
    CompletionResponse,
    CompletionServiceServicer,
    CompletionStreamServiceServicer,
    GrpcContext,
    serve,
)


class StopOnTokens(StoppingCriteria):
    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        stop_ids = [50278, 50279, 50277, 1, 0]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

class StableLM(CompletionServiceServicer, CompletionStreamServiceServicer):
    def __init__(self):
        torch.cuda.init()
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_ID)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
        self.model.half().cuda()
        print("StableLM Loaded...")
    
    def Complete(
        self, request: CompletionRequest, context: GrpcContext
    ) -> CompletionResponse:
        logging.debug(f"Request: { request }")
        inputs = self.tokenizer(request.prompt, return_tensors="pt").to(self.device)

        # error checking for valid params
        tokens = self.model.generate(
            **inputs,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
        )
        logging.debug(f"Response {tokens}")

        # Extract out only the completion tokens
        completion_tokens = tokens[0][inputs["input_ids"].size(1) :]
        completion = self.tokenizer.decode(completion_tokens, skip_special_tokens=True)
        c = CompletionChoice(text=completion, index=0)
        logging.debug(f"Decoded Response: {completion}")

        return CompletionResponse(choices=[c])


    def CompleteStream(self, request: CompletionRequest, context: GrpcContext):
        logging.debug(f"Request:  { request }")
        inputs = self.tokenizer(request.prompt, return_tensors="pt").to(self.device)

        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)

        generation_kwargs = dict(
            inputs,
            streamer=streamer,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
        )

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        for text in streamer:
            completion = CompletionChoice(text=text, index=0)
            yield CompletionResponse(choices=[completion])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    serve(StableLM())

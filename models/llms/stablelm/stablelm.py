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
    CompletionRequest,
    CompletionResponse,
    CompletionServiceServicer,
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


class StableLM(CompletionServiceServicer):
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    model = model.to(device)
    logging.info("StableLM Loaded...")

    def Complete(
        self, request: CompletionRequest, context: GrpcContext
    ) -> CompletionResponse:
        inputs = self.tokenizer(request.prompt, return_tensors="pt").to(self.device)
        logging.debug(f"Request:  { request }")
        # error checking for valid params
        tokens = self.model.generate(
            **inputs,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            # repetition_penalty=request.frequence_penalty,
            top_p=request.top_p,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
        )
        logging.debug(f"Response {tokens}")
        # Extract out only the completion tokens
        completion_tokens = tokens[0][inputs["input_ids"].size(1) :]
        completion = self.tokenizer.decode(completion_tokens, skip_special_tokens=True)

        # response = self.tokenizer.decode(tokens[0], skip_special_tokens=False)
        logging.debug(f"Decoded Response: {completion}")
        return CompletionResponse(completion=completion)

    def CompleteStream(self, request: CompletionRequest, context: GrpcContext):
        inputs = self.tokenizer(request.prompt, return_tensors="pt").to(self.device)
        logging.debug(f"Request:  { request }")

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
            print(text)
            yield text
        # logging.debug(f"Response {tokens}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(StableLM())

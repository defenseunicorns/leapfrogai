import logging

from typing import List
from threading import Thread

import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)

from get_models import MODEL_ID
from leapfrogai import (
    ChatCompletionRequest,
    ChatRole,
    ChatItem,
    CompletionChoice,
    ChatCompletionResponse,
    ChatCompletionServiceServicer,
    GrpcContext,
    serve,
)

class StopOnTokens(StoppingCriteria):
    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        # <|im_end|>, <|endoftext|>
        stop_ids = [50278, 0]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


class MPTChat(ChatCompletionServiceServicer):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    model = model.to(device)
    logging.info("MPT Loaded...")

    def ChatComplete(
        self, request: ChatCompletionRequest, context: GrpcContext
    ) -> ChatCompletionResponse:
        inputs = self.tokenizer(request.prompt, return_tensors="pt").to(self.device)
        logging.debug(f"Request:  { request }")
        # error checking for valid params
        tokens = self.model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
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

        # TODO: extend the completion to the multi-response (n>1) case
        # response = self.tokenizer.decode(tokens[0], skip_special_tokens=False)
        logging.debug(f"Decoded Response: {completion}")
        role = ChatRole.ASSISTANT
        item = ChatItem(role=role, content=completion)
        choice = CompletionChoice(index=0, chat_item=item)
        return ChatCompletionResponse(choices=[choice])

    def ChatCompleteStream(self, request: ChatCompletionRequest, context: GrpcContext):
        inputs = self.tokenizer(request.prompt, return_tensors="pt").to(self.device)
        logging.debug(f"Request:  { request }")

        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
        generation_kwargs = dict(
            inputs,
            streamer=streamer,
            max_new_tokens=request.max_tokens,
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
    serve(MPTChat())

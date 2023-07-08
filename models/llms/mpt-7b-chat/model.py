import logging

from typing import List
from threading import Thread

import torch

from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)
import transformers.utils.logging

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

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
transformers.utils.logging.disable_progress_bar()
transformers.utils.logging.set_verbosity_debug()

MODEL_SAVE_PATH = "mpt-7b-chat-offline"

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
    # create a config, configure the model, and load
    config = AutoConfig.from_pretrained(
        MODEL_SAVE_PATH,
        local_files_only=True,
        trust_remote_code=True
    )
    config.attn_config['attn_impl'] = 'torch'
    config.max_seq_len = 8192
    config.init_device = 'cuda:0'

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_SAVE_PATH,
        config=config,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        local_files_only=True,
    )
    
    # load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_SAVE_PATH, local_files_only=True)

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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(MPTChat())

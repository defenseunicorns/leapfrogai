import logging

from typing import Any, Generator, List
from threading import Thread

import torch

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)
import transformers.utils.logging

# completion
from leapfrogai import (
    CompletionRequest,
    CompletionChoice,
    CompletionFinishReason,
    CompletionUsage,
    CompletionResponse,
    CompletionServiceServicer,
    CompletionStreamServiceServicer,
)

# chat
from leapfrogai import (
    ChatCompletionRequest,
    ChatCompletionChoice,
    ChatItem,
    ChatRole,
    ChatCompletionResponse,
    ChatCompletionServiceServicer,
    ChatCompletionStreamServiceServicer,
)

# general
from leapfrogai import (
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

# Prompt Templates
SYSTEM_FORMAT = "<|im_start|>system\n{}<|im_end|>\n"
USER_FORMAT = "<|im_start|>user\n{}<|im_end|>\n"
ASSISTANT_FORMAT = "<|im_start|>assistant\n{}<|im_end|>\n"
# what gets appended to the end of the prompt to open the assistant's part of the conversation
RESPONSE_PREFIX = ASSISTANT_FORMAT.split("{}")[0]


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


def chat_items_to_prompt(chat_items: RepeatedCompositeFieldContainer[ChatItem]) -> str:
    """Converts a repeated ChatItem from a ChatCompletionRequest proto into a string

    This is the actual string that gets fed into the model to generate the outputs
    """
    prompt = ""
    for item in chat_items:
        if item.role == ChatRole.SYSTEM:
            prompt += SYSTEM_FORMAT.format(item.content)
        elif item.role == ChatRole.ASSISTANT:
            prompt += ASSISTANT_FORMAT.format(item.content)
        elif item.role == ChatRole.USER:
            prompt += USER_FORMAT.format(item.content)
        elif item.role == ChatRole.FUNCTION:
            logging.warning(
                "ChatRole FUNCTION is not implemented for this model and this ChatItem will be ignored."
            )
    # add the response prefix to start the model's reponse
    prompt += RESPONSE_PREFIX
    return prompt


class MPTChat(
    ChatCompletionServiceServicer,
    ChatCompletionStreamServiceServicer,
    CompletionServiceServicer,
    CompletionStreamServiceServicer,
):
    # create a config, configure the model, and load
    config = AutoConfig.from_pretrained(
        MODEL_SAVE_PATH, local_files_only=True, trust_remote_code=True
    )
    config.attn_config["attn_impl"] = "torch"
    config.max_seq_len = 8192
    config.init_device = "cuda:0"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_SAVE_PATH,
        config=config,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        local_files_only=True,
    )

    # load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_SAVE_PATH, local_files_only=True)

    def chat_stream(self, request: ChatCompletionRequest) -> Generator[str, Any, Any]:
        """Implements the logic for the chat endpoint of the MPT model"""
        # convert chat items to prompt and tokenize
        prompt = chat_items_to_prompt(request.chat_items)
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

        # create text streamer and validate parameters
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
        max_new_tokens = 1536 if request.max_new_tokens == 0 else request.max_new_tokens
        temperature = 0.1 if request.temperature == 0.0 else request.temperature
        top_p = 1.0 if request.top_p == 0.0 else request.top_p
        top_k = 0.0 if request.top_k == 0.0 else request.top_k

        # generate stream
        generation_kwargs = dict(
            inputs,
            streamer=streamer,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
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

    def ChatComplete(
        self, request: ChatCompletionRequest, context: GrpcContext
    ) -> ChatCompletionResponse:
        chat_stream = self.chat_stream(request)
        content = ""
        for text_chunk in chat_stream:
            content += text_chunk

        item = ChatItem(role=ChatRole.ASSISTANT, content=content)
        choice = ChatCompletionChoice(index=0, chat_item=item)

        return ChatCompletionResponse(choices=[choice])

    def ChatCompleteStream(
        self, request: ChatCompletionRequest, context: GrpcContext
    ) -> Generator[ChatCompletionResponse, Any, Any]:
        chat_stream = self.chat_stream(request)
        for text_chunk in chat_stream:
            item = ChatItem(role=ChatRole.ASSISTANT, content=text_chunk)
            choice = ChatCompletionChoice(index=0, chat_item=item)

            yield ChatCompletionResponse(choices=[choice])

    def completion_stream(self, request: CompletionRequest) -> Generator[str, Any, Any]:
        """Completion stream for use by Complete and CompleteStream"""
        inputs = self.tokenizer(request.prompt, return_tensors="pt").to("cuda")

        # create text streamer and validate parameters
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
        max_new_tokens = 1536 if request.max_new_tokens == 0 else request.max_new_tokens
        temperature = 0.1 if request.temperature == 0.0 else request.temperature
        top_p = 1.0 if request.top_p == 0.0 else request.top_p
        top_k = 0.0 if request.top_k == 0.0 else request.top_k

        # generate stream
        generation_kwargs = dict(
            inputs,
            streamer=streamer,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
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

    def Complete(
        self, request: CompletionRequest, context: GrpcContext
    ) -> CompletionResponse:
        completion_stream = self.completion_stream(request)
        text = ""
        for text_chunk in completion_stream:
            text += text_chunk

        choice = CompletionChoice(text=text, index=0)
        return CompletionResponse(choices=[choice])

    def CompleteStream(
        self, request: CompletionRequest, context
    ) -> Generator[CompletionResponse, Any, Any]:
        completion_stream = self.completion_stream(request)
        for text_chunk in completion_stream:
            choice = CompletionChoice(text=text_chunk, index=0)
            yield CompletionResponse(choices=[choice])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(MPTChat())

# prompt = chat_items_to_prompt(request.chat_items)
# inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
# logging.debug(f"Request:  { request }")
# # error checking for valid params
# tokens = self.model.generate(
#     **inputs,
#     max_new_tokens=request.max_new_tokens,
#     temperature=request.temperature,
#     # repetition_penalty=request.frequence_penalty,
#     top_p=request.top_p,
#     do_sample=True,
#     pad_token_id=self.tokenizer.eos_token_id,
#     eos_token_id=self.tokenizer.eos_token_id,
#     stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
# )
# logging.debug(f"Response {tokens}")
# # Extract out only the completion tokens
# completion_tokens = tokens[0][inputs["input_ids"].size(1) :]
# completion = self.tokenizer.decode(completion_tokens, skip_special_tokens=True)

# # TODO: extend the completion to the multi-response (n>1) case
# # response = self.tokenizer.decode(tokens[0], skip_special_tokens=False)
# logging.debug(f"Decoded Response: {completion}")
# role = ChatRole.ASSISTANT
# item = ChatItem(role=role, content=completion)
# choice = CompletionChoice(index=0, chat_item=item)
# return ChatCompletionResponse(choices=[choice])

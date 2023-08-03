import logging
from typing import Any, Generator
import os 
from threading import Thread
from ctransformers import AutoModelForCausalLM

from transformers import (
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)
import transformers.utils.logging

from leapfrogai import (
    CompletionChoice,
    CompletionFinishReason,
    CompletionRequest,
    CompletionResponse,
    CompletionUsage,
    GrpcContext,
    serve,
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

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
import torch

model_name = os.environ.get("MODEL_NAME")
if model_name is None:
    model_name = "TheBloke/mpt-30B-chat-GGML"
print(f"Loading Model { model_name }")



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

class CTransformers:
    
    llm = AutoModelForCausalLM.from_pretrained(
            model_name, 
            # model_file="mpt-30b-chat.ggmlv0.q4_0.bin"
        )

    # def chat_stream(self, request: ChatCompletionRequest) -> Generator[str, Any, Any]:
    #     """Implements the logic for the chat endpoint of the MPT model"""
    #     # convert chat items to prompt and tokenize
    #     print(f"chat_stream: Recieved Stream Request: { request }\n")
    #     prompt = chat_items_to_prompt(request.chat_items)
    #     inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

    #     # create text streamer and validate parameters
    #     streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
    #     max_new_tokens = 1536 if request.max_new_tokens == 0 else request.max_new_tokens
    #     temperature = 0.1 if request.temperature == 0.0 else request.temperature
    #     top_p = 1.0 if request.top_p == 0.0 else request.top_p
    #     top_k = 0.0 if request.top_k == 0.0 else request.top_k

    #     # generate stream
    #     generation_kwargs = dict(
    #         inputs,
    #         streamer=streamer,
    #         max_new_tokens=max_new_tokens,
    #         temperature=temperature,
    #         top_p=top_p,
    #         top_k=top_k,
    #         do_sample=True,
    #         pad_token_id=self.tokenizer.eos_token_id,
    #         eos_token_id=self.tokenizer.eos_token_id,
    #         stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
    #     )
    #     thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
    #     thread.start()
    #     for text in streamer:
    #         print(text)
    #         yield text

    def ChatComplete(
        self, request: ChatCompletionRequest, context: GrpcContext
    ) -> ChatCompletionResponse:
        print(f"ChatComplete: Recieved Request: { request }\n", flush=True)
        prompt = chat_items_to_prompt(request.chat_items)
        print(f"ChatComplete: Converted to Prompt:\n\n { prompt }\n", flush=True)
        completionRequest = CompletionRequest(
            prompt=prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            # top_k=request.top_k, #
            top_p=request.top_p,
            n=request.n,
            # do_sample=request.do_sample,
            user=request.user,
            presence_penalty=request.presence_penalty,
            logit_bias=request.logit_bias,
            frequence_penalty=request.frequency_penalty,
            repetition_penalty=request.repetition_penalty,
        )

        res = self.Complete(request=completionRequest, context=context)
        content = res.choices[0].text

        item = ChatItem(role=ChatRole.ASSISTANT, content=content)
        choice = ChatCompletionChoice(index=0, chat_item=item)

        return ChatCompletionResponse(choices=[choice])

    def ChatCompleteStream(
        self, request: ChatCompletionRequest, context: GrpcContext
    ) -> Generator[ChatCompletionResponse, Any, Any]:
        print(f"ChatCompleteStream: Recieved Stream Request: { request }\n", flush=True)
        # chat_stream = self.chat_stream(request)
        yield self.ChatComplete(request=request, context=context)

    def remove_strings(self, string, start_string, end_string):
        """Removes all instances of the start_string and end_string from the string.

        Args:
            string: The string to remove the start_string and end_string from.
            start_string: The string to remove.
            end_string: The string to remove.

        Returns:
            The string with the start_string and end_string removed.
        """

        start_index = string.find(start_string)
        while start_index != -1:
            end_index = string.find(end_string, start_index + len(start_string))
            if end_index != -1:
                string = string[:start_index] + string[end_index + len(end_string):]
                start_index = string.find(start_string)
            else:
                break

        return string


    def Complete(
        self, request: CompletionRequest, context: GrpcContext
    ) -> CompletionResponse:
        print(f"Complete: Recieved Request:\n\n { request }\n", flush=True)
        # Clean up inputs
        max_new_tokens = 1536 if request.max_new_tokens == 0 else request.max_new_tokens
        temperature = 0.1 if request.temperature == 0.0 else request.temperature
        top_p = 1.0 if request.top_p == 0.0 else request.top_p
        top_k = 0.0 if request.top_k == 0.0 else request.top_k

        text = self.llm(
            request.prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            # top_p=top_p,
            # top_k=top_k,
            # do_sample=True,
            # pad_token_id=self.tokenizer.eos_token_id,
            # eos_token_id=self.tokenizer.eos_token_id,
            # stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
            # stop=["<|im_end|>"],
        )
        text = self.remove_strings(text, "<|im_end|>", "<|im_start|>")

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
            # stop=["<|im_end|>"],
        ):
            print(text)
            completion = CompletionChoice(text=text, index=0)
            yield CompletionResponse(choices=[completion])
        print("COMPLETESTREAM END")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(CTransformers())

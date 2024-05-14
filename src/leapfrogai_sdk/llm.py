import copy
import os
from typing import Any, Generator, List

from pydantic import BaseModel

from leapfrogai_sdk import (
    BackendConfig,
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatItem,
    ChatRole,
    CompletionChoice,
    CompletionRequest,
    CompletionResponse,
    GrpcContext, CompletionUsage,
)
from leapfrogai_sdk.chat.chat_pb2 import Usage


class GenerationConfig(BaseModel):
    max_new_tokens: int
    temperature: float
    top_k: int
    top_p: float
    do_sample: bool
    n: int
    stop: List[str]
    repetition_penalty: float
    presence_penalty: float
    frequency_penalty: float | None = None
    best_of: str
    logit_bias: dict[str, int]
    return_full_text: bool
    truncate: int
    typical_p: float
    watermark: bool
    seed: int


def LLM(_cls):
    if not hasattr(_cls, "generate"):
        raise ValueError("LLM class requires a generate method")

    if not hasattr(_cls, "count_tokens"):
        raise ValueError("LLM class requires a count_tokens method")

    def create_chat_completion_response(text: str, finish_reason: str = None, usage: Usage = None) -> ChatCompletionResponse:
        item: ChatItem = ChatItem(role=ChatRole.ASSISTANT, content=text)
        choice: ChatCompletionChoice = ChatCompletionChoice(index=0, chat_item=item)
        response: ChatCompletionResponse = ChatCompletionResponse(choices=[choice])

        if finish_reason:
            response.choices[0].finish_reason = finish_reason

        if usage:
            response.usage = usage

        return response

    def create_completion_response(text: str, finish_reason: str = None, usage: CompletionUsage = None) -> CompletionResponse:
        choice: CompletionChoice = CompletionChoice(index=0, text=text)
        response: CompletionResponse = CompletionResponse(choices=[choice])

        if finish_reason:
            response.choices[0].finish_reason = finish_reason

        if usage:
            response.usage = usage

        return response

    class NewClass(_cls):
        config: BackendConfig

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.config = BackendConfig()

        def _build_gen_stream(
            self, prompt: str, request: ChatCompletionRequest | CompletionRequest
        ) -> Generator[str, Any, Any]:
            config = GenerationConfig(
                max_new_tokens=request.max_new_tokens,
                temperature=request.temperature,
                top_k=request.top_k,
                top_p=request.top_p,
                do_sample=request.do_sample,
                n=request.n,
                stop=list(request.stop),
                repetition_penalty=request.repetition_penalty,
                presence_penalty=request.presence_penalty,
                best_of=request.best_of,
                logit_bias=request.logit_bias,
                return_full_text=request.return_full_text,
                truncate=request.truncate,
                typical_p=request.typical_p,
                watermark=request.watermark,
                seed=request.seed,
            )
            return self.generate(prompt, config)

        async def ChatComplete(
            self, request: ChatCompletionRequest, context: GrpcContext
        ) -> ChatCompletionResponse:
            prompt = self.config.apply_chat_template(request.chat_items)

            gen_stream = self._build_gen_stream(
                prompt, request
            )

            content = ""
            for text_chunk in gen_stream:
                content += text_chunk

            completion_token_count: int = await self.count_tokens(content)

            if completion_token_count < request.max_new_tokens:
                finish_reason = "stop"
            else:
                finish_reason = "length"

            prompt_token_count: int = await self.count_tokens(prompt)
            total_token_count: int = prompt_token_count + completion_token_count

            response = create_chat_completion_response(
                content,
                finish_reason,
                Usage(prompt_token_count, completion_token_count, total_token_count)
            )

            return response

        async def ChatCompleteStream(
            self, request: ChatCompletionRequest, context: GrpcContext
        ) -> Generator[ChatCompletionResponse, Any, Any]:
            prompt = self.config.apply_chat_template(request.chat_items)

            gen_stream = self._build_gen_stream(
                prompt, request
            )

            last_delta: str | None = None
            response_str: str = ""

            for text_chunk in gen_stream:
                if last_delta:
                    last_response: ChatCompletionResponse = create_chat_completion_response(last_delta, "")
                    response_str += last_delta

                    yield last_response

                last_delta = text_chunk

            if last_delta:
                response_str += last_delta

                completion_token_count: int = await self.count_tokens(response_str)

                if completion_token_count < request.max_new_tokens:
                    finish_reason = "stop"
                else:
                    finish_reason = "length"

                prompt_token_count: int = await self.count_tokens(prompt)
                total_token_count: int = prompt_token_count + completion_token_count

                last_response: ChatCompletionResponse = create_chat_completion_response(
                    last_delta,
                    finish_reason,
                    Usage(prompt_token_count, completion_token_count, total_token_count)
                )

                yield last_response

        async def Complete(
            self, request: CompletionRequest, context: GrpcContext
        ) -> CompletionResponse:
            gen_stream = self._build_gen_stream(request.prompt, request)

            content = ""
            for text_chunk in gen_stream:
                content += text_chunk

            completion_token_count: int = await self.count_tokens(content)

            if completion_token_count < request.max_new_tokens:
                finish_reason = "stop"
            else:
                finish_reason = "length"

            prompt_token_count: int = await self.count_tokens(request.prompt)
            total_token_count: int = prompt_token_count + completion_token_count

            return create_completion_response(
                content,
                finish_reason,
                CompletionUsage(prompt_token_count, completion_token_count, total_token_count)
            )

        async def CompleteStream(
            self, request: CompletionRequest, context: GrpcContext
        ) -> Generator[CompletionResponse, Any, Any]:
            gen_stream = self._build_gen_stream(request.prompt, request)
            last_delta: str | None = None
            response_str: str = ""

            for text_chunk in gen_stream:
                if last_delta:
                    last_response = create_completion_response(text=last_delta, finish_reason="")
                    response_str += last_delta

                    yield last_response

                last_delta = text_chunk

            if last_delta:
                response_str += last_delta

                completion_token_count: int = await self.count_tokens(response_str)

                if completion_token_count < request.max_new_tokens:
                    finish_reason = "stop"
                else:
                    finish_reason = "length"

                prompt_token_count: int = await self.count_tokens(request.prompt)
                total_token_count: int = prompt_token_count + completion_token_count

                last_response = create_completion_response(
                    last_delta,
                    finish_reason,
                    CompletionUsage(prompt_token_count, completion_token_count, total_token_count)
                )

                yield last_response

    NewClass.__name__ = _cls.__name__
    return NewClass

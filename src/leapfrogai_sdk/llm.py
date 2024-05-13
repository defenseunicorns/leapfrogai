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
    GrpcContext,
)


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
            gen_stream = self._build_gen_stream(
                self.config.apply_chat_template(request.chat_items), request
            )

            content = ""
            for text_chunk in gen_stream:
                content += text_chunk

            item = ChatItem(role=ChatRole.ASSISTANT, content=content)
            choice = ChatCompletionChoice(index=0, chat_item=item)

            token_count = await self.count_tokens(choice.chat_item.content)

            if token_count < request.max_new_tokens:
                choice.finish_reason = "stop"
            else:
                choice.finish_reason = "length"

            return ChatCompletionResponse(choices=[choice])

        async def ChatCompleteStream(
            self, request: ChatCompletionRequest, context: GrpcContext
        ) -> Generator[ChatCompletionResponse, Any, Any]:
            gen_stream = self._build_gen_stream(
                self.config.apply_chat_template(request.chat_items), request
            )

            print("Attempting to chat stream")

            last_response: ChatCompletionResponse | None = None
            response_str: str = ""

            for text_chunk in gen_stream:
                if last_response:
                    last_response.choices[0].finish_reason = None
                    response_str += last_response.choices[0].chat_item.content
                    yield last_response

                item = ChatItem(role=ChatRole.ASSISTANT, content=text_chunk)
                choice = ChatCompletionChoice(index=0, chat_item=item)

                last_response = ChatCompletionResponse(choices=[choice])

            if last_response:
                response_str += last_response.choices[0].chat_item.content

                token_count = await self.count_tokens(response_str)

                if token_count < request.max_new_tokens:
                    last_response.choices[0].finish_reason = "stop"
                else:
                    last_response.choices[0].finish_reason = "length"

                yield last_response

            print(f"Finish chat stream {response_str}")

        async def Complete(
            self, request: CompletionRequest, context: GrpcContext
        ) -> CompletionResponse:
            gen_stream = self._build_gen_stream(request.prompt, request)

            content = ""
            for text_chunk in gen_stream:
                content += text_chunk

            choice = CompletionChoice(index=0, text=content)
            token_count = await self.count_tokens(choice.text)

            if token_count < request.max_new_tokens:
                choice.finish_reason = "stop"
            else:
                choice.finish_reason = "length"

            return CompletionResponse(choices=[choice])

        async def CompleteStream(
            self, request: CompletionRequest, context: GrpcContext
        ) -> Generator[CompletionResponse, Any, Any]:
            gen_stream = self._build_gen_stream(request.prompt, request)
            last_response: CompletionResponse | None = None
            response_str: str = ""

            print("Attempting to stream")

            for text_chunk in gen_stream:
                if last_response:
                    response_str += last_response.choices[0].text
                    yield last_response

                print(text_chunk)
                choice = CompletionChoice(index=0, text=text_chunk)
                last_response = CompletionResponse(choices=[choice])

            if last_response:
                response_str += last_response.choices[0].text

                token_count = await self.count_tokens(response_str)

                if token_count < request.max_new_tokens:
                    last_response.choices[0].finish_reason = "stop"
                else:
                    last_response.choices[0].finish_reason = "length"

                yield last_response

    NewClass.__name__ = _cls.__name__
    return NewClass

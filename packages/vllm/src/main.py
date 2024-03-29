import asyncio
import json
import logging
import os
import queue
import random
import sys
import threading
import time
from typing import Any, Generator, Dict

from confz import EnvSource
from dotenv import load_dotenv
from leapfrogai_sdk.types import (
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
    serve,
)
from leapfrogai_sdk.types.llm import GenerationConfig
from vllm import SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.outputs import RequestOutput
from vllm.utils import random_uuid

from config import AppConfig

load_dotenv()


def clamp(n: float | int, smallest: float | int, largest: float | int):
    return max(smallest, min(n, largest))


class RandomAsyncIterator:
    """Manages multiple async iterables and allows iterating over them in a random order."""

    def __init__(self, async_iterables):
        # Convert each iterable into an async iterator
        self.async_iterators = [ai.__aiter__() for ai in async_iterables]

    def __aiter__(self):
        return self

    async def __anext__(self):
        """Return the next item from a randomly chosen iterator. If all iterators are exhausted, stop iteration."""
        if not self.async_iterators:  # Check if there are no iterators left
            raise StopAsyncIteration

        # Select a random iterator from the list
        random_index = random.randint(0, len(self.async_iterators) - 1)
        try:
            # Attempt to get the next item from the randomly selected iterator
            return await self.async_iterators[random_index].__anext__()
        except StopAsyncIteration:
            # If the selected iterator is exhausted, remove it from the list
            del self.async_iterators[random_index]

        # If all iterators are exhausted, raise StopAsyncIteration
        raise StopAsyncIteration

    def is_empty(self):
        """Check if there are any iterators left."""
        return len(self.async_iterators) <= 0

    def add_iterator(self, async_iterable):
        """Add a new async iterable to the pool of iterators."""
        self.async_iterators.append(async_iterable.__aiter__())

    def remove_iterator(self, async_iterable):
        """Attempt to remove an async iterable from the pool if it exists."""
        try:
            self.async_iterators.remove(async_iterable.__aiter__())
        except ValueError:
            pass  # If the iterable is not found, ignore the error


def get_backend_configs():
    # Manually load env var as ConfZ does not handle complex types (list)
    stop_tokens: str | None = os.getenv("LAI_STOP_TOKENS")
    if stop_tokens:
        processed_stop_tokens = json.loads(stop_tokens)
    else:
        processed_stop_tokens = []
    del os.environ["LAI_STOP_TOKENS"]

    BackendConfig.CONFIG_SOURCES = EnvSource(
        allow_all=True,
        prefix="LAI_",
        remap={
            "model_source": "model.source",
            "max_context_length": "max_context_length",
            "stop_tokens": "stop_tokens",
            "prompt_format_chat_system": "prompt_format.chat.system",
            "prompt_format_chat_assistant": "prompt_format.chat.assistant",
            "prompt_format_chat_user": "prompt_format.chat.user",
            "prompt_format_defaults_top_p": "prompt_format.defaults.top_p",
            "prompt_format_defaults_top_k": "prompt_format.defaults.top_k",
        },
    )
    # Initialize an immutable config from env variables without stop_tokens list
    backend_configs: BackendConfig = BackendConfig()

    # Create a new config from env variables + stop_tokens
    BackendConfig.CONFIG_SOURCES = None
    backend_configs = BackendConfig(
        name=backend_configs.name,
        model=backend_configs.model,
        max_context_length=backend_configs.max_context_length,
        stop_tokens=processed_stop_tokens,
        prompt_format=backend_configs.prompt_format,
        default=backend_configs.defaults,
    )
    return backend_configs


def get_config_from_request(request: ChatCompletionRequest | CompletionRequest):
    return GenerationConfig(
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p,
        do_sample=request.do_sample,
        n=request.n,
        stop=list(request.stop),
        repetition_penalty=request.repetition_penalty,
        presence_penalty=request.presence_penalty,
        best_of=str(request.best_of),
        logit_bias=request.logit_bias,
        return_full_text=request.return_full_text,
        truncate=request.truncate,
        typical_p=request.typical_p,
        watermark=request.watermark,
        seed=request.seed,
    )


class Model:
    """Implements an LLM model with concurrent output generation and management."""

    done_by_id: Dict[str, bool] = {}
    delta_queue_by_id: Dict[str, queue.Queue] = {}
    result_by_id: Dict[str, RequestOutput] = {}
    random_iterator: RandomAsyncIterator = RandomAsyncIterator([])

    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)

        # Background thread for managing output iteration
        _thread = threading.Thread(target=asyncio.run, args=(self.iterate_outputs(),))
        _thread.start()

        self.backend_config = get_backend_configs()
        self.model = self.backend_config.model.source
        self.engine_args = AsyncEngineArgs(
            engine_use_ray=True,
            model=self.model,
            trust_remote_code=False,
            quantization=AppConfig().backend_options.quantization,
            max_context_len_to_capture=self.backend_config.max_context_length,
            max_model_len=self.backend_config.max_context_length,
            dtype="auto",
            worker_use_ray=True,
            gpu_memory_utilization=0.90,
            tensor_parallel_size=1,
        )
        print(self.engine_args)
        self.engine = AsyncLLMEngine.from_engine_args(self.engine_args)

    async def iterate_outputs(self):
        """Continuously processes outputs from the random iterator and manages state by request IDs."""

        t0_by_id: dict[str, float] = {}
        index_by_id: dict[str, int] = {}
        num_tokens_by_id: dict[str, int] = {}

        while True:
            if not self.random_iterator.is_empty():
                request_output: RequestOutput
                async for request_output in self.random_iterator:
                    request_id = request_output.request_id

                    if request_output.finished:
                        # Signal that the "generate" function can stop waiting for additional inputs
                        logging.info(
                            f"Generated {num_tokens_by_id[request_id]} tokens in {time.time() - t0_by_id[request_id]:.2f}s"
                        )
                        self.done_by_id[request_id] = True
                    else:
                        # Initialize dictionary entries
                        if t0_by_id.get(request_id) is None:
                            t0_by_id[request_id] = time.time()

                        if index_by_id.get(request_id) is None:
                            index_by_id[request_id] = 0

                        if num_tokens_by_id.get(request_id) is None:
                            num_tokens_by_id[request_id] = 0

                    if (
                        request_output.outputs[0].text
                        and "\ufffd" == request_output.outputs[0].text[-1]
                    ):
                        continue

                    # Update tracking information
                    text_delta = request_output.outputs[0].text[
                        index_by_id[request_id] :
                    ]
                    index_by_id[request_id] = len(request_output.outputs[0].text)
                    num_tokens_by_id[request_id] = len(
                        request_output.outputs[0].token_ids
                    )

                    # Add the result to the queue for this request
                    self.delta_queue_by_id[request_id].put(text_delta)
            time.sleep(0)

    async def create_response(
        self, request_id: str, prompt: str, config: GenerationConfig
    ):
        """Initiate a response generation for the given prompt and configuration, adding the result to the iterator
        pool."""

        sampling_params = SamplingParams(
            temperature=config.temperature,
            # Clamp top_p value to prevent float errors
            top_p=clamp(config.top_p, 0.0 + sys.float_info.epsilon, 1.0),
            # Restrict top_k to valid values, -1 disables top_k
            top_k=config.top_k if config.top_k >= 1 else -1,
            stop=self.backend_config.stop_tokens,
            max_tokens=config.max_new_tokens,
            skip_special_tokens=False,
        )
        logging.debug(sampling_params)
        logging.info(f"Begin generation for request {request_id}")
        # Generate texts from the prompts. The output is a list of RequestOutput objects
        # that contain the prompt, generated text, and other information.
        gen_iter = self.engine.generate(prompt, sampling_params, request_id)
        logging.info(f"Begin iteration for request {request_id}")
        self.random_iterator.add_iterator(gen_iter)

    async def generate_session(
        self, session: str, prompt: str, config: GenerationConfig
    ):
        """Manage a session's lifecycle for generating output, including setting up necessary state and iterators."""

        if self.delta_queue_by_id.get(session) is None:
            self.delta_queue_by_id[session] = queue.Queue()

        await self.create_response(session, prompt, config)

    def is_queue_empty(self, request_id) -> bool:
        """Check if the queue for a given request ID is empty or non-existent."""

        cur_request_queue = self.delta_queue_by_id.get(request_id)
        return cur_request_queue is None or cur_request_queue.empty()

    def stream_request(self, config: GenerationConfig, prompt: str):
        """Initiate and manage the generation process for a given prompt, yielding generated text segments."""

        request_id = random_uuid()
        self.done_by_id[request_id] = False

        # Spawns a thread to request a response for the prompt
        _thread = threading.Thread(
            target=asyncio.run,
            args=(self.generate_session(request_id, prompt, config),),
        )
        _thread.start()

        logging.info(f"Begin reading the output for request {request_id}")

        while not self.done_by_id.get(request_id) or not self.is_queue_empty(
            request_id
        ):
            result = ""
            if not self.is_queue_empty(request_id):
                result = self.delta_queue_by_id.get(request_id).get()
            yield result

        logging.info(f"Finished request {request_id}")

    def complete_stream(self, request: CompletionRequest) -> Generator[str, Any, Any]:
        """Wrapper around stream_request to transform prompt and config variables from a CompletionRequest"""

        prompt = request.prompt
        config = get_config_from_request(request)

        return self.stream_request(config, prompt)

    def chat_stream(self, request: ChatCompletionRequest) -> Generator[str, Any, Any]:
        """Wrapper around stream_request to transform prompt and config variables from a ChatCompletionRequest"""

        prompt = self.backend_config.apply_chat_template(request.chat_items)
        config = get_config_from_request(request)

        return self.stream_request(config, prompt)

    async def Complete(
        self, request: CompletionRequest, context: GrpcContext
    ) -> CompletionResponse:
        """
        Handles a completion request and returns the complete response.

        Args:
            request (CompletionRequest): The completion request object containing the prompt and other parameters.
            context (GrpcContext): The gRPC context object.

        Returns:
            CompletionResponse: The completion response object containing the generated text.
        """

        logging.info("Complete:\n---")
        chat_stream = self.complete_stream(request)

        content = ""
        for text_chunk in chat_stream:
            content += text_chunk

        completion = CompletionChoice(index=0, text=content)
        logging.info("Complete END:\n---")
        return CompletionResponse(choices=[completion])

    async def CompleteStream(
        self, request: CompletionRequest, context: GrpcContext
    ) -> Generator[CompletionResponse, Any, Any]:
        """
        Handles a streaming completion request and yields the response in chunks.

        Args:
            request (CompletionRequest): The completion request object containing the prompt and other parameters.
            context (GrpcContext): The gRPC context object.

        Returns:
            CompletionResponse: Yields the completion response object containing a chunk of the generated text.
        """

        logging.info("CompleteStream:\n---")
        chat_stream = self.complete_stream(request)

        for text_chunk in chat_stream:
            choice = CompletionChoice(index=0, text=text_chunk)
            yield CompletionResponse(choices=[choice])

        logging.info("CompleteStream END")

    async def ChatComplete(
        self, request: ChatCompletionRequest, context: GrpcContext
    ) -> ChatCompletionResponse:
        """
        Handles a chat completion request and returns the complete response.

        Args:
            request (ChatCompletionRequest): The chat completion request object containing the chat items and other parameters.
            context (GrpcContext): The gRPC context object.

        Returns:
            ChatCompletionResponse: The chat completion response object containing the generated text.
        """

        logging.info("ChatComplete:\n---")
        chat_stream = self.chat_stream(request)

        content = ""
        for text_chunk in chat_stream:
            content += text_chunk

        item = ChatItem(role=ChatRole.ASSISTANT, content=content)
        choice = ChatCompletionChoice(index=0, chat_item=item)
        logging.info("ChatCompleteStream END:\n---")
        return ChatCompletionResponse(choices=[choice])

    async def ChatCompleteStream(
        self, request: ChatCompletionRequest, context: GrpcContext
    ) -> Generator[ChatCompletionResponse, Any, Any]:
        """
        Handles a streaming chat completion request and yields the response in chunks.

        Args:
            request (ChatCompletionRequest): The chat completion request object containing the chat items and other parameters.
            context (GrpcContext): The gRPC context object.

        Returns:
            ChatCompletionResponse: Yields the chat completion response object containing a chunk of the generated text.
        """

        logging.info("ChatCompleteStream:\n---")
        chat_stream = self.chat_stream(request)

        for text_chunk in chat_stream:
            item = ChatItem(role=ChatRole.ASSISTANT, content=text_chunk)
            choice = ChatCompletionChoice(index=0, chat_item=item)

            yield ChatCompletionResponse(choices=[choice])

        logging.info("ChatCompleteStream END:\n---")


async def main():
    logging.basicConfig(level=logging.INFO)
    await serve(Model())


if __name__ == "__main__":
    asyncio.run(main())

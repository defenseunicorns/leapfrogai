import asyncio
import json
import logging
import os
import random
import sys
import time
from typing import Any, Dict, AsyncGenerator
from confz import EnvSource
from dotenv import load_dotenv
from vllm import SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.utils import random_uuid

from config import AppConfig
from leapfrogai_sdk import BackendConfig, ChatCompletionRequest, CompletionRequest
from leapfrogai_sdk.llm import GenerationConfig, LLM

load_dotenv()

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)


def clamp(n: float | int, smallest: float | int, largest: float | int):
    """Helper function to clamp a value between a minimum and maximum."""
    return max(smallest, min(n, largest))


class RandomAsyncIterator:
    """Manages multiple async iterators, allowing iteration over them in a random order."""

    def __init__(self, async_iterables):
        """Initializes the RandomAsyncIterator with a list of async iterables."""
        self.async_iterators = [ai.__aiter__() for ai in async_iterables]

    def __aiter__(self):
        """Returns the iterator itself, as this class implements __aiter__."""
        return self

    async def __anext__(self):
        """Returns the next item from a randomly chosen iterator, removing exhausted iterators."""
        if not self.async_iterators:
            raise StopAsyncIteration

        random_index = random.randint(0, len(self.async_iterators) - 1)
        try:
            return await self.async_iterators[random_index].__anext__()
        except StopAsyncIteration:
            del self.async_iterators[random_index]

        if not self.async_iterators:
            raise StopAsyncIteration


def get_backend_configs():
    """Loads backend configurations from environment variables and processes stop tokens."""
    stop_tokens = os.getenv("LAI_STOP_TOKENS")
    processed_stop_tokens = json.loads(stop_tokens) if stop_tokens else []

    env_source = EnvSource(
        allow_all=True,
        prefix="LAI_",
        remap={
            "model_source": "model.source",
            "max_context_length": "max_context_length",
            "stop_tokens": "stop_tokens",
            "prompt_format_chat_system": "prompt_format.chat.system",
            "prompt_format_chat_assistant": "prompt_format.chat.assistant",
            "prompt_format_chat_user": "prompt_format.chat.user",
        },
    )

    BackendConfig.CONFIG_SOURCES = env_source
    backend_configs = BackendConfig()
    backend_configs.model_copy(update={"stop_tokens": processed_stop_tokens})

    return backend_configs


def get_config_from_request(request: ChatCompletionRequest | CompletionRequest):
    """Generates a GenerationConfig from a request object."""
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


@LLM
class Model:
    """Implements an LLM model with concurrent output generation and management."""

    done_by_id: Dict[str, bool] = {}
    delta_queue_by_id: Dict[str, asyncio.Queue] = {}
    random_iterator: RandomAsyncIterator = RandomAsyncIterator([])

    def __init__(self):
        """Initializes the model and its configuration based on environment variables."""
        self.backend_config = get_backend_configs()

        quantization = (
            None
            if AppConfig().backend_options.quantization in ["", "None"]
            else AppConfig().backend_options.quantization
        )

        self.engine_args = AsyncEngineArgs(
            # Taken from the LFAI SDK general LLM configuration
            max_seq_len_to_capture=self.backend_config.max_context_length,
            max_model_len=self.backend_config.max_context_length,
            # Taken from the vLLM-specific configuration
            model=AppConfig().backend_options.model_source,
            enforce_eager=AppConfig().backend_options.enforce_eager,
            quantization=quantization,
            engine_use_ray=AppConfig().backend_options.engine_use_ray,
            worker_use_ray=AppConfig().backend_options.worker_use_ray,
            tensor_parallel_size=AppConfig().backend_options.tensor_parallel_size,
            gpu_memory_utilization=AppConfig().backend_options.gpu_memory_utilization,
            trust_remote_code=AppConfig().backend_options.trust_remote_code,
        )

        self.engine = AsyncLLMEngine.from_engine_args(self.engine_args)

    async def iterate_outputs(self):
        """Continuously iterates over the outputs of the random iterator and processes generated text."""
        t0_by_id = {}
        index_by_id = {}
        num_tokens_by_id = {}

        while True:
            if not self.random_iterator.is_empty():
                async for request_output in self.random_iterator:
                    request_id = request_output.request_id

                    if request_output.finished:
                        logger.info(
                            f"Generated {num_tokens_by_id.get(request_id, 0)} tokens in {time.time() - t0_by_id.get(request_id, 0):.2f}s"
                        )
                        self.done_by_id[request_id] = True
                    else:
                        if t0_by_id.get(request_id) is None:
                            t0_by_id[request_id] = time.time()

                        if index_by_id.get(request_id) is None:
                            index_by_id[request_id] = 0

                        if num_tokens_by_id.get(request_id) is None:
                            num_tokens_by_id[request_id] = 0

                    text_delta = request_output.outputs[0].text[
                        index_by_id[request_id] :
                    ]
                    index_by_id[request_id] = len(request_output.outputs[0].text)
                    num_tokens_by_id[request_id] = len(
                        request_output.outputs[0].token_ids
                    )

                    await self.delta_queue_by_id[request_id].put(text_delta)

            await asyncio.sleep(0)

    async def create_response(
        self, request_id: str, prompt: str, config: GenerationConfig
    ):
        """Creates and adds a response for the given request by starting the text generation process."""
        sampling_params = SamplingParams(
            temperature=config.temperature,
            top_p=clamp(config.top_p, 0.0 + sys.float_info.epsilon, 1.0),
            top_k=config.top_k if config.top_k >= 1 else -1,
            stop=self.backend_config.stop_tokens,
            max_tokens=config.max_new_tokens,
            skip_special_tokens=False,
        )

        gen_iter = self.engine.generate(prompt, sampling_params, request_id)
        self.random_iterator.add_iterator(gen_iter)

    async def generate_session(
        self, session: str, prompt: str, config: GenerationConfig
    ):
        """Manages the lifecycle of generating outputs for a session, ensuring prompt processing."""
        if session not in self.delta_queue_by_id:
            self.delta_queue_by_id[session] = asyncio.Queue()

        await self.create_response(session, prompt, config)

    async def generate(
        self, prompt: str, config: GenerationConfig
    ) -> AsyncGenerator[str, Any]:
        """Initiates and manages the generation process for a given prompt, yielding text segments."""
        request_id = random_uuid()
        self.done_by_id[request_id] = False

        await self.generate_session(request_id, prompt, config)

        while (
            not self.done_by_id.get(request_id)
            or not self.delta_queue_by_id[request_id].empty()
        ):
            result = ""
            if not self.delta_queue_by_id[request_id].empty():
                result = await self.delta_queue_by_id[request_id].get()
            yield result

        logger.info(f"Finished request {request_id}")

    async def count_tokens(self, raw_text: str) -> int:
        """Counts the number of tokens in a given raw text using the engine's tokenizer."""
        tokens = (await self.engine.get_tokenizer()).tokenize(raw_text)
        return len(tokens)

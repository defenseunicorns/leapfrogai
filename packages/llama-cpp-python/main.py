import logging
import os
from typing import Any, AsyncGenerator

from llama_cpp import Llama

from leapfrogai_sdk import BackendConfig
from leapfrogai_sdk.llm import LLM, GenerationConfig

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)


@LLM
class Model:
    backend_config = BackendConfig()

    if not os.path.exists(backend_config.model.source):
        raise ValueError(f"Model path ({backend_config.model.source}) does not exist")

    llm = Llama(
        model_path=backend_config.model.source,
        n_ctx=backend_config.max_context_length,
        n_gpu_layers=0,
    )

    async def generate(
        self, prompt: str, config: GenerationConfig
    ) -> AsyncGenerator[str, Any]:
        logger.info("Begin generating streamed response")
        for res in self.llm(
            prompt,
            stream=True,
            temperature=config.temperature,
            max_tokens=config.max_new_tokens,
            top_p=config.top_p,
            top_k=config.top_k,
            stop=self.backend_config.stop_tokens,
        ):
            yield res["choices"][0]["text"]  # type: ignore
        logger.info("Streamed response complete")

    async def count_tokens(self, raw_text: str) -> int:
        string_bytes: bytes = bytes(raw_text, "utf-8")
        tokens: list[int] = self.llm.tokenize(string_bytes)
        return len(tokens)

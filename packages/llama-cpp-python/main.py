import os
from typing import Any, Generator

from leapfrogai_sdk import BackendConfig
from leapfrogai_sdk.llm import LLM, GenerationConfig
from llama_cpp import Llama

GPU_ENABLED = (
    False if os.environ.get("GPU_ENABLED", "False").lower() != "true" else True
)


@LLM
class Model:
    backend_config = BackendConfig()

    llm = Llama(
        model_path=backend_config.model.source,
        n_ctx=backend_config.max_context_length,
        n_gpu_layers=-1 if GPU_ENABLED is True else 0,
    )

    def generate(
        self, prompt: str, config: GenerationConfig
    ) -> Generator[str, Any, Any]:
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

    async def count_tokens(self, raw_text: str):
        string_bytes: bytes = bytes(raw_text, "utf-8")
        tokens: list[int] = self.llm.tokenize(string_bytes)
        return len(tokens)

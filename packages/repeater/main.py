import logging
import os
from typing import Any, AsyncGenerator

from leapfrogai_sdk.llm import LLM, GenerationConfig

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)


@LLM
class Model:
    async def generate(
        self, prompt: str, config: GenerationConfig
    ) -> AsyncGenerator[str, Any]:
        logger.info("Begin generating streamed response")
        for char in prompt:
            yield char  # type: ignore
        logger.info("Streamed response complete")

    async def count_tokens(self, raw_text: str) -> int:
        return len(raw_text)

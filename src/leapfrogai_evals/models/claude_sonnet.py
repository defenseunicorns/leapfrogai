import os

import instructor
from pydantic import BaseModel
from deepeval.models.base_model import DeepEvalBaseLLM
import asyncio
from anthropic import Anthropic
from typing import Optional


class ClaudeSonnet(DeepEvalBaseLLM):
    """A DeepEval LLM class that utilizes the Anthropic API to utilize Claude models"""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20240620"
    ):
        self.model = model
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def load_model(self):
        """Returns the current model selected"""
        return self.model

    def generate(
        self,
        prompt: str,
        schema: BaseModel,
        max_tokens: int = 1024,
    ) -> BaseModel:
        """Generates a response from the Anthropic API"""
        instructor_client = instructor.from_anthropic(self.client)
        response = instructor_client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_model=schema,
        )
        return response

    async def a_generate(
        self, prompt: str, schema: BaseModel, *args, **kwargs
    ) -> BaseModel:
        """Async implementation of the generate function"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, self.generate, prompt, schema, *args, **kwargs
        )

    def get_model_name(self):
        return f"Anthropic {self.model}"

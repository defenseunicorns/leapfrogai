import os

import openai
from pydantic import BaseModel
from deepeval.models.base_model import DeepEvalBaseLLM
import asyncio
from typing import Optional, List


class LFAI_Model(DeepEvalBaseLLM):
    """
    A DeepEval LLM class that utilizes the LeapfrogAI API to prompt certain benchmarks

    Do not use this particular class as an LLM judge.
    This model class is needed to run generation-focused benchmarks, not be used as a judge.
    Use Claude Sonnet or another larger model for LLM-as-judge evaluations
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.model = model or os.getenv("MODEL_TO_EVALUATE")
        self.api_key = api_key or os.getenv("LEAPFROGAI_API_KEY")
        self.base_url = base_url or os.getenv("LEAPFROGAI_API_URL")
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def load_model(self):
        """Returns the current model selected"""
        return self.model

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.75,
        top_p: float = 1.0,
        stop: str = "</s>",
    ) -> str:
        """Generates a response from LeapfrogAI API using the OpenAI SDK"""
        response = self.client.chat.completions.create(
            temperature=temperature,
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            top_p=top_p,
            stop=stop,
        )
        return response.choices[0].message.content

    def generate_samples(self, n: int, *args, **kwargs) -> List[str]:
        """Generates a list of n responses using the generate() function"""
        samples = [self.generate(*args, **kwargs) for ii in range(n)]
        return samples

    async def a_generate(self, prompt: str, *args, **kwargs) -> BaseModel:
        """Async implementation of the generate function"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.generate, prompt, *args, **kwargs)

    def get_model_name(self):
        return f"LeapfrogAI {self.model}"

from typing import List
import leapfrogai_sdk as lfai
from leapfrogai_api.backend.grpc_client import chat_completion
from leapfrogai_api.backend.helpers import grpc_chat_role
from leapfrogai_api.utils.config import Config
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)

logger = logging.getLogger(__name__)


def _create_rerank_prompt(query: str, documents: List[str]) -> str:
    # Create a prompt for reranking
    doc_list = "\n".join([f"{i+1}. {doc}..." for i, doc in enumerate(documents)])
    return f"Given the query: '{query}', rank the following documents in order of relevance. Return only the numbers of the documents in order of relevance, separated by commas.\n\n{doc_list}"


def _parse_rerank_response(response: str | None, documents: List[str]) -> List[int]:
    # Parse the response to get the reranked indices
    try:
        if response is None:
            return list(range(len(documents)))
        return [int(i.strip()) - 1 for i in response.split(",")]
    except ValueError:
        logger.info("Failed to parse the reranked documents")
        return list(range(len(documents)))  # Return original order if parsing fails


class Reranker:
    def __init__(
        self,
        model_config: Config,
        model: str = "llama-cpp-python",
        temperature: float = 0.2,
        max_tokens: int = 500,
    ):
        self.model_config = model_config
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def rerank(self, query: str, documents: List[str]) -> List[str]:
        prompt = _create_rerank_prompt(query, documents)

        chat_items = [lfai.ChatItem(role=grpc_chat_role("user"), content=prompt)]
        request = lfai.ChatCompletionRequest(
            chat_items=chat_items,
            max_new_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        model_backend = self.model_config.get_model_backend(self.model)
        if model_backend is None:
            raise ValueError(f"Model {self.model} not found in configuration")

        response = await chat_completion(model_backend, request)

        reranked_indices = _parse_rerank_response(
            str(response.choices[0].message.content_as_str()), documents
        )
        return [documents[i] for i in reranked_indices]

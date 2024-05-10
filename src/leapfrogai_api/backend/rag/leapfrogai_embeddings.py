"""LeapfrogAI Embeddings via Langchain Embeddings Interface."""

import os
from langchain_core.embeddings import Embeddings
import leapfrogai_sdk as lfai
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.backend.grpc_client import create_embeddings


class LeapfrogAIEmbeddings(Embeddings):
    """LeapfrogAI Embeddings via Langchain Embeddings Interface."""

    async def _get_embeddings(
        self,
        text: str,
        model_name: str = os.getenv("DEFAULT_EMBEDDINGS_MODEL"),
    ) -> list[float]:
        """Get embeddings from a model."""

        model = get_model_config().get_model_backend(model=model_name)
        if model is None:
            raise ValueError("Embeddings model not found.")

        request = lfai.EmbeddingRequest(inputs=text)

        response = await create_embeddings(model=model, request=request)

        return response.data[0].embedding

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        """Asynchronous Embed search docs."""

        list_of_embeddings = []
        for text in texts:
            embedding = await self._get_embeddings(text)
            list_of_embeddings.append(embedding)

        return list_of_embeddings

    async def aembed_query(self, text: str) -> list[float]:
        """Asynchronous Embed query text."""
        return await self._get_embeddings(text)

"""LeapfrogAI Embeddings via Langchain Embeddings Interface."""

import os
from langchain_core.embeddings import Embeddings
import leapfrogai_sdk as lfai
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.backend.grpc_client import create_embeddings


class LeapfrogAIEmbeddings(Embeddings):
    """LeapfrogAI Embeddings via Langchain Embeddings Interface."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        pass

    def embed_query(self, text: str) -> list[float]:
        pass

    async def _get_model(self, model_name: str = os.getenv("DEFAULT_EMBEDDINGS_MODEL")):
        model = get_model_config().get_model_backend(model=model_name)
        if model is None:
            raise ValueError("Embeddings model not found.")

        return model

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        """Asynchronous Embed search docs."""

        model = await self._get_model()
        list_of_embeddings = []
        request = lfai.EmbeddingRequest(inputs=texts)
        response = await create_embeddings(model=model, request=request)

        list_of_embeddings = [data.embedding for data in response.data]

        return list_of_embeddings

    async def aembed_query(self, text: str) -> list[float]:
        """Asynchronous Embed query text."""
        model = await self._get_model()

        request = lfai.EmbeddingRequest(inputs=text)
        response = await create_embeddings(model=model, request=request)

        return response.data[0].embedding

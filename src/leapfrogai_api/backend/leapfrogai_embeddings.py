"""LeapfrogAI Embeddings via Langchain Embeddings Interface."""

import os
from langchain_core.embeddings import Embeddings
import leapfrogai_sdk as lfai
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.backend.grpc_client import create_embeddings


class LeapfrogAIEmbeddings(Embeddings):
    """LeapfrogAI Embeddings via Langchain Embeddings Interface.

    This class provides methods to embed documents and query text using LeapfrogAI embeddings.
    """

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Not implemented yet."""
        # TODO: Implement this to meet Langchain Embeddings Interface.
        raise NotImplementedError("embed_documents has not been implemented yet.")

    def embed_query(self, text: str) -> list[float]:
        """Not implemented yet."""
        # TODO: Implement this to meet Langchain Embeddings Interface.
        raise NotImplementedError("embed_query has not been implemented yet.")

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        """Asynchronously embeds a list of documents.

        Args:
            texts (list[str]): The list of documents to be embedded.

        Returns:
            list[list[float]]: The list of embedding vectors for each document.
        """
        model = await self._get_model()
        list_of_embeddings = []
        request = lfai.EmbeddingRequest(inputs=texts)
        response = await create_embeddings(model=model, request=request)

        list_of_embeddings = [data.embedding for data in response.data]

        return list_of_embeddings

    async def aembed_query(self, text: str) -> list[float]:
        """Asynchronously embeds a query text.

        Args:
            text (str): The query text to be embedded.

        Returns:
            list[float]: The embedding vector for the query text.
        """
        model = await self._get_model()

        request = lfai.EmbeddingRequest(inputs=text)
        response = await create_embeddings(model=model, request=request)

        return response.data[0].embedding

    async def _get_model(self, model_name: str = os.getenv("DEFAULT_EMBEDDINGS_MODEL")):
        """Gets the embeddings model.

        Args:
            model_name (str, optional): The name of the embeddings model. Defaults to the value of DEFAULT_EMBEDDINGS_MODEL environment variable.

        Returns:
            model: The embeddings model.

        Raises:
            ValueError: If the embeddings model is not found.
        """
        model = get_model_config().get_model_backend(model=model_name)
        if model is None:
            raise ValueError("Embeddings model not found.")

        return model

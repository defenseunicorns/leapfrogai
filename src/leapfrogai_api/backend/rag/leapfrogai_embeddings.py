"""LeapfrogAI Embeddings via Langchain Embeddings Interface."""

import os
import leapfrogai_sdk as lfai
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.backend.grpc_client import create_embeddings


# Partially implements the Langchain Core Embeddings interface
class LeapfrogAIEmbeddings:
    """LeapfrogAI Embeddings via Langchain Embeddings Interface.

    This class provides methods to embed documents and query text using LeapfrogAI embeddings.
    """

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        """Asynchronously embeds a list of documents.

        Args:
            texts (list[str]): The list of documents to be embedded.

        Returns:
            list[list[float]]: The list of embedding vectors for each document.
        """
        model = await self._get_model()
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

        list_of_embeddings = await self.aembed_documents([text])

        return list_of_embeddings[0]

    async def _get_model(self, model_name: str = os.getenv("DEFAULT_EMBEDDINGS_MODEL")):
        """Gets the embeddings model.

        Args:
            model_name (str, optional): The name of the embeddings model. Defaults to the value of DEFAULT_EMBEDDINGS_MODEL environment variable.

        Returns:
            model: The embeddings model.

        Raises:
            ValueError: If the embeddings model is not found.
        """

        if not (model := get_model_config().get_model_backend(model=model_name)):
            raise ValueError("Embeddings model not found.")

        return model

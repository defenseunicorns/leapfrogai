"""This module contains the AsyncSupabaseVectorStore class."""

from typing import Any, Iterable, List
from supabase_py_async import AsyncClient
from langchain_core.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document


class AsyncSupabaseVectorStore(VectorStore):
    """An async vector store that uses Supabase as the backend."""

    # TODO: Implement async Supabase Vector Store
    # Sync Example: https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/vectorstores/supabase.py
    # Base: https://github.com/langchain-ai/langchain/blob/master/libs/core/langchain_core/vectorstores.py#L59

    def __init__(
        self,
        client: AsyncClient,
        # TODO: Implement Async Embeddings for LFAI similar to:
        # https://github.com/langchain-ai/langchain/blob/9992beaff9205825993ca65f589e9661bcadd939/libs/community/langchain_community/embeddings/openai.py#L670
        embeddings: Embeddings,
        table_name: str,
        chunk_size: int = 500,
        query_name: str = "match_vectors",
    ) -> None:
        """Initializes the AsyncSupabaseVectorStore."""
        self.client = client
        self.embeddings = embeddings
        self.table_name = table_name
        self.chunk_size = chunk_size
        self.query_name = query_name

    async def aadd_texts(
        self, texts: Iterable[str], metadatas: List[dict] | None = None, **kwargs: Any
    ) -> List[str]:
        """Adds texts to the store."""
        raise NotImplementedError("add_texts is not implemented.")

    async def aadd_documents(
        self, documents: List[Document], **kwargs: Any
    ) -> List[str]:
        """Adds documents to the store."""
        raise NotImplementedError("add_documents is not implemented.")

    async def aadd_vectors(
        self,
        vectors: Iterable[List[float]],
        documents: list[Document],
    ) -> List[str]:
        """Adds vectors to the store."""
        raise NotImplementedError("add_vectors is not implemented.")

    async def asimilarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> list[Document]:
        """Searches for similar documents."""
        # TODO: RPC something like this:
        # self.client.rpc("match_vectors", {"query": query, "k": k})

        raise NotImplementedError("similarity_search is not implemented.")

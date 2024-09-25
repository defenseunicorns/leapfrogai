"""Service for querying the RAG model."""

from typing import Annotated, List
from fastapi import Depends
from supabase import AClient as AsyncClient
from langchain_core.embeddings import Embeddings
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings
from leapfrogai_api.backend.rag.reranker import Reranker
from leapfrogai_api.data.crud_vector_content import CRUDVectorContent
from leapfrogai_api.typedef.rag.rag_types import Configuration
from leapfrogai_api.typedef.vectorstores.search_types import SearchResponse, SearchItem
from leapfrogai_api.backend.constants import TOP_K
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.utils.config import Config
from leapfrogai_api.utils.logging_tools import logger

# Allows for overwriting type of embeddings that will be instantiated
embeddings_type: type[Embeddings] | type[LeapfrogAIEmbeddings] | None = (
    LeapfrogAIEmbeddings
)


class QueryService:
    """Service for querying the RAG model."""

    def __init__(self, db: AsyncClient) -> None:
        """Initializes the QueryService."""
        self.db = db
        self.embeddings = embeddings_type()

    async def query_rag(
        self,
        model_config: Annotated[Config, Depends(get_model_config)],
        query: str,
        vector_store_id: str,
        k: int = TOP_K,
    ) -> SearchResponse:
        """
        Query the Vector Store.

        Args:
            model_config (Config): The current model configuration.
            query (str): The input query string.
            vector_store_id (str): The ID of the vector store.
            k (int, optional): The number of results to retrieve.

        Returns:
            SearchResponse: The search response from the vector store.
        """

        logger.info("Beginning RAG query...")

        # 1. Embed query
        vector = await self.embeddings.aembed_query(query)

        # 2. Perform similarity search
        crud_vector_content = CRUDVectorContent(db=self.db)
        results = await crud_vector_content.similarity_search(
            query=vector, vector_store_id=vector_store_id, k=k
        )

        # 3. Rerank results
        if Configuration.enable_reranking:
            reranker = Reranker(model_config=model_config)
            reranked_results: list[str] = await reranker.rerank(
                query, [result.content for result in results.data]
            )
            results = rerank_search_response(results, reranked_results)
            logger.info(f"Reranking complete {results.get_simple_response()}")

        logger.info("Ending RAG query...")

        return results


def rerank_search_response(
    original_response: SearchResponse, reranked_results: List[str]
) -> SearchResponse:
    """
    Reorder the SearchResponse based on reranked results.

    Args:
        original_response (SearchResponse): The original search response.
        reranked_results (List[str]): List of reranked content strings.

    Returns:
        SearchResponse: A new SearchResponse with reordered items.
    """
    # Create a mapping of content to original SearchItem
    content_to_item = {item.content: item for item in original_response.data}

    # Create new SearchItems based on reranked results
    reranked_items = []
    for idx, content in enumerate(reranked_results):
        if content in content_to_item:
            item: SearchItem = content_to_item[content]
            # Update the similarity to maintain the new order
            item.similarity = 1.0 - ((1.0 / len(reranked_results)) * idx)
            reranked_items.append(item)

    reranked_response = SearchResponse(data=reranked_items)

    logger.info(
        f"Original documents: {original_response.get_simple_response()}\nReranked documents {reranked_response.get_simple_response()}"
    )

    # Create a new SearchResponse with reranked items
    return reranked_response

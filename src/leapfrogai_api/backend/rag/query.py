"""Service for querying the RAG model."""

from typing import Annotated
from fastapi import Depends
from rerankers.results import RankedResults
from supabase import AClient as AsyncClient
from langchain_core.embeddings import Embeddings
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings
from leapfrogai_api.data.crud_vector_content import CRUDVectorContent
from leapfrogai_api.typedef.rag.rag_types import Configuration
from leapfrogai_api.typedef.vectorstores.search_types import SearchResponse, SearchItem
from leapfrogai_api.backend.constants import TOP_K
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.utils.config import Config
from leapfrogai_api.utils.logging_tools import logger
from rerankers import Reranker

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
            ranker = Reranker(Configuration.ranking_model)
            ranked_results: RankedResults = ranker.rank(
                query=query,
                docs=[result.content for result in results.data],
                doc_ids=[result.id for result in results.data],
            )
            results = rerank_search_response(results, ranked_results)
            logger.info(f"Reranking complete {results.get_simple_response()}")

        logger.info("Ending RAG query...")

        return results


def rerank_search_response(
    original_response: SearchResponse, ranked_results: RankedResults
) -> SearchResponse:
    """
    Reorder the SearchResponse based on reranked results.

    Args:
        original_response (SearchResponse): The original search response.
        ranked_results (List[str]): List of ranked content strings.

    Returns:
        SearchResponse: A new SearchResponse with reordered items.
    """
    # Create a mapping of id to original SearchItem
    content_to_item = {item.id: item for item in original_response.data}

    # Create new SearchItems based on reranked results
    reranked_items = []
    for content in ranked_results.results:
        if content.document.doc_id in content_to_item:
            item: SearchItem = content_to_item[content.document.doc_id]
            # TODO: Find a better way to handle this
            # Update the similarity to instead be the rank
            item.rank = content.rank
            item.score = content.score
            reranked_items.append(item)

    reranked_response = SearchResponse(data=reranked_items)

    logger.info(
        f"Original documents: {original_response.get_simple_response()}\nReranked documents {reranked_response.get_simple_response()}"
    )

    # Create a new SearchResponse with reranked items
    return reranked_response

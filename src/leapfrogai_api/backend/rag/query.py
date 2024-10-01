"""Service for querying the RAG model."""

from rerankers.results import RankedResults
from supabase import AClient as AsyncClient
from langchain_core.embeddings import Embeddings
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings
from leapfrogai_api.data.crud_vector_content import CRUDVectorContent
from leapfrogai_api.typedef.rag.rag_types import ConfigurationSingleton
from leapfrogai_api.typedef.vectorstores.search_types import SearchResponse, SearchItem
from leapfrogai_api.backend.constants import TOP_K
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
        query: str,
        vector_store_id: str,
        k: int = TOP_K,
    ) -> SearchResponse:
        """
        Query the Vector Store.

        Args:
            query (str): The input query string.
            vector_store_id (str): The ID of the vector store.
            k (int, optional): The number of results to retrieve.

        Returns:
            SearchResponse: The search response from the vector store.
        """

        logger.debug("Beginning RAG query...")

        # 1. Embed query
        vector = await self.embeddings.aembed_query(query)

        # 2. Perform similarity search
        _k: int = k
        if ConfigurationSingleton.get_instance().enable_reranking:
            """Use the user specified top-k value unless reranking.
            When reranking, use the reranking top-k value to get the initial results.
            Then filter the list down later to just the k that the user has requested after reranking."""
            _k = ConfigurationSingleton.get_instance().rag_top_k_when_reranking

        crud_vector_content = CRUDVectorContent(db=self.db)
        results = await crud_vector_content.similarity_search(
            query=vector, vector_store_id=vector_store_id, k=_k
        )

        # 3. Rerank results
        if (
            ConfigurationSingleton.get_instance().enable_reranking
            and len(results.data) > 0
        ):
            ranker = Reranker(ConfigurationSingleton.get_instance().ranking_model)
            ranked_results: RankedResults = ranker.rank(
                query=query,
                docs=[result.content for result in results.data],
                doc_ids=[result.id for result in results.data],
            )
            results = rerank_search_response(results, ranked_results)
            # Narrow down the results to the top-k value specified by the user
            results.data = results.data[0:k]

        logger.debug("Ending RAG query...")

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
    ranked_items = []
    for content in ranked_results.results:
        if content.document.doc_id in content_to_item:
            item: SearchItem = content_to_item[content.document.doc_id]
            item.rank = content.rank
            item.score = content.score
            ranked_items.append(item)

    ranked_response = SearchResponse(data=ranked_items)

    # Create a new SearchResponse with reranked items
    return ranked_response

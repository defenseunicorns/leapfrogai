from pydantic import BaseModel


class Configuration(BaseModel):
    """Configuration for RAG."""

    enable_reranking: bool = False

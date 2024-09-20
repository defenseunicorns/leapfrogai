from pydantic import BaseModel, Field


class Configuration(BaseModel):
    """Configuration for RAG."""

    enable_reranking: bool = Field(
        default=False,
        description="Whether to enable reranking",
    )

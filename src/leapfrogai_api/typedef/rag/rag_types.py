from typing import ClassVar

from pydantic import BaseModel


class Configuration(BaseModel):
    """Configuration for RAG."""

    enable_reranking: ClassVar[bool] = False


class ConfigurationResponse(BaseModel):
    """Response for RAG configuration."""

    enable_reranking: bool

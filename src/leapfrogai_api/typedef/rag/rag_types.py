from typing import ClassVar

from pydantic import BaseModel, Field


class Configuration(BaseModel):
    """Configuration for RAG."""

    # This is a class variable, shared by all instances of Configuration
    # It sets a default value, but doesn't create an instance variable
    enable_reranking: ClassVar[bool] = False
    # More model info can be found here:
    # https://github.com/AnswerDotAI/rerankers?tab=readme-ov-file
    # https://pypi.org/project/rerankers/
    ranking_model: ClassVar[str] = "flashrank"

    # Note: Pydantic will not create an instance variable for ClassVar fields
    # If you need an instance variable, you should declare it separately


class ConfigurationPayload(BaseModel):
    """Response for RAG configuration."""

    # Singleton instance of this class
    instance: ClassVar[any] = None

    # This is an instance variable, specific to each ConfigurationPayload object
    # It will be included in the JSON output when the model is serialized
    enable_reranking: bool = Field(
        default=False, description="Enables reranking for RAG queries"
    )
    # More model info can be found here:
    # https://github.com/AnswerDotAI/rerankers?tab=readme-ov-file
    # https://pypi.org/project/rerankers/
    ranking_model: str = Field(
        default="flashrank",
        description="What model to use for reranking",
        examples=["flashrank", "rankllm", "cross-encoder", "colbert"],
    )

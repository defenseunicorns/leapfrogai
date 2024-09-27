from typing import Optional

from pydantic import BaseModel, Field


class ConfigurationSingleton:
    """Singleton manager for ConfigurationPayload."""

    _instance = None

    @classmethod
    def get_instance(cls, **kwargs):
        if cls._instance is None:
            cls._instance = ConfigurationPayload(**kwargs)
        return cls._instance


class ConfigurationPayload(BaseModel):
    """Response for RAG configuration."""

    enable_reranking: Optional[bool] = Field(
        default=None,
        examples=[True, False],
        description="Enables reranking for RAG queries",
    )
    # More model info can be found here:
    # https://github.com/AnswerDotAI/rerankers?tab=readme-ov-file
    # https://pypi.org/project/rerankers/
    ranking_model: Optional[str] = Field(
        default=None,
        description="What model to use for reranking. Some options may require additional python dependencies.",
        examples=["flashrank", "rankllm", "cross-encoder", "colbert"],
    )
    rag_top_k_when_reranking: Optional[int] = Field(
        default=None,
        description="The top-k results returned from the RAG call before reranking",
    )

    def update_instance(self, configuration: BaseModel):
        for key, value in configuration.model_dump().items():
            if value is not None:
                setattr(self, key, value)

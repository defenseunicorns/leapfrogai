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

    enable_reranking: bool = Field(
        default=True, description="Enables reranking for RAG queries"
    )
    # More model info can be found here:
    # https://github.com/AnswerDotAI/rerankers?tab=readme-ov-file
    # https://pypi.org/project/rerankers/
    ranking_model: str = Field(
        default="flashrank",
        description="What model to use for reranking. Some options may require additional python dependencies.",
        examples=["flashrank", "rankllm", "cross-encoder", "colbert"],
    )
    rag_top_k_when_reranking: int = Field(
        default=100,
        description="The top-k results returned from the RAG call before reranking",
    )

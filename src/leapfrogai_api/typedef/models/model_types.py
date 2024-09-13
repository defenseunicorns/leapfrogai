from typing import List, Literal
from pydantic import BaseModel, Field


class Model:
    name: str
    backend: str

    def __init__(self, name: str, backend: str, capabilities: List[str] | None = None):
        self.name = name
        self.backend = backend


class ModelResponseModel(BaseModel):
    """Represents a single model in the response."""

    id: str = Field(
        ...,
        description="The unique identifier of the model.",
        examples=["llama-cpp-python"],
    )
    object: Literal["model"] = Field(
        default="model",
        description="The object type, which is always 'model' for this response.",
    )
    created: int = Field(
        default=0,
        description="The Unix timestamp (in seconds) when the model was created. Always 0 for LeapfrogAI models.",
        examples=[0],
    )
    owned_by: Literal["leapfrogai"] = Field(
        default="leapfrogai",
        description="The organization that owns the model. Always 'leapfrogai' for LeapfrogAI models.",
    )


class ModelResponse(BaseModel):
    """Response object for listing available models."""

    object: Literal["list"] = Field(
        default="list",
        description="The object type, which is always 'list' for this response.",
    )
    data: list[ModelResponseModel] = Field(
        ..., description="A list of available models.", min_length=0
    )

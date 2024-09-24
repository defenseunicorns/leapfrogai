from typing import ClassVar

from pydantic import BaseModel


class Configuration(BaseModel):
    """Configuration for RAG."""

    # This is a class variable, shared by all instances of Configuration
    # It sets a default value, but doesn't create an instance variable
    enable_reranking: ClassVar[bool] = False

    # Note: Pydantic will not create an instance variable for ClassVar fields
    # If you need an instance variable, you should declare it separately


class ConfigurationResponse(BaseModel):
    """Response for RAG configuration."""

    # This is an instance variable, specific to each ConfigurationResponse object
    # It will be included in the JSON output when the model is serialized
    enable_reranking: bool


# The separation of Configuration and ConfigurationResponse allows for
# different behavior in input (Configuration) vs output (ConfigurationResponse)

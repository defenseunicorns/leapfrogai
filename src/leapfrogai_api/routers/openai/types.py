"""Typing definitions for assistants API."""

from __future__ import annotations
from typing import Dict, Optional, Literal
from pydantic import BaseModel
from fastapi import UploadFile, Form, File
from openai.types import CompletionUsage as Usage

##########
# MODELS
##########


class ModelResponseModel(BaseModel):
    """Model object for model response."""

    id: str
    object: str = "model"
    created: int = 0
    owned_by: str = "leapfrogai"


class ModelResponse(BaseModel):
    """Response object for models."""

    object: str = "list"
    data: list[ModelResponseModel] = []


############
# COMPLETION
############


class CompletionRequest(BaseModel):
    """Request object for completion."""

    model: str
    prompt: str | list[int]
    stream: bool | None = False
    max_tokens: int | None = 16
    temperature: float | None = 1.0


class CompletionChoice(BaseModel):
    """Choice object for completion."""

    index: int
    text: str
    logprobs: object = None
    finish_reason: str = ""


class CompletionResponse(BaseModel):
    """Response object for completion."""

    id: str = ""
    object: str = "completion"
    created: int = 0
    model: str = ""
    choices: list[CompletionChoice]
    usage: Usage | None = None


##########
# CHAT
##########


class ChatFunction(BaseModel):
    """Function object for chat completion."""

    name: str
    parameters: Dict[str, object]
    description: str


class ChatMessage(BaseModel):
    """Message object for chat completion."""

    role: str
    content: str


class ChatDelta(BaseModel):
    """Delta object for chat completion."""

    role: str
    content: str | None = ""


class ChatCompletionRequest(BaseModel):
    """Request object for chat completion."""

    model: str
    messages: list[ChatMessage]
    functions: list | None = None
    temperature: float | None = 1.0
    top_p: float | None = 1
    stream: bool | None = False
    stop: str | None = None
    max_tokens: int | None = 128


class ChatChoice(BaseModel):
    """Choice object for chat completion."""

    index: int
    message: ChatMessage
    finish_reason: str | None = ""


class ChatStreamChoice(BaseModel):
    """Stream choice object for chat completion."""

    index: int
    delta: ChatDelta
    finish_reason: str | None = ""


class ChatCompletionResponse(BaseModel):
    """Response object for chat completion."""

    id: str = ""
    object: str = "chat.completion"
    created: int = 0
    model: str = ""
    choices: list[ChatChoice] | list[ChatStreamChoice]
    usage: Usage | None = None


#############
# EMBEDDINGS
#############


class CreateEmbeddingRequest(BaseModel):
    """Request object for creating embeddings."""

    model: str
    input: str | list[str] | list[int] | list[list[int]]
    user: str | None = None


class EmbeddingResponseData(BaseModel):
    """Response object for embeddings."""

    embedding: list[float]
    index: int
    object: str = "embedding"


class CreateEmbeddingResponse(BaseModel):
    """Response object for embeddings."""

    data: list[EmbeddingResponseData]
    model: str
    object: str = "list"
    usage: Usage | None = None


##########
# AUDIO
##########


class CreateTranscriptionRequest(BaseModel):
    file: UploadFile
    model: str
    language: str = ""
    prompt: str = ""
    response_format: str = ""
    temperature: float = 1

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        model: str = Form(...),
        language: Optional[str] = Form(""),
        prompt: Optional[str] = Form(""),
        response_format: Optional[str] = Form(""),
        temperature: Optional[float] = Form(1),
    ) -> CreateTranscriptionRequest:
        return cls(
            file=file,
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
        )


class CreateTranscriptionResponse(BaseModel):
    text: str


#############
# FILES
#############


class UploadFileRequest(BaseModel):
    """Request object for uploading a file."""

    file: UploadFile
    purpose: Literal["assistants"] | None = "assistants"

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        purpose: Optional[str] = Form("assistants"),
    ) -> UploadFileRequest:
        """Create an instance of the class from form data."""
        return cls(file=file, purpose=purpose)


#############
# ASSISTANTS
#############


class CreateAssistantRequest(BaseModel):
    """Request object for creating an assistant."""

    model: str = "mistral"
    name: Optional[str] = "Froggy Assistant"
    description: Optional[str] = "A helpful assistant."
    instructions: Optional[str] = "You are a helpful assistant."
    tools: Optional[list[dict[Literal["type"], Literal["file_search"]]]] | None = [
        {"type": "file_search"}
    ]  # This is all we support right now
    tool_resources: Optional[object] | None = {}
    metadata: Optional[object] | None = {}
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    response_format: Optional[Literal["auto"]] | None = (
        "auto"  # This is all we support right now
    )


class ModifyAssistantRequest(CreateAssistantRequest):
    """Request object for modifying an assistant."""

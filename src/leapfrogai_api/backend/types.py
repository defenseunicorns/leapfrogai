"""Typing definitions for assistants API."""

from __future__ import annotations
from typing import Literal
from pydantic import BaseModel
from fastapi import UploadFile, Form, File
from openai.types.beta.vector_store import ExpiresAfter
from openai.types import FileObject
from openai.types.beta import VectorStore
from openai.types.beta import Assistant, AssistantTool
from openai.types.beta.assistant import ToolResources

##########
# GENERIC
##########


class Usage(BaseModel):
    """Usage object."""

    prompt_tokens: int
    completion_tokens: int | None = None
    total_tokens: int


##########
# MODELS
##########


class ModelResponseModel(BaseModel):
    """Response object for models."""

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
    parameters: dict[str, object]
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
    temperature: float = 1.0

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        model: str = Form(...),
        language: str | None = Form(""),
        prompt: str | None = Form(""),
        response_format: str | None = Form(""),
        temperature: float | None = Form(1.0),
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
        purpose: str | None = Form("assistants"),
    ) -> UploadFileRequest:
        """Create an instance of the class from form data."""
        return cls(file=file, purpose=purpose)


class ListFilesResponse(BaseModel):
    """Response object for listing files."""

    object: str = Literal["list"]
    data: list[FileObject] = []


#############
# ASSISTANTS
#############


class CreateAssistantRequest(BaseModel):
    """Request object for creating an assistant."""

    model: str = "mistral"
    name: str | None = "Froggy Assistant"
    description: str | None = "A helpful assistant."
    instructions: str | None = "You are a helpful assistant."
    tools: list[AssistantTool] | None = []  # This is all we support right now
    tool_resources: ToolResources | None = ToolResources()
    metadata: object | None = {}
    temperature: float | None = 1.0
    top_p: float | None = 1.0
    response_format: Literal["auto"] | None = "auto"  # This is all we support right now


class ModifyAssistantRequest(CreateAssistantRequest):
    """Request object for modifying an assistant."""


class ListAssistantsResponse(BaseModel):
    """Response object for listing files."""

    object: str = Literal["list"]
    data: list[Assistant] = []


################
# VECTOR STORES
################


class CreateVectorStoreRequest(BaseModel):
    """Request object for creating a vector store."""

    file_ids: list[str] | None = []
    name: str | None = None
    expires_after: ExpiresAfter | None = ExpiresAfter(anchor="last_active_at", days=0)
    metadata: dict | None = {}


class ModifyVectorStoreRequest(CreateVectorStoreRequest):
    """Request object for modifying a vector store."""


class ListVectorStoresResponse(BaseModel):
    """Response object for listing files."""

    object: str = Literal["list"]
    data: list[VectorStore] = []


################
# LEAPFROGAI RAG
################


class RAGItem(BaseModel):
    """Object for RAG."""

    id: str
    vector_store_id: str
    file_id: str
    content: str
    metadata: dict
    similarity: float


class RAGResponse(BaseModel):
    """Response object for RAG."""

    data: list[RAGItem] = []

"""Typing definitions for assistants API."""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field
from fastapi import UploadFile, Form, File
from openai.types.beta.vector_store import ExpiresAfter
from openai.types import FileObject
from openai.types.beta import VectorStore
from openai.types.beta import Assistant, AssistantTool
from openai.types.beta.threads import Message, MessageContent, TextContentBlock, Text
from openai.types.beta.threads.message import Attachment
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

    model: str = Field(
        description="Model that will be doing the embedding",
        examples=["text-embeddings"],
    )
    input: str | list[str] | list[int] | list[list[int]] = Field(
        description="The text to be embedded", examples=["My test input"]
    )


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
    metadata: dict | None = Field(default=None, examples=[{}])
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


class VectorStoreFileStatus(Enum):
    """Enum for the status of a vector store file."""

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class VectorStoreStatus(Enum):
    """Enum for the status of a vector store."""

    EXPIRED = "expired"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class CreateVectorStoreRequest(BaseModel):
    """Request object for creating a vector store."""

    file_ids: list[str] | None = []
    name: str | None = None
    expires_after: ExpiresAfter | None = Field(
        default=None, examples=[ExpiresAfter(anchor="last_active_at", days=1)]
    )
    metadata: dict | None = Field(default=None, examples=[{}])

    def add_days_to_timestamp(self, timestamp: int, days: int) -> int:
        """
        Adds a specified number of days to a timestamp. Used to when updating the VectorStore.

        Args:
            timestamp(int): An integer representing a timestamp.
            days(int): The number of days to add.

        Returns:
            An integer representing the new timestamp with the added days.
        """

        # Convert the timestamp to a datetime object
        datetime_obj = datetime.datetime.fromtimestamp(timestamp)

        # Add the specified number of days
        new_datetime_obj = datetime_obj + datetime.timedelta(days=days)

        # Convert the new datetime object back to a timestamp
        new_timestamp = new_datetime_obj.timestamp()

        return int(new_timestamp)

    def get_expiry(self, last_active_at: int) -> tuple[ExpiresAfter | None, int | None]:
        """
        Return expiration details based on the provided last_active_at unix timestamp

        Args:
            last_active_at(int): An integer representing a timestamp when the vector store was last active.

        Returns:
            A tuple of when the vector store should expire and the timestamp of the expiry date.
        """
        if isinstance(self.expires_after, ExpiresAfter):
            return self.expires_after, self.add_days_to_timestamp(
                last_active_at, self.expires_after.days
            )

        return None, None  # Will not expire


class ModifyVectorStoreRequest(CreateVectorStoreRequest):
    """Request object for modifying a vector store."""


class ListVectorStoresResponse(BaseModel):
    """Response object for listing files."""

    object: str = Literal["list"]
    data: list[VectorStore] = []


################
# THREADS, RUNS, MESSAGES
################


class CreateThreadRequest(BaseModel):
    """Request object for creating a thread."""

    messages: list[Message] | None = Field(default=None, examples=[None])
    tool_resources: ToolResources | None = Field(default=None, examples=[None])
    metadata: dict | None = Field(default=None, examples=[{}])


class ModifyThreadRequest(BaseModel):
    """Request object for modifying a thread."""

    tool_resources: ToolResources | None = Field(default=None, examples=[None])
    metadata: dict | None = Field(default=None, examples=[{}])


class CreateMessageRequest(BaseModel):
    """Request object for creating a message."""

    role: Literal["user", "assistant"] = Field(default="user")
    content: list[MessageContent] = Field(
        default=[TextContentBlock(text=Text(value="", annotations=[]), type="text")],
        examples=[[TextContentBlock(text=Text(value="", annotations=[]), type="text")]],
    )
    attachments: list[Attachment] | None = Field(default=None, examples=[None])
    metadata: dict | None = Field(default=None, examples=[{}])


class ModifyMessageRequest(BaseModel):
    """Request object for modifying a message."""

    metadata: dict | None = Field(default=None, examples=[{}])


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

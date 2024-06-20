"""Typing definitions for assistants API."""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Literal

from fastapi import UploadFile, Form, File
from openai.types import FileObject
from openai.types.beta import Assistant, AssistantTool
from openai.types.beta import VectorStore
from openai.types.beta.assistant import (
    ToolResources as BetaAssistantToolResources,
    ToolResourcesFileSearch,
)
from openai.types.beta.assistant_tool import FileSearchTool
from openai.types.beta.thread import ToolResources as BetaThreadToolResources
from openai.types.beta.thread_create_params import (
    ToolResourcesFileSearchVectorStoreChunkingStrategy,
    ToolResourcesFileSearchVectorStoreChunkingStrategyAuto,
)
from openai.types.beta.threads.text_content_block_param import TextContentBlockParam
from openai.types.beta.vector_store import ExpiresAfter
from pydantic import BaseModel, Field


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

    role: Literal["user", "assistant", "system", "function"] = Field(
        default="user",
        description="The role of the message author.",
        examples=["user"]
    )
    content: str | list[TextContentBlockParam] = Field(
        default="",
        description="The content of the message. Can be a string or a list of text content blocks.",
        examples=["Hello, how are you?"]
    )


class ChatDelta(BaseModel):
    """Delta object for chat completion."""

    role: str = Field(
        default="",
        description="The role of the author of this message delta.",
        examples=["assistant"]
    )
    content: str | None = Field(
        default="",
        description="The content of this message delta."
    )


class ChatCompletionRequest(BaseModel):
    """Request object for chat completion."""

    model: str = Field(
        default="",
        description="The ID of the model to use for chat completion.",
        examples=["llama-cpp-python"]
    )
    messages: list[ChatMessage] = Field(
        default=[],
        description="A list of messages comprising the conversation so far."
    )
    functions: list | None = Field(
        default=None,
        description="A list of functions that the model may generate JSON inputs for."
    )
    temperature: float | None = Field(
        default=1.0,
        description="What sampling temperature to use, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.",
        ge=0,
        le=2
    )
    top_p: float | None = Field(
        default=1,
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
        gt=0,
        le=1
    )
    stream: bool | None = Field(
        default=False,
        description="If set, partial message deltas will be sent. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message."
    )
    stop: str | None = Field(
        default=None,
        description="Sequences that determine where the API will stop generating further tokens."
    )
    max_tokens: int | None = Field(
        default=128,
        description="The maximum number of tokens to generate in the chat completion.",
        gt=0
    )


class ChatChoice(BaseModel):
    """Choice object for chat completion."""

    index: int = Field(
        default=0,
        description="The index of this choice among the list of choices."
    )
    message: ChatMessage = Field(
        default=ChatMessage(),
        description="The message content for this choice."
    )
    finish_reason: str | None = Field(
        default="",
        description="The reason why the model stopped generating tokens.",
        examples=["stop", "length"]
    )


class ChatStreamChoice(BaseModel):
    """Stream choice object for chat completion."""

    index: int = Field(
        default=0,
        description="The index of this choice among the list of choices."
    )
    delta: ChatDelta = Field(
        default=ChatDelta(),
        description="The delta content for this streaming choice."
    )
    finish_reason: str | None = Field(
        default="",
        description="The reason why the model stopped generating tokens.",
        examples=["stop", "length"]
    )


class ChatCompletionResponse(BaseModel):
    """Response object for chat completion."""

    id: str = Field(
        default="",
        description="A unique identifier for the chat completion."
    )
    object: str = Field(
        default="chat.completion",
        description="The object type, which is always 'chat.completion' for this response."
    )
    created: int = Field(
        default=0,
        description="The Unix timestamp (in seconds) of when the chat completion was created."
    )
    model: str = Field(
        default="",
        description="The ID of the model used for the chat completion."
    )
    choices: list[ChatChoice] | list[ChatStreamChoice] = Field(
        default=[],
        description="A list of chat completion choices. Can be either ChatChoice or ChatStreamChoice depending on whether streaming is enabled."
    )
    usage: Usage | None = Field(
        default=None,
        description="Usage statistics for the completion request."
    )


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
    """Request object for creating a transcription."""

    file: UploadFile = Field(
        ...,
        description="The audio file to transcribe. Supports any audio format that ffmpeg can handle. For a complete list of supported formats, see: https://ffmpeg.org/ffmpeg-formats.html"
    )
    model: str = Field(
        ...,
        description="ID of the model to use."
    )
    language: str = Field(
        default="",
        description="The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency."
    )
    prompt: str = Field(
        default="",
        description="An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language."
    )
    response_format: str = Field(
        default="json",
        description="The format of the transcript output, in one of these options: json, text, srt, verbose_json, or vtt.",
    )
    temperature: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description="The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit."
    )

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        model: str = Form(...),
        language: str | None = Form(""),
        prompt: str | None = Form(""),
        response_format: str | None = Form("json"),
        temperature: float | None = Form(1.0),
    ) -> "CreateTranscriptionRequest":
        return cls(
            file=file,
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
        )


class CreateTranscriptionResponse(BaseModel):
    """Response object for transcription."""

    text: str = Field(
        ...,
        description="The transcribed text.",
        examples=["Hello, this is a transcription of the audio file."]
    )


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

    model: str = Field(
        default="llama-cpp-python",
        examples=["llama-cpp-python"],
        description="The model to be used by the assistant. Default is 'llama-cpp-python'."
    )
    name: str | None = Field(
        default=None,
        examples=["Froggy Assistant"],
        description="The name of the assistant. Optional."
    )
    description: str | None = Field(
        default=None,
        examples=["A helpful assistant."],
        description="A description of the assistant's purpose. Optional."
    )
    instructions: str | None = Field(
        default=None,
        examples=["You are a helpful assistant."],
        description="Instructions that the assistant should follow. Optional."
    )
    tools: list[AssistantTool] | None = Field(
        default=None,
        examples=[[FileSearchTool(type="file_search")]],
        description="List of tools the assistant can use. Optional."
    )
    tool_resources: BetaAssistantToolResources | None = Field(
        default=None,
        examples=[
            BetaAssistantToolResources(
                file_search=ToolResourcesFileSearch(vector_store_ids=[])
            )
        ],
        description="Resources for the tools used by the assistant. Optional."
    )
    metadata: dict | None = Field(
        default={},
        examples=[{}],
        description="Additional metadata for the assistant. Optional."
    )
    temperature: float | None = Field(
        default=None,
        examples=[1.0],
        description="Sampling temperature for the model. Optional."
    )
    top_p: float | None = Field(
        default=None,
        examples=[1.0],
        description="Nucleus sampling parameter. Optional."
    )
    response_format: Literal["auto"] | None = Field(
        default=None,
        examples=["auto"],
        description="The format of the assistant's responses. Currently only 'auto' is supported. Optional."
    )


class ModifyAssistantRequest(CreateAssistantRequest):
    """Request object for modifying an assistant."""
    # Inherits all fields from CreateAssistantRequest
    # All fields are optional for modification


class ListAssistantsResponse(BaseModel):
    """Response object for listing assistants."""

    object: str = Field(
        default="list",
        const=True,
        description="The type of object. Always 'list' for this response."
    )
    data: list[Assistant] = Field(
        description="A list of Assistant objects."
    )


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


class CreateVectorStoreFileRequest(BaseModel):
    """Request object for creating a vector store file."""

    chunking_strategy: ToolResourcesFileSearchVectorStoreChunkingStrategy | None = (
        Field(
            default=None,
            examples=[
                ToolResourcesFileSearchVectorStoreChunkingStrategyAuto(type="auto")
            ],
        )
    )

    file_id: str = Field(default="", examples=[""])


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


class ModifyRunRequest(BaseModel):
    """Request object for modifying a run."""

    metadata: dict[str, str] | None = Field(default=None, examples=[{}])


class ModifyThreadRequest(BaseModel):
    """Request object for modifying a thread."""

    tool_resources: BetaThreadToolResources | None = Field(
        default=None, examples=[None]
    )
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

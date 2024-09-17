"""Typing definitions for assistants API."""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Literal

from fastapi import UploadFile, Form, File
from openai.types import FileObject
from openai.types.beta import Assistant
from openai.types.beta import VectorStore

from openai.types.beta.thread import ToolResources as BetaThreadToolResources
from openai.types.beta.thread_create_params import (
    ToolResourcesFileSearchVectorStoreChunkingStrategy,
    ToolResourcesFileSearchVectorStoreChunkingStrategyAuto,
)
from openai.types.beta.threads.text_content_block_param import TextContentBlockParam
from openai.types.beta.vector_store import ExpiresAfter
from pydantic import BaseModel, Field

##########
# DEFAULTS
##########


DEFAULT_MAX_COMPLETION_TOKENS = 4096
DEFAULT_MAX_PROMPT_TOKENS = 4096


##########
# GENERIC
##########


class Usage(BaseModel):
    """Usage object."""

    prompt_tokens: int = Field(
        ..., description="The number of tokens used in the prompt."
    )
    completion_tokens: int | None = Field(
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        description="The number of tokens generated in the completion.",
    )
    total_tokens: int = Field(
        ..., description="The total number of tokens used (prompt + completion)."
    )


class FinishReason(Enum):
    NONE = 0  # Maps to "None"
    STOP = 1  # Maps to "stop"
    LENGTH = 2  # Maps to "length"

    def to_string(self) -> str:
        if self == FinishReason.NONE:
            return None
        elif self == FinishReason.STOP:
            return "stop"
        elif self == FinishReason.LENGTH:
            return "length"
        else:
            raise ValueError(f"Unsupported finish reason: {self}")


##########
# MODELS
##########


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


############
# COMPLETION
############


class CompletionRequest(BaseModel):
    """Request object for completion."""

    model: str = Field(
        ...,
        description="The ID of the model to use for completion.",
        example="llama-cpp-python",
    )
    prompt: str | list[int] = Field(
        ...,
        description="The prompt to generate completions for. Can be a string or a list of integers representing token IDs.",
        examples=["Once upon a time,"],
    )
    stream: bool = Field(
        False, description="Whether to stream the results as they become available."
    )
    max_tokens: int | None = Field(
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        description="The maximum number of tokens to generate.",
        ge=1,
    )
    temperature: float | None = Field(
        1.0,
        description="Sampling temperature to use. Higher values mean more random completions. Use lower values for more deterministic completions. The upper limit may vary depending on the backend used.",
        ge=0.0,
    )


class CompletionChoice(BaseModel):
    """Choice object for completion."""

    index: int = Field(..., description="The index of this completion choice.")
    text: str = Field(..., description="The generated text for this completion choice.")
    logprobs: object | None = Field(
        None,
        description="Log probabilities for the generated tokens. Only returned if requested.",
    )
    finish_reason: str = Field(
        default="stop",
        description="The reason why the model stopped generating tokens.",
        examples=["stop", "length"],
    )


class CompletionStreamChoice(BaseModel):
    """Stream choice object for completion."""

    index: int = Field(..., description="The index of this completion choice.")
    text: str = Field(..., description="The generated text for this completion choice.")
    logprobs: object | None = Field(
        None,
        description="Log probabilities for the generated tokens. Only returned if requested.",
    )
    finish_reason: str | None = Field(
        default=None,
        description="The reason why the model stopped generating tokens.",
        examples=["stop", "length", None],
    )


class CompletionResponse(BaseModel):
    """Response object for completion."""

    id: str = Field("", description="A unique identifier for this completion response.")
    object: Literal["completion"] = Field(
        "completion",
        description="The object type, which is always 'completion' for this response.",
    )
    created: int = Field(
        0,
        description="The Unix timestamp (in seconds) of when the completion was created.",
    )
    model: str = Field("", description="The ID of the model used for the completion.")
    choices: list[CompletionChoice] | list[CompletionStreamChoice] = Field(
        default=[],
        description="A list of completion choices. Can be either CompletionChoice or CompletionStreamChoice depending on whether streaming is enabled.",
    )
    usage: Usage | None = Field(
        None, description="Usage statistics for the completion request."
    )


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
        examples=["user", "assistant", "system", "function"],
    )
    content: str | list[TextContentBlockParam] = Field(
        default="",
        description="The content of the message. Can be a string or a list of text content blocks.",
        examples=[
            "Hello, how are you?",
            [{"type": "text", "text": "Hello, how are you?"}],
        ],
    )


class ChatDelta(BaseModel):
    """Delta object for chat completion."""

    role: str = Field(
        default="",
        description="The role of the author of this message delta.",
        examples=["assistant"],
    )
    content: str | None = Field(
        default="", description="The content of this message delta."
    )


class ChatCompletionRequest(BaseModel):
    """Request object for chat completion."""

    model: str = Field(
        default="",
        description="The ID of the model to use for chat completion.",
        examples=["llama-cpp-python"],
    )
    messages: list[ChatMessage] = Field(
        default=[], description="A list of messages comprising the conversation so far."
    )
    functions: list | None = Field(
        default=None,
        description="A list of functions that the model may generate JSON inputs for.",
    )
    temperature: float | None = Field(
        default=1.0,
        description="What sampling temperature to use. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. The upper limit may vary depending on the backend used.",
        ge=0,
    )
    top_p: float | None = Field(
        default=1,
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
        gt=0,
        le=1,
    )
    stream: bool | None = Field(
        default=False,
        description="If set, partial message deltas will be sent. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.",
    )
    stop: str | None = Field(
        default=None,
        description="Sequences that determine where the API will stop generating further tokens.",
    )
    max_tokens: int | None = Field(
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        description="The maximum number of tokens to generate in the chat completion.",
        gt=0,
    )


class ChatChoice(BaseModel):
    """Choice object for chat completion."""

    index: int = Field(
        default=0, description="The index of this choice among the list of choices."
    )
    message: ChatMessage = Field(
        default=ChatMessage(), description="The message content for this choice."
    )
    finish_reason: str | None = Field(
        default="stop",
        description="The reason why the model stopped generating tokens.",
        examples=["stop", "length"],
    )


class ChatStreamChoice(BaseModel):
    """Stream choice object for chat completion."""

    index: int = Field(
        default=0, description="The index of this choice among the list of choices."
    )
    delta: ChatDelta = Field(
        default=ChatDelta(), description="The delta content for this streaming choice."
    )
    finish_reason: str | None = Field(
        default=None,
        description="The reason why the model stopped generating tokens.",
        examples=["stop", "length", None],
    )


class ChatCompletionResponse(BaseModel):
    """Response object for chat completion."""

    id: str = Field(
        default="", description="A unique identifier for the chat completion."
    )
    object: str = Field(
        default="chat.completion",
        description="The object type, which is always 'chat.completion' for this response.",
    )
    created: int = Field(
        default=0,
        description="The Unix timestamp (in seconds) of when the chat completion was created.",
    )
    model: str = Field(
        default="", description="The ID of the model used for the chat completion."
    )
    choices: list[ChatChoice] | list[ChatStreamChoice] = Field(
        default=[],
        description="A list of chat completion choices. Can be either ChatChoice or ChatStreamChoice depending on whether streaming is enabled.",
    )
    usage: Usage | None = Field(
        default=None, description="Usage statistics for the completion request."
    )


#############
# EMBEDDINGS
#############


class CreateEmbeddingRequest(BaseModel):
    """Request object for creating embeddings."""

    model: str = Field(
        description="The ID of the model to use for generating embeddings.",
        examples=["text-embeddings"],
    )
    input: str | list[str] | list[int] | list[list[int]] = Field(
        description="The text to generate embeddings for. Can be a string, array of strings, array of tokens, or array of token arrays.",
        examples=["The quick brown fox jumps over the lazy dog", ["Hello", "World"]],
    )


class EmbeddingResponseData(BaseModel):
    """Response object for embeddings."""

    embedding: list[float] = Field(
        default=[],
        description="The embedding vector representing the input text.",
    )
    index: int = Field(
        default=0,
        description="The index of the embedding in the list of generated embeddings.",
    )
    object: str = Field(
        default="embedding",
        description="The object type, which is always 'embedding'.",
    )


class CreateEmbeddingResponse(BaseModel):
    """Response object for embeddings."""

    data: list[EmbeddingResponseData] = Field(
        default=[],
        description="A list of embedding objects.",
    )
    model: str = Field(
        default="",
        examples=["text-embeddings"],
        description="The ID of the model used for generating the embeddings.",
    )
    object: str = Field(
        default="list",
        description="The object type, which is always 'list' for embedding responses.",
    )
    usage: Usage | None = Field(
        default=None,
        description="Usage statistics for the API call.",
    )


##########
# AUDIO
##########


class CreateTranscriptionRequest(BaseModel):
    """Request object for creating a transcription."""

    file: UploadFile = Field(
        ...,
        description="The audio file to transcribe. Supports any audio format that ffmpeg can handle. For a complete list of supported formats, see: https://ffmpeg.org/ffmpeg-formats.html",
    )
    model: str = Field(..., description="ID of the model to use.")
    language: str = Field(
        default="",
        description="The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency.",
    )
    prompt: str = Field(
        default="",
        description="An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language.",
    )
    response_format: str = Field(
        default="json",
        description="The format of the transcript output, in one of these options: json, text, srt, verbose_json, or vtt.",
    )
    temperature: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description="The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.",
    )
    timestamp_granularities: list[Literal["word", "segment"]] | None = Field(
        default=None,
        description="The timestamp granularities to populate for this transcription. response_format must be set to verbose_json to use timestamp granularities. Either or both of these options are supported: word, or segment. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency.",
    )

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        model: str = Form(...),
        language: str | None = Form(""),
        prompt: str | None = Form(""),
        response_format: str | None = Form(""),
        temperature: float | None = Form(1.0),
        timestamp_granularities: list[Literal["word", "segment"]] | None = Form(None),
    ) -> CreateTranscriptionRequest:
        return cls(
            file=file,
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            timestamp_granularities=timestamp_granularities,
        )


class CreateTranscriptionResponse(BaseModel):
    """Response object for transcription."""

    text: str = Field(
        ...,
        description="The transcribed text.",
        examples=["Hello, this is a transcription of the audio file."],
    )


class CreateTranslationRequest(BaseModel):
    """Request object for creating a translation."""

    file: UploadFile = Field(
        ...,
        description="The audio file to translate. Supports any audio format that ffmpeg can handle. For a complete list of supported formats, see: https://ffmpeg.org/ffmpeg-formats.html",
    )
    model: str = Field(..., description="ID of the model to use.")
    prompt: str = Field(
        default="",
        description="An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language.",
    )
    response_format: str = Field(
        default="json",
        description="The format of the transcript output, in one of these options: json, text, srt, verbose_json, or vtt.",
    )
    temperature: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description="The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.",
    )

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        model: str = Form(...),
        prompt: str | None = Form(""),
        response_format: str | None = Form(""),
        temperature: float | None = Form(1.0),
    ) -> CreateTranslationRequest:
        return cls(
            file=file,
            model=model,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
        )


class CreateTranslationResponse(BaseModel):
    """Response object for translation."""

    text: str = Field(
        ...,
        description="The translated text.",
        examples=["Hello, this is a translation of the audio file."],
    )


#############
# FILES
#############


class UploadFileRequest(BaseModel):
    """Request object for uploading a file."""

    file: UploadFile = Field(
        ...,
        description="The file to be uploaded. Must be a supported file type.",
    )
    purpose: Literal["assistants"] | None = Field(
        default="assistants",
        description="The intended purpose of the uploaded file. Currently, only 'assistants' is supported.",
    )

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

    object: Literal["list"] = Field(
        default="list",
        description="The type of object returned. Always 'list' for file listing.",
    )
    data: list[FileObject] = Field(
        default=[],
        description="An array of File objects, each representing an uploaded file.",
    )


#############
# ASSISTANTS
#############


class ListAssistantsResponse(BaseModel):
    """Response object for listing assistants."""

    object: Literal["list"] = Field(
        default="list",
        description="The type of object. Always 'list' for this response.",
    )
    data: list[Assistant] = Field(description="A list of Assistant objects.")


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
            description="The strategy for chunking the file content. Use 'auto' for automatic chunking.",
            examples=[
                ToolResourcesFileSearchVectorStoreChunkingStrategyAuto(type="auto")
            ],
        )
    )

    file_id: str = Field(
        default="",
        description="The ID of the file to be added to the vector store.",
        examples=["file-abc123"],
    )


class CreateVectorStoreRequest(BaseModel):
    """Request object for creating a vector store."""

    file_ids: list[str] | None = Field(
        default=[],
        description="List of file IDs to be included in the vector store.",
        example=["file-abc123", "file-def456"],
    )
    name: str | None = Field(
        default=None,
        description="Optional name for the vector store.",
        example="My Vector Store",
    )
    expires_after: ExpiresAfter | None = Field(
        default=None,
        description="Expiration settings for the vector store.",
        examples=[ExpiresAfter(anchor="last_active_at", days=1)],
    )
    metadata: dict | None = Field(
        default=None,
        description="Optional metadata for the vector store.",
        example={"project": "AI Research", "version": "1.0"},
    )

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

    object: Literal["list"] = Field(
        default="list",
        description="The type of object. Always 'list' for this response.",
    )
    data: list[VectorStore] = Field(
        default=[],
        description="A list of VectorStore objects.",
    )


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
# LEAPFROGAI Vector Stores
################


class SearchItem(BaseModel):
    """Object representing a single item in a search result."""

    id: str = Field(..., description="Unique identifier for the search item.")
    vector_store_id: str = Field(
        ..., description="ID of the vector store containing this item."
    )
    file_id: str = Field(..., description="ID of the file associated with this item.")
    content: str = Field(..., description="The actual content of the item.")
    metadata: dict = Field(
        ..., description="Additional metadata associated with the item."
    )
    similarity: float = Field(
        ..., description="Similarity score of this item to the query."
    )


class SearchResponse(BaseModel):
    """Response object for RAG queries."""

    data: list[SearchItem] = Field(
        ...,
        description="List of RAG items returned as a result of the query.",
        min_length=0,
    )

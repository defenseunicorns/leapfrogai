from __future__ import annotations

from typing import Dict, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel


##########
# GENERIC
##########
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int | None = None
    total_tokens: int


##########
# COMPLETION
##########
class CompletionRequest(BaseModel):
    model: str
    prompt: str | list[int]
    stream: bool | None = False
    max_tokens: int | None = 16
    temperature: float | None = 1.0


class CompletionChoice(BaseModel):
    index: int
    text: str
    logprobs: object = None
    finish_reason: str = ""


class CompletionResponse(BaseModel):
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
    name: str
    parameters: Dict[str, object]
    description: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatDelta(BaseModel):
    role: str
    content: str | None = ""


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    functions: list | None = None
    temperature: float | None = 1.0
    top_p: float | None = 1
    stream: bool | None = False
    stop: str | None = None
    max_tokens: int | None = 128


class ChatChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str | None = ""


class ChatStreamChoice(BaseModel):
    index: int
    delta: ChatDelta
    finish_reason: str | None = ""


class ChatCompletionResponse(BaseModel):
    """https://platform.openai.com/docs/api-reference/chat/object"""

    id: str = ""
    object: str = "chat.completion"
    created: int = 0
    model: str = ""
    choices: list[ChatChoice] | list[ChatStreamChoice]
    usage: Usage | None = None


class CreateEmbeddingRequest(BaseModel):
    model: str
    input: str | list[str] | list[int] | list[list[int]]
    user: str | None = None


class EmbeddingResponseData(BaseModel):
    embedding: list[float]
    index: int
    object: str = "embedding"


class CreateEmbeddingResponse(BaseModel):
    data: list[EmbeddingResponseData]
    model: str
    object: str = "list"
    usage: Usage


# yes I know, this is a pure API response class for matching OpenAI
class ModelResponseModel(BaseModel):
    id: str
    object: str = "model"
    created: int = 0
    owned_by: str = "leapfrogai"


class ModelResponse(BaseModel):
    object: str = "list"
    data: list[ModelResponseModel] = []


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

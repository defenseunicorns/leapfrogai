from pydantic import BaseModel, Field
from typing import Literal
from openai.types.beta.threads.text_content_block_param import TextContentBlockParam

from ..common import Usage
from ...backend.constants import DEFAULT_MAX_COMPLETION_TOKENS


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

    def content_as_str(self) -> str:
        """If content is a string, return it. Otherwise, concatenate the text fields of the list of TextContentBlockParam objects.

        Returns:
            str: content as a string
        """
        if isinstance(self.content, str):
            return self.content
        return "".join([(part.get("text") or "") for part in self.content])


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


class ChatChoice(BaseModel):
    """Choice object for chat completion."""

    index: int = Field(
        default=0, description="The index of this choice among the list of choices."
    )
    message: ChatMessage = Field(
        default=ChatMessage(), description="The message content for this choice."
    )
    finish_reason: str | None = Field(
        default="",
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
        default="",
        description="The reason why the model stopped generating tokens.",
        examples=["stop", "length"],
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

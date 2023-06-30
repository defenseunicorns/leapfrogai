from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenAIChatRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    USER: _ClassVar[OpenAIChatRole]
    SYSTEM: _ClassVar[OpenAIChatRole]
    FUNCTION: _ClassVar[OpenAIChatRole]
    ASSISTANT: _ClassVar[OpenAIChatRole]
USER: OpenAIChatRole
SYSTEM: OpenAIChatRole
FUNCTION: OpenAIChatRole
ASSISTANT: OpenAIChatRole

class ChatRequest(_message.Message):
    __slots__ = ["inputs"]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, inputs: _Optional[_Iterable[str]] = ...) -> None: ...

class Chat(_message.Message):
    __slots__ = ["chat"]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    chat: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, chat: _Optional[_Iterable[float]] = ...) -> None: ...

class ChatResponse(_message.Message):
    __slots__ = ["chat"]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    chat: _containers.RepeatedCompositeFieldContainer[Chat]
    def __init__(self, chat: _Optional[_Iterable[_Union[Chat, _Mapping]]] = ...) -> None: ...

class OpenAIChatItem(_message.Message):
    __slots__ = ["role", "content"]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    role: OpenAIChatRole
    content: str
    def __init__(self, role: _Optional[_Union[OpenAIChatRole, str]] = ..., content: _Optional[str] = ...) -> None: ...

class OpenAIChatCompletionRequest(_message.Message):
    __slots__ = ["model", "chat_items", "temperature", "top_p", "n", "stream", "stop", "max_tokens", "presence_penalty", "frequency_penalty", "logit_bias", "user"]
    class LogitBiasEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    MODEL_FIELD_NUMBER: _ClassVar[int]
    CHAT_ITEMS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    STREAM_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_PENALTY_FIELD_NUMBER: _ClassVar[int]
    LOGIT_BIAS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    model: str
    chat_items: _containers.RepeatedCompositeFieldContainer[OpenAIChatItem]
    temperature: float
    top_p: float
    n: int
    stream: bool
    stop: _containers.RepeatedScalarFieldContainer[str]
    max_tokens: int
    presence_penalty: float
    frequency_penalty: float
    logit_bias: _containers.ScalarMap[str, int]
    user: str
    def __init__(self, model: _Optional[str] = ..., chat_items: _Optional[_Iterable[_Union[OpenAIChatItem, _Mapping]]] = ..., temperature: _Optional[float] = ..., top_p: _Optional[float] = ..., n: _Optional[int] = ..., stream: bool = ..., stop: _Optional[_Iterable[str]] = ..., max_tokens: _Optional[int] = ..., presence_penalty: _Optional[float] = ..., frequency_penalty: _Optional[float] = ..., logit_bias: _Optional[_Mapping[str, int]] = ..., user: _Optional[str] = ...) -> None: ...

class OpenAICompletionChoice(_message.Message):
    __slots__ = ["index", "chas_item", "finish_reason"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CHAS_ITEM_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    index: int
    chas_item: OpenAIChatItem
    finish_reason: str
    def __init__(self, index: _Optional[int] = ..., chas_item: _Optional[_Union[OpenAIChatItem, _Mapping]] = ..., finish_reason: _Optional[str] = ...) -> None: ...

class Usage(_message.Message):
    __slots__ = ["prompt_tokens", "completion_tokens", "total_tokens"]
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ...) -> None: ...

class ChatCompletionRequest(_message.Message):
    __slots__ = ["id", "object", "created", "choices", "usage"]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    object: str
    created: int
    choices: _containers.RepeatedCompositeFieldContainer[OpenAICompletionChoice]
    usage: Usage
    def __init__(self, id: _Optional[str] = ..., object: _Optional[str] = ..., created: _Optional[int] = ..., choices: _Optional[_Iterable[_Union[OpenAICompletionChoice, _Mapping]]] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ...) -> None: ...

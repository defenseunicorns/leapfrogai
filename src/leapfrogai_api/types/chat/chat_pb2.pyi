from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER: _ClassVar[ChatRole]
    SYSTEM: _ClassVar[ChatRole]
    FUNCTION: _ClassVar[ChatRole]
    ASSISTANT: _ClassVar[ChatRole]
USER: ChatRole
SYSTEM: ChatRole
FUNCTION: ChatRole
ASSISTANT: ChatRole

class ChatItem(_message.Message):
    __slots__ = ("role", "content")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    role: ChatRole
    content: str
    def __init__(self, role: _Optional[_Union[ChatRole, str]] = ..., content: _Optional[str] = ...) -> None: ...

class ChatCompletionRequest(_message.Message):
    __slots__ = ("chat_items", "max_new_tokens", "temperature", "top_k", "top_p", "do_sample", "n", "stop", "repetition_penalty", "presence_penalty", "frequency_penalty", "best_of", "logit_bias", "return_full_text", "truncate", "typical_p", "watermark", "seed", "user")
    class LogitBiasEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    CHAT_ITEMS_FIELD_NUMBER: _ClassVar[int]
    MAX_NEW_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    DO_SAMPLE_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    REPETITION_PENALTY_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_PENALTY_FIELD_NUMBER: _ClassVar[int]
    BEST_OF_FIELD_NUMBER: _ClassVar[int]
    LOGIT_BIAS_FIELD_NUMBER: _ClassVar[int]
    RETURN_FULL_TEXT_FIELD_NUMBER: _ClassVar[int]
    TRUNCATE_FIELD_NUMBER: _ClassVar[int]
    TYPICAL_P_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    chat_items: _containers.RepeatedCompositeFieldContainer[ChatItem]
    max_new_tokens: int
    temperature: float
    top_k: float
    top_p: float
    do_sample: bool
    n: int
    stop: _containers.RepeatedScalarFieldContainer[str]
    repetition_penalty: float
    presence_penalty: float
    frequency_penalty: float
    best_of: str
    logit_bias: _containers.ScalarMap[str, int]
    return_full_text: bool
    truncate: int
    typical_p: float
    watermark: bool
    seed: int
    user: str
    def __init__(self, chat_items: _Optional[_Iterable[_Union[ChatItem, _Mapping]]] = ..., max_new_tokens: _Optional[int] = ..., temperature: _Optional[float] = ..., top_k: _Optional[float] = ..., top_p: _Optional[float] = ..., do_sample: bool = ..., n: _Optional[int] = ..., stop: _Optional[_Iterable[str]] = ..., repetition_penalty: _Optional[float] = ..., presence_penalty: _Optional[float] = ..., frequency_penalty: _Optional[float] = ..., best_of: _Optional[str] = ..., logit_bias: _Optional[_Mapping[str, int]] = ..., return_full_text: bool = ..., truncate: _Optional[int] = ..., typical_p: _Optional[float] = ..., watermark: bool = ..., seed: _Optional[int] = ..., user: _Optional[str] = ...) -> None: ...

class ChatCompletionChoice(_message.Message):
    __slots__ = ("index", "chat_item", "finish_reason")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CHAT_ITEM_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    index: int
    chat_item: ChatItem
    finish_reason: str
    def __init__(self, index: _Optional[int] = ..., chat_item: _Optional[_Union[ChatItem, _Mapping]] = ..., finish_reason: _Optional[str] = ...) -> None: ...

class Usage(_message.Message):
    __slots__ = ("prompt_tokens", "completion_tokens", "total_tokens")
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ...) -> None: ...

class ChatCompletionResponse(_message.Message):
    __slots__ = ("id", "object", "created", "choices", "usage")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    object: str
    created: int
    choices: _containers.RepeatedCompositeFieldContainer[ChatCompletionChoice]
    usage: Usage
    def __init__(self, id: _Optional[str] = ..., object: _Optional[str] = ..., created: _Optional[int] = ..., choices: _Optional[_Iterable[_Union[ChatCompletionChoice, _Mapping]]] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ...) -> None: ...

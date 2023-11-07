from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

ASSISTANT: ChatRole
DESCRIPTOR: _descriptor.FileDescriptor
FUNCTION: ChatRole
SYSTEM: ChatRole
USER: ChatRole

class ChatCompletionChoice(_message.Message):
    __slots__ = ["chat_item", "finish_reason", "index"]
    CHAT_ITEM_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    chat_item: ChatItem
    finish_reason: str
    index: int
    def __init__(self, index: _Optional[int] = ..., chat_item: _Optional[_Union[ChatItem, _Mapping]] = ..., finish_reason: _Optional[str] = ...) -> None: ...

class ChatCompletionRequest(_message.Message):
    __slots__ = ["best_of", "chat_items", "do_sample", "frequency_penalty", "logit_bias", "max_new_tokens", "n", "presence_penalty", "repetition_penalty", "return_full_text", "seed", "stop", "temperature", "top_k", "top_p", "truncate", "typical_p", "user", "watermark"]
    class LogitBiasEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    BEST_OF_FIELD_NUMBER: _ClassVar[int]
    CHAT_ITEMS_FIELD_NUMBER: _ClassVar[int]
    DO_SAMPLE_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_PENALTY_FIELD_NUMBER: _ClassVar[int]
    LOGIT_BIAS_FIELD_NUMBER: _ClassVar[int]
    MAX_NEW_TOKENS_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    REPETITION_PENALTY_FIELD_NUMBER: _ClassVar[int]
    RETURN_FULL_TEXT_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    TRUNCATE_FIELD_NUMBER: _ClassVar[int]
    TYPICAL_P_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    best_of: str
    chat_items: _containers.RepeatedCompositeFieldContainer[ChatItem]
    do_sample: bool
    frequency_penalty: float
    logit_bias: _containers.ScalarMap[str, int]
    max_new_tokens: int
    n: int
    presence_penalty: float
    repetition_penalty: float
    return_full_text: bool
    seed: int
    stop: _containers.RepeatedScalarFieldContainer[str]
    temperature: float
    top_k: float
    top_p: float
    truncate: int
    typical_p: float
    user: str
    watermark: bool
    def __init__(self, chat_items: _Optional[_Iterable[_Union[ChatItem, _Mapping]]] = ..., max_new_tokens: _Optional[int] = ..., temperature: _Optional[float] = ..., top_k: _Optional[float] = ..., top_p: _Optional[float] = ..., do_sample: bool = ..., n: _Optional[int] = ..., stop: _Optional[_Iterable[str]] = ..., repetition_penalty: _Optional[float] = ..., presence_penalty: _Optional[float] = ..., frequency_penalty: _Optional[float] = ..., best_of: _Optional[str] = ..., logit_bias: _Optional[_Mapping[str, int]] = ..., return_full_text: bool = ..., truncate: _Optional[int] = ..., typical_p: _Optional[float] = ..., watermark: bool = ..., seed: _Optional[int] = ..., user: _Optional[str] = ...) -> None: ...

class ChatCompletionResponse(_message.Message):
    __slots__ = ["choices", "created", "id", "object", "usage"]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    choices: _containers.RepeatedCompositeFieldContainer[ChatCompletionChoice]
    created: int
    id: str
    object: str
    usage: Usage
    def __init__(self, id: _Optional[str] = ..., object: _Optional[str] = ..., created: _Optional[int] = ..., choices: _Optional[_Iterable[_Union[ChatCompletionChoice, _Mapping]]] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ...) -> None: ...

class ChatItem(_message.Message):
    __slots__ = ["content", "role"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    content: str
    role: ChatRole
    def __init__(self, role: _Optional[_Union[ChatRole, str]] = ..., content: _Optional[str] = ...) -> None: ...

class Usage(_message.Message):
    __slots__ = ["completion_tokens", "prompt_tokens", "total_tokens"]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ...) -> None: ...

class ChatRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

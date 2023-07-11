from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
LENGTH: CompletionFinishReason
STOP: CompletionFinishReason

class CompletionChoice(_message.Message):
    __slots__ = ["finish_reason", "index", "text"]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    finish_reason: CompletionFinishReason
    index: int
    text: str
    def __init__(self, text: _Optional[str] = ..., index: _Optional[int] = ..., finish_reason: _Optional[_Union[CompletionFinishReason, str]] = ...) -> None: ...

class CompletionRequest(_message.Message):
    __slots__ = ["best_of", "do_sample", "echo", "frequence_penalty", "logit_bias", "logprobs", "max_new_tokens", "n", "presence_penalty", "prompt", "repetition_penalty", "return_full_text", "seed", "stop", "suffix", "temperature", "top_k", "top_p", "truncate", "typical_p", "user", "watermark"]
    class LogitBiasEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    BEST_OF_FIELD_NUMBER: _ClassVar[int]
    DO_SAMPLE_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    FREQUENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    LOGIT_BIAS_FIELD_NUMBER: _ClassVar[int]
    LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    MAX_NEW_TOKENS_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    REPETITION_PENALTY_FIELD_NUMBER: _ClassVar[int]
    RETURN_FULL_TEXT_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    TRUNCATE_FIELD_NUMBER: _ClassVar[int]
    TYPICAL_P_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    best_of: int
    do_sample: bool
    echo: bool
    frequence_penalty: float
    logit_bias: _containers.ScalarMap[str, int]
    logprobs: int
    max_new_tokens: int
    n: int
    presence_penalty: float
    prompt: str
    repetition_penalty: float
    return_full_text: bool
    seed: int
    stop: _containers.RepeatedScalarFieldContainer[str]
    suffix: str
    temperature: float
    top_k: int
    top_p: float
    truncate: int
    typical_p: float
    user: str
    watermark: bool
    def __init__(self, prompt: _Optional[str] = ..., suffix: _Optional[str] = ..., max_new_tokens: _Optional[int] = ..., temperature: _Optional[float] = ..., top_k: _Optional[int] = ..., top_p: _Optional[float] = ..., do_sample: bool = ..., n: _Optional[int] = ..., logprobs: _Optional[int] = ..., echo: bool = ..., stop: _Optional[_Iterable[str]] = ..., repetition_penalty: _Optional[float] = ..., presence_penalty: _Optional[float] = ..., frequence_penalty: _Optional[float] = ..., best_of: _Optional[int] = ..., logit_bias: _Optional[_Mapping[str, int]] = ..., return_full_text: bool = ..., truncate: _Optional[int] = ..., typical_p: _Optional[float] = ..., watermark: bool = ..., seed: _Optional[int] = ..., user: _Optional[str] = ...) -> None: ...

class CompletionResponse(_message.Message):
    __slots__ = ["choices", "usage"]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    choices: _containers.RepeatedCompositeFieldContainer[CompletionChoice]
    usage: CompletionUsage
    def __init__(self, choices: _Optional[_Iterable[_Union[CompletionChoice, _Mapping]]] = ..., usage: _Optional[_Union[CompletionUsage, _Mapping]] = ...) -> None: ...

class CompletionUsage(_message.Message):
    __slots__ = ["completion_tokens", "prompt_tokens", "total_tokens"]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ...) -> None: ...

class CompletionFinishReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

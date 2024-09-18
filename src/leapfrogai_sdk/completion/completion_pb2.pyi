from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CompletionFinishReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STOP: _ClassVar[CompletionFinishReason]
    LENGTH: _ClassVar[CompletionFinishReason]

STOP: CompletionFinishReason
LENGTH: CompletionFinishReason

class CompletionRequest(_message.Message):
    __slots__ = (
        "prompt",
        "suffix",
        "max_new_tokens",
        "temperature",
        "top_k",
        "top_p",
        "do_sample",
        "n",
        "logprobs",
        "echo",
        "stop",
        "repetition_penalty",
        "presence_penalty",
        "frequence_penalty",
        "best_of",
        "logit_bias",
        "return_full_text",
        "truncate",
        "typical_p",
        "watermark",
        "seed",
        "user",
    )
    class LogitBiasEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[int] = ...
        ) -> None: ...

    PROMPT_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    MAX_NEW_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    DO_SAMPLE_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    REPETITION_PENALTY_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    FREQUENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    BEST_OF_FIELD_NUMBER: _ClassVar[int]
    LOGIT_BIAS_FIELD_NUMBER: _ClassVar[int]
    RETURN_FULL_TEXT_FIELD_NUMBER: _ClassVar[int]
    TRUNCATE_FIELD_NUMBER: _ClassVar[int]
    TYPICAL_P_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    suffix: str
    max_new_tokens: int
    temperature: float
    top_k: int
    top_p: float
    do_sample: bool
    n: int
    logprobs: int
    echo: bool
    stop: _containers.RepeatedScalarFieldContainer[str]
    repetition_penalty: float
    presence_penalty: float
    frequence_penalty: float
    best_of: str
    logit_bias: _containers.ScalarMap[str, int]
    return_full_text: bool
    truncate: int
    typical_p: float
    watermark: bool
    seed: int
    user: str
    def __init__(
        self,
        prompt: _Optional[str] = ...,
        suffix: _Optional[str] = ...,
        max_new_tokens: _Optional[int] = ...,
        temperature: _Optional[float] = ...,
        top_k: _Optional[int] = ...,
        top_p: _Optional[float] = ...,
        do_sample: bool = ...,
        n: _Optional[int] = ...,
        logprobs: _Optional[int] = ...,
        echo: bool = ...,
        stop: _Optional[_Iterable[str]] = ...,
        repetition_penalty: _Optional[float] = ...,
        presence_penalty: _Optional[float] = ...,
        frequence_penalty: _Optional[float] = ...,
        best_of: _Optional[str] = ...,
        logit_bias: _Optional[_Mapping[str, int]] = ...,
        return_full_text: bool = ...,
        truncate: _Optional[int] = ...,
        typical_p: _Optional[float] = ...,
        watermark: bool = ...,
        seed: _Optional[int] = ...,
        user: _Optional[str] = ...,
    ) -> None: ...

class CompletionChoice(_message.Message):
    __slots__ = ("text", "index", "finish_reason")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    text: str
    index: int
    finish_reason: CompletionFinishReason
    def __init__(
        self,
        text: _Optional[str] = ...,
        index: _Optional[int] = ...,
        finish_reason: _Optional[_Union[CompletionFinishReason, str]] = ...,
    ) -> None: ...

class CompletionUsage(_message.Message):
    __slots__ = ("prompt_tokens", "completion_tokens", "total_tokens")
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    def __init__(
        self,
        prompt_tokens: _Optional[int] = ...,
        completion_tokens: _Optional[int] = ...,
        total_tokens: _Optional[int] = ...,
    ) -> None: ...

class CompletionResponse(_message.Message):
    __slots__ = ("choices", "usage")
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    choices: _containers.RepeatedCompositeFieldContainer[CompletionChoice]
    usage: CompletionUsage
    def __init__(
        self,
        choices: _Optional[_Iterable[_Union[CompletionChoice, _Mapping]]] = ...,
        usage: _Optional[_Union[CompletionUsage, _Mapping]] = ...,
    ) -> None: ...

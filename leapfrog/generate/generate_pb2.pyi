from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CompletionRequest(_message.Message):
    __slots__ = ["best_of", "echo", "frequence_penalty", "logit_bias", "logprobs", "max_tokens", "presence_penalty", "prompt", "stop", "stream", "suffix", "temperature", "top_p"]
    class LogitBiasEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    BEST_OF_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    FREQUENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    LOGIT_BIAS_FIELD_NUMBER: _ClassVar[int]
    LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    STREAM_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    best_of: int
    echo: bool
    frequence_penalty: float
    logit_bias: _containers.ScalarMap[str, int]
    logprobs: int
    max_tokens: int
    presence_penalty: float
    prompt: str
    stop: _containers.RepeatedScalarFieldContainer[str]
    stream: bool
    suffix: str
    temperature: float
    top_p: float
    def __init__(self, prompt: _Optional[str] = ..., suffix: _Optional[str] = ..., max_tokens: _Optional[int] = ..., temperature: _Optional[float] = ..., top_p: _Optional[float] = ..., stream: bool = ..., logprobs: _Optional[int] = ..., echo: bool = ..., stop: _Optional[_Iterable[str]] = ..., presence_penalty: _Optional[float] = ..., frequence_penalty: _Optional[float] = ..., best_of: _Optional[int] = ..., logit_bias: _Optional[_Mapping[str, int]] = ...) -> None: ...

class CompletionResponse(_message.Message):
    __slots__ = ["completion", "finish_reason"]
    COMPLETION_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    completion: str
    finish_reason: str
    def __init__(self, completion: _Optional[str] = ..., finish_reason: _Optional[str] = ...) -> None: ...

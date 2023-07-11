from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
TRANSCRIBE: AudioTask
TRANSLATE: AudioTask

class AudioMetadata(_message.Message):
    __slots__ = ["format", "inputlanguage", "prompt", "temperature"]
    class AudioFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    INPUTLANGUAGE_FIELD_NUMBER: _ClassVar[int]
    JSON: AudioMetadata.AudioFormat
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    SRT: AudioMetadata.AudioFormat
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TEXT: AudioMetadata.AudioFormat
    VERBOSE_JSON: AudioMetadata.AudioFormat
    VTT: AudioMetadata.AudioFormat
    format: AudioMetadata.AudioFormat
    inputlanguage: str
    prompt: str
    temperature: float
    def __init__(self, prompt: _Optional[str] = ..., temperature: _Optional[float] = ..., inputlanguage: _Optional[str] = ..., format: _Optional[_Union[AudioMetadata.AudioFormat, str]] = ...) -> None: ...

class AudioRequest(_message.Message):
    __slots__ = ["chunk_data", "metadata"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    metadata: AudioMetadata
    def __init__(self, metadata: _Optional[_Union[AudioMetadata, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...) -> None: ...

class AudioResponse(_message.Message):
    __slots__ = ["duration", "language", "segments", "task", "text"]
    class Segment(_message.Message):
        __slots__ = ["avg_logprob", "compression_ratio", "end", "id", "no_speech_prob", "seek", "start", "temperature", "text", "tokens", "transient"]
        AVG_LOGPROB_FIELD_NUMBER: _ClassVar[int]
        COMPRESSION_RATIO_FIELD_NUMBER: _ClassVar[int]
        END_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        NO_SPEECH_PROB_FIELD_NUMBER: _ClassVar[int]
        SEEK_FIELD_NUMBER: _ClassVar[int]
        START_FIELD_NUMBER: _ClassVar[int]
        TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
        TEXT_FIELD_NUMBER: _ClassVar[int]
        TOKENS_FIELD_NUMBER: _ClassVar[int]
        TRANSIENT_FIELD_NUMBER: _ClassVar[int]
        avg_logprob: float
        compression_ratio: float
        end: float
        id: int
        no_speech_prob: float
        seek: int
        start: float
        temperature: float
        text: str
        tokens: _containers.RepeatedScalarFieldContainer[int]
        transient: bool
        def __init__(self, id: _Optional[int] = ..., seek: _Optional[int] = ..., start: _Optional[float] = ..., end: _Optional[float] = ..., text: _Optional[str] = ..., tokens: _Optional[_Iterable[int]] = ..., temperature: _Optional[float] = ..., avg_logprob: _Optional[float] = ..., compression_ratio: _Optional[float] = ..., no_speech_prob: _Optional[float] = ..., transient: bool = ...) -> None: ...
    DURATION_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    duration: float
    language: str
    segments: _containers.RepeatedCompositeFieldContainer[AudioResponse.Segment]
    task: AudioTask
    text: str
    def __init__(self, task: _Optional[_Union[AudioTask, str]] = ..., language: _Optional[str] = ..., duration: _Optional[float] = ..., segments: _Optional[_Iterable[_Union[AudioResponse.Segment, _Mapping]]] = ..., text: _Optional[str] = ...) -> None: ...

class AudioTask(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

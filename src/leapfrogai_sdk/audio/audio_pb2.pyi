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

class AudioTask(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRANSCRIBE: _ClassVar[AudioTask]
    TRANSLATE: _ClassVar[AudioTask]

TRANSCRIBE: AudioTask
TRANSLATE: AudioTask

class AudioMetadata(_message.Message):
    __slots__ = ("prompt", "temperature", "inputlanguage", "format")

    class AudioFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        JSON: _ClassVar[AudioMetadata.AudioFormat]
        TEXT: _ClassVar[AudioMetadata.AudioFormat]
        SRT: _ClassVar[AudioMetadata.AudioFormat]
        VERBOSE_JSON: _ClassVar[AudioMetadata.AudioFormat]
        VTT: _ClassVar[AudioMetadata.AudioFormat]

    JSON: AudioMetadata.AudioFormat
    TEXT: AudioMetadata.AudioFormat
    SRT: AudioMetadata.AudioFormat
    VERBOSE_JSON: AudioMetadata.AudioFormat
    VTT: AudioMetadata.AudioFormat
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    INPUTLANGUAGE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    temperature: float
    inputlanguage: str
    format: AudioMetadata.AudioFormat
    def __init__(
        self,
        prompt: _Optional[str] = ...,
        temperature: _Optional[float] = ...,
        inputlanguage: _Optional[str] = ...,
        format: _Optional[_Union[AudioMetadata.AudioFormat, str]] = ...,
    ) -> None: ...

class AudioRequest(_message.Message):
    __slots__ = ("metadata", "chunk_data")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    metadata: AudioMetadata
    chunk_data: bytes
    def __init__(
        self,
        metadata: _Optional[_Union[AudioMetadata, _Mapping]] = ...,
        chunk_data: _Optional[bytes] = ...,
    ) -> None: ...

class AudioResponse(_message.Message):
    __slots__ = ("task", "language", "duration", "segments", "text")

    class Segment(_message.Message):
        __slots__ = (
            "id",
            "seek",
            "start",
            "end",
            "text",
            "tokens",
            "temperature",
            "avg_logprob",
            "compression_ratio",
            "no_speech_prob",
            "transient",
        )
        ID_FIELD_NUMBER: _ClassVar[int]
        SEEK_FIELD_NUMBER: _ClassVar[int]
        START_FIELD_NUMBER: _ClassVar[int]
        END_FIELD_NUMBER: _ClassVar[int]
        TEXT_FIELD_NUMBER: _ClassVar[int]
        TOKENS_FIELD_NUMBER: _ClassVar[int]
        TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
        AVG_LOGPROB_FIELD_NUMBER: _ClassVar[int]
        COMPRESSION_RATIO_FIELD_NUMBER: _ClassVar[int]
        NO_SPEECH_PROB_FIELD_NUMBER: _ClassVar[int]
        TRANSIENT_FIELD_NUMBER: _ClassVar[int]
        id: int
        seek: int
        start: float
        end: float
        text: str
        tokens: _containers.RepeatedScalarFieldContainer[int]
        temperature: float
        avg_logprob: float
        compression_ratio: float
        no_speech_prob: float
        transient: bool
        def __init__(
            self,
            id: _Optional[int] = ...,
            seek: _Optional[int] = ...,
            start: _Optional[float] = ...,
            end: _Optional[float] = ...,
            text: _Optional[str] = ...,
            tokens: _Optional[_Iterable[int]] = ...,
            temperature: _Optional[float] = ...,
            avg_logprob: _Optional[float] = ...,
            compression_ratio: _Optional[float] = ...,
            no_speech_prob: _Optional[float] = ...,
            transient: bool = ...,
        ) -> None: ...

    TASK_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    task: AudioTask
    language: str
    duration: float
    segments: _containers.RepeatedCompositeFieldContainer[AudioResponse.Segment]
    text: str
    def __init__(
        self,
        task: _Optional[_Union[AudioTask, str]] = ...,
        language: _Optional[str] = ...,
        duration: _Optional[float] = ...,
        segments: _Optional[_Iterable[_Union[AudioResponse.Segment, _Mapping]]] = ...,
        text: _Optional[str] = ...,
    ) -> None: ...

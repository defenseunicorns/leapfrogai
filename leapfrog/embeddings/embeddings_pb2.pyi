from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EmbeddingRequest(_message.Message):
    __slots__ = ["inputs"]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, inputs: _Optional[_Iterable[str]] = ...) -> None: ...

class EmbeddingResponse(_message.Message):
    __slots__ = ["embeddings"]
    EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
    embeddings: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, embeddings: _Optional[_Iterable[float]] = ...) -> None: ...

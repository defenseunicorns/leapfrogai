from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class TokenCountRequest(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class TokenCountResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class TokenCountUsage(_message.Message):
    __slots__ = ("total_tokens",)
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    total_tokens: int
    def __init__(self, total_tokens: _Optional[int] = ...) -> None: ...

class TokenCountResult(_message.Message):
    __slots__ = ("result", "usage")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    result: TokenCountResponse
    usage: TokenCountUsage
    def __init__(
        self,
        result: _Optional[_Union[TokenCountResponse, _Mapping]] = ...,
        usage: _Optional[_Union[TokenCountUsage, _Mapping]] = ...,
    ) -> None: ...

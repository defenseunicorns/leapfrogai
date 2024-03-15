# __init__.py
# ruff: noqa: F401

from grpc import ServicerContext as GrpcContext

from leapfrogai_api.types.audio.audio_pb2 import (
    AudioMetadata,
    AudioRequest,
    AudioResponse,
)
from leapfrogai_api.types.audio.audio_pb2_grpc import Audio, AudioServicer, AudioStub
from leapfrogai_api.types.chat.chat_pb2 import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatItem,
    ChatRole,
)
from leapfrogai_api.types.chat.chat_pb2_grpc import (
    ChatCompletionService,
    ChatCompletionServiceServicer,
    ChatCompletionServiceStub,
    ChatCompletionStreamService,
    ChatCompletionStreamServiceServicer,
    ChatCompletionStreamServiceStub,
)
from leapfrogai_api.types.completion.completion_pb2 import (
    CompletionChoice,
    CompletionFinishReason,
    CompletionRequest,
    CompletionResponse,
    CompletionUsage,
)
from leapfrogai_api.types.completion.completion_pb2_grpc import (
    CompletionService,
    CompletionServiceServicer,
    CompletionServiceStub,
    CompletionStreamService,
    CompletionStreamServiceServicer,
    CompletionStreamServiceStub,
)
from leapfrogai_api.types.config import BackendConfig
from leapfrogai_api.types.embeddings.embeddings_pb2 import (
    Embedding,
    EmbeddingRequest,
    EmbeddingResponse,
)
from leapfrogai_api.types.embeddings.embeddings_pb2_grpc import (
    EmbeddingsService,
    EmbeddingsServiceServicer,
    EmbeddingsServiceStub,
)
from leapfrogai_api.types.name.name_pb2 import NameResponse
from leapfrogai_api.types.name.name_pb2_grpc import (
    NameService,
    NameServiceServicer,
    NameServiceStub,
)
from leapfrogai_api.types.serve import serve

print("Initializing Leapfrog")

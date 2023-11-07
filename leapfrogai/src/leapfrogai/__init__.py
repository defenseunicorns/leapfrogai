# __init__.py


from grpc import ServicerContext as GrpcContext

from .audio.audio_pb2 import AudioMetadata, AudioRequest, AudioResponse
from .audio.audio_pb2_grpc import Audio, AudioServicer, AudioStub
from .chat.chat_pb2 import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatItem,
    ChatRole,
)
from .chat.chat_pb2_grpc import (
    ChatCompletionService,
    ChatCompletionServiceServicer,
    ChatCompletionServiceStub,
    ChatCompletionStreamService,
    ChatCompletionStreamServiceServicer,
    ChatCompletionStreamServiceStub,
)
from .completion.completion_pb2 import (
    CompletionChoice,
    CompletionFinishReason,
    CompletionRequest,
    CompletionResponse,
    CompletionUsage,
)
from .completion.completion_pb2_grpc import (
    CompletionService,
    CompletionServiceServicer,
    CompletionServiceStub,
    CompletionStreamService,
    CompletionStreamServiceServicer,
    CompletionStreamServiceStub,
)
from .config import BackendConfig
from .embeddings.embeddings_pb2 import Embedding, EmbeddingRequest, EmbeddingResponse
from .embeddings.embeddings_pb2_grpc import (
    EmbeddingsService,
    EmbeddingsServiceServicer,
    EmbeddingsServiceStub,
)
from .name.name_pb2 import NameResponse
from .name.name_pb2_grpc import NameService, NameServiceServicer, NameServiceStub
from .serve import serve

print("Initializing Leapfrog")

# __init__.py


from grpc import ServicerContext as GrpcContext

from .audio.audio_pb2 import AudioMetadata, AudioRequest, AudioResponse
from .audio.audio_pb2_grpc import Audio, AudioServicer, AudioStub
from .embeddings.embeddings_pb2 import Embedding, EmbeddingRequest, EmbeddingResponse
from .embeddings.embeddings_pb2_grpc import (
    EmbeddingsService,
    EmbeddingsServiceServicer,
    EmbeddingsServiceStub,
)
from .completion.completion_pb2 import (
    CompletionRequest,
    CompletionResponse,
    CompletionChoice,
    CompletionUsage, 
    CompletionFinishReason,
)
from .completion.completion_pb2_grpc import (
    CompletionService,
    CompletionServiceServicer,
    CompletionServiceStub,
    CompletionStreamService,
    CompletionStreamServiceServicer,
    CompletionStreamServiceStub,
)
from .chat.chat_pb2 import (
    ChatCompletionRequest,
    ChatRole,
    ChatItem,
    ChatCompletionChoice,
    ChatCompletionResponse,
)
from .chat.chat_pb2_grpc import (
    ChatCompletionService,
    ChatCompletionServiceServicer,
    ChatCompletionServiceStub,
    ChatCompletionStreamService,
    ChatCompletionStreamServiceServicer,
    ChatCompletionStreamServiceStub,
)
from .name.name_pb2 import NameResponse
from .name.name_pb2_grpc import NameService, NameServiceServicer, NameServiceStub
from .serve import serve

print("Initializing Leapfrog")

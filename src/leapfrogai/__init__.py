# __init__.py


from grpc import ServicerContext as GrpcContext

from leapfrogai.audio.audio_pb2 import AudioMetadata, AudioRequest, AudioResponse
from leapfrogai.audio.audio_pb2_grpc import Audio, AudioServicer, AudioStub
from leapfrogai.chat.chat_pb2 import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatItem,
    ChatRole,
)
from leapfrogai.chat.chat_pb2_grpc import (
    ChatCompletionService,
    ChatCompletionServiceServicer,
    ChatCompletionServiceStub,
    ChatCompletionStreamService,
    ChatCompletionStreamServiceServicer,
    ChatCompletionStreamServiceStub,
)
from leapfrogai.completion.completion_pb2 import (
    CompletionChoice,
    CompletionFinishReason,
    CompletionRequest,
    CompletionResponse,
    CompletionUsage,
)
from leapfrogai.completion.completion_pb2_grpc import (
    CompletionService,
    CompletionServiceServicer,
    CompletionServiceStub,
    CompletionStreamService,
    CompletionStreamServiceServicer,
    CompletionStreamServiceStub,
)
from leapfrogai.config import BackendConfig
from leapfrogai.embeddings.embeddings_pb2 import (
    Embedding,
    EmbeddingRequest,
    EmbeddingResponse,
)
from leapfrogai.embeddings.embeddings_pb2_grpc import (
    EmbeddingsService,
    EmbeddingsServiceServicer,
    EmbeddingsServiceStub,
)
from leapfrogai.name.name_pb2 import NameResponse
from leapfrogai.name.name_pb2_grpc import (
    NameService,
    NameServiceServicer,
    NameServiceStub,
)
from leapfrogai.serve import serve

print("Initializing Leapfrog")

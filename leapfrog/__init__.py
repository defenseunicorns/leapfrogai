# __init__.py


from .generate.generate_pb2_grpc import CompletionService,CompletionServiceServicer,CompletionServiceStub
from .generate.generate_pb2 import CompletionRequest,CompletionResponse
from .embeddings.embeddings_pb2 import EmbeddingRequest,EmbeddingResponse, Embedding
from .embeddings.embeddings_pb2_grpc import EmbeddingsService,EmbeddingsServiceServicer,EmbeddingsServiceStub
from .name.name_pb2 import NameResponse
from .name.name_pb2_grpc import NameServiceStub,NameService,NameServiceServicer
from .audio.audio_pb2 import AudioRequest,AudioResponse
from .audio.audio_pb2_grpc import AudioServicer, AudioStub, Audio
from .name.name_pb2_grpc import NameService,NameServiceServicer,NameServiceStub
from .name.name_pb2 import NameResponse
from .serve import serve
from grpc import ServicerContext as GrpcContext


print("Initializing Leapfrog")

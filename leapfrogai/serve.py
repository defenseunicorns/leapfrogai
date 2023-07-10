from concurrent import futures

import grpc

from .audio import audio_pb2_grpc
from .chat import chat_pb2_grpc
from .embeddings import embeddings_pb2_grpc
from .completion import completion_pb2_grpc
from .name import name_pb2_grpc


def serve(o):
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))

    if hasattr(o, "ChatComplete"):
        chat_pb2_grpc.add_ChatCompletionServiceServicer_to_server(o, server)

    if hasattr(o, "ChatCompleteStream"):
        chat_pb2_grpc.add_ChatCompletionStreamServiceServicer_to_server(o, server)

    if hasattr(o, "LLMConfig"):
        completion_pb2_grpc.add_LLMConfigServiceServicer_to_server(o, server)

    if hasattr(o, "Complete"):
        completion_pb2_grpc.add_CompletionServiceServicer_to_server(o, server)

    if hasattr(o, "CompleteStream"):
        completion_pb2_grpc.add_CompletionStreamServiceServicer_to_server(o, server)

    if hasattr(o, "CreateEmbedding"):
        embeddings_pb2_grpc.add_EmbeddingsServiceServicer_to_server(o, server)

    if hasattr(o, "Name"):
        name_pb2_grpc.add_NameServiceServicer_to_server(o, server)

    if hasattr(o, "Transcribe") and hasattr(o, "Translate"):
        audio_pb2_grpc.add_AudioServicer_to_server(o, server)

    # Listen on port 50051
    print("Starting server. Listening on port 50051.")
    server.add_insecure_port("[::]:50051")
    server.start()

    # block the thread until the server terminates...without using async to await the completion
    # of all requests, this is the best we can do to gracefully wait while the server responds to requests
    server.wait_for_termination()

from concurrent import futures

import grpc

from .audio import audio_pb2_grpc
from .embeddings import embeddings_pb2_grpc
from .generate import generate_pb2_grpc
from .name import name_pb2_grpc


def serve(o):
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

    if hasattr(o, "Complete"):
        generate_pb2_grpc.add_CompletionServiceServicer_to_server(o, server)

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
    server.wait_for_termination()

    # Keep thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

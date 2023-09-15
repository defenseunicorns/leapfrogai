from concurrent import futures
import grpc

from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from grpc_reflection.v1alpha import reflection

from .audio import audio_pb2_grpc
from .chat import chat_pb2_grpc
from .embeddings import embeddings_pb2_grpc
from .completion import completion_pb2_grpc
from .name import name_pb2_grpc


async def serve(o):
    # Create a tuple of all of the services we want to export via reflection.
    services = (reflection.SERVICE_NAME, health.SERVICE_NAME)

    # Create a gRPC server
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=40))

    if hasattr(o, "ChatComplete"):
        chat_pb2_grpc.add_ChatCompletionServiceServicer_to_server(o, server)
        services += ("chat.ChatCompletionService",)

    if hasattr(o, "ChatCompleteStream"):
        chat_pb2_grpc.add_ChatCompletionStreamServiceServicer_to_server(o, server)
        services += ("chat.ChatCompletionStreamService",)

    if hasattr(o, "Complete"):
        completion_pb2_grpc.add_CompletionServiceServicer_to_server(o, server)
        services += ("completion.CompletionService",)

    if hasattr(o, "CompleteStream"):
        completion_pb2_grpc.add_CompletionStreamServiceServicer_to_server(o, server)
        services += ("completion.CompletionStreamService",)

    if hasattr(o, "CreateEmbedding"):
        embeddings_pb2_grpc.add_EmbeddingsServiceServicer_to_server(o, server)
        services += ("embeddings.EmbeddingsService",)

    if hasattr(o, "Name"):
        name_pb2_grpc.add_NameServiceServicer_to_server(o, server)
        services += ("name.NameService",)

    if hasattr(o, "Transcribe") and hasattr(o, "Translate"):
        audio_pb2_grpc.add_AudioServicer_to_server(o, server)
        services += ("audio.Audio",)

    # Do reflection things to list all the gRPC services (allows for `grpcurl --plaintext localhost:50051 list`)
    reflection.enable_server_reflection(services, server)

    # Create a health_servicer and list all services as 'healthy'
    # NOTE: Health checks can be validated via `grpcurl --plaintext -d {"service": "SERVICE_NAME"}' localhost:50051 grpc.health.v1.Health/Check`
    health_servicer = health.HealthServicer(experimental_non_blocking=True)
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    for service in services:
        # TODO: I still need to modify the protos for the services to add a 'check' endpoint
        health_servicer.set(service, health_pb2.HealthCheckResponse.SERVING)

    # Listen on port 50051
    print("Starting server. Listening on port 50051.")
    server.add_insecure_port("[::]:50051")
    await server.start()

    # block the thread until the server terminates...without using async to await the completion
    # of all requests, this is the best we can do to gracefully wait while the server responds to requests
    await server.wait_for_termination()

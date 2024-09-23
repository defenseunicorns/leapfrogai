import asyncio
import signal
from concurrent import futures

import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

from leapfrogai_sdk.audio import audio_pb2_grpc
from leapfrogai_sdk.chat import chat_pb2_grpc
from leapfrogai_sdk.completion import completion_pb2_grpc
from leapfrogai_sdk.counting import counting_pb2_grpc
from leapfrogai_sdk.embeddings import embeddings_pb2_grpc
from leapfrogai_sdk.name import name_pb2_grpc


async def serve(o, host="0.0.0.0", port=50051):
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

    if hasattr(o, "CountTokens"):
        counting_pb2_grpc.add_TokenCountServiceServicer_to_server(o, server)
        services += ("counting.TokenCountService",)

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
    server.add_insecure_port("{}:{}".format(host, port))
    print("Starting server. Listening on {}:{}.".format(host, port))
    await server.start()

    # Setup graceful shutdown
    shutdown_event = asyncio.Event()

    def signal_handler(*_):
        print("Shutdown signal received")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    # Wait for shutdown signal
    await shutdown_event.wait()

    # Properly shutdown the server
    await server.stop(5)
    print("Server has been shut down")

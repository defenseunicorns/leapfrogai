from concurrent import futures
import grpc
import generate_pb2
import generate_pb2_grpc
import name_pb2
import name_pb2_grpc
import embeddings_pb2
import embeddings_pb2_grpc
import audio_pb2
import audio_pb2_grpc
import logging

class Repeater(generate_pb2_grpc.GenerateServiceServicer):
    def Complete(self, request, context):

        result = request.prompt # just returns what's provided
        print(f"Repeater.Complete:  { request }")
        return generate_pb2.CompletionResponse(completion=result)

    def CreateEmbedding(self, request, context):
        return embeddings_pb2.EmbeddingResponse(
            embeddings=["a;fdlkajd;fakjdf;lakdjf"]
        )

    def Name(self, request, context):
        return name_pb2.NameResponse ( name = "repeater" )




def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    r = Repeater()
    generate_pb2_grpc.add_GenerateServiceServicer_to_server(r, server)
    embeddings_pb2_grpc.add_GenerateServiceServicer_to_server(r, server)
    name_pb2_grpc.add_NameServiceServicer_to_server(r, server)
    audio_pb2_grpc.add_GenerateServiceServicer_to_server(r, server)

    # Listen on port 50051
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

    # Keep thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
from concurrent import futures
import grpc
import generate_pb2
import generate_pb2_grpc


class Repeater(object):
    def Complete(self, request, context):

        result = request.prompt # just returns what's provided
        return generate_pb2.CompletionResponse(completion=result)


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    generate_pb2_grpc.add_GenerateServiceServicer_to_server(Repeater(), server)

    # Listen on port 50051
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()

    # Keep thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
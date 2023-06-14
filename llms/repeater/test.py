import grpc
import generate_pb2
import generate_pb2_grpc
import embeddings_pb2_grpc
import embeddings_pb2
import name_pb2_grpc
import name_pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

def run():
    # Set up a channel to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        # Instantiate a stub (client)
        stub = generate_pb2_grpc.GenerateServiceStub(channel)

        # Create a request
        request = generate_pb2.CompletionRequest(
            prompt="Hello, Chatbot!",
            # add other parameters as necessary
        )

        # Make a call to the server and get a response
        response = stub.Complete(request)

        # Print the response
        print("Received response: ", response.completion)

        name = name_pb2_grpc.NameServiceStub(channel)
        response = name.Name(google_dot_protobuf_dot_empty__pb2.Empty())
        print(f"Recieved name: { response }")

        embed = embeddings_pb2_grpc.GenerateServiceStub(channel)
        r = embed.CreateEmbedding(embeddings_pb2.EmbeddingRequest(
            inputs=["foobar"]
        ))
        print(f"Recieved embedding: { r }")
if __name__ == "__main__":
    run()
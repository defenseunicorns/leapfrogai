from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)
import grpc
import leapfrog
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

def run():
    # Set up a channel to the server
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        # Instantiate a stub (client)
        stub = leapfrog.CompletionServiceStub(channel)

        # Create a request
        request = leapfrog.CompletionRequest(
            prompt="Hello, Chatbot!",
            max_tokens=150,
            # add other parameters as necessary
        )

        # Make a call to the server and get a response
        response = stub.Complete(request)

        # Print the response
        print("Received response: ", response.completion)

        name = leapfrog.NameServiceStub(channel)
        response = name.Name(google_dot_protobuf_dot_empty__pb2.Empty())
        print(f"Recieved name: { response }")

        embed = leapfrog.EmbeddingsServiceStub(channel)
        r = embed.CreateEmbedding(leapfrog.EmbeddingRequest(
            inputs=["foobar"]
        ))
        print(f"Recieved embedding: { r }")
if __name__ == "__main__":
    run()
import grpc
import generate_pb2
import generate_pb2_grpc

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

if __name__ == "__main__":
    run()
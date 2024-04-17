import sys
from pathlib import Path
import grpc

# from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

import leapfrogai_sdk

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)


def run():
    # Set up a channel to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        # Instantiate a stub (client)
        stub = leapfrogai_sdk.CompletionServiceStub(channel)

        # Create a request
        request = leapfrogai_sdk.CompletionRequest(
            prompt="This is a story about a cat named whiskers:\n",
            max_new_tokens=150,
            temperature=0.7,
            # add other parameters as necessary
        )

        # Make a call to the server and get a response
        response = stub.Complete(request)

        # Print the response
        print("Received response: ", response)

        # Check the healthcheck endpoitn
        health_stub = health_pb2_grpc.HealthStub(channel)
        health_request = health_pb2.HealthCheckRequest()
        health_resp = health_stub.Check(health_request)
        print("Response of health stub: ", health_resp)

        # name = leapfrogai_sdk.NameServiceStub(channel)
        # response = name.Name(google_dot_protobuf_dot_empty__pb2.Empty())
        # print(f"Recieved name: { response }")

        # embed = leapfrogai_sdk.EmbeddingsServiceStub(channel)
        # r = embed.CreateEmbedding(leapfrogai_sdk.EmbeddingRequest(inputs=["foobar"]))
        # print(f"Recieved embedding: { r }")


if __name__ == "__main__":
    run()

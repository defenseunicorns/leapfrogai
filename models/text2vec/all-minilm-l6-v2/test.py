import sys
from pathlib import Path

import grpc

import leapfrogai

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)


def run():
    # Set up a channel to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        embed = leapfrogai.EmbeddingsServiceStub(channel)
        r: leapfrogai.EmbeddingResponse = embed.CreateEmbedding(
            leapfrogai.EmbeddingRequest(inputs=["foobar"])
        )

        print(f"Recieved embedding: { r }")


if __name__ == "__main__":
    run()

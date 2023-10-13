import os
import sys
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)
import grpc

import leapfrogai


def read_iterfile(filepath, chunk_size=1024, language="en"):
    metadata = leapfrogai.AudioMetadata(
        prompt=None, temperature=0.0, inputlanguage=language
    )
    yield leapfrogai.AudioRequest(metadata=metadata)
    with open(filepath, mode="rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                entry_request = leapfrogai.AudioRequest(chunk_data=chunk)
                yield entry_request
            else:  # The chunk was empty, which means we're at the end of the file
                return


def run():
    # Set up a channel to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = leapfrogai.AudioStub(channel)
        response: leapfrogai.AudioResponse = stub.Transcribe(
            read_iterfile("geohot.m4a")
        )
        print(f"Received Transcription: {response.text}")


if __name__ == "__main__":
    run()

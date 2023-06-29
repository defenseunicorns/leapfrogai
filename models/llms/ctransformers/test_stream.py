import copy
import sys
from pathlib import Path
from typing import Iterator

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)
import grpc

import leapfrogai

system_prompt = """Below is an instruction that describes a task. Write a response that appropriately completes the request.
### Instruction:
Tell me a story about cats
### Response:
"""


class Completion:
    text: str

    def __init__(self, completion):
        self.text = completion.completion


def run():
    # Set up a channel to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        # Instantiate a stub (client)

        stub = leapfrogai.CompletionStreamServiceStub(channel)

        # Create a request
        request = leapfrogai.CompletionRequest(
            prompt=system_prompt,
            max_tokens=512,
            temperature=1.0,
        )

        # Make a call to the server and get a response
        response: Iterator[leapfrogai.CompletionResponse] = stub.CompleteStream(request)

        for text in response:
            print(text, end="")


if __name__ == "__main__":
    run()

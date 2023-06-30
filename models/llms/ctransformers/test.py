import copy
import sys
from pathlib import Path
from typing import Iterator

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)
import grpc

import leapfrogai

system_prompt = """<|im_start|>system
You are an AI assistant that answers participates in chat discussions in an honest, concise, friendly way.<|im_end|>
<|im_start|>user
Write two sequences composed of 3 'A's and 2 'B's such that there are no two successive identical letter. Be concise.<|im_end|>
<|im_assistant|>
"""


class Completion:
    text: str

    def __init__(self, completion):
        self.text = completion.completion


def run():
    # Set up a channel to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        # Instantiate a stub (client)

        stub = leapfrogai.CompletionServiceStub(channel)

        # Create a request
        request = leapfrogai.CompletionRequest(
            prompt=system_prompt,
            max_new_tokens=512,
            temperature=1.0,
        )

        # Make a call to the server and get a response
        response: leapfrogai.CompletionResponse = stub.Complete(request)

        print(response)


if __name__ == "__main__":
    run()

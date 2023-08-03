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
Write a story about a frog who leaps<|im_end|>
<|im_start|>assistant
"""

def run():
    # Set up a channel to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        # Instantiate a stub (client)

        stub = leapfrogai.CompletionStreamServiceStub(channel)

        # Create a request
        request = leapfrogai.CompletionRequest(
            prompt=system_prompt,
            max_new_tokens=512,
            temperature=1.0,
        )

        # Make a call to the server and get a response
        response: Iterator[leapfrogai.CompletionResponse] = stub.CompleteStream(request)

        for completion in response:
            print(completion.choices[0].text, end="", flush=True)


if __name__ == "__main__":
    run()

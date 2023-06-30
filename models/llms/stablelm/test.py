import sys
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)
import grpc

import leapfrogai

system_prompt = """<|SYSTEM|># StableLM Tuned (Alpha version)
- StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
- StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
- StableLM is more than just an information source, StableLM is also able to write poetry, short stories, and make jokes.
- StableLM will refuse to participate in anything that could harm a human.
"""

prompt = f"{system_prompt}<|USER|>What's your mood today?<|ASSISTANT|>"


def run():
    # Set up a channel to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        # Instantiate a stub (client)
        stub = leapfrogai.CompletionServiceStub(channel)

        # Create a request
        request = leapfrogai.CompletionRequest(
            prompt=prompt,
            max_tokens=64,
            temperature=0.01,
        )

        # Make a call to the server and get a response
        response = stub.Complete(request)

        # Print the response
        print("Received response: ", response)


if __name__ == "__main__":
    run()

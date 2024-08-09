"""Conformance test the LeapfrogAI API against the OpenAI spec."""

import os
from pathlib import Path
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types import FileObject, FileDeleted
import pytest
from deepdiff import DeepDiff

### CONSTANTS ###
LEAPFROGAI_MODEL = "vllm"
OPENAI_MODEL = "gpt-4o-mini"
CHAT_PARAMS = [
    (
        (LEAPFROGAI_MODEL, OPENAI_MODEL),  # (LeapfrogAI model, OpenAI model)
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
        ],
    ),
]


@pytest.fixture
def openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@pytest.fixture
def leapfrogai_client():
    return OpenAI(
        base_url=os.getenv("LEAPFROGAI_API_URL"),
        api_key=os.getenv("LEAPFROGAI_API_KEY"),
    )


@pytest.fixture
def text_file_path():
    return Path(os.path.dirname(__file__) + "/../../data/test.txt")


@pytest.fixture(params=[("openai", OPENAI_MODEL), ("leapfrogai", LEAPFROGAI_MODEL)])
def client_and_model(request, openai_client, leapfrogai_client):
    if request.param[0] == "openai":
        return openai_client, request.param[1]
    elif request.param[0] == "leapfrogai":
        return leapfrogai_client, request.param[1]


def print_diff_structure(d, indent=0):
    if isinstance(d, dict):
        for key, value in d.items():
            print("  " * indent + str(key) + ":", end="")
            if isinstance(value, (dict, list)):
                print()
                print_diff_structure(value, indent + 1)
            else:
                print(" " + str(value))
    elif isinstance(d, list):
        for item in d:
            print_diff_structure(item, indent)
    else:
        print(" " + str(d))


def compare_responses(lfai_response, openai_response):
    # Compare structures and highlight differences
    diff = DeepDiff(lfai_response, openai_response, ignore_order=True)

    if diff:
        diff_dict = diff.to_dict()

        # Replace "old" with "lfai" and "new" with "openai" in the diff
        def replace_strings(obj):
            if isinstance(obj, dict):
                return {
                    k.replace("old", "lfai").replace("new", "openai"): replace_strings(
                        v
                    )
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [replace_strings(item) for item in obj]
            elif isinstance(obj, str):
                return obj.replace("old", "lfai").replace("new", "openai")
            else:
                return obj

        diff_dict = replace_strings(diff_dict)

        print_diff_structure(diff_dict)


@pytest.mark.parametrize("models,messages", CHAT_PARAMS)
def test_chat_completion(openai_client, leapfrogai_client, models, messages):
    """Conformance test for the chat completion endpoint."""
    lfai_model, openai_model = models
    results = {}

    for client, model, client_name in [
        (leapfrogai_client, lfai_model, "LeapfrogAI"),
        (openai_client, openai_model, "OpenAI"),
    ]:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )

        assert isinstance(response, ChatCompletion)
        assert response.choices[0].message.role == "assistant"
        assert len(response.choices[0].message.content) > 0

        # Convert the response to a dictionary
        response_dict = response.model_dump()
        results[client_name] = {"model": model, "response": response_dict}

    assert (
        results["LeapfrogAI"]["response"]["object"]
        == results["OpenAI"]["response"]["object"]
        == "chat.completion"
    )

    # TODO: LeapfrogAI currently returns `FinishReason.STOP` while OpenAI returns `stop`
    # assert results["LeapfrogAI"]["response"]["finish_reason"] == results["OpenAI"]["response"]["finish_reason"] == "complete"

    # Compare responses
    print("\nConformance for test_chat_completion:")
    compare_responses(results["LeapfrogAI"]["response"], results["OpenAI"]["response"])


@pytest.mark.parametrize("models,messages", CHAT_PARAMS)
def test_chat_completion_streaming(openai_client, leapfrogai_client, models, messages):
    """Conformance test for the chat completion endpoint with streaming."""
    lfai_model, openai_model = models
    results = {}

    for client, model, client_name in [
        (leapfrogai_client, lfai_model, "LeapfrogAI"),
        (openai_client, openai_model, "OpenAI"),
    ]:
        stream = client.chat.completions.create(
            model=model, messages=messages, stream=True
        )
        accumulated_content = ""
        for chunk in stream:
            assert isinstance(chunk, ChatCompletionChunk)
            assert chunk.object == "chat.completion.chunk"
            if chunk.choices[0].delta.content is not None:
                accumulated_content += chunk.choices[0].delta.content
        assert len(accumulated_content) > 0

        results[client_name] = {"model": model, "response": accumulated_content}

    print("\nConformance for test_chat_completion_streaming:")
    compare_responses(results["LeapfrogAI"]["response"], results["OpenAI"]["response"])


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])


@pytest.mark.parametrize("models", CHAT_PARAMS)
def test_files(openai_client, leapfrogai_client, text_file_path, models):
    """Conformance test the files endpoint."""

    lfai_model, openai_model = models
    results = {}

    for client, model, client_name in [
        (leapfrogai_client, lfai_model, "LeapfrogAI"),
        (openai_client, openai_model, "OpenAI"),
    ]:
        # Create file
        create_file_response = client.files.create(
            file=text_file_path,
            purpose="assistants",
        )
        assert isinstance(create_file_response, FileObject)
        assert create_file_response.id is not None

        # Retrieve file
        get_file_response = client.files.retrieve(file_id=create_file_response.id)
        assert isinstance(get_file_response, FileObject)

        # # List files
        list_files_response = client.files.list()
        assert any(
            file.id == create_file_response.id for file in list_files_response.data
        )

        # Delete file
        delete_file_response = client.files.delete(file_id=create_file_response.id)
        assert isinstance(delete_file_response, FileDeleted)

        results[client_name] = {
            "model": model,
            "create_file_response": create_file_response.model_dump(),
            "get_file_response": get_file_response.model_dump(),
            "list_files_response": [
                file
                for file in list_files_response.data
                if file.id == create_file_response.id
            ],  # Only include the created file
            "delete_file_response": delete_file_response.model_dump(),
        }

    assert (
        results["LeapfrogAI"]["create_file_response"]["object"]
        == results["OpenAI"]["create_file_response"]["object"]
        == "file"
    )
    assert (
        results["LeapfrogAI"]["create_file_response"]["purpose"]
        == results["OpenAI"]["create_file_response"]["purpose"]
        == "assistants"
    )
    assert (
        results["LeapfrogAI"]["create_file_response"]["filename"]
        == results["OpenAI"]["create_file_response"]["filename"]
        == text_file_path.name
    )
    # TODO: Leapfrogai currently returns `status: uploaded` while OpenAI returns `status: processed`

    # Compare responses
    print("\nConformance for create file:")
    compare_responses(
        results["LeapfrogAI"]["create_file_response"],
        results["OpenAI"]["create_file_response"],
    )
    print("\nConformance for get file:")
    compare_responses(
        results["LeapfrogAI"]["get_file_response"],
        results["OpenAI"]["get_file_response"],
    )
    print("\nConformance for list files:")
    compare_responses(
        results["LeapfrogAI"]["list_files_response"],
        results["OpenAI"]["list_files_response"],
    )
    print("\nConformance for delete file:")
    compare_responses(
        results["LeapfrogAI"]["delete_file_response"],
        results["OpenAI"]["delete_file_response"],
    )


# TODO: Create tests for vector stores, runs, messages, threads, etc.
# TODO: Specifically test for annotations while doing file search.

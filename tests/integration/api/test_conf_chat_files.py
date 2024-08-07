import pytest
import os
from pathlib import Path
from openai import OpenAI
from openai.types.beta.threads.annotation import (
    FileCitationAnnotation,
    FilePathAnnotation,
)

LEAPFROGAI_MODEL = "vllm"
OPENAI_MODEL = "gpt-4o-mini"
MESSAGES = [
    {"role": "assistant", "content": "Hello how can I help you today?"},
    {"role": "user", "content": "Who is Sam?"},
]


def text_file_path():
    return Path(os.path.dirname(__file__) + "/../../data/test_with_data.txt")


def openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def leapfrogai_client():
    return OpenAI(
        base_url=os.getenv("LEAPFROGAI_API_URL"),
        api_key=os.getenv("LEAPFROGAI_API_KEY"),
    )


def client_config_factory(client_name):
    if client_name == "openai":
        return dict(client=openai_client(), model=OPENAI_MODEL)
    elif client_name == "leapfrogai":
        return dict(client=leapfrogai_client(), model=LEAPFROGAI_MODEL)


def make_test_assistant(client, model):
    vector_store = client.beta.vector_stores.create(name="Test data")

    file_streams = [open(text_file_path(), "rb")]

    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    assistant = client.beta.assistants.create(
        name="Test Assistant",
        instructions="You must provide a response based on the attached files.",
        model=model,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    return assistant


def make_test_thread(client):
    thread = client.beta.threads.create(messages=MESSAGES)
    return thread


def make_test_run(client, assistant, thread):
    run = client.beta.threads.runs.create_and_poll(
        assistant_id=assistant.id, thread_id=thread.id
    )
    return run


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_file_annotations(client_name):
    config = client_config_factory(client_name)
    client = config["client"]  # shorthand
    assistant = make_test_assistant(client, config["model"])
    thread = make_test_thread(client)
    run = make_test_run(client, assistant, thread)

    messages = list(
        client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    )

    message_content = messages[0].content[0].text
    annotations = message_content.annotations

    # Check message return type
    assert isinstance(message_content.value, str)

    # Check annotations return type
    for annot in annotations:
        assert isinstance(annot, (FileCitationAnnotation, FilePathAnnotation))

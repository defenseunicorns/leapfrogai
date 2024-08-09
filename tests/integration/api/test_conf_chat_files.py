import pytest
import os
from pathlib import Path
from openai import OpenAI
from openai.types.beta.threads.annotation import (
    FileCitationAnnotation,
    FilePathAnnotation,
)
from openai.types.beta.vector_store import VectorStore
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread


LEAPFROGAI_MODEL = "llama-cpp-python"
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


def make_vector_store_batched(client):
    vector_store = client.beta.vector_stores.create(name="Test data")

    file_streams = [open(text_file_path(), "rb")]

    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    return vector_store.id


def make_vector_store(client):
    vector_store = client.beta.vector_stores.create(name="Test data")
    with open(text_file_path(), "rb") as file:
        client.beta.vector_stores.files.upload(
            vector_store_id=vector_store.id, file=file
        )
    return vector_store


def make_test_assistant(client, model, vector_store_id):
    assistant = client.beta.assistants.create(
        name="Test Assistant",
        instructions="You must provide a response based on the attached files.",
        model=model,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
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
def test_vector_store(client_name):
    config = client_config_factory(client_name)
    client = config["client"]  # shorthand

    vector_store = make_vector_store(client)

    assert isinstance(vector_store, VectorStore)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_assistant(client_name):
    config = client_config_factory(client_name)
    client = config["client"]

    vector_store = make_vector_store(client)
    assistant = make_test_assistant(client, config["model"], vector_store.id)

    assert isinstance(assistant, Assistant)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_thread(client_name):
    config = client_config_factory(client_name)
    client = config["client"]

    thread = make_test_thread(client)

    assert isinstance(thread, Thread)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_file_annotations(client_name):
    config = client_config_factory(client_name)
    client = config["client"]  # shorthand

    vector_store = make_vector_store(client)
    assistant = make_test_assistant(client, config["model"], vector_store.id)
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

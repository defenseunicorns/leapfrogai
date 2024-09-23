import pytest
from openai.types.beta.threads.annotation import (
    FileCitationAnnotation,
    FilePathAnnotation,
)
from openai.types.beta.threads.text import Text
from openai.types.beta.threads.message import Message
import re

from ..utils.client import client_config_factory, text_file_path


def make_vector_store_with_file(client):
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


def make_test_run(client, assistant, thread):
    run = client.beta.threads.runs.create_and_poll(
        assistant_id=assistant.id, thread_id=thread.id
    )
    return run


def validate_annotation_format(annotation):
    pattern = r"【\d+:\d+†source】"
    match = re.fullmatch(pattern, annotation)
    return match is not None


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_thread_file_annotations(client_name):
    config = client_config_factory(client_name)
    client = config.client  # shorthand

    vector_store = make_vector_store_with_file(client)
    assistant = make_test_assistant(client, config.model, vector_store.id)
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Who is Sam?",
    )
    run = make_test_run(client, assistant, thread)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id, run_id=run.id
    ).data

    # Runs will only have the messages that were generated by the run, not previous messages
    assert len(messages) == 1
    assert all(isinstance(message, Message) for message in messages)

    # Get the response content
    message_content = messages[0].content[0].text
    assert isinstance(message_content, Text)

    # Check annotations return type
    for a in message_content.annotations:
        assert isinstance(a, (FileCitationAnnotation, FilePathAnnotation))
        assert validate_annotation_format(a.text) is True
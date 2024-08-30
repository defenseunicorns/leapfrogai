import pytest
from openai.types.beta.threads import Run, Message, TextContentBlock, Text

from .utils import client_config_factory


def make_mock_message_object(role, message_text):
    Message(
        id="",
        thread_id="",
        created_at=0,
        object="thread.message",
        status="in_progress",
        role=role,
        content=[
            TextContentBlock(text=Text(value=message_text, annotations=[]), type="text")
        ],
    )


def make_mock_message_simple(role, message_text):
    return dict(role=role, content=message_text)


mock_message = make_mock_message_simple(role="user", message_text="Hello world!")


@pytest.mark.parametrize(
    "client_name, test_messages",
    [
        ("openai", []),
        ("openai", [mock_message]),
        ("leapfrogai", []),
        ("leapfrogai", [mock_message]),
    ],
)
def test_run_completion(client_name, test_messages):
    # Setup
    config = client_config_factory(client_name)
    client = config["client"]

    assistant = client.beta.assistants.create(
        name="Test Assistant",
        instructions="You must provide a response based on the attached files.",
        model=config["model"],
    )
    thread = client.beta.threads.create()

    for m in test_messages:
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role=m["role"],
            content=m["content"],
        )

    # Run the test
    run = client.beta.threads.runs.create_and_poll(
        assistant_id=assistant.id, thread_id=thread.id
    )

    # Check results
    messages = client.beta.threads.messages.list(
        thread_id=thread.id, run_id=run.id
    ).data
    assert len(messages) >= 1
    assert isinstance(run, Run)

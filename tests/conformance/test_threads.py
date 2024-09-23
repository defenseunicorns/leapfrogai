import pytest
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Message, TextContentBlock, Text

from tests.utils.client import client_config_factory


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


mock_message = make_mock_message_simple(role="user", message_text="Who is Sam?")


@pytest.mark.parametrize(
    "client_name, test_messages",
    [
        ("openai", []),
        ("openai", [mock_message]),
        ("leapfrogai", []),
        ("leapfrogai", [mock_message]),
    ],
)
def test_thread(client_name, test_messages):
    config = client_config_factory(client_name)
    client = config.client

    thread = client.beta.threads.create(
        messages=test_messages
    )  # TODO: This breaks with LeapfrogAI

    assert isinstance(thread, Thread)

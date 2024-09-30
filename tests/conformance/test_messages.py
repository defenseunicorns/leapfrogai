import pytest

from openai.types.beta.threads.message import Message

from tests.utils.client import client_config_factory


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_message_create(client_name):
    config = client_config_factory(client_name)
    client = config.client

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="mock data",
    )

    assert isinstance(message, Message)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_message_list(client_name):
    config = client_config_factory(client_name)
    client = config.client

    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="mock data",
    )

    messages = client.beta.threads.messages.list(thread_id=thread.id)

    assert len(messages.data) == 1
    assert all(isinstance(message, Message) for message in messages.data)

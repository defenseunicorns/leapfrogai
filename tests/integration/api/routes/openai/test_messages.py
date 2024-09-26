"""Test the API endpoints for assistants."""

import pytest
from fastapi import status
from openai.types.beta import Thread, ThreadDeleted
from openai.types.beta.threads import TextContentBlock, Text, Message, MessageDeleted

from leapfrogai_api.typedef.messages import CreateMessageRequest, ModifyMessageRequest
from leapfrogai_api.typedef.threads import (
    CreateThreadRequest,
)
from tests.utils.client import LeapfrogAIClient


@pytest.fixture(scope="session")
def app_client():
    yield LeapfrogAIClient()


# Create a thread with the previously created file and fake embeddings
@pytest.fixture(scope="session")
def create_thread(app_client):
    """Create a thread for testing. Requires a running Supabase instance."""

    request = CreateThreadRequest(
        messages=None,
        tool_resources=None,
        metadata={},
    )

    return app_client.post("/openai/v1/threads", json=request.model_dump())


@pytest.fixture(scope="session")
def create_message(app_client, create_thread):
    """Create a message for testing. Requires a running Supabase instance."""

    request = CreateMessageRequest(
        role="user",
        content=[
            TextContentBlock(text=Text(value="test", annotations=[]), type="text")
        ],
        attachments=None,
        metadata={},
    )

    message = app_client.post(
        f"/openai/v1/threads/{create_thread.json()['id']}/messages",
        json=request.model_dump(),
    )

    return {"message": message, "thread_id": create_thread.json()["id"]}


def test_create_thread(create_thread):
    """Test creating a thread. Requires a running Supabase instance."""
    assert create_thread.status_code == status.HTTP_200_OK
    assert Thread.model_validate(create_thread.json()), "Create should create a Thread."


def test_create_message(create_message):
    """Test creating a message. Requires a running Supabase instance."""
    assert create_message["message"].status_code == status.HTTP_200_OK
    assert Message.model_validate(
        create_message["message"].json()
    ), "Create should create a Message."


def test_get_message(app_client, create_message):
    """Test getting a messages. Requires a running Supabase instance."""
    message_id = create_message["message"].json()["id"]
    thread_id = create_message["thread_id"]
    get_response = app_client.get(
        f"/openai/v1/threads/{thread_id}/messages/{message_id}"
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert Message.model_validate(
        get_response.json()
    ), f"Get should return Message {message_id}."


def test_list_message(app_client, create_message):
    """Test listing messages. Requires a running Supabase instance."""
    thread_id = create_message["thread_id"]
    list_response = app_client.get(f"/openai/v1/threads/{thread_id}/messages")
    assert list_response.status_code == status.HTTP_200_OK
    for message_object in list_response.json()["data"]:
        assert Message.model_validate(
            message_object
        ), "Should return a list of Message."


def test_modify_message(app_client, create_message):
    """Test modifying a thread. Requires a running Supabase instance."""
    message_id = create_message["message"].json()["id"]
    thread_id = create_message["thread_id"]
    request = ModifyMessageRequest(
        metadata={"test": "modified"},
    )

    modify_response = app_client.post(
        f"/openai/v1/threads/{thread_id}/messages/{message_id}",
        json=request.model_dump(),
    )
    assert modify_response.status_code == status.HTTP_200_OK
    assert Message.model_validate(modify_response.json()), "Should return a Message."
    assert (
        modify_response.json()["metadata"]["test"] == "modified"
    ), "Should be modified."


def test_get_modified_message(app_client, create_message):
    """Test getting a modified threads. Requires a running Supabase instance."""
    message_id = create_message["message"].json()["id"]
    thread_id = create_message["thread_id"]
    get_modified_response = app_client.get(
        f"/openai/v1/threads/{thread_id}/messages/{message_id}"
    )
    assert get_modified_response.status_code == status.HTTP_200_OK
    assert Message.model_validate(
        get_modified_response.json()
    ), f"Get should return modified Message {message_id}."
    assert (
        get_modified_response.json()["metadata"]["test"] == "modified"
    ), "Should be modified."


def test_delete_message(app_client, create_message):
    """Test deleting a message. Requires a running Supabase instance."""
    message_id = create_message["message"].json()["id"]
    thread_id = create_message["thread_id"]
    delete_response = app_client.delete(
        f"/openai/v1/threads/{thread_id}/messages/{message_id}"
    )
    assert delete_response.status_code == status.HTTP_200_OK
    assert MessageDeleted.model_validate(
        delete_response.json()
    ), "Should return a MessageDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."


def test_delete_thread(app_client, create_thread):
    """Test deleting a thread. Requires a running Supabase instance."""
    thread_id = create_thread.json()["id"]
    delete_response = app_client.delete(f"/openai/v1/threads/{thread_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    assert ThreadDeleted.model_validate(
        delete_response.json()
    ), "Should return a ThreadDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."


def test_delete_twice_message(app_client, create_message):
    """Test deleting a message twice. Requires a running Supabase instance."""
    message_id = create_message["message"].json()["id"]
    thread_id = create_message["thread_id"]
    delete_response = app_client.delete(
        f"/openai/v1/threads/{thread_id}/messages/{message_id}"
    )
    assert delete_response.status_code == status.HTTP_200_OK
    assert MessageDeleted.model_validate(
        delete_response.json()
    ), "Should return a MessageDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), "Should not be able to delete twice."


def test_get_nonexistent_message(app_client, create_message):
    """Test getting a nonexistent message. Requires a running Supabase instance."""
    message_id = create_message["message"].json()["id"]
    thread_id = create_message["thread_id"]
    get_response = app_client.get(
        f"/openai/v1/threads/{thread_id}/messages/{message_id}"
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert (
        get_response.json() is None
    ), f"Get should not return deleted Message {message_id}."

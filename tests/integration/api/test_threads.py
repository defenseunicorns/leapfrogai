"""Test the API endpoints for assistants."""

import os
import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from openai.types.beta import Thread, ThreadDeleted
from openai.types.beta.thread import ToolResourcesCodeInterpreter, ToolResources
from openai.types.beta.threads import TextContentBlock, Text

from leapfrogai_api.typedef.threads import (
    CreateThreadRequest,
    ModifyThreadRequest,
)
from leapfrogai_api.typedef.messages import (
    CreateMessageRequest,
)
from leapfrogai_api.routers.openai.threads import router


class MissingEnvironmentVariable(Exception):
    pass


headers: dict[str, str] = {}

try:
    headers = {"Authorization": f"Bearer {os.environ['SUPABASE_USER_JWT']}"}
except KeyError as exc:
    raise MissingEnvironmentVariable(
        "SUPABASE_USER_JWT must be defined for the test to pass. "
        "Please check the api README for instructions on obtaining this token."
    ) from exc


@pytest.fixture(scope="session")
def app_client():
    with TestClient(router, headers=headers) as client:
        yield client


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


def test_code_interpreter_fails(app_client):
    """Test code interpreter fails."""

    tool_resources = ToolResources(
        code_interpreter=ToolResourcesCodeInterpreter(file_ids=["test"])
    )

    request = CreateThreadRequest(
        messages=None,
        tool_resources=tool_resources,
        metadata={},
    )

    with pytest.raises(HTTPException) as code_exc:
        app_client.post("/openai/v1/threads", json=request.model_dump())

    assert code_exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert code_exc.value.detail == f"Unsupported tool resource: {tool_resources}"


def test_create_thread(create_thread):
    """Test creating a thread. Requires a running Supabase instance."""
    assert create_thread.status_code == status.HTTP_200_OK
    assert Thread.model_validate(create_thread.json()), "Create should create a Thread."
    assert "user_id" not in create_thread.json(), "Create should not return a user_id."


def test_get_thread(app_client, create_thread):
    """Test getting a threads. Requires a running Supabase instance."""
    threads_id = create_thread.json()["id"]
    get_response = app_client.get(f"/openai/v1/threads/{threads_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert Thread.model_validate(
        get_response.json()
    ), f"Get should return Thread {threads_id}."


def test_modify_thread(app_client, create_thread):
    """Test modifying a thread. Requires a running Supabase instance."""
    thread_id = create_thread.json()["id"]
    request = ModifyThreadRequest(
        tool_resources=None,
        metadata={"test": "modified"},
    )

    modify_response = app_client.post(
        f"/openai/v1/threads/{thread_id}",
        json=request.model_dump(),
    )
    assert modify_response.status_code == status.HTTP_200_OK
    assert Thread.model_validate(modify_response.json()), "Should return a Thread."
    assert (
        modify_response.json()["metadata"]["test"] == "modified"
    ), "Should be modified."


def test_delete_thread(app_client, create_thread):
    """Test deleting a thread. Requires a running Supabase instance."""
    thread_id = create_thread.json()["id"]
    delete_response = app_client.delete(f"/openai/v1/threads/{thread_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    assert ThreadDeleted.model_validate(
        delete_response.json()
    ), "Should return a ThreadDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."


def test_delete_twice_thread(app_client, create_thread):
    """Test deleting a thread twice. Requires a running Supabase instance."""
    thread_id = create_thread.json()["id"]
    delete_response = app_client.delete(f"/openai/v1/threads/{thread_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    assert ThreadDeleted.model_validate(
        delete_response.json()
    ), "Should return a ThreadDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), "Should not be able to delete twice."


@pytest.mark.xfail
def test_get_nonexistent_thread(app_client, create_thread):
    """Test getting a nonexistent thread. Requires a running Supabase instance."""
    thread_id = create_thread.json()["id"]
    fail_response = app_client.get(f"/openai/v1/threads/{thread_id}")
    assert fail_response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        fail_response.json().get("detail") == "Thread not found"
    ), f"Get should not return deleted Thread {thread_id}."

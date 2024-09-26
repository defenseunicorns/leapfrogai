"""Test the API endpoints for assistants."""

import pytest
from fastapi import status
from openai.types.beta import Assistant, Thread, AssistantDeleted, ThreadDeleted
from openai.types.beta.thread import ToolResources, ToolResourcesFileSearch
from openai.types.beta.threads import Message, Text, TextContentBlock, Run

from leapfrogai_api.typedef.assistants import (
    CreateAssistantRequest,
)
from leapfrogai_api.typedef.messages import (
    CreateMessageRequest,
)
from leapfrogai_api.typedef.runs import (
    RunCreateParamsRequest,
)
from leapfrogai_api.typedef.threads import (
    CreateThreadRequest,
    ThreadRunCreateParamsRequest,
)
from tests.utils.client import LeapfrogAIClient, get_leapfrogai_model

starting_assistant = Assistant(
    id="",
    created_at=0,
    name="test",
    description="test",
    instructions="test",
    model=get_leapfrogai_model(),
    object="assistant",
    tools=[],
    tool_resources=None,
    temperature=1.0,
    top_p=1.0,
    metadata={},
    response_format="auto",
)


@pytest.fixture(scope="session")
def app_client():
    yield LeapfrogAIClient()


@pytest.fixture(scope="session")
def create_assistant(app_client):
    """Create an assistant for testing. Requires a running Supabase instance."""
    request = CreateAssistantRequest(
        model=starting_assistant.model,
        name=starting_assistant.name,
        description=starting_assistant.description,
        instructions=starting_assistant.instructions,
        tools=starting_assistant.tools,
        tool_resources=starting_assistant.tool_resources,
        metadata=starting_assistant.metadata,
        temperature=starting_assistant.temperature,
        top_p=starting_assistant.top_p,
        response_format=starting_assistant.response_format,
    )

    return app_client.post("/openai/v1/assistants", json=request.model_dump())


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


@pytest.fixture(scope="session")
def create_run(app_client, create_assistant, create_thread):
    """Create a run for testing. Requires a running Supabase instance."""
    assistant_id = create_assistant.json()["id"]
    thread_id = create_thread.json()["id"]

    request = RunCreateParamsRequest(
        assistant_id=assistant_id,
        instructions="You are a conversational assistant.",
        additional_instructions="Respond as a Unicorn assistant named Doug.",
        tool_resources=ToolResources(file_search={}),
        metadata={},
        stream=False,
    )

    return app_client.post(
        f"/openai/v1/threads/{thread_id}/runs", json=request.model_dump()
    )


def test_create_assistant(create_assistant):
    """Test creating an assistant. Requires a running Supabase instance."""
    assert create_assistant.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        create_assistant.json()
    ), "Create should create an Assistant."


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


def test_create_thread_and_run(app_client, create_assistant):
    """Test running an assistant. Requires a running Supabase instance."""
    assistant_id = create_assistant.json()["id"]

    request = ThreadRunCreateParamsRequest(
        assistant_id=assistant_id,
        instructions="You are a conversational assistant.",
        additional_instructions="Respond as a Unicorn assistant named Doug.",
        tool_resources=ToolResources(
            file_search=ToolResourcesFileSearch(vector_store_ids=[])
        ),
        metadata={},
        stream=False,
    )

    response = app_client.post("/openai/v1/threads/runs", json=request.model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert "'user_id'" not in response.json(), "Create should not return a user_id."
    assert Run.model_validate(response.json()), "Create should create a Run."


def test_create_run(create_run):
    """Test running an assistant. Requires a running Supabase instance."""

    assert create_run.status_code == status.HTTP_200_OK
    assert Run.model_validate(create_run.json()), "Create should create a Run."
    assert "user_id" not in create_run.json(), "Create should not return a user_id."


def test_list_runs(app_client, create_thread):
    """Test listing runs. Requires a running Supabase instance."""

    thread_id = create_thread.json()["id"]

    response = app_client.get(f"/openai/v1/threads/{thread_id}/runs")

    assert response.status_code == status.HTTP_200_OK
    for run in response.json()["data"]:
        assert Run.model_validate(run), "List should return a list of Runs."


def test_retrieve_run(app_client, create_run):
    """Test retrieving a run. Requires a running Supabase instance."""
    thread_id = create_run.json()["thread_id"]
    run_id = create_run.json()["id"]

    response = app_client.get(f"/openai/v1/threads/{thread_id}/runs/{run_id}")

    assert response.status_code == status.HTTP_200_OK
    assert Run.model_validate(response.json()), "Retrieve should return a Run."


def test_modify_run(app_client, create_run):
    """Test modifying a run. Requires a running Supabase instance."""
    thread_id = create_run.json()["thread_id"]
    run_id = create_run.json()["id"]
    updated_metadata = {
        "test": "testing",
    }

    response = app_client.post(
        f"/openai/v1/threads/{thread_id}/runs/{run_id}",
        json={"metadata": updated_metadata},
    )

    assert response.status_code == status.HTTP_200_OK
    assert Run.model_validate(response.json()), "Modify should return a Run."
    assert (
        response.json()["metadata"] == updated_metadata
    ), "Modify should return a Run with the modified metadata."


def test_delete_assistant(app_client, create_assistant):
    """Test deleting an assistant. Requires a running Supabase instance."""
    assistant_id = create_assistant.json()["id"]

    response = app_client.delete(f"/openai/v1/assistants/{assistant_id}")
    assert response.status_code is status.HTTP_200_OK
    assert AssistantDeleted.model_validate(
        response.json()
    ), "Should return a AssistantDeleted object."
    assert (
        response.json()["deleted"] is True
    ), f"Assistant {assistant_id} should be deleted."


def test_delete_threads(app_client, create_thread):
    """Test deleting a thread. Requires a running Supabase instance."""
    thread_id = create_thread.json()["id"]

    response = app_client.delete(f"/openai/v1/threads/{thread_id}")
    assert response.status_code is status.HTTP_200_OK
    assert ThreadDeleted.model_validate(
        response.json()
    ), "Should return a ThreadDeleted object."
    assert response.json()["deleted"] is True, f"Thread {thread_id} should be deleted."


def test_get_nonexistent_run(app_client, create_run):
    """Test retrieving a run that does not exist. Requires a running Supabase instance."""
    thread_id = create_run.json()["thread_id"]
    run_id = create_run.json()["id"]

    print(thread_id, run_id)

    response = app_client.get(f"/openai/v1/threads/{thread_id}/runs/{run_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": f"Run {run_id} not found for thread {thread_id}."
    }

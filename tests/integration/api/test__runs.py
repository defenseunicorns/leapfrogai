"""Test the API endpoints for assistants."""

import os
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from openai.types.beta import Assistant, Thread, AssistantDeleted, ThreadDeleted
from openai.types.beta.thread import ToolResources
from openai.types.beta.threads import Message, Text, TextContentBlock, Run
from leapfrogai_api.backend.types import CreateAssistantRequest
from leapfrogai_api.main import app
from leapfrogai_api.routers.openai.requests.create_message_request import (
    CreateMessageRequest,
)
from leapfrogai_api.routers.openai.requests.create_thread_request import (
    CreateThreadRequest,
)
from leapfrogai_api.routers.openai.requests.run_create_params_request import (
    RunCreateParamsRequestBaseRequest,
)
from leapfrogai_api.routers.openai.requests.thread_run_create_params_request import (
    ThreadRunCreateParamsRequestBaseRequest,
)

CHAT_MODEL = "test-chat"

LFAI_CONFIG_FILENAME = os.environ["LFAI_CONFIG_FILENAME"] = "test-config.yaml"
LFAI_CONFIG_PATH = os.environ["LFAI_CONFIG_PATH"] = os.path.join(
    os.path.dirname(__file__), "fixtures"
)
LFAI_CONFIG_FILEPATH = os.path.join(LFAI_CONFIG_PATH, LFAI_CONFIG_FILENAME)


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

starting_assistant = Assistant(
    id="",
    created_at=0,
    name="test",
    description="test",
    instructions="test",
    model=CHAT_MODEL,
    object="assistant",
    tools=[{"type": "file_search"}],
    tool_resources={},
    temperature=1.0,
    top_p=1.0,
    metadata={},
    response_format="auto",
)


@pytest.fixture(scope="session")
def app_client():
    with TestClient(app, headers=headers) as client:
        yield client


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

    return app_client.post(url="/openai/v1/assistants", json=request.model_dump())


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


@pytest.fixture(scope="session")
def create_run(app_client, create_assistant, create_thread):
    """Create a run for testing. Requires a running Supabase instance."""
    assistant_id = create_assistant.json()["id"]
    thread_id = create_thread.json()["id"]

    request = RunCreateParamsRequestBaseRequest(
        assistant_id=assistant_id,
        instructions="Be happy!",
        additional_instructions="Also be sad!",
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


def test_config_load(app_client):
    """Test that the config is loaded correctly."""
    response = app_client.get("/models")

    assert response.status_code == 200
    assert response.json() == {
        "config_sources": {"test-config.yaml": [CHAT_MODEL]},
        "models": {CHAT_MODEL: {"backend": "localhost:50051", "name": CHAT_MODEL}},
    }


@pytest.fixture(scope="session")
def test_create_thread_and_run(app_client, create_assistant):
    """Test running an assistant. Requires a running Supabase instance."""
    assistant_id = create_assistant.json()["id"]

    request = ThreadRunCreateParamsRequestBaseRequest(
        assistant_id=assistant_id,
        instructions="Be happy!",
        additional_instructions="Also be sad!",
        tool_resources=ToolResources(file_search={}),
        metadata={},
        stream=False,
    )

    response = app_client.post("/openai/v1/threads/runs", json=request.model_dump())

    assert response.status_code == status.HTTP_200_OK
    assert Run.model_validate(response.json()), "Create should create a Run."

    return response


def test_create_run(create_run):
    """Test running an assistant. Requires a running Supabase instance."""

    assert create_run.status_code == status.HTTP_200_OK
    assert Run.model_validate(create_run.json()), "Create should create a Run."


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
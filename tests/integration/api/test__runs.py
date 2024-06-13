"""Test the API endpoints for assistants."""

import os

import pytest
from fastapi import Response, status
from fastapi.testclient import TestClient
from openai.types.beta import Assistant, Thread
from openai.types.beta.threads import Message, Text, TextContentBlock
from leapfrogai_api.backend.types import CreateAssistantRequest
from leapfrogai_api.routers.openai.assistants import \
    router as assistants_router
from leapfrogai_api.routers.openai.requests.create_message_request import \
    CreateMessageRequest
from leapfrogai_api.routers.openai.requests.create_thread_request import \
    CreateThreadRequest
from leapfrogai_api.routers.openai.threads import router as threads_router

CHAT_MODEL="llama-cpp-python"

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


assistant_client = TestClient(assistants_router, headers=headers)
threads_client = TestClient(threads_router, headers=headers)

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

assistant_response: Response

@pytest.fixture(scope="session", autouse=True)
def create_assistant():
    """Create an assistant for testing. Requires a running Supabase instance."""

    global assistant_response  # pylint: disable=global-statement

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

    assistant_response = assistant_client.post(
        url="/openai/v1/assistants", json=request.model_dump()
    )

# Create a thread with the previously created file and fake embeddings
@pytest.fixture(scope="session")
def create_thread():
    """Create a thread for testing. Requires a running Supabase instance."""

    request = CreateThreadRequest(
        messages=None,
        tool_resources=None,
        metadata={},
    )

    return threads_client.post("/openai/v1/threads", json=request.model_dump())

@pytest.fixture(scope="session")
def create_message(create_thread):
    """Create a message for testing. Requires a running Supabase instance."""

    request = CreateMessageRequest(
        role="user",
        content=[
            TextContentBlock(text=Text(value="test", annotations=[]), type="text")
        ],
        attachments=None,
        metadata={},
    )

    message = threads_client.post(
        f"/openai/v1/threads/{create_thread.json()['id']}/messages",
        json=request.model_dump(),
    )

    return {"message": message, "thread_id": create_thread.json()["id"]}

def test_create():
    """Test creating an assistant. Requires a running Supabase instance."""
    assert assistant_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        assistant_response.json()
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

# TODO: Create a run and test the run endpoints
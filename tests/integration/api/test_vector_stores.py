"""Test the API endpoints for assistants."""

import json
import os
import time

import pytest
from fastapi import Response, status
from fastapi.testclient import TestClient
from openai.types import FileDeleted
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_store import ExpiresAfter
from langchain_core.embeddings.fake import FakeEmbeddings
from leapfrogai_api.backend.types import (
    CreateVectorStoreRequest,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.routers.openai.requests.create_modify_assistant_request import (
    CreateAssistantRequest,
)
from leapfrogai_api.routers.openai.threads import router as threads_router
from leapfrogai_api.routers.openai.messages import router as messages_router
from leapfrogai_api.routers.openai.assistants import router as assistants_router
from leapfrogai_api.routers.openai.runs import router as runs_router
import leapfrogai_api.backend.rag.index
from leapfrogai_api.routers.openai.vector_stores import router as vector_store_router
from leapfrogai_api.routers.openai.files import router as files_router

INSTRUCTOR_XL_EMBEDDING_SIZE: int = 768


# Used to mock the creation of embeddings as the remote embeddings service is unavailable in this test
class FakeEmbeddingsWrapper(FakeEmbeddings):
    def __init__(self):
        super().__init__(size=INSTRUCTOR_XL_EMBEDDING_SIZE)


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

vector_store_client = TestClient(vector_store_router, headers=headers)
files_client = TestClient(files_router, headers=headers)
assistants_client = TestClient(assistants_router, headers=headers)
threads_client = TestClient(threads_router, headers=headers)
messages_client = TestClient(messages_router, headers=headers)
runs_client = TestClient(runs_router, headers=headers)

# Read in file for use with vector store files
@pytest.fixture(scope="session", autouse=True)
def read_testfile():
    """Read the test file content."""

    with open(
        os.path.dirname(__file__) + "/../../../tests/data/test.txt", "rb"
    ) as testfile:
        testfile_content = testfile.read()

    return testfile_content


# Adds file to Supabase
@pytest.fixture(scope="session", autouse=True)
def create_file(read_testfile):  # pylint: disable=redefined-outer-name, unused-argument
    """Create a file for testing. Requires a running Supabase instance."""

    file_response = files_client.post(
        "/openai/v1/files",
        files={"file": ("test.txt", read_testfile, "text/plain")},
        data={"purpose": "assistants"},
    )

    json_data = json.loads(file_response.text)

    return json_data


vector_store_response: Response
expired_vector_store_response: Response


# Create a vector store with the previously created file and fake embeddings
@pytest.fixture(scope="session", autouse=True)
def create_vector_store(create_file):
    """Create a vector store for testing. Requires a running Supabase instance."""

    global vector_store_response  # pylint: disable=global-statement
    global expired_vector_store_response  # pylint: disable=global-statement

    # Mock out the embeddings creation using a fake
    leapfrogai_api.backend.rag.index.embeddings_type = FakeEmbeddingsWrapper

    request = CreateVectorStoreRequest(
        file_ids=[create_file["id"]],
        name="test",
        expires_after=ExpiresAfter(anchor="last_active_at", days=10),
        metadata={},
    )

    vector_store_response = vector_store_client.post(
        "/openai/v1/vector_stores", json=request.model_dump()
    )

    expired_request = CreateVectorStoreRequest(
        file_ids=[create_file["id"]],
        name="test2",
        expires_after=ExpiresAfter(anchor="last_active_at", days=0),
        metadata={},
    )

    expired_vector_store_response = vector_store_client.post(
        "/openai/v1/vector_stores", json=expired_request.model_dump()
    )


def test_create():
    """Test creating a vector store. Requires a running Supabase instance."""
    assert vector_store_response.status_code == status.HTTP_200_OK
    assert VectorStore.model_validate(
        vector_store_response.json()
    ), "Create should create a VectorStore."

    assert (
        "user_id" not in vector_store_response.json()
    ), "Create should not return a user_id."


def test_create_expired():
    assert expired_vector_store_response.status_code == status.HTTP_200_OK
    assert VectorStore.model_validate(
        expired_vector_store_response.json()
    ), "Create should create a VectorStore, even if expired."


def test_get():
    """Test getting a vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    get_response = vector_store_client.get(
        f"/openai/v1/vector_stores/{vector_store_id}"
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert VectorStore.model_validate(
        get_response.json()
    ), f"Get should return VectorStore {vector_store_id}. Instead returned {get_response.json()}."

    assert get_response.json()["file_counts"]["completed"] == 1
    assert (
        get_response.json()["file_counts"]["total"] == 1
    ), "Should have an accurate file count"


def test_get_expired():
    time.sleep(1)  # Wait an arbitrary amount of time for the vector store to expire
    expired_vector_store_id = expired_vector_store_response.json()["id"]
    get_expired_response = vector_store_client.get(
        f"/openai/v1/vector_stores/{expired_vector_store_id}"
    )
    assert get_expired_response.status_code == status.HTTP_200_OK
    assert (
        get_expired_response.json() is None
    ), f"Get should not return VectorStore {expired_vector_store_id}."


def test_list():
    """Test listing vector stores. Requires a running Supabase instance."""
    list_response = vector_store_client.get("/openai/v1/vector_stores")
    assert list_response.status_code == status.HTTP_200_OK
    for vector_store_object in list_response.json()["data"]:
        assert VectorStore.model_validate(
            vector_store_object
        ), "Should return a list of VectorStore."


def test_list_expired():
    time.sleep(1)  # Wait an arbitrary amount of time for the vector store to expire
    list_expired_response = vector_store_client.get("/openai/v1/vector_stores")
    assert list_expired_response.status_code == status.HTTP_200_OK
    for vector_store_object in list_expired_response.json()["data"]:
        assert (
            vector_store_object["id"] is not expired_vector_store_response.json()["id"]
        ), "Expired vector store should not exists in results"


def test_modify(create_file):
    """Test modifying a vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    request = ModifyVectorStoreRequest(
        file_ids=[create_file["id"]],
        name="test1",
        metadata={},
    )

    modify_response = vector_store_client.post(
        f"/openai/v1/vector_stores/{vector_store_id}",
        json=request.model_dump(),
    )
    assert modify_response.status_code == status.HTTP_200_OK
    assert VectorStore.model_validate(
        modify_response.json()
    ), "Should return a VectorStore."
    assert modify_response.json()["name"] == "test1", "Should be modified."


def test_modify_expired(create_file):
    with pytest.raises(Exception) as e_info:
        expired_vector_store_id = expired_vector_store_response.json()["id"]
        expired_request = ModifyVectorStoreRequest(
            file_ids=[create_file["id"]],
            name="test2",
            expires_after=ExpiresAfter(anchor="last_active_at", days=0),
            metadata={},
        )

        vector_store_client.post(
            f"/openai/v1/vector_stores/{expired_vector_store_id}",
            json=expired_request.model_dump(),
        )
    assert e_info.match("Vector store not found")


def test_get_modified():
    """Test getting a modified vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    get_modified_response = vector_store_client.get(
        f"/openai/v1/vector_stores/{vector_store_id}"
    )
    assert get_modified_response.status_code == status.HTTP_200_OK
    assert VectorStore.model_validate(
        get_modified_response.json()
    ), f"Get should return modified VectorStore {vector_store_id}. Instead returned {get_modified_response.json()}."
    assert get_modified_response.json()["name"] == "test1", "Should be modified."


def test_get_modified_expired():
    """Test getting a modified vector store. Requires a running Supabase instance."""
    vector_store_id = expired_vector_store_response.json()["id"]
    get_modified_response = vector_store_client.get(
        f"/openai/v1/vector_stores/{vector_store_id}"
    )
    assert get_modified_response.status_code == status.HTTP_200_OK
    assert get_modified_response.json() is None


def test_run_with_background_task(create_file):
    """Test creating a run while the vector store is still being processed in the background."""
    # Create a vector store with files
    request = CreateVectorStoreRequest(
        file_ids=[create_file["id"]],
        name="test_background",
        expires_after=ExpiresAfter(anchor="last_active_at", days=10),
        metadata={},
    )

    vector_store_response = vector_store_client.post(
        "/openai/v1/vector_stores", json=request.model_dump()
    )
    assert vector_store_response.status_code == status.HTTP_200_OK
    vector_store_id = vector_store_response.json()["id"]

    # Create an assistant with the vector store
    assistant_request = CreateAssistantRequest(
        model="test-chat",
        name="Test Assistant",
        instructions="You are a helpful assistant with access to a knowledge base.",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )

    assistant_response = assistants_client.post(
        "/openai/v1/assistants", json=assistant_request.model_dump()
    )
    assert assistant_response.status_code == status.HTTP_200_OK
    assistant_id = assistant_response.json()["id"]

    # Create a thread
    thread_response = threads_client.post("/openai/v1/threads", json={})
    assert thread_response.status_code == status.HTTP_200_OK
    thread_id = thread_response.json()["id"]

    # Create a message in the thread
    message_request = {
        "role": "user",
        "content": [
            {
                "text": {
                    "annotations": [],
                    "value": "What information can you provide about the content in the vector store?",
                },
                "type": "text",
            },
        ],
    }

    message_response = messages_client.post(
        f"/openai/v1/threads/{thread_id}/messages", json=message_request
    )
    assert message_response.status_code == status.HTTP_200_OK

    # Create a run
    run_request = {
        "assistant_id": assistant_id,
        "instructions": "Please use the file_search tool to find relevant information.",
    }
    run_response = runs_client.post(
        f"/openai/v1/threads/{thread_id}/runs", json=run_request
    )
    assert run_response.status_code == status.HTTP_200_OK

    # Retrieve the assistant's message
    messages_response = messages_client.get(f"/openai/v1/threads/{thread_id}/messages")
    assert messages_response.status_code == status.HTTP_200_OK
    messages = messages_response.json()["data"]
    assert len(messages) > 1, "No response message from the assistant"
    assistant_message = messages[0]["content"][0]["text"]["value"]

    # Check that the assistant's response contains relevant information
    assert len(assistant_message) > 0, "Assistant's response is empty"
    assert (
        "vector store" in assistant_message.lower()
    ), "Assistant's response doesn't mention the vector store"

    # Clean up
    delete_assistant_response = assistants_client.delete(
        f"/openai/v1/assistants/{assistant_id}"
    )
    assert delete_assistant_response.status_code == status.HTTP_200_OK
    delete_vector_store_response = vector_store_client.delete(
        f"/openai/v1/vector_stores/{vector_store_id}"
    )
    assert delete_vector_store_response.status_code == status.HTTP_200_OK

def test_delete():
    """Test deleting a vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    delete_response = vector_store_client.delete(
        f"/openai/v1/vector_stores/{vector_store_id}"
    )
    assert delete_response.status_code == status.HTTP_200_OK
    assert VectorStoreDeleted.model_validate(
        delete_response.json()
    ), "Should return a VectorStoreDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."


def test_delete_twice():
    """Test deleting a vector store twice. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    delete_response = vector_store_client.delete(
        f"/openai/v1/vector_stores/{vector_store_id}"
    )
    assert delete_response.status_code == status.HTTP_200_OK
    assert VectorStoreDeleted.model_validate(
        delete_response.json()
    ), "Should return a VectorStoreDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), "Should not be able to delete twice."


def test_get_nonexistent():
    """Test getting a nonexistent vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    get_response = vector_store_client.get(
        f"/openai/v1/vector_stores/{vector_store_id}"
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert (
        get_response.json() is None
    ), f"Get should not return deleted VectorStore {vector_store_id}."


def test_cleanup_file(create_file):
    """Test cleaning up the file created for the vector store. Requires a running Supabase instance."""
    file_id = create_file["id"]
    cleanup_response = files_client.delete(f"/openai/v1/files/{file_id}")
    assert cleanup_response.status_code == status.HTTP_200_OK
    assert FileDeleted.model_validate(
        cleanup_response.json()
    ), "Should return a FileDeleted object."
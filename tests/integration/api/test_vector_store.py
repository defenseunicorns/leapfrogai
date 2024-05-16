"""Test the API endpoints for assistants."""

import pytest
from fastapi import Response
from fastapi.testclient import TestClient
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_store import ExpiresAfter
from leapfrogai_api.backend.types import (
    CreateVectorStoreRequest,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.routers.openai.vector_store import router

vector_store_response: Response

client = TestClient(router)


@pytest.fixture(scope="session", autouse=True)
def create_vector_store():
    """Create a vector store for testing. Requires a running Supabase instance."""

    global vector_store_response  # pylint: disable=global-statement

    request = CreateVectorStoreRequest(
        file_ids=[],
        name="test",
        expires_after=ExpiresAfter(anchor="last_active_at", days=0),
        metadata={},
    )

    vector_store_response = client.post(
        "/openai/v1/vector_store", json=request.model_dump()
    )


def test_create():
    """Test creating a vector store. Requires a running Supabase instance."""
    assert vector_store_response.status_code == 200
    assert VectorStore.model_validate(
        vector_store_response.json()
    ), "Create should create a VectorStore."


def test_get():
    """Test getting a vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    get_response = client.get(f"/openai/v1/vector_store/{vector_store_id}")
    assert get_response.status_code == 200
    assert VectorStore.model_validate(
        get_response.json()
    ), f"Get should return VectorStore {vector_store_id}."


def test_list():
    """Test listing vector stores. Requires a running Supabase instance."""
    list_response = client.get("/openai/v1/vector_store")
    assert list_response.status_code == 200
    for vector_store_object in list_response.json()["data"]:
        assert VectorStore.model_validate(
            vector_store_object
        ), "Should return a list of VectorStore."


def test_modify():
    """Test modifying a vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    request = ModifyVectorStoreRequest(
        file_ids=[],
        name="test1",
        expires_after=ExpiresAfter(anchor="last_active_at", days=0),
        metadata={},
    )

    modify_response = client.post(
        f"/openai/v1/vector_store/{vector_store_id}",
        json=request.model_dump(),
    )
    assert modify_response.status_code == 200
    assert VectorStore.model_validate(
        modify_response.json()
    ), "Should return a VectorStore."
    assert modify_response.json()["name"] == "test1", "Should be modified."


def test_get_modified():
    """Test getting a modified vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    get_modified_response = client.get(f"/openai/v1/vector_store/{vector_store_id}")
    assert get_modified_response.status_code == 200
    assert VectorStore.model_validate(
        get_modified_response.json()
    ), f"Get should return modified VectorStore {vector_store_id}."
    assert get_modified_response.json()["name"] == "test1", "Should be modified."


def test_delete():
    """Test deleting a vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    delete_response = client.delete(f"/openai/v1/vector_store/{vector_store_id}")
    assert delete_response.status_code == 200
    assert VectorStoreDeleted.model_validate(
        delete_response.json()
    ), "Should return a VectorStoreDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."


def test_delete_twice():
    """Test deleting a vector store twice. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    delete_response = client.delete(f"/openai/v1/vector_store/{vector_store_id}")
    assert delete_response.status_code == 200
    assert VectorStoreDeleted.model_validate(
        delete_response.json()
    ), "Should return a VectorStoreDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), "Should not be able to delete twice."


def test_get_nonexistent():
    """Test getting a nonexistent vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    get_response = client.get(f"/openai/v1/vector_store/{vector_store_id}")
    assert get_response.status_code == 200
    assert (
        get_response.json() is None
    ), f"Get should not return deleted VectorStore {vector_store_id}."

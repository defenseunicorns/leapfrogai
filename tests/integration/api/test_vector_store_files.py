"""Test the API endpoints for assistants."""

import pytest
from fastapi import Response, status
from fastapi.testclient import TestClient
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_store import ExpiresAfter
from leapfrogai_api.backend.types import (
    CreateVectorStoreRequest,
)
from leapfrogai_api.routers.openai.vector_stores import router

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
        "/openai/v1/vector_stores", json=request.model_dump()
    )


def test_create():
    """Test creating a vector store. Requires a running Supabase instance."""
    assert vector_store_response.status_code == status.HTTP_200_OK
    assert VectorStore.model_validate(
        vector_store_response.json()
    ), "Create should create a VectorStore."


def test_delete():
    """Test deleting a vector store. Requires a running Supabase instance."""
    vector_store_id = vector_store_response.json()["id"]
    delete_response = client.delete(f"/openai/v1/vector_stores/{vector_store_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    assert VectorStoreDeleted.model_validate(
        delete_response.json()
    ), "Should return a VectorStoreDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."

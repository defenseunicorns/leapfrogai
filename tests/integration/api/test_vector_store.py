"""Test the API endpoints for assistants."""

from fastapi.testclient import TestClient
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_store import ExpiresAfter

from leapfrogai_api.routers.openai.vector_store import router
from leapfrogai_api.backend.types import (
    CreateVectorStoreRequest,
    ModifyVectorStoreRequest,
)

client = TestClient(router)


def test_vector_store():
    """Test creating an assistant. Requires a running Supabase instance."""
    request = CreateVectorStoreRequest(
        file_ids=[],
        name="test",
        expires_after=ExpiresAfter(anchor="last_active_at", days=0),
        metadata={},
    )

    create_response = client.post("/openai/v1/vector_store", json=request.model_dump())
    assert create_response.status_code == 200
    assert VectorStore.model_validate(create_response.json())

    list_response = client.get("/openai/v1/vector_store")
    assert list_response.status_code == 200
    for vector_store_object in list_response.json():
        assert VectorStore.model_validate(
            vector_store_object
        ), "Should return a list of VectorStore."

    get_response = client.get(f"/openai/v1/vector_store/{create_response.json()['id']}")
    assert get_response.status_code == 200
    assert VectorStore.model_validate(
        get_response.json()
    ), "Should return a VectorStore."

    request = ModifyVectorStoreRequest(
        file_ids=[],
        name="test1",
        expires_after=ExpiresAfter(anchor="last_active_at", days=0),
        metadata={},
    )

    modify_response = client.post(
        f"/openai/v1/vector_store/{create_response.json()['id']}",
        json=request.model_dump(),
    )
    assert modify_response.status_code == 200
    assert VectorStore.model_validate(
        modify_response.json()
    ), "Should return a VectorStore."
    assert modify_response.json()["name"] == "test1", "Should be modified."

    get_modified_response = client.get(
        f"/openai/v1/vector_store/{create_response.json()['id']}"
    )
    assert get_modified_response.status_code == 200
    assert VectorStore.model_validate(
        get_modified_response.json()
    ), "Should return a VectorStore."
    assert get_modified_response.json()["name"] == "test1", "Should be modified."

    delete_response = client.delete(
        f"/openai/v1/vector_store/{create_response.json()['id']}"
    )
    assert delete_response.status_code == 200
    assert VectorStoreDeleted.model_validate(
        delete_response.json()
    ), "Should return a VectorStoreDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."

    delete_response = client.delete(
        f"/openai/v1/vector_store/{create_response.json()['id']}"
    )
    assert (
        delete_response.status_code == 200
    ), "Should return 200 even if the vector store is not found."
    assert VectorStoreDeleted.model_validate(
        delete_response.json()
    ), "Should return a VectorStoreDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), "Should not be able to delete twice."

    # Make sure the vector store is not still present
    get_response = client.get(f"/openai/v1/vector_store/{create_response.json()['id']}")
    assert get_response.status_code == 200
    assert get_response.json() is None

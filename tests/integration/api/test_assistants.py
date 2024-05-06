"""Test the API endpoints for assistants."""

from fastapi import status
from fastapi.testclient import TestClient
from openai.types.beta import Assistant, AssistantDeleted

from leapfrogai_api.routers.openai.assistants import router
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ModifyAssistantRequest,
)

client = TestClient(router)


def test_assistants():
    """Test creating an assistant. Requires a running Supabase instance."""
    request = CreateAssistantRequest(
        model="test",
        name="test",
        description="test",
        instructions="test",
        tools=[{"type": "file_search"}],
        tool_resources={},
        metadata={},
        temperature=1.0,
        top_p=1.0,
        response_format="auto",
    )

    create_response = client.post("/openai/v1/assistants", json=request.model_dump())
    assert create_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        create_response.json()
    ), "Create should create an Assistant."

    assistant_id = create_response.json()["id"]

    list_response = client.get("/openai/v1/assistants")
    assert list_response.status_code is status.HTTP_200_OK
    for assistant_object in list_response.json()["data"]:
        assert Assistant.model_validate(
            assistant_object
        ), "List should return a list of Assistants."

    get_response = client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_response.json()
    ), f"Get endpoint should return Assistant {assistant_id}."

    modified_name = "test1"

    request = ModifyAssistantRequest(
        model="test1",
        name=modified_name,
        description="test1",
        instructions="test1",
        tools=[{"type": "file_search"}],
        tool_resources={},
        metadata={},
        temperature=1.0,
        top_p=1.0,
        response_format="auto",
    )

    modify_response = client.post(
        f"/openai/v1/assistants/{assistant_id}",
        json=request.model_dump(),
    )
    assert modify_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        modify_response.json()
    ), "Should return a Assistant."
    assert (
        modify_response.json()["name"] == modified_name
    ), f"Assistant {assistant_id} should be modified via modify endpoint."

    get_modified_response = client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_modified_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_modified_response.json()
    ), "Should return a Assistant."
    assert (
        get_modified_response.json()["model"] == "test1"
    ), f"Get endpoint should return modified Assistant {assistant_id}."

    delete_response = client.delete(f"/openai/v1/assistants/{assistant_id}")
    assert delete_response.status_code is status.HTTP_200_OK
    assert AssistantDeleted.model_validate(
        delete_response.json()
    ), "Should return a AssistantDeleted object."
    assert (
        delete_response.json()["deleted"] is True
    ), f"Assistant {assistant_id} should be deleted."

    delete_response = client.delete(f"/openai/v1/assistants/{assistant_id}")
    assert (
        delete_response.status_code is status.HTTP_200_OK
    ), "Should return 200 even if the assistant is not found."
    assert AssistantDeleted.model_validate(
        delete_response.json()
    ), "Should return a AssistantDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), f"Assistant {assistant_id} should not be able to delete twice."

    # Make sure the assistant is not still present
    get_response = client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert get_response.json() is None

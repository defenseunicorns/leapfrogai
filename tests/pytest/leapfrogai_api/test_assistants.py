""" Test the API endpoints for assistants. """
from fastapi.testclient import TestClient
from openai.types.beta import Assistant

from leapfrogai_api.routers.openai.assistants import router
from leapfrogai_api.backend.types import (
    CreateAssistantRequest,
    ModifyAssistantRequest,
)

client = TestClient(router)

# TODO: Mock Supabase session

def test_assistants():
    """Test creating an assistant."""
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
    assert create_response.status_code == 200
    assert Assistant.model_validate(create_response.json())

    list_response = client.get("/openai/v1/assistants")
    assert list_response.status_code == 200
    assert Assistant.model_validate(list_response.json()[0])

    get_response = client.get(f"/openai/v1/assistants/{create_response.json()['id']}")
    assert get_response.status_code == 200

    request = ModifyAssistantRequest(
        model="test1",
        name="test1",
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
        f"/openai/v1/assistants/{create_response.json()['id']}",
        json=request.model_dump(),
    )
    assert modify_response.status_code == 200
    assert Assistant.model_validate(modify_response.json())

    get_modified_response = client.get(
        f"/openai/v1/assistants/{create_response.json()['id']}"
    )
    assert get_modified_response.status_code == 200

    delete_response = client.delete(
        f"/openai/v1/assistants/{create_response.json()['id']}"
    )
    assert delete_response.status_code == 200

    # Make sure the assistant is not still present
    retrieve_assistant_response = client.get(
        f"/openai/v1/assistants/{create_response.json()['id']}"
    )
    assert retrieve_assistant_response.status_code == 200
    assert retrieve_assistant_response.json() is None

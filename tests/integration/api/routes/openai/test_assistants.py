"""Test the API endpoints for assistants."""

import os

import json
import pytest
from fastapi import Response, status
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException
from langchain_core.embeddings.fake import FakeEmbeddings
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.assistant import ToolResources
from openai.types.beta.vector_store import ExpiresAfter

import leapfrogai_api.backend.rag.index
from leapfrogai_api.routers.openai.vector_stores import router as vector_store_router
from leapfrogai_api.routers.openai.files import router as files_router
from leapfrogai_api.routers.openai.assistants import router as assistants_router
from leapfrogai_api.typedef.vectorstores import CreateVectorStoreRequest
from leapfrogai_api.typedef.assistants import (
    CreateAssistantRequest,
    ModifyAssistantRequest,
)
from tests.utils.data_path import data_path, TXT_FILE_NAME

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
except KeyError:
    raise MissingEnvironmentVariable(
        "SUPABASE_USER_JWT must be defined for the test to pass. "
        "Please check the api README for instructions on obtaining this token."
    )

assistant_response: Response

assistants_client = TestClient(assistants_router, headers=headers)
vector_store_client = TestClient(vector_store_router, headers=headers)
files_client = TestClient(files_router, headers=headers)

starting_assistant = Assistant(
    id="",
    created_at=0,
    name="test",
    description="test",
    instructions="test",
    model="test",
    object="assistant",
    tools=[{"type": "file_search"}],
    tool_resources={},
    temperature=1.0,
    top_p=1.0,
    metadata={},
    response_format="auto",
)

modified_assistant = Assistant(
    id="",
    created_at=0,
    name="test1",
    description="test1",
    instructions="test1",
    model="test1",
    object="assistant",
    tools=[{"type": "file_search"}],
    tool_resources=ToolResources(
        file_search=None,
        code_interpreter=None,
    ),
    temperature=0,
    top_p=0.1,
    metadata={},
    response_format="auto",
)


# Read in file for use with vector store files
@pytest.fixture(scope="session", autouse=True)
def read_testfile():
    """Read the test file content."""

    with open(data_path(TXT_FILE_NAME), "rb") as testfile:
        testfile_content = testfile.read()

    return testfile_content


# Adds file to Supabase
@pytest.fixture(scope="session", autouse=True)
def create_file(read_testfile):  # pylint: disable=redefined-outer-name, unused-argument
    """Create a file for testing. Requires a running Supabase instance."""

    global file_response  # pylint: disable=global-statement

    file_response = files_client.post(
        "/openai/v1/files",
        files={"file": (TXT_FILE_NAME, read_testfile, "text/plain")},
        data={"purpose": "assistants"},
    )

    json_data = json.loads(file_response.text)

    return json_data


vector_store_response: Response
expired_vector_store_response: Response
file_response: Response


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

    assistant_response = assistants_client.post(
        url="/openai/v1/assistants", json=request.model_dump()
    )


def test_code_interpreter_fails():
    """Test creating an assistant with a code interpreter tool. Requires a running Supabase instance."""
    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "code_interpreter"}],
        tool_resources=modified_assistant.tool_resources,
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    with pytest.raises(HTTPException) as exc:
        assistants_client.post("/openai/v1/assistants", json=request.model_dump())

    assert exc.value.status_code is status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "Unsupported tool type: code_interpreter"


def test_create():
    """Test creating an assistant. Requires a running Supabase instance."""
    assert assistant_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        assistant_response.json()
    ), "Create should create an Assistant."
    assert (
        "user_id" not in assistant_response.json()
    ), "Create should not return a user_id."


def test_get():
    """Test getting an assistant. Requires a running Supabase instance."""
    assistant_id = assistant_response.json()["id"]
    get_response = assistants_client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_response.json()
    ), f"Get should return Assistant {assistant_id}."


def test_list():
    """Test listing assistants. Requires a running Supabase instance."""
    list_response = assistants_client.get("/openai/v1/assistants")
    assert list_response.status_code is status.HTTP_200_OK
    for assistant_object in list_response.json()["data"]:
        assert Assistant.model_validate(
            assistant_object
        ), "List should return a list of Assistants."


def test_modify():
    """Test modifying an assistant. Requires a running Supabase instance."""

    global modified_assistant  # pylint: disable=global-statement

    assistant_id = assistant_response.json()["id"]
    get_response = assistants_client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_response.json()
    ), f"Get endpoint should return Assistant {assistant_id}."

    request = ModifyAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=modified_assistant.tools,
        tool_resources=modified_assistant.tool_resources,
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    modify_response = assistants_client.post(
        f"/openai/v1/assistants/{assistant_id}",
        json=request.model_dump(),
    )
    assert modify_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        modify_response.json()
    ), "Should return a Assistant."

    modified_assistant.id = modify_response.json()["id"]
    modified_assistant.created_at = modify_response.json()["created_at"]

    assert modified_assistant == Assistant(
        **modify_response.json()
    ), f"Modify endpoint should return modified Assistant {assistant_id}."

    get_modified_response = assistants_client.get(
        f"/openai/v1/assistants/{assistant_id}"
    )
    assert get_modified_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_modified_response.json()
    ), "Should return a Assistant."
    assert (
        get_modified_response.json()["model"] == "test1"
    ), f"Get endpoint should return modified Assistant {assistant_id}."


def test_modify_with_no_tools():
    """Test modifying an assistant without tools or tool_resources. Requires a running Supabase instance."""

    global modified_assistant  # pylint: disable=global-statement

    assistant_id = assistant_response.json()["id"]
    get_response = assistants_client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_response.json()
    ), f"Get endpoint should return Assistant {assistant_id}."

    request = ModifyAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=None,
        tool_resources=None,
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    modify_response = assistants_client.post(
        f"/openai/v1/assistants/{assistant_id}",
        json=request.model_dump(),
    )
    assert modify_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        modify_response.json()
    ), "Should return a Assistant."

    modified_assistant.id = modify_response.json()["id"]
    modified_assistant.created_at = modify_response.json()["created_at"]

    assert modified_assistant == Assistant(
        **modify_response.json()
    ), f"Modify endpoint should return modified Assistant {assistant_id}."

    get_modified_response = assistants_client.get(
        f"/openai/v1/assistants/{assistant_id}"
    )
    assert get_modified_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_modified_response.json()
    ), "Should return a Assistant."
    assert (
        get_modified_response.json()["model"] == "test1"
    ), f"Get endpoint should return modified Assistant {assistant_id}."


def test_create_with_new_vector_store():
    """Test creating a new assistant and vector store in the same request. Requires a running Supabase instance."""

    file_id = file_response.json()["id"]

    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_stores": [{"file_ids": [file_id]}]}},
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    new_vs_response = assistants_client.post(
        "/openai/v1/assistants",
        json=request.model_dump(),
    )
    assert new_vs_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        new_vs_response.json()
    ), "Should return a Assistant."

    list_vs_response = vector_store_client.get("/openai/v1/vector_stores")
    vs_ids = [datum["id"] for datum in list_vs_response.json()["data"]]

    assert (
        new_vs_response.json()["tool_resources"]["file_search"]["vector_store_ids"][0]
        in vs_ids
    ), "New vector store id should be found within the list of vector stores"

    assert (
        new_vs_response.json()["tool_resources"]["file_search"]["vector_stores"] is None
    ), "The created Assistant object should not have a 'vector_stores' field"

    vs_files_response = vector_store_client.get(
        f"/openai/v1/vector_stores/{new_vs_response.json()['tool_resources']['file_search']['vector_store_ids'][0]}/files"
    )

    assert (
        file_id == vs_files_response.json()["data"][0]["id"]
    ), "Original file id should be retrievable from the new vector store"


def test_create_with_existing_vector_store():
    """Test creating a new assistant and attaching it to an existing vector store. Requires a running Supabase instance."""

    vector_store_id = vector_store_response.json()["id"]

    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    new_vs_response = assistants_client.post(
        "/openai/v1/assistants",
        json=request.model_dump(),
    )
    assert new_vs_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        new_vs_response.json()
    ), "Should return a Assistant."

    assert (
        new_vs_response.json()["tool_resources"]["file_search"]["vector_store_ids"][0]
        == vector_store_id
    ), "New vector store id should match the supplied vector store id"

    assert (
        new_vs_response.json()["tool_resources"]["file_search"]["vector_stores"] is None
    ), "The created Assistant object should not have a 'vector_stores' field"


def test_modify_with_new_vector_store():
    """Test modifying an existing assistant and create a new vector store in the same request. Requires a running Supabase instance."""

    file_id = file_response.json()["id"]

    assistant_id = assistant_response.json()["id"]
    get_response = assistants_client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_response.json()
    ), f"Get endpoint should return Assistant {assistant_id}."

    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_stores": [{"file_ids": [file_id]}]}},
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    modify_vs_response = assistants_client.post(
        f"/openai/v1/assistants/{assistant_id}",
        json=request.model_dump(),
    )
    assert modify_vs_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        modify_vs_response.json()
    ), "Should return an Assistant."

    list_vs_response = vector_store_client.get("/openai/v1/vector_stores")
    vs_ids = [datum["id"] for datum in list_vs_response.json()["data"]]

    assert (
        modify_vs_response.json()["tool_resources"]["file_search"]["vector_store_ids"][
            0
        ]
        in vs_ids
    ), "New vector store id should be found within the list of vector stores"

    assert (
        modify_vs_response.json()["tool_resources"]["file_search"]["vector_stores"]
        is None
    ), "The created Assistant object should not have a 'vector_stores' field"

    vs_files_response = vector_store_client.get(
        f"/openai/v1/vector_stores/{modify_vs_response.json()['tool_resources']['file_search']['vector_store_ids'][0]}/files"
    )

    assert (
        file_id == vs_files_response.json()["data"][0]["id"]
    ), "Original file id should be retrievable from the new vector store"


def test_modify_with_existing_vector_store():
    """Test modifying an existing assistant by attaching it to an existing vector store. Requires a running Supabase instance."""

    vector_store_id = vector_store_response.json()["id"]

    assistant_id = assistant_response.json()["id"]
    get_response = assistants_client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        get_response.json()
    ), f"Get endpoint should return Assistant {assistant_id}."

    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    modify_vs_response = assistants_client.post(
        f"/openai/v1/assistants/{assistant_id}",
        json=request.model_dump(),
    )
    assert modify_vs_response.status_code is status.HTTP_200_OK
    assert Assistant.model_validate(
        modify_vs_response.json()
    ), "Should return an Assistant."

    assert (
        modify_vs_response.json()["id"] == assistant_id
    ), "The assistant's id should be unchanged"

    assert (
        modify_vs_response.json()["tool_resources"]["file_search"]["vector_store_ids"][
            0
        ]
        == vector_store_id
    ), "New vector store id should match the supplied vector store id"

    assert (
        modify_vs_response.json()["tool_resources"]["file_search"]["vector_stores"]
        is None
    ), "The created Assistant object should not have a 'vector_stores' field"


def test_delete():
    """Test deleting an assistant. Requires a running Supabase instance."""
    assistant_id = assistant_response.json()["id"]

    delete_response = assistants_client.delete(f"/openai/v1/assistants/{assistant_id}")
    assert delete_response.status_code is status.HTTP_200_OK
    assert AssistantDeleted.model_validate(
        delete_response.json()
    ), "Should return a AssistantDeleted object."
    assert (
        delete_response.json()["deleted"] is True
    ), f"Assistant {assistant_id} should be deleted."


def test_delete_twice():
    """Test deleting an assistant twice. Requires a running Supabase instance."""
    assistant_id = assistant_response.json()["id"]
    delete_response = assistants_client.delete(f"/openai/v1/assistants/{assistant_id}")
    assert delete_response.status_code is status.HTTP_200_OK
    assert AssistantDeleted.model_validate(
        delete_response.json()
    ), "Should return a AssistantDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), f"Assistant {assistant_id} should not be able to delete twice."


def test_get_nonexistent():
    """Test getting a nonexistent assistant. Requires a running Supabase instance."""
    assistant_id = assistant_response.json()["id"]

    get_response = assistants_client.get(f"/openai/v1/assistants/{assistant_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert (
        get_response.json() is None
    ), f"Get should not return deleted Assistant {assistant_id}."


def test_create_with_too_many_vector_store_ids_fails():
    """Test creating a new assistant and supplying too many vector store ids. Requires a running Supabase instance."""

    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": ["id_one", "id_two"]}},
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    try:
        new_vs_fail_response = assistants_client.post(
            "/openai/v1/assistants",
            json=request.model_dump(),
        )

        assert new_vs_fail_response.status_code is status.HTTP_400_BAD_REQUEST
        assert (
            new_vs_fail_response.json()["detail"]
            == "There can be a maximum of 1 vector store attached to the assistant"
        )

    except HTTPException as exc:
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            exc.detail
            == "There can be a maximum of 1 vector store attached to the assistant"
        )


def test_create_with_too_many_vector_store_file_lists_fails():
    """Test creating a new assistant and supplying too many vector store lists. Requires a running Supabase instance."""
    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_stores": [
                    {"file_ids": ["file_1", "file_2"]},
                    {"file_ids": ["file_3", "file_4"]},
                ]
            }
        },
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    try:
        new_vs_fail_response = assistants_client.post(
            "/openai/v1/assistants",
            json=request.model_dump(),
        )

        assert new_vs_fail_response.status_code is status.HTTP_400_BAD_REQUEST
        assert (
            new_vs_fail_response.json()["detail"]
            == "There can be a maximum of 1 vector store attached to the assistant"
        ), "Should return HTTP 400 error due to invalid request"

    except HTTPException as exc:
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            exc.detail
            == "There can be a maximum of 1 vector store attached to the assistant"
        )


def test_create_with_vector_store_files_and_ids_fails():
    """Test creating a new assistant and supplying both vector store ids and file lists. Requires a running Supabase instance."""
    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": ["id_one"],
                "vector_stores": [{"file_ids": ["file_1", "file_2"]}],
            }
        },
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    try:
        new_vs_fail_response = assistants_client.post(
            "/openai/v1/assistants",
            json=request.model_dump(),
        )

        assert new_vs_fail_response.status_code is status.HTTP_400_BAD_REQUEST
        assert (
            new_vs_fail_response.json()["detail"]
            == "There can be a maximum of 1 vector store attached to the assistant"
        ), "Should return HTTP 400 error due to invalid request"

    except HTTPException as exc:
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            exc.detail
            == "There can be a maximum of 1 vector store attached to the assistant"
        )


def test_create_with_invalid_vector_store_id_fails():
    """Test creating a new assistant and supply an invalid vector store id. Requires a running Supabase instance."""

    request = CreateAssistantRequest(
        model=modified_assistant.model,
        name=modified_assistant.name,
        description=modified_assistant.description,
        instructions=modified_assistant.instructions,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {"vector_store_ids": ["invalid_vector_store_id"]}
        },
        metadata=modified_assistant.metadata,
        temperature=modified_assistant.temperature,
        top_p=modified_assistant.top_p,
        response_format=modified_assistant.response_format,
    )

    try:
        new_vs_fail_response = assistants_client.post(
            "/openai/v1/assistants",
            json=request.model_dump(),
        )
        assert new_vs_fail_response.status_code is status.HTTP_400_BAD_REQUEST
        assert (
            new_vs_fail_response.json()["detail"]
            == "Invalid vector store id was provided"
        ), "Should return HTTP 400 error due to invalid request"

    except HTTPException as exc:
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Invalid vector store id was provided"

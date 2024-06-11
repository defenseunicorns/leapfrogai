"""Test the API endpoints for files."""

import os

import pytest
from fastapi import HTTPException, Response, status
from fastapi.testclient import TestClient
from openai.types import FileDeleted, FileObject
from leapfrogai_api.routers.openai.files import router

file_response: Response
testfile_content: bytes


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

client = TestClient(router, headers=headers)


@pytest.fixture(scope="session", autouse=True)
def read_testfile():
    """Read the test file content."""
    global testfile_content  # pylint: disable=global-statement
    with open(os.path.dirname(__file__) + "/../../data/test.txt", "rb") as testfile:
        testfile_content = testfile.read()


@pytest.fixture(scope="session", autouse=True)
def create_file(read_testfile):  # pylint: disable=redefined-outer-name, unused-argument
    """Create a file for testing. Requires a running Supabase instance."""

    global file_response  # pylint: disable=global-statement

    file_response = client.post(
        "/openai/v1/files",
        files={"file": ("test.txt", testfile_content, "text/plain")},
        data={"purpose": "assistants"},
    )


def test_create():
    """Test creating a file. Requires a running Supabase instance."""
    assert file_response.status_code is status.HTTP_200_OK
    assert FileObject.model_validate(
        file_response.json()
    ), "Create should create a FileObject."


def test_get():
    """Test getting a file. Requires a running Supabase instance."""
    file_id = file_response.json()["id"]
    get_response = client.get(f"/openai/v1/files/{file_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert FileObject.model_validate(
        get_response.json()
    ), f"Get should return FileObject {file_id}."


def test_get_content():
    """Test getting file content. Requires a running Supabase instance."""
    file_id = file_response.json()["id"]
    get_content_response = client.get(f"/openai/v1/files/{file_id}/content")
    assert get_content_response.status_code is status.HTTP_200_OK
    assert (
        testfile_content.decode() in get_content_response.text
    ), f"get_content should return the content for File {file_id}."


def test_list():
    """Test listing files. Requires a running Supabase instance."""
    list_response = client.get("/openai/v1/files")
    assert list_response.status_code is status.HTTP_200_OK
    for file_object in list_response.json()["data"]:
        assert FileObject.model_validate(
            file_object
        ), "List should return a list of FileObjects."


def test_delete():
    """Test deleting a file. Requires a running Supabase instance."""
    file_id = file_response.json()["id"]

    delete_response = client.delete(f"/openai/v1/files/{file_id}")
    assert delete_response.status_code is status.HTTP_200_OK
    assert FileDeleted.model_validate(
        delete_response.json()
    ), "Should return a FileDeleted object."
    assert (
        delete_response.json()["deleted"] is True
    ), f"Delete should be able to delete File {file_id}."


def test_delete_twice():
    """Test deleting a file twice. Requires a running Supabase instance."""
    file_id = file_response.json()["id"]
    delete_response = client.delete(f"/openai/v1/files/{file_id}")
    assert delete_response.status_code is status.HTTP_200_OK
    assert FileDeleted.model_validate(
        delete_response.json()
    ), "Should return a FileDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), f"Delete should not be able to delete File {file_id} twice."


def test_get_nonexistent():
    """Test getting a nonexistent file. Requires a running Supabase instance."""
    file_id = file_response.json()["id"]

    get_response = client.get(f"/openai/v1/files/{file_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert (
        get_response.json() is None
    ), f"Get should not return deleted FileObject {file_id}."


def test_invalid_file_type():
    """Test creating uploading an invalid file type."""

    file_path = "../../../tests/data/0min12sec.wav"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    relative_file_path = os.path.join(dir_path, file_path)

    with pytest.raises(HTTPException) as exception:
        with open(relative_file_path, "rb") as testfile:
            _ = client.post(
                "/openai/v1/files",
                files={"file": ("0min12sec.wav", testfile, "audio/wav")},
                data={"purpose": "assistants"},
            )
            assert exception.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

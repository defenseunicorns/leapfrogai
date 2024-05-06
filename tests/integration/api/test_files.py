"""Test the API endpoints for files."""

from fastapi import HTTPException
from fastapi import status
from fastapi.testclient import TestClient
from openai.types import FileObject, FileDeleted
import pytest
from leapfrogai_api.routers.openai.files import router

client = TestClient(router)


def test_files():
    """Test creating a file. Requires a running Supabase instance."""

    with open("tests/data/test.txt", "rb") as testfile:
        testfile_content = testfile.read()
        create_response = client.post(
            "/openai/v1/files",
            files={"file": ("test.txt", testfile, "text/plain")},
            data={"purpose": "assistants"},
        )

    assert create_response.status_code is status.HTTP_200_OK
    assert FileObject.model_validate(
        create_response.json()
    ), "Create should create a FileObject."

    file_id = create_response.json()["id"]

    list_response = client.get("/openai/v1/files")
    assert list_response.status_code is status.HTTP_200_OK
    for file_object in list_response.json()["data"]:
        assert FileObject.model_validate(
            file_object
        ), "List should return a list of FileObjects."

    get_response = client.get(f"/openai/v1/files/{file_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert FileObject.model_validate(
        get_response.json()
    ), f"Get should return FileObject {file_id}."

    get_content_response = client.get(f"/openai/v1/files/{file_id}/content")
    assert get_content_response.status_code is status.HTTP_200_OK
    assert (
        testfile_content.decode() in get_content_response.text
    ), f"get_content should return the content for File {file_id}."

    delete_response = client.delete(f"/openai/v1/files/{file_id}")
    assert delete_response.status_code is status.HTTP_200_OK
    assert FileDeleted.model_validate(
        delete_response.json()
    ), "Should return a FileDeleted object."
    assert (
        delete_response.json()["deleted"] is True
    ), f"Delete should be able to delete File {file_id}."

    delete_response = client.delete(f"/openai/v1/files/{file_id}")
    assert (
        delete_response.status_code is status.HTTP_200_OK
    ), "Should return 200 even if the file is not found."
    assert FileDeleted.model_validate(
        delete_response.json()
    ), "Should return a FileDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), f"Delete should not be able to delete File {file_id} twice."

    # Make sure the file is not still present
    get_response = client.get(f"/openai/v1/files/{file_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert (
        get_response.json() is None
    ), f"Get should not return deleted FileObject {file_id}."

  def test_invalid_file_type():
      """Test creating uploading an invalid file type."""

      with pytest.raises(HTTPException):
          with open("tests/data/0min12sec.wav", "rb") as testfile:
              _ = client.post(
                  "/openai/v1/files",
                  files={"file": ("0min12sec.wav", testfile, "audio/wav")},
                  data={"purpose": "assistants"},
              )

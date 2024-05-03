"""Test the API endpoints for files."""

from fastapi import HTTPException
from fastapi.testclient import TestClient
from openai.types import FileObject, FileDeleted
import pytest
from leapfrogai_api.routers.openai.files import router

client = TestClient(router)


def test_files():
    """Test uploading a file. Requires a running Supabase instance."""

    with open("tests/data/test.txt", "rb") as testfile:
        testfile_content = testfile.read()
        create_response = client.post(
            "/openai/v1/files",
            files={"file": ("test.txt", testfile, "text/plain")},
            data={"purpose": "assistants"},
        )

    assert create_response.status_code == 200
    assert FileObject.model_validate(create_response.json())

    list_response = client.get("/openai/v1/files")
    assert list_response.status_code == 200
    for file_object in list_response.json():
        assert FileObject.model_validate(
            file_object
        ), "Should return a list of FileObjects."

    get_response = client.get(f"/openai/v1/files/{create_response.json()['id']}")
    assert get_response.status_code == 200
    assert FileObject.model_validate(get_response.json()), "Should return a FileObject."

    get_content_response = client.get(
        f"/openai/v1/files/{create_response.json()['id']}/content"
    )
    assert get_content_response.status_code == 200
    assert (
        testfile_content.decode() in get_content_response.text
    ), "Should return the file content."

    delete_response = client.delete(f"/openai/v1/files/{create_response.json()['id']}")
    assert delete_response.status_code == 200
    assert FileDeleted.model_validate(
        delete_response.json()
    ), "Should return a FileDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."

    delete_response = client.delete(f"/openai/v1/files/{create_response.json()['id']}")
    assert (
        delete_response.status_code == 200
    ), "Should return 200 even if the file is not found."
    assert FileDeleted.model_validate(
        delete_response.json()
    ), "Should return a FileDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), "Should not be able to delete twice."

    # Make sure the file is not still present
    get_response = client.get(f"/openai/v1/files/{create_response.json()['id']}")
    assert get_response.status_code == 200
    assert get_response.json() is None


def test_invalid_file_type():
    """Test creating uploading an invalid file type."""

    with pytest.raises(HTTPException):
        with open("tests/data/0min12sec.wav", "rb") as testfile:
            _ = client.post(
                "/openai/v1/files",
                files={"file": ("0min12sec.wav", testfile, "audio/wav")},
                data={"purpose": "assistants"},
            )

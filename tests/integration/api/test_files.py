"""Test the API endpoints for files."""

from fastapi import status
from fastapi.testclient import TestClient
from openai.types import FileObject, FileDeleted
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
    assert FileObject.model_validate(create_response.json())

    list_response = client.get("/openai/v1/files")
    assert list_response.status_code is status.HTTP_200_OK
    for file_object in list_response.json()["data"]:
        assert FileObject.model_validate(
            file_object
        ), "Should return a list of FileObjects."

    get_response = client.get(f"/openai/v1/files/{create_response.json()['id']}")
    assert get_response.status_code is status.HTTP_200_OK
    assert FileObject.model_validate(get_response.json()), "Should return a FileObject."

    get_content_response = client.get(
        f"/openai/v1/files/{create_response.json()['id']}/content"
    )
    assert get_content_response.status_code is status.HTTP_200_OK
    assert (
        testfile_content.decode() in get_content_response.text
    ), "Should return the file content."

    delete_response = client.delete(f"/openai/v1/files/{create_response.json()['id']}")
    assert delete_response.status_code is status.HTTP_200_OK
    assert FileDeleted.model_validate(
        delete_response.json()
    ), "Should return a FileDeleted object."
    assert delete_response.json()["deleted"] is True, "Should be able to delete."

    delete_response = client.delete(f"/openai/v1/files/{create_response.json()['id']}")
    assert (
        delete_response.status_code is status.HTTP_200_OK
    ), "Should return 200 even if the file is not found."
    assert FileDeleted.model_validate(
        delete_response.json()
    ), "Should return a FileDeleted object."
    assert (
        delete_response.json()["deleted"] is False
    ), "Should not be able to delete twice."

    # Make sure the file is not still present
    get_response = client.get(f"/openai/v1/files/{create_response.json()['id']}")
    assert get_response.status_code is status.HTTP_200_OK
    assert get_response.json() is None

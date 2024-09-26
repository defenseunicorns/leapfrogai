"""Test the API endpoints for files."""

import pytest
from fastapi import HTTPException, Response, status
from openai.types import FileDeleted, FileObject

from leapfrogai_api.backend.rag.document_loader import load_file, split

from tests.utils.client import client_config_factory
from tests.utils.data_path import (
    data_path,
    TXT_FILE_NAME,
    PPTX_FILE_NAME,
    WAV_FILE_NAME,
    XLSX_FILE_NAME,
)


file_response: Response
testfile_content: bytes


@pytest.fixture(scope="session", autouse=True)
def client():
    """Create a client for testing."""
    return client_config_factory("leapfrogai").client


@pytest.fixture(scope="session", autouse=True)
def read_testfile():
    """Read the test file content."""
    global testfile_content  # pylint: disable=global-statement
    with open(data_path(TXT_FILE_NAME), "rb") as testfile:
        testfile_content = testfile.read()


@pytest.fixture(scope="session", autouse=True)
def create_file(client, read_testfile):  # pylint: disable=redefined-outer-name, unused-argument
    """Create a file for testing. Requires a running Supabase instance."""

    global file_response  # pylint: disable=global-statement

    file_response = client.post(
        "/openai/v1/files",
        files={"file": (TXT_FILE_NAME, testfile_content, "text/plain")},
        data={"purpose": "assistants"},
    )


def test_create():
    """Test creating a file. Requires a running Supabase instance."""
    assert file_response.status_code is status.HTTP_200_OK
    assert FileObject.model_validate(
        file_response.json()
    ), "Create should create a FileObject."

    assert "user_id" not in file_response.json(), "Create should not return a user_id."


def test_get(client):
    """Test getting a file. Requires a running Supabase instance."""
    file_id = file_response.json()["id"]
    get_response = client.get(f"/openai/v1/files/{file_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert FileObject.model_validate(
        get_response.json()
    ), f"Get should return FileObject {file_id}."


def test_get_content(client):
    """Test getting file content. Requires a running Supabase instance."""
    file_id = file_response.json()["id"]
    get_content_response = client.get(f"/openai/v1/files/{file_id}/content")
    assert get_content_response.status_code is status.HTTP_200_OK
    assert (
        testfile_content.decode() in get_content_response.text
    ), f"get_content should return the content for File {file_id}."


def test_list(client):
    """Test listing files. Requires a running Supabase instance."""
    list_response = client.get("/openai/v1/files")
    assert list_response.status_code is status.HTTP_200_OK
    for file_object in list_response.json()["data"]:
        assert FileObject.model_validate(
            file_object
        ), "List should return a list of FileObjects."


def test_delete(client):
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


def test_delete_twice(client):
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


def test_get_nonexistent(client):
    """Test getting a nonexistent file. Requires a running Supabase instance."""
    file_id = file_response.json()["id"]

    get_response = client.get(f"/openai/v1/files/{file_id}")
    assert get_response.status_code is status.HTTP_200_OK
    assert (
        get_response.json() is None
    ), f"Get should not return deleted FileObject {file_id}."


def test_invalid_file_type(client):
    """Test creating uploading an invalid file type."""

    with pytest.raises(HTTPException) as exception:
        with open(data_path(WAV_FILE_NAME), "rb") as testfile:
            _ = client.post(
                "/openai/v1/files",
                files={"file": (WAV_FILE_NAME, testfile, "audio/wav")},
                data={"purpose": "assistants"},
            )
            assert exception.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.asyncio
async def test_excel_file_handling(client):
    """Test handling of an Excel file including upload, retrieval, and deletion."""
    # Test file loading and splitting
    documents = await load_file(data_path(XLSX_FILE_NAME))
    assert len(documents) > 0, "No documents were loaded from the Excel file"
    assert documents[0].page_content, "The first document has no content"

    split_documents = await split(documents)
    assert len(split_documents) >= len(documents), "Documents were not split properly"
    assert split_documents[0].page_content, "The first split document has no content"

    # Test file upload via API
    with open(data_path(XLSX_FILE_NAME), "rb") as excel_file:
        response = client.post(
            "/openai/v1/files",
            files={
                "file": (
                    XLSX_FILE_NAME,
                    excel_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
            data={"purpose": "assistants"},
        )

    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Failed to upload Excel file: {response.text}"
    file_object = FileObject.model_validate(response.json())

    # Test file retrieval
    get_response = client.get(f"/openai/v1/files/{file_object.id}")
    assert (
        get_response.status_code == status.HTTP_200_OK
    ), f"Failed to retrieve file: {get_response.text}"
    retrieved_file = FileObject.model_validate(get_response.json())
    assert (
        retrieved_file.id == file_object.id
    ), "Retrieved file ID doesn't match uploaded file ID"

    # Test file content retrieval
    content_response = client.get(f"/openai/v1/files/{file_object.id}/content")
    assert (
        content_response.status_code == status.HTTP_200_OK
    ), f"Failed to retrieve file content: {content_response.text}"
    assert (
        content_response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert (
        content_response.headers["Content-Disposition"]
        == f'attachment; filename="{file_object.filename}"'
    )
    assert len(content_response.content) > 0, "File content is empty"

    # Test file deletion
    delete_response = client.delete(f"/openai/v1/files/{file_object.id}")
    assert (
        delete_response.status_code == status.HTTP_200_OK
    ), f"Failed to delete file: {delete_response.text}"
    assert (
        delete_response.json()["deleted"] is True
    ), "File was not deleted successfully"

    # Verify file is no longer retrievable
    get_deleted_response = client.get(f"/openai/v1/files/{file_object.id}")
    assert get_deleted_response.status_code == status.HTTP_200_OK
    assert get_deleted_response.json() is None, "Deleted file should not be retrievable"


@pytest.mark.asyncio
async def test_powerpoint_file_handling(client):
    """Test handling of a PowerPoint file including upload, retrieval, and deletion."""
    # Test file loading and splitting
    documents = await load_file(data_path(PPTX_FILE_NAME))
    assert len(documents) > 0, "No documents were loaded from the PowerPoint file"
    assert documents[0].page_content, "The first document has no content"

    split_documents = await split(documents)
    assert len(split_documents) >= len(documents), "Documents were not split properly"
    assert split_documents[0].page_content, "The first split document has no content"

    # Test file upload via API
    with open(data_path(PPTX_FILE_NAME), "rb") as pptx_file:
        response = client.post(
            "/openai/v1/files",
            files={
                "file": (
                    PPTX_FILE_NAME,
                    pptx_file,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            },
            data={"purpose": "assistants"},
        )

    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Failed to upload PowerPoint file: {response.text}"
    file_object = FileObject.model_validate(response.json())

    # Test file retrieval
    get_response = client.get(f"/openai/v1/files/{file_object.id}")
    assert (
        get_response.status_code == status.HTTP_200_OK
    ), f"Failed to retrieve file: {get_response.text}"
    retrieved_file = FileObject.model_validate(get_response.json())
    assert (
        retrieved_file.id == file_object.id
    ), "Retrieved file ID doesn't match uploaded file ID"

    # Test file content retrieval
    content_response = client.get(f"/openai/v1/files/{file_object.id}/content")
    assert (
        content_response.status_code == status.HTTP_200_OK
    ), f"Failed to retrieve file content: {content_response.text}"
    assert (
        content_response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    assert (
        content_response.headers["Content-Disposition"]
        == f'attachment; filename="{file_object.filename}"'
    )
    assert len(content_response.content) > 0, "File content is empty"

    # Test file deletion
    delete_response = client.delete(f"/openai/v1/files/{file_object.id}")
    assert (
        delete_response.status_code == status.HTTP_200_OK
    ), f"Failed to delete file: {delete_response.text}"
    assert (
        delete_response.json()["deleted"] is True
    ), "File was not deleted successfully"

    # Verify file is no longer retrievable
    get_deleted_response = client.get(f"/openai/v1/files/{file_object.id}")
    assert get_deleted_response.status_code == status.HTTP_200_OK
    assert get_deleted_response.json() is None, "Deleted file should not be retrievable"

"""Test the API endpoints for files."""

import os
import pytest
from fastapi import HTTPException, Response, status
from fastapi.testclient import TestClient
from openai.types import FileDeleted, FileObject

from leapfrogai_api.backend.rag.document_loader import load_file, split
from leapfrogai_api.routers.openai.files import router
from tests.utils.data_path import data_path, WAV_FILE

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

    assert "user_id" not in file_response.json(), "Create should not return a user_id."


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

    with pytest.raises(HTTPException) as exception:
        with open(data_path(WAV_FILE), "rb") as testfile:
            _ = client.post(
                "/openai/v1/files",
                files={"file": (WAV_FILE, testfile, "audio/wav")},
                data={"purpose": "assistants"},
            )
            assert exception.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.asyncio
async def test_excel_file_handling():
    """Test handling of an Excel file including upload, retrieval, and deletion."""
    # Path to the test Excel file
    excel_file_path = os.path.join(os.path.dirname(__file__), "../../data/test.xlsx")

    # Ensure the file exists
    assert os.path.exists(
        excel_file_path
    ), f"Test Excel file not found at {excel_file_path}"

    # Test file loading and splitting
    documents = await load_file(excel_file_path)
    assert len(documents) > 0, "No documents were loaded from the Excel file"
    assert documents[0].page_content, "The first document has no content"

    split_documents = await split(documents)
    assert len(split_documents) >= len(documents), "Documents were not split properly"
    assert split_documents[0].page_content, "The first split document has no content"

    # Test file upload via API
    with open(excel_file_path, "rb") as excel_file:
        response = client.post(
            "/openai/v1/files",
            files={
                "file": (
                    "test.xlsx",
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
async def test_powerpoint_file_handling():
    """Test handling of a PowerPoint file including upload, retrieval, and deletion."""
    # Path to the test PowerPoint file
    pptx_file_path = os.path.join(os.path.dirname(__file__), "../../data/test.pptx")

    # Ensure the file exists
    assert os.path.exists(
        pptx_file_path
    ), f"Test PowerPoint file not found at {pptx_file_path}"

    # Test file loading and splitting
    documents = await load_file(pptx_file_path)
    assert len(documents) > 0, "No documents were loaded from the PowerPoint file"
    assert documents[0].page_content, "The first document has no content"

    split_documents = await split(documents)
    assert len(split_documents) >= len(documents), "Documents were not split properly"
    assert split_documents[0].page_content, "The first split document has no content"

    # Test file upload via API
    with open(pptx_file_path, "rb") as pptx_file:
        response = client.post(
            "/openai/v1/files",
            files={
                "file": (
                    "test.pptx",
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

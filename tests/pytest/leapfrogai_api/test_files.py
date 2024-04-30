"""Test cases for files router"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from openai.types import FileObject, FileDeleted
from leapfrogai_api.routers.openai.files import router

client = TestClient(router)

test_file_object = FileObject(
    id="1",
    filename="test.jpg",
    bytes=1000,
    created_at=123456,
    object="file",
    purpose="assistants",
    status="uploaded",
    status_details=None,
)

test_file_deleted = FileDeleted(
    id="1",
    object="file",
    deleted=True,
)

test_file_list = [
    test_file_object,
    test_file_object.model_copy(update={"id": "2"}),
]


@patch("leapfrogai_api.routers.openai.files.SupabaseWrapper.list_files")
def test_list_files(mock_list_files):
    """Test list_files endpoint"""
    mock_list_files.return_value = test_file_list
    response = client.get("/openai/v1/files/")
    assert response.status_code == 200
    assert response.json() == {
        "data": [FileObject.model_dump(file) for file in test_file_list],
        "object": "list",
    }

    mock_list_files.assert_called_once()


@patch("leapfrogai_api.routers.openai.files.SupabaseWrapper.get_file_object")
def test_retrieve_file(mock_get_file_object):
    """Test retrieve_file endpoint"""

    mock_get_file_object.return_value = test_file_object
    response = client.get("/openai/v1/files/1")
    assert response.status_code == 200
    assert FileObject.model_validate(response.json())
    assert response.json() == FileObject.model_dump(test_file_object)
    mock_get_file_object.assert_called_once_with(file_id="1")


@patch("leapfrogai_api.routers.openai.files.SupabaseWrapper.delete_file")
def test_delete_file(mock_delete_file):
    """Test delete_file endpoint"""
    mock_delete_file.return_value = test_file_deleted
    response = client.delete("/openai/v1/files/1")
    assert response.status_code == 200
    assert FileDeleted.model_validate(response.json())
    assert response.json() == FileDeleted.model_dump(test_file_deleted)
    mock_delete_file.assert_called_once_with(file_id="1")


@patch("leapfrogai_api.routers.openai.files.SupabaseWrapper.get_file_content")
def test_get_file_content(mock_get_file_content):
    """Test get_file_content endpoint"""
    mock_get_file_content.return_value = b"test"
    response = client.get("/openai/v1/files/1/content")
    assert response.status_code == 200
    # assert response.content == b"test"
    mock_get_file_content.assert_called_once_with(file_id="1")

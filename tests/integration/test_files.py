"""Test the API endpoints for assistants."""

from fastapi.testclient import TestClient
from openai.types import FileObject, FileDeleted
from leapfrogai_api.routers.openai.files import router

client = TestClient(router)


def test_files():
    """Test creating an assistant. Requires a running Supabase instance."""

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
    assert FileObject.model_validate(list_response.json()[0])

    get_response = client.get(f"/openai/v1/files/{create_response.json()['id']}")
    assert get_response.status_code == 200

    get_content_response = client.get(
        f"/openai/v1/files/{create_response.json()['id']}/content"
    )
    assert get_content_response.status_code == 200
    assert testfile_content.decode() in get_content_response.text

    delete_response = client.delete(f"/openai/v1/files/{create_response.json()['id']}")
    assert delete_response.status_code == 200
    assert FileDeleted.model_validate(delete_response.json())

    # Make sure the assistant is not still present
    get_response = client.get(f"/openai/v1/files/{create_response.json()['id']}")
    assert get_response.status_code == 200
    assert get_response.json() is None

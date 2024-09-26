"""Test the API endpoints for auth."""

import os
import time
import pytest
from fastapi import status, HTTPException
from fastapi.testclient import TestClient
from leapfrogai_api.routers.leapfrogai.auth import (
    router,
    APIKeyItem,
)
from leapfrogai_api.backend.security.api_key import APIKey
from leapfrogai_api.backend.constants import THIRTY_DAYS_SECONDS


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
def create_api_key():
    """Create an API key for testing. Requires a running Supabase instance."""

    request = {
        "name": "API Keys Are Cool!",
        "expires_at": int(time.time()) + THIRTY_DAYS_SECONDS,
    }

    response = client.post("/leapfrogai/v1/auth/api-keys", json=request)
    return response


def test_create_api_key(create_api_key):
    """Test creating an API key. Requires a running Supabase instance."""
    assert create_api_key.status_code is status.HTTP_200_OK
    assert "api_key" in create_api_key.json(), "Create should return an API key."
    assert "name" in create_api_key.json(), "Create should return a name."
    assert (
        create_api_key.json()["name"] == "API Keys Are Cool!"
    ), "Create should return a name as 'API Keys Are Cool!'."
    assert "id" in create_api_key.json(), "Create should return an ID."
    assert "created_at" in create_api_key.json(), "Create should return a created_at."
    assert "expires_at" in create_api_key.json(), "Create should return an expires_at."
    assert APIKey.parse(create_api_key.json()["api_key"]), "API key should be valid."


def test_list_api_keys(create_api_key):
    """Test listing API keys. Requires a running Supabase instance."""

    id_ = create_api_key.json()["id"]

    response = client.get("/leapfrogai/v1/auth/api-keys")
    assert response.status_code is status.HTTP_200_OK
    assert len(response.json()) > 0, "List should return at least one API key."
    for api_key in response.json():
        assert APIKeyItem.model_validate(api_key), "API key should be valid."

    assert any(
        api_key["id"] == id_ for api_key in response.json()
    ), "List should return the created API key."


def test_update_api_key(create_api_key):
    """Test updating an API key. Requires a running Supabase instance."""

    id_ = create_api_key.json()["id"]

    request = {
        "name": "API Keys Are Still Cool!",
        "expires_at": int(time.time()) + 100,
    }

    response = client.patch(f"/leapfrogai/v1/auth/api-keys/{id_}", json=request)
    assert response.status_code is status.HTTP_200_OK
    assert APIKeyItem.model_validate(response.json()), "API key should be valid."
    assert response.json()["id"] == id_, "Update should return the created API key."


def test_revoke_api_key(create_api_key):
    """Test revoking an API key. Requires a running Supabase instance."""

    api_key_id = create_api_key.json()["id"]

    response = client.delete(f"/leapfrogai/v1/auth/api-keys/{api_key_id}")
    assert response.status_code is status.HTTP_204_NO_CONTENT

    with pytest.raises(HTTPException):
        response = client.delete(f"/leapfrogai/v1/auth/api-keys/{api_key_id}")
        assert response.status_code is status.HTTP_404_NOT_FOUND

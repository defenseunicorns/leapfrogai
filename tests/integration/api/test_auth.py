"""Test the API endpoints for auth."""

import os
import time

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from leapfrogai_api.routers.leapfrogai.auth import THIRTY_DAYS
from leapfrogai_api.routers.leapfrogai.auth import router


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
        "expires_at": int(time.time()) + THIRTY_DAYS,
    }

    response = client.post("/leapfrogai/v1/auth/create-api-key", json=request)
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


def test_revoke_api_key(create_api_key):
    """Test revoking an API key. Requires a running Supabase instance."""

    api_key_id = create_api_key.json()["id"]

    response = client.delete(f"/leapfrogai/v1/auth/revoke-api-key/{api_key_id}")
    assert response.status_code is status.HTTP_200_OK
    assert "revoked" in response.json(), "Revoke should return a revoked."
    assert response.json()["revoked"] is True, "Revoke should return a revoked as True."
    assert "message" in response.json(), "Revoke should return a message."
    assert (
        response.json()["message"] == "API key revoked."
    ), "Revoke should return a message as 'API key revoked.'."

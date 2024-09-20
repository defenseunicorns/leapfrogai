"""Test the API endpoints for token counting."""

import os
from fastapi import status
from fastapi.testclient import TestClient

from leapfrogai_api.routers.leapfrogai.count import router
from leapfrogai_api.typedef.counting import (
    TokenCountRequestHttp,
    TokenCountResponseHttp,
)

CHAT_MODEL = "test-chat"
INVALID_MODEL = "invalid-model"


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


def test_token_count():
    """Test token counting"""
    request = TokenCountRequestHttp(
        model=CHAT_MODEL, text="This is a test sentence for token counting."
    )

    response = client.post("/leapfrogai/v1/count/tokens", json=request.model_dump())

    assert response.status_code == status.HTTP_200_OK
    token_count_response = TokenCountResponseHttp.model_validate(response.json())
    assert token_count_response.token_count > 0, "Token count should be greater than 0"


def test_token_count_empty_text():
    """Test token counting with empty text"""
    request = TokenCountRequestHttp(model=CHAT_MODEL, text="")

    response = client.post("/leapfrogai/v1/count/tokens", json=request.model_dump())

    assert response.status_code == status.HTTP_200_OK
    token_count_response = TokenCountResponseHttp.model_validate(response.json())
    assert (
        token_count_response.token_count == 0
    ), "Token count should be 0 for empty text"


def test_token_count_invalid_model():
    """Test token counting with an invalid model"""
    request = TokenCountRequestHttp(
        model=INVALID_MODEL, text="This is a test sentence."
    )

    response = client.post("/leapfrogai/v1/count/tokens", json=request.model_dump())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Model 'invalid-model' not found"


def test_token_count_various_lengths():
    """Test token counting with various text lengths, comparing shorter to longer texts."""
    texts = [
        "Short text",
        "This is a slightly longer sentence for testing.",
        "A" * 1000,  # Simulate a very long text
    ]

    token_counts = []

    for text in texts:
        request = TokenCountRequestHttp(model=CHAT_MODEL, text=text)

        response = client.post("/leapfrogai/v1/count/tokens", json=request.model_dump())

        assert response.status_code == status.HTTP_200_OK
        token_count_response = TokenCountResponseHttp.model_validate(response.json())
        token_counts.append(token_count_response.token_count)

    # Assert that each text has more tokens than the previous one
    for i in range(1, len(token_counts)):
        assert (
            token_counts[i] > token_counts[i - 1]
        ), f"Text {i} should have more tokens than text {i-1}"

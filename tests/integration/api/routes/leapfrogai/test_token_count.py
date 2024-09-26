"""Test the API endpoints for token counting."""

from fastapi import status
import pytest

# from leapfrogai_api.routers.leapfrogai.count import router
from leapfrogai_api.typedef.counting import (
    TokenCountRequest,
    TokenCountResponse,
)
from tests.utils.client import get_leapfrogai_model, LeapfrogAIClient

INVALID_MODEL = "invalid-model"


@pytest.fixture(scope="session")
def client():
    return LeapfrogAIClient()


def test_token_count(client):
    """Test token counting"""
    request = TokenCountRequest(
        model=get_leapfrogai_model(), text="This is a test sentence for token counting."
    )

    response = client.post("/leapfrogai/v1/count/tokens", json=request.model_dump())

    assert response.status_code == status.HTTP_200_OK
    token_count_response = TokenCountResponse.model_validate(response.json())
    assert token_count_response.token_count > 0, "Token count should be greater than 0"


def test_token_count_empty_text(client):
    """Test token counting with empty text"""
    request = TokenCountRequest(model=get_leapfrogai_model(), text="")

    response = client.post("/leapfrogai/v1/count/tokens", json=request.model_dump())
    assert response.status_code == status.HTTP_200_OK
    token_count_response = TokenCountResponse.model_validate(response.json())
    assert (
        token_count_response.token_count == 0
    ), "Token count should be 0 for empty text"


def test_token_count_invalid_model(client):
    """Test token counting with an invalid model"""
    request = TokenCountRequest(model=INVALID_MODEL, text="This is a test sentence.")

    response = client.post("/leapfrogai/v1/count/tokens", json=request.model_dump())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Model '{INVALID_MODEL}' not found"}


def test_token_count_various_lengths(client):
    """Test token counting with various text lengths, comparing shorter to longer texts."""
    texts = [
        "Short text",
        "This is a slightly longer sentence for testing.",
        "A" * 1000,  # Simulate a very long text
    ]

    token_counts = []

    for text in texts:
        request = TokenCountRequest(model=get_leapfrogai_model(), text=text)

        response = client.post("/leapfrogai/v1/count/tokens", json=request.model_dump())

        assert response.status_code == status.HTTP_200_OK
        token_count_response = TokenCountResponse.model_validate(response.json())
        token_counts.append(token_count_response.token_count)

    # Assert that each text has more tokens than the previous one
    for i in range(1, len(token_counts)):
        assert (
            token_counts[i] > token_counts[i - 1]
        ), f"Text {i} should have more tokens than text {i-1}"

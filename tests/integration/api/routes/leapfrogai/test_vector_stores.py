from leapfrogai_api.typedef.vectorstores import SearchItem
from tests.utils.client import client_config_factory
from tests.utils.data_path import data_path, TXT_DATA_FILE
from leapfrogai_api.typedef.vectorstores import SearchResponse
from leapfrogai_api.typedef.vectorstores import Vector
import pytest
from tests.utils.client import LeapfrogAIClient
from fastapi import status


@pytest.fixture(scope="session")
def leapfrogai_client():
    return LeapfrogAIClient()


@pytest.fixture(scope="session")
def make_test_vector_store():
    config = client_config_factory("leapfrogai")
    client = config.client
    vector_store = client.beta.vector_stores.create(name="Test data")

    with open(data_path(TXT_DATA_FILE), "rb") as file:
        client.beta.vector_stores.files.upload(
            vector_store_id=vector_store.id, file=file
        )

    yield vector_store

    # Clean up
    client.beta.vector_stores.delete(vector_store_id=vector_store.id)


@pytest.fixture(scope="session")
def make_test_search_response(leapfrogai_client, make_test_vector_store):
    params = {
        "query": "Who is Sam?",
        "vector_store_id": make_test_vector_store.id,
    }

    return leapfrogai_client.post(
        endpoint="/leapfrogai/v1/vector_stores/search", params=params
    )


def test_search(make_test_search_response):
    """Test that the search endpoint returns a valid response."""
    search_response = make_test_search_response
    assert search_response.status_code == status.HTTP_200_OK
    assert len(search_response.json()) > 0
    assert SearchResponse.model_validate(search_response.json())


def test_get_vector(leapfrogai_client, make_test_search_response):
    """Test that the get vector endpoint returns a valid response."""

    search_response = SearchResponse.model_validate(make_test_search_response.json())
    search_item = SearchItem.model_validate(search_response.data[0])
    vector_id = search_item.id

    get_vector_response = leapfrogai_client.get(
        f"/leapfrogai/v1/vector_stores/vector/{vector_id}"
    )

    assert get_vector_response.status_code == status.HTTP_200_OK
    assert len(get_vector_response.json()) > 0
    assert Vector.model_validate(get_vector_response.json())

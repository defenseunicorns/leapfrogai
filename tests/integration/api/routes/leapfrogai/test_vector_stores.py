from leapfrogai_api.typedef.vectorstores.search_types import SearchItem
from tests.utils.client import client_config_factory, text_file_path
from leapfrogai_api.typedef.vectorstores import SearchResponse
from leapfrogai_api.typedef.vectorstores import Vector
import pytest
from tests.utils.client import LeapfrogAIClient


@pytest.fixture(scope="session")
def leapfrogai_client():
    return LeapfrogAIClient()


@pytest.fixture(scope="session")
def make_test_vector_store():
    config = client_config_factory("leapfrogai")
    client = config.client
    vector_store = client.beta.vector_stores.create(name="Test data")

    with open(text_file_path(), "rb") as file:
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
    # perform a search on the vector store

    search_response = make_test_search_response

    # assert the search response fits the pydanctic model of SearchResponse
    assert len(search_response) > 0
    assert SearchResponse.model_validate(search_response)


def test_get_vector(leapfrogai_client, make_test_search_response):
    # get the first vector from the search response

    search_response = SearchResponse.model_validate(make_test_search_response)
    search_item = SearchItem.model_validate(search_response.data[0])
    vector_id = search_item.id

    get_vector_response = leapfrogai_client.get(
        f"/leapfrogai/v1/vector_stores/vector/{vector_id}"
    )

    # check the pydantic model of the response against the Vector type
    assert len(get_vector_response) > 0
    assert Vector.model_validate(get_vector_response)

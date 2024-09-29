import pytest

from openai.types.beta.vector_store import VectorStore
from openai.types.beta.vector_store_deleted import VectorStoreDeleted

from tests.utils.client import client_config_factory


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_vector_store_create(client_name):
    config = client_config_factory(client_name)
    client = config.client  # shorthand

    vector_store = client.beta.vector_stores.create(name="Test data")

    assert isinstance(vector_store, VectorStore)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_vector_store_list(client_name):
    config = client_config_factory(client_name)
    client = config.client  # shorthand

    client.beta.vector_stores.create(name="Test data")

    vector_store_list = client.beta.vector_stores.list()

    assert len(vector_store_list.data) > 0
    assert all(
        isinstance(vector_store, VectorStore) for vector_store in vector_store_list.data
    )


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_vector_store_delete(client_name):
    config = client_config_factory(client_name)
    client = config.client

    vector_store = client.beta.vector_stores.create(name="Test data")

    result = client.beta.vector_stores.delete(vector_store_id=vector_store.id)

    assert isinstance(result, VectorStoreDeleted)
    assert result.id == vector_store.id

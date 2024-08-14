import pytest

from openai.types.beta.vector_store import VectorStore

from .utils import client_config_factory, text_file_path


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_vector_store_empty(client_name):
    config = client_config_factory(client_name)
    client = config["client"]  # shorthand

    vector_store = client.beta.vector_stores.create(name="Test data")

    assert isinstance(vector_store, VectorStore)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_vector_store_with_file(client_name):
    config = client_config_factory(client_name)
    client = config["client"]  # shorthand

    vector_store = client.beta.vector_stores.create(name="Test data")
    with open(text_file_path(), "rb") as file:
        client.beta.vector_stores.files.upload(
            vector_store_id=vector_store.id, file=file
        )

    assert isinstance(vector_store, VectorStore)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_vector_store_batched(client_name):
    config = client_config_factory(client_name)
    client = config["client"]  # shorthand

    vector_store = client.beta.vector_stores.create(name="Test data")

    file_streams = [open(text_file_path(), "rb")]

    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    assert isinstance(vector_store, VectorStore)

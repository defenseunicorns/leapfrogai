import pytest

from openai.types.beta.vector_store import VectorStore
from openai.types.beta.vector_stores.vector_store_file_deleted import (
    VectorStoreFileDeleted,
)
from openai.types.beta.vector_stores.vector_store_file import VectorStoreFile

from .utils import client_config_factory, text_file_path


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_file_upload(client_name):
    config = client_config_factory(client_name)
    client = config["client"]  # shorthand

    vector_store = client.beta.vector_stores.create(name="Test data")
    with open(text_file_path(), "rb") as file:
        vector_store_file = client.beta.vector_stores.files.upload(
            vector_store_id=vector_store.id, file=file
        )

    assert isinstance(vector_store, VectorStore)
    assert isinstance(vector_store_file, VectorStoreFile)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_file_upload_batches(client_name):
    config = client_config_factory(client_name)
    client = config["client"]  # shorthand

    vector_store = client.beta.vector_stores.create(name="Test data")

    file_streams = [open(text_file_path(), "rb")]

    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    assert isinstance(vector_store, VectorStore)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_file_delete(client_name):
    config = client_config_factory(client_name)
    client = config["client"]

    vector_store = client.beta.vector_stores.create(name="Test data")
    with open(text_file_path(), "rb") as file:
        vector_store_file = client.beta.vector_stores.files.upload(
            vector_store_id=vector_store.id, file=file
        )

    res = client.beta.vector_stores.files.delete(
        file_id=vector_store_file.id, vector_store_id=vector_store.id
    )

    assert isinstance(res, VectorStoreFileDeleted)
    assert res.id == vector_store_file.id

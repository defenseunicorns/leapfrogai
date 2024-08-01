"""Conformance test the LeapfrogAI API against the OpenAI spec."""

import os
from pathlib import Path
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types import FileObject, FileDeleted
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_stores import VectorStoreFile
import pytest

client = OpenAI(
    base_url=os.getenv("LEAPFROGAI_API_URL"), api_key=os.getenv("LEAPFROGAI_API_KEY")
)

TEST_FILE_PATH = Path(os.path.dirname(__file__) + "/../../data/test.txt")

CHAT_PARAMS = [
    (
        "vllm",
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
        ],
    ),
    (
        "llama-cpp-python",
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
        ],
    ),
]


@pytest.mark.parametrize("model,messages", CHAT_PARAMS)
def test_chat_completion(model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    assert isinstance(response, ChatCompletion)
    assert response.choices[0].message.role == "assistant"
    assert len(response.choices[0].message.content) > 0


@pytest.mark.parametrize("model,messages", CHAT_PARAMS)
def test_chat_completion_streaming(model, messages):
    """
    Test the chat completion endpoint with streaming.

    This function verifies that the chat completion API:
    1. Returns a stream of ChatCompletionChunk objects
    2. Each streamed response contains a delta with content
    """
    stream = client.chat.completions.create(model=model, messages=messages, stream=True)
    accumulated_content = ""
    for chunk in stream:
        assert isinstance(chunk, ChatCompletionChunk)
        if chunk.choices[0].delta.content is not None:
            accumulated_content += chunk.choices[0].delta.content
    assert len(accumulated_content) > 0


def test_files():
    """
    Test file operations including create, retrieve, list, and delete.

    This function verifies that the file API can:
    1. Create a new file and return a FileObject
    2. Retrieve a file by ID
    3. List files and include the created file
    4. Delete a file and confirm the deletion
    """
    # Create file
    create_file_response = client.files.create(
        file=TEST_FILE_PATH,
        purpose="assistants",
    )
    assert isinstance(create_file_response, FileObject)
    assert create_file_response.id is not None

    # Retrieve file
    get_file_response = client.files.retrieve(file_id=create_file_response.id)
    assert isinstance(get_file_response, FileObject)
    assert get_file_response.purpose == "assistants"

    # List files
    list_files_response = client.files.list()
    assert any(file.id == create_file_response.id for file in list_files_response.data)

    # Delete file
    delete_file_response = client.files.delete(file_id=create_file_response.id)
    assert isinstance(delete_file_response, FileDeleted)
    assert delete_file_response.deleted is True


def test_vector_store():
    """
    Test vector store operations including create, add file, list, and delete.

    This function verifies that the vector store API can:
    1. Create a new vector store
    2. Create a file and add it to the vector store
    3. List vector stores and files within a vector store
    4. Delete the vector store and confirm the deletion
    """
    # Create vector store
    create_vector_store_response = client.beta.vector_stores.create(
        name="test_vector_store"
    )
    assert isinstance(create_vector_store_response, VectorStore)
    assert create_vector_store_response.name == "test_vector_store"
    assert create_vector_store_response.id is not None

    # Create file
    create_file_response = client.files.create(
        file=TEST_FILE_PATH,
        purpose="assistants",
    )

    # Add file to vector store
    create_vector_store_file_response = client.beta.vector_stores.files.create(
        vector_store_id=create_vector_store_response.id, file_id=create_file_response.id
    )
    assert isinstance(create_vector_store_file_response, VectorStoreFile)
    assert (
        create_vector_store_file_response.vector_store_id
        == create_vector_store_response.id
    )

    # List vector stores
    list_vector_stores_response = client.beta.vector_stores.list()
    assert any(
        vs.id == create_vector_store_response.id
        for vs in list_vector_stores_response.data
    )

    # List files in vector store
    list_vector_store_files_response = client.beta.vector_stores.files.list(
        vector_store_id=create_vector_store_response.id
    )
    assert any(
        file.id == create_file_response.id
        for file in list_vector_store_files_response.data
    )

    # Delete vector store
    delete_vector_store_response = client.beta.vector_stores.delete(
        vector_store_id=create_vector_store_response.id
    )
    assert isinstance(delete_vector_store_response, VectorStoreDeleted)
    assert delete_vector_store_response.deleted is True

    # Clean up file
    client.files.delete(file_id=create_file_response.id)

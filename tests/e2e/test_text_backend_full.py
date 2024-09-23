import time
import tempfile
import requests
import pytest
from openai import OpenAI
from openai.types.beta.vector_store import VectorStore

from leapfrogai_api.typedef.vectorstores import VectorStoreStatus


def download_arxiv_pdf():
    url = "https://arxiv.org/pdf/1706.03762.pdf"
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    else:
        raise Exception(
            f"Failed to download PDF from ArXiv. Status code: {response.status_code}"
        )


def test_run_with_background_task(client: OpenAI, model_name: str):
    """
    This test confirms whether a vector store for an assistant can index files
    while chatting at the same time.
    """
    print("Starting test_run_with_background_task")

    # Download the ArXiv PDF
    pdf_path = download_arxiv_pdf()
    print(f"Downloaded ArXiv PDF to: {pdf_path}")

    # Upload the PDF file
    with open(pdf_path, "rb") as file:
        file_upload = client.files.create(file=file, purpose="assistants")
    assert file_upload.id is not None
    print(f"Uploaded PDF file with ID: {file_upload.id}")

    # Create a vector store
    vector_store: VectorStore = client.beta.vector_stores.create(
        name="test_background",
        file_ids=[file_upload.id],
    )
    assert vector_store.id is not None
    print(f"Created vector store with ID: {vector_store.id}")

    # Check initial status
    assert vector_store.status == VectorStoreStatus.IN_PROGRESS.value
    print(f"Initial vector store status: {vector_store.status}")

    # Create an assistant
    assistant = client.beta.assistants.create(
        model=model_name,
        name="Test Assistant",
        instructions="You are a helpful assistant with access to a knowledge base about AI and machine learning.",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    assert assistant.id is not None
    print(f"Created assistant with ID: {assistant.id}")

    # Create a thread
    thread = client.beta.threads.create()
    assert thread.id is not None
    print(f"Created thread with ID: {thread.id}")

    # Function to check vector store status
    def check_vector_store_status():
        nonlocal vector_store
        vector_store = client.beta.vector_stores.retrieve(
            vector_store_id=vector_store.id
        )
        return vector_store.status

    # Perform multiple runs while indexing is in progress
    num_runs = 5
    responses = []

    for i in range(num_runs):
        # Check if indexing is still in progress
        current_status = check_vector_store_status()
        print(f"Run {i + 1}: Current vector store status: {current_status}")
        if current_status == VectorStoreStatus.COMPLETED.value:
            pytest.fail(
                f"Vector store indexing completed without concurrently running multiple runs and ended after only {i} run(s)"
            )

        # Add a message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Run {i + 1}: What is the main topic of the paper in the vector store?",
        )
        assert message.id is not None
        print(f"Run {i + 1}: Added message to thread")

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Please use the file_search tool to find relevant information from the uploaded ArXiv paper.",
        )
        assert run.id is not None
        print(f"Run {i + 1}: Created run with ID: {run.id}")

        # Retrieve the assistant's message
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assert (
            len(messages.data) > i + 1
        ), f"No response message from the assistant for run {i + 1}"
        assistant_message = messages.data[0].content[0].text.value
        responses.append(assistant_message)
        print(f"Run {i + 1}: Received assistant's response")

        print(f"Completed run {i + 1}")

        # Check if indexing is still in progress
        current_status = check_vector_store_status()
        if current_status == VectorStoreStatus.COMPLETED.value:
            print(f"Vector store indexing completed after {i + 1} run(s)")
            pytest.fail(
                f"Vector store indexing completed without concurrently running multiple runs and ended after only {i} run(s)"
            )

    # Wait for indexing to complete if it hasn't already
    max_wait_time_in_seconds = 60 * 3  # 3 minutes
    start_time = time.time()
    while check_vector_store_status() != VectorStoreStatus.COMPLETED.value:
        if time.time() - start_time > max_wait_time_in_seconds:
            pytest.fail(
                "Vector store indexing did not complete within the expected time"
            )
        time.sleep(2)
        print(
            f"Waiting for indexing to complete... Current status: {check_vector_store_status()}"
        )

    # Verify final vector store status
    assert vector_store.status == VectorStoreStatus.COMPLETED.value
    print(f"Final vector store status: {vector_store.status}")

    # Check that at least one of the assistant's responses contains relevant information
    assert any(
        len(response) > 0 for response in responses
    ), "All assistant responses are empty"
    assert any(
        "arxiv" in response.lower() or "paper" in response.lower()
        for response in responses
    ), "None of the assistant's responses mention the ArXiv paper"
    print("Verified assistant responses")

    # Clean up
    client.beta.assistants.delete(assistant_id=assistant.id)
    client.beta.vector_stores.delete(vector_store_id=vector_store.id)
    client.files.delete(file_id=file_upload.id)
    print("Cleaned up resources")

    print("test_run_with_background_task completed successfully")

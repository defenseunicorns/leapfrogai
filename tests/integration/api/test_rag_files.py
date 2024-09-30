import os
from typing import Optional

import requests
from openai.types.beta.threads.text import Text
import pytest
from tests.utils.data_path import data_path

from leapfrogai_api.typedef.rag.rag_types import ConfigurationPayload
from tests.utils.client import client_config_factory


def make_test_assistant(client, model, vector_store_id):
    assistant = client.beta.assistants.create(
        name="Test Assistant",
        instructions="You must provide a response based on the attached files.",
        model=model,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    return assistant


def make_test_run(client, assistant, thread):
    run = client.beta.threads.runs.create_and_poll(
        assistant_id=assistant.id, thread_id=thread.id
    )
    return run


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_NIAH_TESTS") != "true",
    reason="LFAI_RUN_NIAH_TESTS envvar was not set to true",
)
def test_rag_needle_haystack():
    config = client_config_factory("leapfrogai")
    client = config.client

    vector_store = client.beta.vector_stores.create(name="Test data")
    file_names = [
        "test_rag_1.1.txt",
        "test_rag_1.2.txt",
        "test_rag_1.3.txt",
        "test_rag_1.4.txt",
        "test_rag_1.5.txt",
        "test_rag_2.1.txt",
    ]
    vector_store_files = []
    for file_name in file_names:
        with open(data_path(file_name), "rb") as file:
            vector_store_files.append(
                client.beta.vector_stores.files.upload(
                    vector_store_id=vector_store.id, file=file
                )
            )

    assistant = make_test_assistant(client, config.model, vector_store.id)
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Tell me about cats.",
    )
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="There is one piece of fruit in the fridge. What is it and where is it located?",
    )
    run = make_test_run(client, assistant, thread)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id, run_id=run.id
    ).data

    # Get the response content from the last message
    message_content = messages[-1].content[0].text
    assert isinstance(message_content, Text)
    assert "orange" in message_content.value
    assert len(message_content.annotations) > 0

    for a in message_content.annotations:
        print(a.text)


def configure_rag(
    base_url: str,
    enable_reranking: bool,
    ranking_model: str,
    rag_top_k_when_reranking: int,
):
    """
    Configures the RAG settings.

    Args:
        base_url: The base URL of the API (e.g., "http://localhost:8000").
        enable_reranking: Whether to enable reranking.
        ranking_model: The ranking model to use.
        rag_top_k_when_reranking: The top-k results to return before reranking.
    """

    url = f"{base_url}/leapfrogai/v1/rag/configure"
    configuration = ConfigurationPayload(
        enable_reranking=enable_reranking,
        ranking_model=ranking_model,
        rag_top_k_when_reranking=rag_top_k_when_reranking,
    )

    try:
        response = requests.patch(url, json=configuration.model_dump())
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print("RAG configuration updated successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error configuring RAG: {e}")


def get_rag_configuration(base_url: str) -> Optional[ConfigurationPayload]:
    """
    Retrieves the current RAG configuration.

    Args:
        base_url: The base URL of the API.

    Returns:
        The RAG configuration, or None if there was an error.
    """
    url = f"{base_url}/leapfrogai/v1/rag/configure"

    try:
        response = requests.get(url)
        response.raise_for_status()
        config = ConfigurationPayload.model_validate_json(response.text)
        print(f"Current RAG configuration: {config}")
        return config
    except requests.exceptions.RequestException as e:
        print(f"Error getting RAG configuration: {e}")
        return None


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_NIAH_TESTS") != "true",
    reason="LFAI_RUN_NIAH_TESTS envvar was not set to true",
)
def test_rag_needle_haystack_with_reranking():
    base_url = os.getenv(
        "LEAPFROGAI_API_URL", "https://leapfrogai-api.uds.dev/openai/v1"
    )
    configure_rag(base_url, True, "flashrank", 100)
    config_result = get_rag_configuration(base_url)
    assert config_result.enable_reranking is True
    test_rag_needle_haystack()

import pytest
from openai.types.beta.assistant import Assistant

from tests.utils.client import client_config_factory


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_assistant(client_name):
    config = client_config_factory(client_name)
    client = config.client

    vector_store = client.beta.vector_stores.create(name="Test data")

    assistant = client.beta.assistants.create(
        name="Test Assistant",
        instructions="You must provide a response based on the attached files.",
        model=config.model,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    assert isinstance(assistant, Assistant)

    client.beta.assistants.delete(assistant.id)


@pytest.mark.parametrize("client_name", ["openai", "leapfrogai"])
def test_modify_assistant(client_name):
    config = client_config_factory(client_name)
    client = config.client

    vector_store = client.beta.vector_stores.create(name="Test data")

    assistant = client.beta.assistants.create(
        name="Test Assistant",
        instructions="You must provide a response based on the attached files.",
        model=config.model,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        metadata={"Test": "Testing."},
    )

    modified_assistant = client.beta.assistants.update(
        assistant.id,
        name="Modified Assistant",
        metadata={"Test 2": "This is the test."},
    )

    assert modified_assistant.name == "Modified Assistant"
    assert modified_assistant.id == assistant.id
    assert modified_assistant.model == assistant.model

    client.beta.assistants.delete(modified_assistant.id)

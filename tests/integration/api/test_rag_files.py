import os
from pathlib import Path
from openai.types.beta.threads.text import Text
from openai import OpenAI


LEAPFROGAI_MODEL = "llama-cpp-python"
OPENAI_MODEL = "gpt-4o-mini"


def text_file_path():
    return Path(os.path.dirname(__file__) + "/../../data/test_with_data.txt")


def openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def leapfrogai_client():
    return OpenAI(
        base_url=os.getenv("LEAPFROGAI_API_URL"),
        api_key=os.getenv("LEAPFROGAI_API_KEY"),
    )


def client_config_factory(client_name):
    if client_name == "openai":
        return dict(client=openai_client(), model=OPENAI_MODEL)
    elif client_name == "leapfrogai":
        return dict(client=leapfrogai_client(), model=LEAPFROGAI_MODEL)


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


def test_rag_needle_haystack():
    config = client_config_factory("leapfrogai")
    client = config["client"]

    vector_store = client.beta.vector_stores.create(name="Test data")
    file_path = "../../data"
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
        with open(
            f"{Path(os.path.dirname(__file__))}/{file_path}/{file_name}", "rb"
        ) as file:
            vector_store_files.append(
                client.beta.vector_stores.files.upload(
                    vector_store_id=vector_store.id, file=file
                )
            )

    assistant = make_test_assistant(client, config["model"], vector_store.id)
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
    assert len(message_content.annotations) > 0

    for a in message_content.annotations:
        print(a.text)

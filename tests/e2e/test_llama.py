from pathlib import Path

import pytest
from openai import InternalServerError, OpenAI

from .utils import create_test_user

client = OpenAI(
    base_url="https://leapfrogai-api.uds.dev/openai/v1", api_key=create_test_user()
)

model_name = "llama-cpp-python"


def test_chat_completions():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is your name?"},
    ]

    chat_completion = client.chat.completions.create(
        model=model_name, messages=messages
    )
    assert chat_completion.model == model_name
    assert len(chat_completion.choices) == 1
    assert chat_completion.choices[0].message.role == "assistant"
    assert len(chat_completion.choices[0].message.content) > 0
    assert len(chat_completion.choices[0].message.content) < 500


def test_embeddings():
    with pytest.raises(InternalServerError) as excinfo:
        client.embeddings.create(
            model=model_name,
            input="This should result in a failure",
        )
    assert str(excinfo.value) == "Internal Server Error"


def test_transcriptions():
    with pytest.raises(InternalServerError) as excinfo:
        client.audio.transcriptions.create(
            model=model_name, file=Path("tests/data/0min12sec.wav")
        )

    assert str(excinfo.value) == "Internal Server Error"

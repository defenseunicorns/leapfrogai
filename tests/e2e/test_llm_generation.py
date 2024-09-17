from pathlib import Path

import pytest
from openai import InternalServerError, OpenAI


def test_chat_completions(client: OpenAI, model_name: str):
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


def test_completions(client: OpenAI, model_name: str):
    completion = client.completions.create(
        model=model_name, prompt="Say hello to me.", max_new_tokens=200
    )
    assert completion.model == model_name
    assert len(completion.choices) == 1
    assert len(completion.choices[0].text) > 0
    assert len(completion.choices[0].text) < 500


def test_embeddings(client: OpenAI, model_name: str):
    with pytest.raises(InternalServerError) as excinfo:
        client.embeddings.create(
            model=model_name,
            input="This should result in a failure",
        )
    assert str(excinfo.value) == "Internal Server Error"


def test_transcriptions(client: OpenAI, model_name: str):
    with pytest.raises(InternalServerError) as excinfo:
        client.audio.transcriptions.create(
            model=model_name, file=Path("tests/data/0min12sec.wav")
        )

    assert str(excinfo.value) == "Internal Server Error"

from pathlib import Path

import pytest
from openai import InternalServerError

model_name = "text-embeddings"


def test_completions(client):
    with pytest.raises(InternalServerError) as excinfo:
        client.completions.create(
            model=model_name,
            prompt="This should result in a failure",
        )
    assert str(excinfo.value) == "Internal Server Error"


def test_chat_completions(client):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "This should result in a failure"},
    ]

    with pytest.raises(InternalServerError) as excinfo:
        client.chat.completions.create(model=model_name, messages=messages)
    assert str(excinfo.value) == "Internal Server Error"


def test_embeddings(client):
    embedding_response = client.embeddings.create(
        model=model_name,
        input="This should result in a failure",
    )

    assert embedding_response.model == model_name
    assert len(embedding_response.data) > 0
    assert len(embedding_response.data[0].embedding) > 0
    assert len(embedding_response.data[0].embedding) < 1000


def test_transcriptions(client):
    with pytest.raises(InternalServerError) as excinfo:
        client.audio.transcriptions.create(
            model=model_name, file=Path("tests/data/0min12sec.wav")
        )
    assert str(excinfo.value) == "Internal Server Error"

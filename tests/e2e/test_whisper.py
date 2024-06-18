from pathlib import Path

import pytest
from openai import InternalServerError

def test_completions(client):
    with pytest.raises(InternalServerError) as excinfo:
        client.completions.create(
            model="whisper",
            prompt="This should result in a failure",
        )
    assert str(excinfo.value) == "Internal Server Error"


def test_chat_completions(client):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "This should result in a failure"},
    ]

    with pytest.raises(InternalServerError) as excinfo:
        client.chat.completions.create(model="whisper", messages=messages)
    assert str(excinfo.value) == "Internal Server Error"


def test_embeddings(client):
    with pytest.raises(InternalServerError) as excinfo:
        client.embeddings.create(
            model="whisper",
            input="This should result in a failure",
        )
    assert str(excinfo.value) == "Internal Server Error"


def test_transcriptions(client):
    transcription = client.audio.transcriptions.create(
        model="whisper", file=Path("tests/data/0min12sec.wav")
    )

    assert len(transcription.text) > 0  # The transcription should not be empty
    assert len(transcription.text) < 500  # The transcription should not be too long

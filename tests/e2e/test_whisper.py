import string
from pathlib import Path

import pytest
from openai import InternalServerError, OpenAI
import unicodedata


def test_completions(client: OpenAI):
    with pytest.raises(InternalServerError) as excinfo:
        client.completions.create(
            model="whisper",
            prompt="This should result in a failure",
        )
    assert str(excinfo.value) == "Internal Server Error"


def test_chat_completions(client: OpenAI):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "This should result in a failure"},
    ]

    with pytest.raises(InternalServerError) as excinfo:
        client.chat.completions.create(model="whisper", messages=messages)
    assert str(excinfo.value) == "Internal Server Error"


def test_embeddings(client: OpenAI):
    with pytest.raises(InternalServerError) as excinfo:
        client.embeddings.create(
            model="whisper",
            input="This should result in a failure",
        )
    assert str(excinfo.value) == "Internal Server Error"


def test_transcriptions(client: OpenAI):
    transcription = client.audio.transcriptions.create(
        model="whisper",
        file=Path("tests/data/0min12sec.wav"),
        language="en",
        prompt="This is a test transcription.",
        response_format="json",
        temperature=0.5,
        timestamp_granularities=["word", "segment"],
    )

    assert len(transcription.text) > 0, "The transcription should not be empty"
    assert len(transcription.text) < 500, "The transcription should not be too long"


def test_translations(client: OpenAI):
    translation = client.audio.translations.create(
        model="whisper",
        file=Path("tests/data/arabic-audio.wav"),
        prompt="This is a test translation.",
        response_format="json",
        temperature=0.5,
    )

    assert len(translation.text) > 0, "The translation should not be empty"
    assert len(translation.text) < 500, "The translation should not be too long"

    def is_english_or_punctuation(c):
        if c in string.punctuation or c.isspace():
            return True
        if c.isalpha():
            # Allow uppercase letters (for proper nouns) and common Latin characters
            return c.isupper() or unicodedata.name(c).startswith(("LATIN", "COMMON"))
        return False

    english_chars = [is_english_or_punctuation(c) for c in translation.text]

    assert all(english_chars), "Non-English characters have been returned"


def test_non_english_transcription(client: OpenAI):
    # Arabic transcription
    arabic_transcription = client.audio.transcriptions.create(
        model="whisper",
        file=Path("tests/data/arabic-audio.wav"),
        response_format="json",
        temperature=0.5,
        timestamp_granularities=["word", "segment"],
    )

    assert (
        len(arabic_transcription.text) > 0
    ), "The Arabic transcription should not be empty"
    assert (
        len(arabic_transcription.text) < 500
    ), "The Arabic transcription should not be too long"

    def is_arabic_or_punctuation(c):
        if c in string.punctuation or c.isspace():
            return True
        return unicodedata.name(c).startswith("ARABIC")

    arabic_chars = [is_arabic_or_punctuation(c) for c in arabic_transcription.text]
    assert all(
        arabic_chars
    ), "Non-Arabic characters have been returned in Arabic transcription"

    # Russian transcription
    russian_transcription = client.audio.transcriptions.create(
        model="whisper",
        file=Path("tests/data/russian.mp3"),
        response_format="json",
        temperature=0.5,
        timestamp_granularities=["word", "segment"],
    )

    assert (
        len(russian_transcription.text) > 0
    ), "The Russian transcription should not be empty"
    assert (
        len(russian_transcription.text) < 500
    ), "The Russian transcription should not be too long"

    def is_russian_or_punctuation(c):
        if c in string.punctuation or c.isspace():
            return True
        return unicodedata.name(c).startswith("CYRILLIC")

    russian_chars = [is_russian_or_punctuation(c) for c in russian_transcription.text]
    assert all(
        russian_chars
    ), "Non-Russian characters have been returned in Russian transcription"

from pathlib import Path
import os
from typing import Iterable

import pytest
from openai import InternalServerError, OpenAI
from openai.types.chat import ChatCompletionMessageParam
from tests.utils.data_path import data_path, WAV_FILE

# Test generation parameters
SYSTEM_PROMPT = "You are a helpful assistant."
USER_PROMPT = "Only return 1 word"
MAX_TOKENS = 128
TEMPERATURE = 0


def test_chat_completions(client: OpenAI, model_name: str):
    messages: Iterable[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ]

    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    assert chat_completion.model == model_name
    assert len(chat_completion.choices) == 1
    if (
        chat_completion.choices[0].message.content is not None
        and chat_completion.choices[0].message.role is not None
    ):
        assert chat_completion.choices[0].message.role == "assistant"
        assert len(chat_completion.choices[0].message.content) > 0
        assert len(chat_completion.choices[0].message.content) < 500


def test_completions(client: OpenAI, model_name: str):
    completion = client.completions.create(
        model=model_name,
        prompt=USER_PROMPT,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
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
            model=model_name,
            file=data_path(WAV_FILE),
        )

    assert str(excinfo.value) == "Internal Server Error"

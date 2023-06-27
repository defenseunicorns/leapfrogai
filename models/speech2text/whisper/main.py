import logging
import tempfile
from typing import Iterator

import whisper

import leapfrog

model = whisper.load_model("large")


def make_transcribe_request(filename, task, language, temperature, prompt):
    return model.transcribe(
        filename, task=task, language=language, temperature=temperature, prompt=prompt
    )


def call_whisper(
    request_iterator: Iterator[leapfrog.AudioRequest], task: str
) -> leapfrog.AudioResponse:
    data = bytearray()
    prompt = ""
    temperature = 0.0
    inputLanguage = "en"

    for request in request_iterator:
        if (
            request.metadata.prompt
            and request.metadata.temperature
            and request.metadata.inputlanguage
        ):
            prompt = request.metadata.prompt
            temperature = request.metadata.temperature
            inputLanguage = request.metadata.inputlanguage
            audioFormat = request.metadata.format
            continue

        data.extend(request.chunk_data)

    with tempfile.NamedTemporaryFile("wb") as f:
        f.write(data)
        result = make_transcribe_request(
            f.name, task, inputLanguage, temperature, prompt
        )
        text = str(result["text"])
        return leapfrog.AudioResponse(text=text)


class Whisper(leapfrog.AudioServicer):
    def Translate(
        self,
        request_iterator: Iterator[leapfrog.AudioRequest],
        context: leapfrog.GrpcContext,
    ):
        return call_whisper(request_iterator, "translate")

    def Transcribe(
        self,
        request_iterator: Iterator[leapfrog.AudioRequest],
        context: leapfrog.GrpcContext,
    ):
        return call_whisper(request_iterator, "transcribe")

    def Name(self, request, context):
        return leapfrog.NameResponse(name="whisper")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    leapfrog.serve(Whisper())

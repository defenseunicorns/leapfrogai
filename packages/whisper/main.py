import asyncio
import logging
import os
import tempfile
from typing import Iterator

import leapfrogai_sdk as lfai
from faster_whisper import WhisperModel

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)

model_path = os.environ.get("LFAI_MODEL_PATH", ".model")

GPU_ENABLED = True if int(os.environ.get("GPU_REQUEST", 0)) > 0 else False


def make_transcribe_request(filename, task, language, temperature, prompt):
    device = "cuda" if GPU_ENABLED else "cpu"
    model = WhisperModel(model_path, device=device, compute_type="float32")

    # Prepare kwargs with non-None values
    kwargs = {}
    if task:
        if task in ["transcribe", "translate"]:
            kwargs["task"] = task
            logger.info(f"Task {task} is starting")
        else:
            logger.error(f"Task {task} is not supported")
            return {"text": ""}
    if language:
        if language in model.supported_languages:
            kwargs["language"] = language
            logger.info(f"Language {language} is supported")
        else:
            logger.error(f"Language {language} is not supported")
    if temperature:
        kwargs["temperature"] = temperature
        logger.info(f"Temperature {temperature} is set")
    if prompt:
        kwargs["initial_prompt"] = prompt
        logger.info(f"Prompt {prompt} is set")

    try:
        # Call transcribe with only non-None parameters
        segments, info = model.transcribe(filename, beam_size=5, **kwargs)
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return {"text": ""}

    output = ""
    for segment in segments:
        output += segment.text

    logger.info("Completed " + filename)

    return {"text": output}


def call_whisper(
    request_iterator: Iterator[lfai.AudioRequest], task: str
) -> lfai.AudioResponse:
    data = bytearray()
    prompt = ""
    temperature = 0.0
    # By default, automatically detect the language
    inputLanguage = "en"

    for request in request_iterator:
        metadata = request.metadata
        updated = False

        if metadata.prompt:
            prompt = metadata.prompt
            updated = True

        if metadata.temperature:
            temperature = metadata.temperature
            updated = True

        if metadata.inputlanguage:
            inputLanguage = metadata.inputlanguage
            updated = True

        if updated:
            logger.info(
                f"Updated metadata: Prompt='{prompt}', Temperature={temperature}, Input Language='{inputLanguage}'"
            )
        else:
            data.extend(request.chunk_data)

    with tempfile.NamedTemporaryFile("wb") as f:
        f.write(data)
        result = make_transcribe_request(
            f.name, task, inputLanguage, temperature, prompt
        )
        text = str(result["text"])

        if task == "transcribe":
            logger.info("Transcription complete!")
        elif task == "translate":
            logger.info("Translation complete!")
        return lfai.AudioResponse(text=text)


class Whisper(lfai.AudioServicer):
    def Translate(
        self,
        request_iterator: Iterator[lfai.AudioRequest],
        context: lfai.GrpcContext,
    ):
        return call_whisper(request_iterator, "translate")

    def Transcribe(
        self,
        request_iterator: Iterator[lfai.AudioRequest],
        context: lfai.GrpcContext,
    ):
        return call_whisper(request_iterator, "transcribe")

    def Name(self, request, context):
        return lfai.NameResponse(name="whisper")


async def main():
    logger.info(f"GPU_ENABLED = {GPU_ENABLED}")
    await lfai.serve(Whisper())


if __name__ == "__main__":
    asyncio.run(main())

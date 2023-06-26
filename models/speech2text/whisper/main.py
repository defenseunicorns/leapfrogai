import whisper
import aiofiles
import asyncio
from typing import Annotated
from enum import Enum
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import leapfrog
import logging

class Whisper(leapfrog.AudioService):
    model = whisper.load_model("large")

    def Translate(self, request: leapfrog.AudioRequest, context: leapfrog.GrpcContext):
        # TODO @gerred can you complete this?
        raise NotImplementedError('Method not implemented!')

    def Transcribe(self, request: leapfrog.AudioRequest, context: leapfrog.GrpcContext):
        # TODO @gerred can you complete this?
        raise NotImplementedError('Method not implemented!')

    def Name(self, request, context):
        return leapfrog.NameResponse ( name = "repeater" )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    leapfrog.serve(Whisper())



app = FastAPI()

model = whisper.load_model("large")
loop = asyncio.get_event_loop()


def make_transcribe_request(filename, task, language):
    return model.transcribe(filename, task=task, language=language)


class WhisperTask(str, Enum):
    transcribe = "transcribe"
    translate = "translate"


# TODO: Make this class use a dict, and show languages in Swagger
class LanguageCode(str, Enum):
    af = "af"
    ar = "ar"
    az = "az"
    be = "be"
    bg = "bg"
    bs = "bs"
    ca = "ca"
    cs = "cs"
    cy = "cy"
    da = "da"
    de = "de"
    el = "el"
    en = "en"
    es = "es"
    et = "et"
    fa = "fa"
    fi = "fi"
    fr = "fr"
    gl = "gl"
    he = "he"
    hi = "hi"
    hr = "hr"
    hu = "hu"
    hy = "hy"
    id = "id"
    icelandic = "is"
    it = "it"
    ja = "ja"
    kk = "kk"
    kn = "kn"
    ko = "ko"
    lt = "lt"
    lv = "lv"
    mk = "mk"
    ms = "ms"
    mr = "mr"
    mi = "mi"
    nl = "nl"
    ne = "ne"
    no = "no"
    pl = "pl"
    pt = "pt"
    ro = "ro"
    ru = "ru"
    sk = "sk"
    sl = "sl"
    sr = "sr"
    sv = "sv"
    sw = "sw"
    ta = "ta"
    th = "th"
    tl = "tl"
    tr = "tr"
    uk = "uk"
    ur = "ur"
    vi = "vi"
    zh = "zh"


class TranscribeResponse(BaseModel):
    result: str


@app.post("/transcribe")
async def transcribe(
    file: Annotated[
        UploadFile, File(description="Audio file to run the Whisper model on")
    ],
    task: Annotated[
        WhisperTask, Form(description="The Whisper task to perform")
    ] = "transcribe",
    language: Annotated[
        LanguageCode,
        Form(
            description="The ISO 3166-1 alpha-2 (two letter language) code of the source audio"
        ),
    ] = "en",
) -> TranscribeResponse:
    async with aiofiles.tempfile.NamedTemporaryFile("wb") as f:
        contents = await file.read()
        await f.write(contents)
        result = await loop.run_in_executor(
            None, make_transcribe_request, f.name, task, language
        )
        return TranscribeResponse(result=result["text"])


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


Instrumentator().instrument(app).expose(app)

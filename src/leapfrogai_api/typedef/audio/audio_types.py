from typing import Literal
from pydantic import BaseModel, Field
from fastapi import UploadFile, Form, File


class CreateTranscriptionRequest(BaseModel):
    """Request object for creating a transcription."""

    file: UploadFile = Field(
        ...,
        description="The audio file to transcribe. Supports any audio format that ffmpeg can handle. For a complete list of supported formats, see: https://ffmpeg.org/ffmpeg-formats.html",
    )
    model: str = Field(..., description="ID of the model to use.")
    language: str = Field(
        default="",
        description="The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency.",
    )
    prompt: str = Field(
        default="",
        description="An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language.",
    )
    response_format: str = Field(
        default="json",
        description="The format of the transcript output, in one of these options: json, text, srt, verbose_json, or vtt.",
    )
    temperature: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description="The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.",
    )
    timestamp_granularities: list[Literal["word", "segment"]] | None = Field(
        default=None,
        description="The timestamp granularities to populate for this transcription. response_format must be set to verbose_json to use timestamp granularities. Either or both of these options are supported: word, or segment. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency.",
    )

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        model: str = Form(...),
        language: str | None = Form(""),
        prompt: str | None = Form(""),
        response_format: str | None = Form(""),
        temperature: float | None = Form(1.0),
        timestamp_granularities: list[Literal["word", "segment"]] | None = Form(None),
    ):
        return cls(
            file=file,
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            timestamp_granularities=timestamp_granularities,
        )


class CreateTranscriptionResponse(BaseModel):
    """Response object for transcription."""

    text: str = Field(
        ...,
        description="The transcribed text.",
        examples=["Hello, this is a transcription of the audio file."],
    )


class CreateTranslationRequest(BaseModel):
    """Request object for creating a translation."""

    file: UploadFile = Field(
        ...,
        description="The audio file to translate. Supports any audio format that ffmpeg can handle. For a complete list of supported formats, see: https://ffmpeg.org/ffmpeg-formats.html",
    )
    model: str = Field(..., description="ID of the model to use.")
    prompt: str = Field(
        default="",
        description="An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language.",
    )
    response_format: str = Field(
        default="json",
        description="The format of the transcript output, in one of these options: json, text, srt, verbose_json, or vtt.",
    )
    temperature: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description="The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.",
    )

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        model: str = Form(...),
        prompt: str | None = Form(""),
        response_format: str | None = Form(""),
        temperature: float | None = Form(1.0),
    ):
        return cls(
            file=file,
            model=model,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
        )


class CreateTranslationResponse(BaseModel):
    """Response object for translation."""

    text: str = Field(
        ...,
        description="The translated text.",
        examples=["Hello, this is a translation of the audio file."],
    )

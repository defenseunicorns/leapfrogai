"""Typing definitions for assistants API."""

from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel
from fastapi import UploadFile, Form, File


### Files Types ###
class UploadFileRequest(BaseModel):
    """Request object for uploading a file."""

    file: UploadFile
    purpose: Literal["assistants"] | None = "assistants"

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        purpose: Optional[str] = Form("assistants"),
    ) -> UploadFileRequest:
        """Create an instance of the class from form data."""
        return cls(file=file, purpose=purpose)


### Assistants Types ###


class CreateAssistantRequest(BaseModel):
    """Request object for creating an assistant."""

    model: str = "mistral"
    name: Optional[str] = "Froggy Assistant"
    description: Optional[str] = "A helpful assistant."
    instructions: Optional[str] = "You are a helpful assistant."
    tools: Optional[list[dict[Literal["type"], Literal["file_search"]]]] | None = [
        {"type": "file_search"}
    ]  # This is all we support right now
    tool_resources: Optional[object] | None = {}
    metadata: Optional[object] | None = {}
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    response_format: Optional[Literal["auto"]] | None = (
        "auto"  # This is all we support right now
    )


class ModifyAssistantRequest(CreateAssistantRequest):
    """Request object for modifying an assistant."""

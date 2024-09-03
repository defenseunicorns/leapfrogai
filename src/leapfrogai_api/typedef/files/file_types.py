from pydantic import BaseModel, Field
from typing import Literal
from fastapi import UploadFile, Form, File
from openai.types import FileObject


class UploadFileRequest(BaseModel):
    """Request object for uploading a file."""

    file: UploadFile = Field(
        ...,
        description="The file to be uploaded. Must be a supported file type.",
    )
    purpose: Literal["assistants"] | None = Field(
        default="assistants",
        description="The intended purpose of the uploaded file. Currently, only 'assistants' is supported.",
    )

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        purpose: str | None = Form("assistants"),
    ) -> "UploadFileRequest":
        """Create an instance of the class from form data."""
        return cls(file=file, purpose=purpose)


class ListFilesResponse(BaseModel):
    """Response object for listing files."""

    object: Literal["list"] = Field(
        default="list",
        description="The type of object returned. Always 'list' for file listing.",
    )
    data: list[FileObject] = Field(
        default=[],
        description="An array of File objects, each representing an uploaded file.",
    )

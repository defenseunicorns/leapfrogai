"""Typing definitions for assistants API."""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Literal

from fastapi import UploadFile, Form, File
from openai.types import FileObject
from openai.types.beta import VectorStore

from openai.types.beta.thread_create_params import (
    ToolResourcesFileSearchVectorStoreChunkingStrategy,
    ToolResourcesFileSearchVectorStoreChunkingStrategyAuto,
)
from openai.types.beta.vector_store import ExpiresAfter
from pydantic import BaseModel, Field


#############
# FILES
#############


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
    ) -> UploadFileRequest:
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


#############
# ASSISTANTS
#############


################
# VECTOR STORES
################


class VectorStoreFileStatus(Enum):
    """Enum for the status of a vector store file."""

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class VectorStoreStatus(Enum):
    """Enum for the status of a vector store."""

    EXPIRED = "expired"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class CreateVectorStoreFileRequest(BaseModel):
    """Request object for creating a vector store file."""

    chunking_strategy: ToolResourcesFileSearchVectorStoreChunkingStrategy | None = (
        Field(
            default=None,
            description="The strategy for chunking the file content. Use 'auto' for automatic chunking.",
            examples=[
                ToolResourcesFileSearchVectorStoreChunkingStrategyAuto(type="auto")
            ],
        )
    )

    file_id: str = Field(
        default="",
        description="The ID of the file to be added to the vector store.",
        examples=["file-abc123"],
    )


class CreateVectorStoreRequest(BaseModel):
    """Request object for creating a vector store."""

    file_ids: list[str] | None = Field(
        default=[],
        description="List of file IDs to be included in the vector store.",
        example=["file-abc123", "file-def456"],
    )
    name: str | None = Field(
        default=None,
        description="Optional name for the vector store.",
        example="My Vector Store",
    )
    expires_after: ExpiresAfter | None = Field(
        default=None,
        description="Expiration settings for the vector store.",
        examples=[ExpiresAfter(anchor="last_active_at", days=1)],
    )
    metadata: dict | None = Field(
        default=None,
        description="Optional metadata for the vector store.",
        example={"project": "AI Research", "version": "1.0"},
    )

    def add_days_to_timestamp(self, timestamp: int, days: int) -> int:
        """
        Adds a specified number of days to a timestamp. Used to when updating the VectorStore.

        Args:
            timestamp(int): An integer representing a timestamp.
            days(int): The number of days to add.

        Returns:
            An integer representing the new timestamp with the added days.
        """

        # Convert the timestamp to a datetime object
        datetime_obj = datetime.datetime.fromtimestamp(timestamp)

        # Add the specified number of days
        new_datetime_obj = datetime_obj + datetime.timedelta(days=days)

        # Convert the new datetime object back to a timestamp
        new_timestamp = new_datetime_obj.timestamp()

        return int(new_timestamp)

    def get_expiry(self, last_active_at: int) -> tuple[ExpiresAfter | None, int | None]:
        """
        Return expiration details based on the provided last_active_at unix timestamp

        Args:
            last_active_at(int): An integer representing a timestamp when the vector store was last active.

        Returns:
            A tuple of when the vector store should expire and the timestamp of the expiry date.
        """
        if isinstance(self.expires_after, ExpiresAfter):
            return self.expires_after, self.add_days_to_timestamp(
                last_active_at, self.expires_after.days
            )

        return None, None  # Will not expire


class ModifyVectorStoreRequest(CreateVectorStoreRequest):
    """Request object for modifying a vector store."""


class ListVectorStoresResponse(BaseModel):
    """Response object for listing files."""

    object: Literal["list"] = Field(
        default="list",
        description="The type of object. Always 'list' for this response.",
    )
    data: list[VectorStore] = Field(
        default=[],
        description="A list of VectorStore objects.",
    )


################
# LEAPFROGAI Vector Stores
################


class SearchItem(BaseModel):
    """Object representing a single item in a search result."""

    id: str = Field(..., description="Unique identifier for the search item.")
    vector_store_id: str = Field(
        ..., description="ID of the vector store containing this item."
    )
    file_id: str = Field(..., description="ID of the file associated with this item.")
    content: str = Field(..., description="The actual content of the item.")
    metadata: dict = Field(
        ..., description="Additional metadata associated with the item."
    )
    similarity: float = Field(
        ..., description="Similarity score of this item to the query."
    )


class SearchResponse(BaseModel):
    """Response object for RAG queries."""

    data: list[SearchItem] = Field(
        ...,
        description="List of RAG items returned as a result of the query.",
        min_length=0,
    )

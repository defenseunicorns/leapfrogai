"""OpenAI Compliant Files API Router."""

import time
from uuid import uuid4 as uuid

from fastapi import Depends, APIRouter, HTTPException
from openai.types import FileObject, FileDeleted

from leapfrogai_api.backend.types import UploadFileRequest
from leapfrogai_api.data.supabase_client import SupabaseWrapper

router = APIRouter(prefix="/openai/v1/files", tags=["openai/files"])


@router.post("/")
async def upload_file(
    request: UploadFileRequest = Depends(UploadFileRequest.as_form),
) -> FileObject:
    """Upload a file."""

    try:
        file_object = FileObject(
            id=str(uuid()),
            bytes=request.file.size,
            created_at=int(time.time()),
            filename=request.file.filename,
            object="file",  # Per OpenAI Spec this should always be file
            purpose="assistants",  # we only support assistants for now
            status="uploaded",
            status_details=None,
        )
        print(file_object)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to parse file") from exc

    try:
        supabase_wrapper = SupabaseWrapper()
        return await supabase_wrapper.upsert_file(request.file, file_object)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to store file") from exc


@router.get("/")
async def list_files():
    """List all files."""
    try:
        supabase_wrapper = SupabaseWrapper()
        response = await supabase_wrapper.list_files(purpose="assistants")
        return {"data": response, "object": "list"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="No file objects found") from exc


@router.get("/{file_id}")
async def retrieve_file(file_id: str) -> FileObject:
    """Retrieve a file."""
    try:
        supabase_wrapper = SupabaseWrapper()
        return await supabase_wrapper.get_file_object(file_id=file_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=500, detail="Multiple files found with same id"
        ) from exc


@router.delete("/{file_id}")
async def delete_file(file_id: str) -> FileDeleted:
    """Delete a file."""
    try:
        supabase_wrapper = SupabaseWrapper()
        return await supabase_wrapper.delete_file(file_id=file_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc


@router.get("/{file_id}/content")
async def retrieve_file_content(file_id: str):
    """Retrieve the content of a file."""
    try:
        supabase_wrapper = SupabaseWrapper()
        return await supabase_wrapper.get_file_content(file_id=file_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc

"""OpenAI Compliant Files API Router."""

import time

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from openai.types import FileDeleted, FileObject

from leapfrogai_api.backend.types import UploadFileRequest
from leapfrogai_api.data.crud_file_object import CRUDFileObject
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/openai/v1/files", tags=["openai/files"])


@router.post("")
async def upload_file(
    client: Session,
    request: UploadFileRequest = Depends(UploadFileRequest.as_form),
) -> FileObject:
    """Upload a file."""

    try:
        file_object = FileObject(
            id="",  # This is set by the database to prevent conflicts
            bytes=request.file.size,
            created_at=int(time.time()),
            filename=request.file.filename,
            object="file",  # Per OpenAI Spec this should always be file
            purpose="assistants",  # we only support assistants for now
            status="uploaded",
            status_details=None,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to parse file") from exc

    try:
        crud_file_object = CRUDFileObject(model=FileObject)
        file_object = await crud_file_object.create(
            file_object=file_object, client=client
        )

        if not file_object:
            raise HTTPException(status_code=500, detail="Failed to create file object")

        crud_file_bucket = CRUDFileBucket(model=UploadFile)
        await crud_file_bucket.upload(
            client=client, file=request.file, id_=file_object.id
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to store file") from exc

    return file_object


@router.get("")
async def list_files(session: Session) -> list[FileObject] | None:
    """List all files."""
    try:
        crud_file = CRUDFileObject(model=FileObject)
        return await crud_file.list(client=session)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="No file objects found") from exc


@router.get("/{file_id}")
async def retrieve_file(client: Session, file_id: str) -> FileObject | None:
    """Retrieve a file."""
    try:
        crud_file = CRUDFileObject(model=FileObject)
        return await crud_file.get(file_id=file_id, client=client)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=500, detail="Multiple files found with same id"
        ) from exc


@router.delete("/{file_id}")
async def delete_file(session: Session, file_id: str) -> FileDeleted:
    """Delete a file."""
    try:
        crud_file_object = CRUDFileObject(model=FileObject)
        file_deleted = await crud_file_object.delete(file_id=file_id, client=session)

        crud_file_bucket = CRUDFileBucket(model=UploadFile)
        await crud_file_bucket.delete(client=session, id_=file_id)

        return file_deleted
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc


@router.get("/{file_id}/content")
async def retrieve_file_content(session: Session, file_id: str):
    """Retrieve the content of a file."""
    try:
        crud_file_bucket = CRUDFileBucket(model=UploadFile)
        return await crud_file_bucket.download(client=session, id_=file_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=500, detail="Multiple files found with same id"
        ) from exc

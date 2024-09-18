"""OpenAI Compliant Files API Router."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import Response
from openai.types import FileDeleted, FileObject

from leapfrogai_api.backend.rag.document_loader import (
    is_supported_mime_type,
    get_mime_type_from_filename,
)
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.data.crud_file_object import CRUDFileObject, FilterFileObject
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.typedef.files import ListFilesResponse, UploadFileRequest

router = APIRouter(prefix="/openai/v1/files", tags=["openai/files"])


@router.post("")
async def upload_file(
    session: Session,
    request: UploadFileRequest = Depends(UploadFileRequest.as_form),
) -> FileObject:
    """Upload a file."""

    if not request.file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided!",
        )

    if request.file.content_type and not is_supported_mime_type(
        request.file.content_type
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type {request.file.content_type}!",
        )

    try:
        empty_file_object = FileObject(
            id="",  # This is set by the database to prevent conflicts
            bytes=request.file.size if request.file.size else 0,
            created_at=0,  # This is set by the database to prevent conflicts
            filename=request.file.filename if request.file.filename else "",
            object="file",  # Per OpenAI Spec this should always be file
            purpose="assistants",  # we only support assistants for now
            status="uploaded",
            status_details=None,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to parse file"
        ) from exc

    crud_file_object = CRUDFileObject(session)

    if not (file_object := await crud_file_object.create(object_=empty_file_object)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store file",
        )

    crud_file_bucket = CRUDFileBucket(db=session, model=UploadFile)
    try:
        await crud_file_bucket.upload(file=request.file, id_=file_object.id)
        return file_object
    except Exception as exc:
        await crud_file_object.delete(filters=FilterFileObject(id=file_object.id))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store file",
        ) from exc


@router.get("")
async def list_files(
    session: Session,
) -> ListFilesResponse:
    """List all files."""
    crud_file_object = CRUDFileObject(session)
    crud_response = await crud_file_object.list()

    return ListFilesResponse(
        object="list",
        data=crud_response or [],
    )


@router.get("/{file_id}")
async def retrieve_file(
    session: Session,
    file_id: str,
) -> FileObject | None:
    """Retrieve a file."""
    crud_file_object = CRUDFileObject(session)
    return await crud_file_object.get(filters=FilterFileObject(id=file_id))


@router.delete("/{file_id}")
async def delete_file(
    session: Session,
    file_id: str,
) -> FileDeleted:
    """Delete a file."""

    crud_file_object = CRUDFileObject(session)
    file_deleted: bool = await crud_file_object.delete(
        filters=FilterFileObject(id=file_id)
    )

    # We need to check if the RLS allowed the deletion before continuing with the bucket deletion
    if file_deleted:
        crud_file_bucket = CRUDFileBucket(db=session, model=UploadFile)
        await crud_file_bucket.delete(id_=file_id)

    return FileDeleted(
        id=file_id,
        object="file",
        deleted=bool(file_deleted),
    )


@router.get("/{file_id}/content")
async def retrieve_file_content(
    session: Session,
    file_id: str,
):
    """Retrieve the content of a file."""
    try:
        crud_file_bucket = CRUDFileBucket(db=session, model=UploadFile)
        file_content = await crud_file_bucket.download(id_=file_id)

        # Get the file object to retrieve the filename
        crud_file_object = CRUDFileObject(session)
        file_object = await crud_file_object.get(filters=FilterFileObject(id=file_id))

        if not file_object:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )

        # Determine the content type
        content_type = get_mime_type_from_filename(file_object.filename)

        # Ensure the content type is supported
        if not is_supported_mime_type(content_type):
            content_type = "application/octet-stream"

        # Return the file content as a downloadable attachment
        return Response(
            content=file_content,
            media_type=content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{file_object.filename}"'
            },
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File not found"
        ) from exc

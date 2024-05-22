"""OpenAI Compliant Files API Router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from openai.types import FileDeleted, FileObject
from leapfrogai_api.backend.types import ListFilesResponse, UploadFileRequest
from leapfrogai_api.data.crud_file_object import CRUDFileObject
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket

router = APIRouter(prefix="/openai/v1/files", tags=["openai/files"])
security = HTTPBearer()


@router.post("")
async def upload_file(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    request: UploadFileRequest = Depends(UploadFileRequest.as_form),
) -> FileObject:
    """Upload a file."""

    try:
        file_object = FileObject(
            id="",  # This is set by the database to prevent conflicts
            bytes=request.file.size,
            created_at=0,  # This is set by the database to prevent conflicts
            filename=request.file.filename,
            object="file",  # Per OpenAI Spec this should always be file
            purpose="assistants",  # we only support assistants for now
            status="uploaded",
            status_details=None,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to parse file"
        ) from exc

    crud_file_object = await CRUDFileObject(auth_creds.credentials)

    try:
        file_object = await crud_file_object.create(object_=file_object)
        crud_file_bucket = await CRUDFileBucket(
            jwt=auth_creds.credentials, model=UploadFile
        )
        await crud_file_bucket.upload(file=request.file, id_=file_object.id)

        return file_object

    except Exception as exc:
        crud_file_object.delete(id_=file_object.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store file",
        ) from exc


@router.get("")
async def list_files(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> ListFilesResponse:
    """List all files."""
    crud_file_object = await CRUDFileObject(auth_creds.credentials)
    crud_response = await crud_file_object.list()

    return ListFilesResponse(
        object="list",
        data=crud_response or [],
    )


@router.get("/{file_id}")
async def retrieve_file(
    file_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> FileObject | None:
    """Retrieve a file."""
    crud_file_object = await CRUDFileObject(auth_creds.credentials)
    return await crud_file_object.get(id_=file_id)


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> FileDeleted:
    """Delete a file."""

    crud_file_object = await CRUDFileObject(auth_creds.credentials)
    file_deleted = await crud_file_object.delete(id_=file_id)

    crud_file_bucket = await CRUDFileBucket(
        jwt=auth_creds.credentials, model=UploadFile
    )
    await crud_file_bucket.delete(id_=file_id)

    return FileDeleted(
        id=file_id,
        object="file",
        deleted=bool(file_deleted),
    )


@router.get("/{file_id}/content")
async def retrieve_file_content(
    file_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """Retrieve the content of a file."""
    try:
        crud_file_bucket = await CRUDFileBucket(
            jwt=auth_creds.credentials, model=UploadFile
        )
        return await crud_file_bucket.download(id_=file_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File not found"
        ) from exc

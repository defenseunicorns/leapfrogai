"""OpenAI Compliant Files API Router."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from openai.types import FileDeleted, FileObject
from leapfrogai_api.backend.types import ListFilesResponse, UploadFileRequest
from leapfrogai_api.data.crud_file_object import CRUDFileObject
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.routers.supabase_session import Session, get_user_session

router = APIRouter(prefix="/openai/v1/files", tags=["openai/files"])
security = HTTPBearer()


@router.post("")
async def upload_file(
    session: Session,
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

    crud_file_object = CRUDFileObject(model=FileObject)

    user_session = get_user_session(session, auth_creds.credentials)

    try:
        file_object = await crud_file_object.create(
            db=user_session, object_=file_object
        )

        crud_file_bucket = CRUDFileBucket(model=UploadFile)
        await crud_file_bucket.upload(
            client=user_session, file=request.file, id_=file_object.id
        )

        return file_object

    except Exception as exc:
        crud_file_object.delete(db=user_session, id_=file_object.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store file",
        ) from exc


@router.get("")
async def list_files(
    session: Session, auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> ListFilesResponse:
    """List all files."""
    crud_file = CRUDFileObject(model=FileObject)
    crud_response = await crud_file.list(db=get_user_session(session, auth_creds.credentials))

    return ListFilesResponse(
        object="list",
        data=crud_response or [],
    )


@router.get("/{file_id}")
async def retrieve_file(
    session: Session, file_id: str, auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> FileObject | None:
    """Retrieve a file."""
    crud_file = CRUDFileObject(model=FileObject)
    return await crud_file.get(db=get_user_session(session, auth_creds.credentials), id_=file_id)


@router.delete("/{file_id}")
async def delete_file(
    session: Session, file_id: str, auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> FileDeleted:
    """Delete a file."""
    user_session = get_user_session(session, auth_creds.credentials)

    crud_file_object = CRUDFileObject(model=FileObject)
    file_deleted = await crud_file_object.delete(db=user_session, id_=file_id)

    crud_file_bucket = CRUDFileBucket(model=UploadFile)
    await crud_file_bucket.delete(client=user_session, id_=file_id)

    return FileDeleted(
        id=file_id,
        object="file",
        deleted=bool(file_deleted),
    )


@router.get("/{file_id}/content")
async def retrieve_file_content(
    session: Session, file_id: str, auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """Retrieve the content of a file."""
    try:
        crud_file_bucket = CRUDFileBucket(model=UploadFile)
        return await crud_file_bucket.download(
            client=get_user_session(session, auth_creds.credentials), id_=file_id
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File not found"
        ) from exc

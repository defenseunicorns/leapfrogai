"""OpenAI Compliant Files API Router."""

from fastapi import Depends, APIRouter, HTTPException
from openai.types import FileObject, FileDeleted

from leapfrogai_api.routers.openai.types import UploadFileRequest

router = APIRouter(prefix="/openai/v1/files", tags=["openai/files"])


@router.post("")
async def upload_file(
    request: UploadFileRequest = Depends(UploadFileRequest.as_form),
) -> FileObject:
    """Upload a file."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("")
async def list_files():
    """List all files."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{file_id}")
async def retrieve_file(file_id: str) -> FileObject:
    """Retrieve a file."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{file_id}")
async def delete_file(file_id: str) -> FileDeleted:
    """Delete a file."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{file_id}/content")
async def retrieve_file_content(file_id: str):
    """Retrieve the content of a file."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

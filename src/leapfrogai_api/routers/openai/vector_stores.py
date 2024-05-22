"""OpenAI Compliant Vector Store API Router."""

import time
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_store import FileCounts
from openai.types.beta.vector_stores import VectorStoreFile, VectorStoreFileDeleted
from leapfrogai_api.backend.rag.index import IndexingService
from leapfrogai_api.backend.types import (
    CreateVectorStoreRequest,
    ListVectorStoresResponse,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.data.crud_vector_store_file import CRUDVectorStoreFile
from leapfrogai_api.data.crud_vector_store_object import CRUDVectorStore
from leapfrogai_api.data.supabase_vector_store import AsyncSupabaseVectorStore
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/openai/v1/vector_stores", tags=["openai/vector_stores"])
security = HTTPBearer()


@router.post("")
async def create_vector_store(
    request: CreateVectorStoreRequest,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> VectorStore:
    """Create a vector store."""
    crud_vector_store = await CRUDVectorStore(auth_creds.credentials)

    vector_store_object = VectorStore(
        id="",  # Leave blank to have Postgres generate a UUID
        bytes=0,  # Automatically calculated by DB
        created_at=0,  # Leave blank to have Postgres generate a timestamp
        file_counts=FileCounts(
            cancelled=0, completed=0, failed=0, in_progress=0, total=0
        ),
        last_active_at=int(time.time()),  # Set to current time
        metadata=request.metadata,
        name=request.name,
        object="vector_store",
        status="in_progress",
        expires_after=None,  # TODO: Handle expires_after
        expires_at=None,  # TODO: Handle expires_at
    )
    try:
        new_vector_store = await crud_vector_store.create(object_=vector_store_object)
        # if request.file_ids != []:
        #     indexing_service = IndexingService(session=session)
        #     for file_id in request.file_ids:
        #         response = await indexing_service.index_file(
        #             vector_store_id=new_vector_store.id, file_id=file_id
        #         )

        #         if response.status == "completed":
        #             new_vector_store.file_counts.completed += 1
        #         elif response.status == "failed":
        #             new_vector_store.file_counts.failed += 1
        #         elif response.status == "in_progress":
        #             new_vector_store.file_counts.in_progress += 1
        #         elif response.status == "cancelled":
        #             new_vector_store.file_counts.cancelled += 1
        #         new_vector_store.file_counts.total += 1

        new_vector_store.status = "completed"

        return await crud_vector_store.update(
            id_=new_vector_store.id,
            object_=new_vector_store,
        )
    except Exception as exc:
        logging.debug(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create vector store",
        ) from exc


@router.get("")
async def list_vector_stores(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # pylint: disable=unused-argument
) -> ListVectorStoresResponse:
    """List all the vector stores."""

    crud_vector_store = await CRUDVectorStore(auth_creds.credentials)
    crud_response = await crud_vector_store.list()

    return ListVectorStoresResponse(
        object="list",
        data=crud_response or [],
    )


@router.get("/{vector_store_id}")
async def retrieve_vector_store(
    vector_store_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # pylint: disable=unused-argument
) -> VectorStore | None:
    """Retrieve a vector store."""

    crud_vector_store = await CRUDVectorStore(auth_creds.credentials)
    return await crud_vector_store.get(id_=vector_store_id)


@router.post("/{vector_store_id}")
async def modify_vector_store(
    vector_store_id: str,
    request: ModifyVectorStoreRequest,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # pylint: disable=unused-argument
) -> VectorStore:
    """Modify a vector store."""
    crud_vector_store = await CRUDVectorStore(auth_creds.credentials)

    if not (old_vector_store := await crud_vector_store.get(id_=vector_store_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vector store not found",
        )

    try:
        new_vector_store = VectorStore(
            id=vector_store_id,
            bytes=old_vector_store.bytes,  # Automatically calculated by DB
            created_at=old_vector_store.created_at,
            file_counts=old_vector_store.file_counts,
            last_active_at=old_vector_store.last_active_at,  # Update after indexing files
            metadata=getattr(request, "metadata", old_vector_store.metadata),
            name=getattr(request, "name", old_vector_store.name),
            object="vector_store",
            status="in_progress",
            expires_after=None,  # TODO: Handle expires_after
            expires_at=None,  # TODO: Handle expires_at
        )

        await crud_vector_store.update(
            id_=vector_store_id,
            object_=new_vector_store,
        )  # Sets status to in_progress for the duration of this function
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse vector store request",
        ) from exc

    try:
        # if request.file_ids != []:
        #     indexing_service = IndexingService(session=session)
        #     for file_id in request.file_ids:
        #         response = await indexing_service.index_file(
        #             vector_store_id=vector_store_id, file_id=file_id
        #         )

        #         if response.status == "completed":
        #             new_vector_store.file_counts.completed += 1
        #         elif response.status == "failed":
        #             new_vector_store.file_counts.failed += 1
        #         elif response.status == "in_progress":
        #             new_vector_store.file_counts.in_progress += 1
        #         elif response.status == "cancelled":
        #             new_vector_store.file_counts.cancelled += 1
        #         new_vector_store.file_counts.total += 1

        new_vector_store.status = "completed"

        new_vector_store.last_active_at = int(
            time.time()
        )  # Update after indexing files

        return await crud_vector_store.update(
            id_=vector_store_id,
            object_=new_vector_store,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update vector store",
        ) from exc


@router.delete("/{vector_store_id}")
async def delete_vector_store(
    vector_store_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # pylint: disable=unused-argument
) -> VectorStoreDeleted:
    """Delete a vector store."""

    crud_vector_store = await CRUDVectorStore(auth_creds.credentials)

    vector_store_deleted = await crud_vector_store.delete(id_=vector_store_id)
    return VectorStoreDeleted(
        id=vector_store_id,
        object="vector_store.deleted",
        deleted=bool(vector_store_deleted),
    )


@router.post("/{vector_store_id}/files")
async def create_vector_store_file(
    session: Session,
    vector_store_id: str,
    file_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # pylint: disable=unused-argument
) -> VectorStoreFile:
    """Create a file in a vector store."""

    try:
        indexing_service = IndexingService(session=session)
        vector_store_file = await indexing_service.index_file(
            vector_store_id=vector_store_id, file_id=file_id
        )
        return vector_store_file
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create vector store file",
        ) from exc


@router.get("/{vector_store_id}/files")
async def list_vector_store_files(
    session: Session,
    vector_store_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # pylint: disable=unused-argument
) -> list[VectorStoreFile]:
    """List all the files in a vector store."""

    try:
        crud_vector_store_file = CRUDVectorStoreFile(model=VectorStoreFile)
        vector_store_files = await crud_vector_store_file.list(
            db=session, vector_store_id=vector_store_id
        )

        return vector_store_files
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list vector store files",
        ) from exc


@router.get("/{vector_store_id}/files/{file_id}")
async def retrieve_vector_store_file(
    session: Session,
    vector_store_id: str,
    file_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # pylint: disable=unused-argument
) -> VectorStoreFile:
    """Retrieve a file in a vector store."""

    crud_vector_store_file = CRUDVectorStoreFile(model=VectorStoreFile)
    return await crud_vector_store_file.get(
        db=session, vector_store_id=vector_store_id, file_id=file_id
    )


@router.delete("/{vector_store_id}/files/{file_id}")
async def delete_vector_store_file(
    session: Session,
    vector_store_id: str,
    file_id: str,
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # pylint: disable=unused-argument
) -> VectorStoreFileDeleted:
    """Delete a file in a vector store."""

    vector_store = AsyncSupabaseVectorStore(client=session)
    vectors_deleted = await vector_store.adelete_file(
        vector_store_id=vector_store_id, file_id=file_id
    )

    crud_vector_store_file = CRUDVectorStoreFile(model=VectorStoreFile)

    vector_store_file_deleted = await crud_vector_store_file.delete(
        db=session, vector_store_id=vector_store_id, file_id=file_id
    )

    deleted = vectors_deleted and vector_store_file_deleted

    return VectorStoreFileDeleted(
        id=file_id,
        object="vector_store.file.deleted",
        deleted=deleted,
    )

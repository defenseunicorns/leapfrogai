"""OpenAI Compliant Vector Store API Router."""

import logging
import time
import traceback
from fastapi import APIRouter, HTTPException, status
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_store import FileCounts
from openai.types.beta.vector_stores import VectorStoreFile, VectorStoreFileDeleted
from leapfrogai_api.backend.rag.index import FileAlreadyIndexedError, IndexingService
from leapfrogai_api.backend.types import (
    CreateVectorStoreRequest,
    ListVectorStoresResponse,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore, FilterVectorStore
from leapfrogai_api.data.crud_vector_store_file import (
    CRUDVectorStoreFile,
    FilterVectorStoreFile,
)
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.backend.types import VectorStoreFileStatus, VectorStoreStatus

router = APIRouter(prefix="/openai/v1/vector_stores", tags=["openai/vector_stores"])


@router.post("")
async def create_vector_store(
    request: CreateVectorStoreRequest,
    session: Session,
) -> VectorStore:
    """Create a vector store."""
    crud_vector_store = CRUDVectorStore(db=session)

    last_active_at = int(time.time())

    expires_after, expires_at = request.get_expiry(last_active_at)

    vector_store = VectorStore(
        id="",  # Leave blank to have Postgres generate a UUID
        bytes=0,  # Automatically calculated by DB
        created_at=0,  # Leave blank to have Postgres generate a timestamp
        file_counts=FileCounts(
            cancelled=0, completed=0, failed=0, in_progress=0, total=0
        ),
        last_active_at=last_active_at,  # Set to current time
        metadata=request.metadata,
        name=request.name,
        object="vector_store",
        status=VectorStoreStatus.IN_PROGRESS.value,
        expires_after=expires_after,
        expires_at=expires_at,
    )
    try:
        new_vector_store = await crud_vector_store.create(object_=vector_store)
        if request.file_ids != []:
            indexing_service = IndexingService(db=session)
            for file_id in request.file_ids:
                response = await indexing_service.index_file(
                    vector_store_id=new_vector_store.id, file_id=file_id
                )

                if response.status == VectorStoreFileStatus.COMPLETED.value:
                    new_vector_store.file_counts.completed += 1
                elif response.status == VectorStoreFileStatus.FAILED.value:
                    new_vector_store.file_counts.failed += 1
                elif response.status == VectorStoreFileStatus.IN_PROGRESS.value:
                    new_vector_store.file_counts.in_progress += 1
                elif response.status == VectorStoreFileStatus.CANCELLED.value:
                    new_vector_store.file_counts.cancelled += 1
                new_vector_store.file_counts.total += 1

        new_vector_store.status = VectorStoreStatus.COMPLETED.value

        return await crud_vector_store.update(
            id_=new_vector_store.id,
            object_=new_vector_store,
        )
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create vector store",
        ) from exc


@router.get("")
async def list_vector_stores(
    session: Session,
) -> ListVectorStoresResponse:
    """List all the vector stores."""

    crud_vector_store = CRUDVectorStore(db=session)
    crud_response = await crud_vector_store.list()

    return ListVectorStoresResponse(
        object="list",
        data=crud_response or [],
    )


@router.get("/{vector_store_id}")
async def retrieve_vector_store(
    vector_store_id: str,
    session: Session,
) -> VectorStore | None:
    """Retrieve a vector store."""

    crud_vector_store = CRUDVectorStore(db=session)
    return await crud_vector_store.get(filters=FilterVectorStore(id=vector_store_id))


@router.post("/{vector_store_id}")
async def modify_vector_store(
    vector_store_id: str,
    request: ModifyVectorStoreRequest,
    session: Session,
) -> VectorStore:
    """Modify a vector store."""
    crud_vector_store = CRUDVectorStore(db=session)

    if not (
        old_vector_store := await crud_vector_store.get(
            filters=FilterVectorStore(id=vector_store_id)
        )
    ):
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
            status=VectorStoreStatus.IN_PROGRESS.value,
            expires_after=old_vector_store.expires_after,
            expires_at=old_vector_store.expires_at,
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
        if request.file_ids:
            indexing_service = IndexingService(db=session)

            for file_id in request.file_ids:
                try:
                    response = await indexing_service.index_file(
                        vector_store_id=vector_store_id, file_id=file_id
                    )
                except FileAlreadyIndexedError:
                    logging.info(
                        "File %s already exists and cannot be re-indexed", file_id
                    )
                    continue
                except Exception as exc:
                    raise exc

                if response.status == VectorStoreFileStatus.COMPLETED.value:
                    new_vector_store.file_counts.completed += 1
                elif response.status == VectorStoreFileStatus.FAILED.value:
                    new_vector_store.file_counts.failed += 1
                elif response.status == VectorStoreFileStatus.IN_PROGRESS.value:
                    new_vector_store.file_counts.in_progress += 1
                elif response.status == VectorStoreFileStatus.CANCELLED.value:
                    new_vector_store.file_counts.cancelled += 1
                new_vector_store.file_counts.total += 1

        new_vector_store.status = VectorStoreStatus.COMPLETED.value

        last_active_at = int(time.time())
        new_vector_store.last_active_at = last_active_at  # Update after indexing files
        expires_after, expires_at = request.get_expiry(last_active_at)

        if expires_at and expires_at:
            new_vector_store.expires_after = expires_after
            new_vector_store.expires_at = expires_at

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
    session: Session,
) -> VectorStoreDeleted:
    """Delete a vector store."""

    crud_vector_store = CRUDVectorStore(db=session)

    vector_store_deleted = await crud_vector_store.delete(
        filters=FilterVectorStore(id=vector_store_id)
    )
    return VectorStoreDeleted(
        id=vector_store_id,
        object="vector_store.deleted",
        deleted=vector_store_deleted,
    )


@router.post("/{vector_store_id}/files")
async def create_vector_store_file(
    vector_store_id: str,
    file_id: str,
    session: Session,
) -> VectorStoreFile:
    """Create a file in a vector store."""

    try:
        indexing_service = IndexingService(db=session)
        vector_store_file = await indexing_service.index_file(
            vector_store_id=vector_store_id, file_id=file_id
        )
        return vector_store_file
    except Exception as exc:
        logging.exception("Error indexing file")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create vector store file",
        ) from exc


@router.get("/{vector_store_id}/files")
async def list_vector_store_files(
    vector_store_id: str,
    session: Session,
) -> list[VectorStoreFile]:
    """List all the files in a vector store."""

    try:
        crud_vector_store_file = CRUDVectorStoreFile(db=session)
        vector_store_files = await crud_vector_store_file.list(
            filters=FilterVectorStoreFile(vector_store_id=vector_store_id)
        )
        return vector_store_files
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list vector store files",
        ) from exc


@router.get("/{vector_store_id}/files/{file_id}")
async def retrieve_vector_store_file(
    vector_store_id: str,
    file_id: str,
    session: Session,
) -> VectorStoreFile:
    """Retrieve a file in a vector store."""

    crud_vector_store_file = CRUDVectorStoreFile(db=session)
    return await crud_vector_store_file.get(
        filters=FilterVectorStoreFile(vector_store_id=vector_store_id, id=file_id)
    )


@router.delete("/{vector_store_id}/files/{file_id}")
async def delete_vector_store_file(
    session: Session,
    vector_store_id: str,
    file_id: str,
) -> VectorStoreFileDeleted:
    """Delete a file in a vector store."""

    vector_store = IndexingService(db=session)
    vectors_deleted = await vector_store.adelete_file(
        vector_store_id=vector_store_id, file_id=file_id
    )

    crud_vector_store_file = CRUDVectorStoreFile(db=session)

    vector_store_file_deleted = await crud_vector_store_file.delete(
        filters=FilterVectorStoreFile(vector_store_id=vector_store_id, id=file_id)
    )

    deleted = vectors_deleted and vector_store_file_deleted

    return VectorStoreFileDeleted(
        id=file_id,
        object="vector_store.file.deleted",
        deleted=deleted,
    )

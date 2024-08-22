"""OpenAI Compliant Vector Store API Router."""

import logging
import traceback
import time

from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from openai.pagination import SyncCursorPage
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_stores import VectorStoreFile, VectorStoreFileDeleted
from openai.types.beta.vector_store import FileCounts
from leapfrogai_api.backend.rag.index import IndexingService
from leapfrogai_api.backend.types import (
    CreateVectorStoreFileRequest,
    CreateVectorStoreRequest,
    ListVectorStoresResponse,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.data.crud_vector_content import CRUDVectorContent
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore, FilterVectorStore
from leapfrogai_api.data.crud_vector_store_file import (
    CRUDVectorStoreFile,
    FilterVectorStoreFile,
)
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/openai/v1/vector_stores", tags=["openai/vector_stores"])


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


@router.post("")
async def create_vector_store(
    request: CreateVectorStoreRequest,
    session: Session,
    background_tasks: BackgroundTasks,
) -> VectorStore:
    """Create a vector store."""

    indexing_service = IndexingService(db=session)
    try:
        current_time = int(time.time())
        # Create a placeholder vector store
        placeholder_vector_store = VectorStore(
            id="placeholder_id",
            name=request.name or "",
            status="in_progress",
            object="vector_store",
            created_at=current_time,
            last_active_at=current_time,
            file_counts=FileCounts(
                cancelled=0,
                completed=0,
                failed=0,
                in_progress=0,
                total=0
            ),
            usage_bytes=0,
            metadata=request.metadata if hasattr(request, 'metadata') else None,
            expires_after=None,
            expires_at=None
        )

        # Add the actual creation task to background tasks
        background_tasks.add_task(
            indexing_service.create_new_vector_store,
            request
        )

        return placeholder_vector_store
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create vector store",
        ) from exc


@router.post("/{vector_store_id}")
async def modify_vector_store(
    vector_store_id: str,
    request: ModifyVectorStoreRequest,
    session: Session,
) -> VectorStore:
    """Modify a vector store."""

    indexing_service = IndexingService(db=session)
    try:
        modified_vector_store = await indexing_service.modify_existing_vector_store(
            vector_store_id=vector_store_id, request=request
        )
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to modify vector store",
        ) from exc
    return modified_vector_store


@router.get("/{vector_store_id}")
async def retrieve_vector_store(
    vector_store_id: str,
    session: Session,
) -> VectorStore | None:
    """Retrieve a vector store."""

    crud_vector_store = CRUDVectorStore(db=session)
    return await crud_vector_store.get(filters=FilterVectorStore(id=vector_store_id))


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
    request: CreateVectorStoreFileRequest,
    session: Session,
) -> VectorStoreFile:
    """Create a file in a vector store."""

    try:
        indexing_service = IndexingService(db=session)
        vector_store_file = await indexing_service.index_file(
            vector_store_id=vector_store_id, file_id=request.file_id
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
) -> SyncCursorPage[VectorStoreFile]:
    """List all the files in a vector store."""

    try:
        crud_vector_store_file = CRUDVectorStoreFile(db=session)
        vector_store_files = await crud_vector_store_file.list(
            filters=FilterVectorStoreFile(vector_store_id=vector_store_id)
        )

        if vector_store_files is None:
            return SyncCursorPage(object="list", data=[])

        return SyncCursorPage(object="list", data=vector_store_files)
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

    vector_content = CRUDVectorContent(db=session)
    vectors_deleted = await vector_content.delete_vectors(
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
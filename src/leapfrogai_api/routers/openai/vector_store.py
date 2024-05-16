"""OpenAI Compliant Vector Store API Router."""

import time
from fastapi import HTTPException, APIRouter, status
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_stores import VectorStoreFile, VectorStoreFileDeleted
from openai.types.beta.vector_store import ExpiresAfter, FileCounts
from leapfrogai_api.backend.types import (
    CreateVectorStoreRequest,
    ListVectorStoresResponse,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.data.crud_vector_store_object import CRUDVectorStore
from leapfrogai_api.data.crud_vector_store_file import CRUDVectorStoreFile
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.backend.rag.index import IndexingService
from leapfrogai_api.data.supabase_vector_store import AsyncSupabaseVectorStore

router = APIRouter(prefix="/openai/v1/vector_store", tags=["openai/vector_store"])


@router.post("")
async def create_vector_store(
    session: Session, request: CreateVectorStoreRequest
) -> VectorStore:
    """Create a vector store."""

    crud_vector_store = CRUDVectorStore(model=VectorStore)

    try:
        if request.file_ids == []:
            # TODO: Handle file counts, expires_after, expires_at, and last_active_at
            vector_store_object = VectorStore(
                id="",  # Leave blank to have Postgres generate a UUID
                bytes=0,
                created_at=int(time.time()),
                file_counts=FileCounts(
                    cancelled=0, completed=0, failed=0, in_progress=0, total=0
                ),
                last_active_at=None,
                metadata=request.metadata,
                name=request.name,
                object="vector_store",
                status="completed",
                expires_after=ExpiresAfter.model_validate(request.expires_after)
                or None,
                expires_at=None,
            )
            return await crud_vector_store.create(
                object_=vector_store_object, db=session
            )
        else:
            # TODO: Create a vector store from file ids
            raise HTTPException(
                status_code=405,
                detail="Not Implemented: Cannot create vector store from list of file ids",
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create vector store",
        ) from exc


@router.get("")
async def list_vector_stores(
    session: Session,
) -> ListVectorStoresResponse:
    """List all the vector stores."""

    crud_vector_store = CRUDVectorStore(model=VectorStore)
    crud_response = await crud_vector_store.list(db=session)

    return ListVectorStoresResponse(
        object="list",
        data=crud_response or [],
    )


@router.get("/{vector_store_id}")
async def retrieve_vector_store(
    session: Session, vector_store_id: str
) -> VectorStore | None:
    """Retrieve a vector store."""

    crud_vector_store = CRUDVectorStore(model=VectorStore)
    return await crud_vector_store.get(db=session, id_=vector_store_id)


@router.post("/{vector_store_id}")
async def modify_vector_store(
    session: Session, vector_store_id: str, request: ModifyVectorStoreRequest
) -> VectorStore:
    """Modify a vector store."""
    # TODO: This needs work
    try:
        vector_store_object = VectorStore(
            id=vector_store_id,  # Leave blank to have Postgres generate a UUID
            bytes=0,
            created_at=int(time.time()),
            file_counts=FileCounts(
                cancelled=0, completed=0, failed=0, in_progress=0, total=0
            ),
            last_active_at=None,
            metadata=request.metadata,
            name=request.name,
            object="vector_store",
            status="completed",
            expires_after=ExpiresAfter.model_validate(request.expires_after) or None,
            expires_at=None,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to parse vector store request"
        ) from exc

    try:
        crud_vector_store = CRUDVectorStore(model=VectorStore)
        return await crud_vector_store.update(
            id_=vector_store_id,
            object_=vector_store_object,
            db=session,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to update vector store"
        ) from exc


@router.delete("/{vector_store_id}")
async def delete_vector_store(
    session: Session, vector_store_id: str
) -> VectorStoreDeleted:
    """Delete a vector store."""

    crud_vector_store = CRUDVectorStore(model=VectorStore)

    vector_store_deleted = await crud_vector_store.delete(
        db=session, id_=vector_store_id
    )
    return VectorStoreDeleted(
        id=vector_store_id,
        object="vector_store.deleted",
        deleted=bool(vector_store_deleted),
    )


@router.post("/{vector_store_id}/files")
async def create_vector_store_file(
    session: Session, vector_store_id: str, file_id: str
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
            status_code=500, detail="Failed to create vector store file"
        ) from exc


@router.get("/{vector_store_id}/files")
async def list_vector_store_files(
    session: Session, vector_store_id: str
) -> list[VectorStoreFile]:
    """List all the files in a vector store."""

    try:
        crud_vector_store_file = CRUDVectorStoreFile(model=VectorStoreFile)
        vector_store_files = await crud_vector_store_file.list(
            db=session, vector_store_id=vector_store_id
        )

        print(vector_store_files)
        return vector_store_files
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="Failed to list vector store files"
        ) from exc


@router.delete("/{vector_store_id}/files/{file_id}")
async def delete_vector_store_file(
    session: Session, vector_store_id: str, file_id: str
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

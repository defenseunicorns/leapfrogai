"""OpenAI Compliant Vector Store API Router."""

import time
from fastapi import HTTPException, APIRouter
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.vector_stores import VectorStoreFile, VectorStoreFileDeleted
from openai.types.beta.vector_store import ExpiresAfter, FileCounts
from leapfrogai_api.backend.types import (
    CreateVectorStoreRequest,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/openai/v1/vector_store", tags=["openai/vector_store"])


@router.post("")
async def create_vector_store(
    session: Session, request: CreateVectorStoreRequest
) -> VectorStore:
    """Create a vector store."""

    try:
        if request.file_ids == []:
            vector_store = VectorStore(
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
                expires_after=ExpiresAfter.model_validate(request.expires_after),
                expires_at=None,
            )
        else:
            raise HTTPException(
                status_code=405, detail="Unable to parse vector store request"
            )
    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to parse vector store request"
        ) from exc

    try:
        crud_vector_store = CRUDVectorStore(model=VectorStore)
        return await crud_vector_store.create(vector_store=vector_store, client=session)
    except Exception as exc:
        raise HTTPException(
            status_code=405, detail="Unable to create vector store"
        ) from exc


@router.get("")
async def list_vector_stores(session: Session) -> list[VectorStore] | None:
    """List all the vector stores."""
    try:
        crud_vector_store = CRUDVectorStore(model=VectorStore)
        return await crud_vector_store.list(client=session)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="Failed to list vector stores"
        ) from exc


@router.get("/{vector_store_id}")
async def retrieve_vector_store(
    session: Session, vector_store_id: str
) -> VectorStore | None:
    """Retrieve a vector store."""
    try:
        crud_vector_store = CRUDVectorStore(model=VectorStore)
        return await crud_vector_store.get(
            client=session, vector_store_id=vector_store_id
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve vector store"
        ) from exc


@router.post("/{vector_store_id}")
async def modify_vector_store(
    session: Session, vector_store_id: str, request: ModifyVectorStoreRequest
) -> VectorStore:
    """Modify a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{vector_store_id}")
async def delete_vector_store(
    session: Session, vector_store_id: str
) -> VectorStoreDeleted:
    """Delete a vector store."""
    try:
        crud_vector_store = CRUDVectorStore(model=VectorStore)
        return await crud_vector_store.delete(
            client=session, vector_store_id=vector_store_id
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="Failed to delete vector store"
        ) from exc


@router.post("/{vector_store_id}/files")
async def create_vector_store_file(
    session: Session, vector_store_id: str
) -> VectorStoreFile:
    """Create a file in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{vector_store_id}/files")
async def list_vector_store_files(
    session: Session, vector_store_id: str
) -> list[VectorStoreFile]:
    """List all the files in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{vector_store_id}/files/{file_id}")
async def delete_vector_store_file(
    session: Session, vector_store_id: str, file_id: str
) -> VectorStoreFileDeleted:
    """Delete a file in a vector store."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

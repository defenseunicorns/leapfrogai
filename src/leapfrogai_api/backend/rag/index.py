"""Indexing service for RAG files."""

import logging
import tempfile
import time
from fastapi import HTTPException, UploadFile, status, BackgroundTasks
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from openai.types.beta.vector_store import FileCounts, VectorStore
from openai.types.beta.vector_stores import VectorStoreFile
from openai.types.beta.vector_stores.vector_store_file import LastError
from supabase import AClient as AsyncClient

from leapfrogai_api.backend.rag.document_loader import load_file, split
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.data.crud_file_object import CRUDFileObject, FilterFileObject
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore, FilterVectorStore
from leapfrogai_api.typedef.vectorstores import (
    VectorStoreStatus,
    VectorStoreFileStatus,
    CreateVectorStoreRequest,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.data.crud_vector_store_file import (
    CRUDVectorStoreFile,
    FilterVectorStoreFile,
)

from leapfrogai_api.data.crud_vector_content import CRUDVectorContent, Vector

logger = logging.getLogger(__name__)

# Allows for overwriting type of embeddings that will be instantiated
embeddings_type: type[Embeddings] | type[LeapfrogAIEmbeddings] | None = (
    LeapfrogAIEmbeddings
)


class FileAlreadyIndexedError(Exception):
    """Raised when a file is already indexed."""


class IndexingService:
    """Service for indexing files into a vector store."""

    def __init__(self, db: AsyncClient):
        self.db = db
        self.embeddings = embeddings_type()
        self.query_name: str = "match_vectors"
        self.table_name: str = "vector_content"

    async def index_file(self, vector_store_id: str, file_id: str) -> VectorStoreFile:
        """Index a file into a vector store."""

        crud_vector_store_file = CRUDVectorStoreFile(db=self.db)
        crud_vector_store = CRUDVectorStore(db=self.db)

        if existing_file := await crud_vector_store_file.get(
            filters=FilterVectorStoreFile(vector_store_id=vector_store_id, id=file_id)
        ):
            logger.warning("File already indexed: %s", file_id)
            return existing_file

        if not (
            await crud_vector_store.get(filters=FilterVectorStore(id=vector_store_id))
        ):
            logger.error("Vector store doesn't exist: %s", vector_store_id)
            raise ValueError("Vector store not found")

        crud_file_object = CRUDFileObject(db=self.db)
        crud_file_bucket = CRUDFileBucket(db=self.db, model=UploadFile)

        file_object = await crud_file_object.get(filters=FilterFileObject(id=file_id))

        if not file_object:
            raise ValueError("File not found")
        file_bytes = await crud_file_bucket.download(id_=file_id)

        with tempfile.NamedTemporaryFile(suffix=file_object.filename) as temp_file:
            temp_file.write(file_bytes)
            temp_file.seek(0)
            documents = await load_file(temp_file.name)
            chunks = await split(documents)

            if len(chunks) == 0:
                vector_store_file = VectorStoreFile(
                    id=file_id,
                    created_at=0,
                    last_error=LastError(
                        message="No text found in file", code="parsing_error"
                    ),
                    object="vector_store.file",
                    status=VectorStoreFileStatus.FAILED.value,
                    usage_bytes=0,  # Leave blank to have Postgres calculate the document bytes
                    vector_store_id=vector_store_id,
                )
                return await crud_vector_store_file.create(object_=vector_store_file)

            vector_store_file = VectorStoreFile(
                id=file_id,
                created_at=0,
                last_error=None,
                object="vector_store.file",
                status=VectorStoreFileStatus.IN_PROGRESS.value,
                usage_bytes=0,  # Leave blank to have Postgres calculate the document bytes
                vector_store_id=vector_store_id,
            )

            vector_store_file = await crud_vector_store_file.create(
                object_=vector_store_file
            )

        try:
            ids = await self.aadd_documents(
                documents=chunks,
                vector_store_id=vector_store_id,
                file_id=file_id,
            )

            if len(ids) == 0:
                vector_store_file.status = VectorStoreFileStatus.FAILED.value
            else:
                vector_store_file.status = VectorStoreFileStatus.COMPLETED.value

            await crud_vector_store_file.update(
                id_=vector_store_file.id, object_=vector_store_file
            )
        except Exception as exc:
            vector_store_file.status = VectorStoreFileStatus.FAILED.value
            await crud_vector_store_file.update(
                id_=vector_store_file.id, object_=vector_store_file
            )
            raise exc

        return await crud_vector_store_file.get(
            filters=FilterVectorStoreFile(vector_store_id=vector_store_id, id=file_id)
        )

    async def index_files(
        self, vector_store_id: str, file_ids: list[str]
    ) -> list[VectorStoreFile]:
        """Index a list of files into a vector store."""
        responses = []
        for file_id in file_ids:
            try:
                response = await self.index_file(
                    vector_store_id=vector_store_id, file_id=file_id
                )
                responses.append(response)
            except FileAlreadyIndexedError:
                logger.info("File %s already exists and cannot be re-indexed", file_id)
                continue
            except Exception as exc:
                raise exc

        return responses

    async def create_new_vector_store(
        self,
        request: CreateVectorStoreRequest,
        background_tasks: BackgroundTasks | None = None,
    ) -> VectorStore:
        """Create a new vector store given a set of file ids"""
        crud_vector_store = CRUDVectorStore(db=self.db)

        current_time = int(time.time())
        expires_after, expires_at = request.get_expiry(current_time)
        saved_placeholder = None

        try:
            # Create a placeholder vector store
            placeholder_vector_store = VectorStore(
                id="",  # Leave blank to have Postgres generate a UUID
                name=request.name or "",
                status=VectorStoreStatus.IN_PROGRESS.value,
                object="vector_store",
                created_at=0,  # Leave blank to have Postgres generate a timestamp
                last_active_at=current_time,
                file_counts=FileCounts(
                    cancelled=0, completed=0, failed=0, in_progress=0, total=0
                ),
                usage_bytes=0,  # Leave blank to have Postgres calculate the document bytes
                metadata=request.metadata,
                expires_after=expires_after,
                expires_at=expires_at,
            )

            # Save the placeholder to the database
            saved_placeholder = await crud_vector_store.create(
                object_=placeholder_vector_store
            )

            if saved_placeholder is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unable to create vector store",
                )

            # Split the files, convert the chunks into vectors, and insert them into the db
            if background_tasks:
                # Perform the indexing in the background
                background_tasks.add_task(
                    self._complete_vector_store_creation,
                    saved_placeholder.id,
                    request,
                )
            else:
                await self._complete_vector_store_creation(
                    saved_placeholder.id, request
                )

            return saved_placeholder
        except Exception as exc:
            logging.error(exc)
            # Clean up the placeholder vector store if it was created
            if saved_placeholder:
                await crud_vector_store.delete(id_=saved_placeholder.id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to parse vector store request",
            ) from exc

    async def _complete_vector_store_creation(
        self, vector_store_id: str, request: CreateVectorStoreRequest
    ):
        """Complete the vector store creation process in the background."""
        crud_vector_store = CRUDVectorStore(db=self.db)
        vector_store = await crud_vector_store.get(
            filters=FilterVectorStore(id=vector_store_id)
        )

        if request.file_ids != []:
            responses = await self.index_files(vector_store_id, request.file_ids)
            for response in responses:
                await self._increment_vector_store_file_status(vector_store, response)

        vector_store.status = VectorStoreStatus.COMPLETED.value
        vector_store.last_active_at = int(time.time())

        await crud_vector_store.update(id_=vector_store_id, object_=vector_store)

    async def modify_existing_vector_store(
        self,
        vector_store_id: str,
        request: ModifyVectorStoreRequest,
        background_tasks: BackgroundTasks | None = None,
    ) -> VectorStore:
        """Modify an existing vector store given its id."""
        crud_vector_store = CRUDVectorStore(db=self.db)

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
                usage_bytes=old_vector_store.usage_bytes,  # Automatically calculated by DB
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

            # Update the vector store with the new information and set status to in_progress for the duration of this function
            updated_vector_store = await crud_vector_store.update(
                id_=vector_store_id,
                object_=new_vector_store,
            )

            if updated_vector_store is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unable to modify vector store",
                )

            # Split the files, convert the chunks into vectors, and insert them into the db
            if request.file_ids:
                if background_tasks:
                    # Perform the indexing in the background
                    background_tasks.add_task(
                        self._complete_vector_store_modification,
                        vector_store_id,
                        request,
                    )
                else:
                    await self._complete_vector_store_modification(
                        vector_store_id, request
                    )

            return updated_vector_store
        except Exception as exc:
            logger.error(exc)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to parse vector store request",
            ) from exc

    async def _complete_vector_store_modification(
        self, vector_store_id: str, request: ModifyVectorStoreRequest
    ):
        """Complete the vector store modification process in the background."""
        crud_vector_store = CRUDVectorStore(db=self.db)
        vector_store = await crud_vector_store.get(
            filters=FilterVectorStore(id=vector_store_id)
        )

        if request.file_ids:
            responses = await self.index_files(vector_store_id, request.file_ids)
            for response in responses:
                await self._increment_vector_store_file_status(vector_store, response)

        vector_store.status = VectorStoreStatus.COMPLETED.value
        last_active_at = int(time.time())
        vector_store.last_active_at = last_active_at  # Update after indexing files

        expires_after, expires_at = request.get_expiry(last_active_at)
        if expires_after and expires_at:
            vector_store.expires_after = expires_after
            vector_store.expires_at = expires_at

        await crud_vector_store.update(id_=vector_store_id, object_=vector_store)

    async def file_ids_are_valid(self, file_ids: str | list[str]) -> bool:
        """Check if the provided file ids exist"""
        crud_file_object = CRUDFileObject(db=self.db)

        if not isinstance(file_ids, list):
            file_ids = [file_ids]

        try:
            for file_id in file_ids:
                await crud_file_object.get(filters=FilterFileObject(id=file_id))
        except Exception:
            return False

        return True

    async def aadd_documents(
        self,
        documents: list[Document],
        vector_store_id: str,
        file_id: str,
        batch_size: int = 100,
    ) -> list[str]:
        """Adds documents to the vector store in batches.
        Args:
            documents (list[Document]): A list of Langchain Document objects to be added.
            vector_store_id (str): The ID of the vector store where the documents will be added.
            file_id (str): The ID of the file associated with the documents.
            batch_size (int): The size of the batches that will
            be pushed to the db. This value defaults to 100
                as a balance between the memory impact of large files and performance improvements from batching.
        Returns:
            List[str]: A list of IDs assigned to the added documents.
        Raises:
            Any exceptions that may occur during the execution of the method.
        """
        ids = []
        embeddings = await self.embeddings.aembed_documents(
            texts=[document.page_content for document in documents]
        )

        vectors: list[Vector] = []
        for document, embedding in zip(documents, embeddings):
            vector = Vector(
                id="",
                vector_store_id=vector_store_id,
                file_id=file_id,
                content=document.page_content,
                metadata=document.metadata,
                embedding=embedding,
            )
            vectors.append(vector)

        crud_vector_content = CRUDVectorContent(db=self.db)

        for i in range(0, len(vectors), batch_size):
            batch = vectors[i : i + batch_size]

            response = await crud_vector_content.add_vectors(batch)
            ids.extend([item.id for item in response])
        return ids

    async def _increment_vector_store_file_status(
        self, vector_store: VectorStore, file_response: VectorStoreFile
    ):
        """Increment the file count of a given vector store based on the file response"""
        if file_response.status == VectorStoreFileStatus.COMPLETED.value:
            vector_store.file_counts.completed += 1
        elif file_response.status == VectorStoreFileStatus.FAILED.value:
            vector_store.file_counts.failed += 1
        elif file_response.status == VectorStoreFileStatus.IN_PROGRESS.value:
            vector_store.file_counts.in_progress += 1
        elif file_response.status == VectorStoreFileStatus.CANCELLED.value:
            vector_store.file_counts.cancelled += 1
        vector_store.file_counts.total += 1

"""Indexing service for RAG files."""

import logging
import tempfile
import time


from fastapi import HTTPException, UploadFile, status
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from openai.types.beta.vector_store import FileCounts, VectorStore
from openai.types.beta.vector_stores import VectorStoreFile
from openai.types.beta.vector_stores.vector_store_file import LastError
from supabase_py_async import AsyncClient
from leapfrogai_api.backend.rag.document_loader import load_file, split
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.data.crud_file_object import CRUDFileObject, FilterFileObject
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore, FilterVectorStore
from leapfrogai_api.backend.types import (
    VectorStoreStatus,
    VectorStoreFileStatus,
    CreateVectorStoreRequest,
    ModifyVectorStoreRequest,
)
from leapfrogai_api.data.crud_vector_store_file import (
    CRUDVectorStoreFile,
    FilterVectorStoreFile,
)

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

        if await crud_vector_store_file.get(
            filters=FilterVectorStoreFile(vector_store_id=vector_store_id, id=file_id)
        ):
            print("File already indexed: %s", file_id)
            logging.error("File already indexed: %s", file_id)
            raise FileAlreadyIndexedError("File already indexed")

        if not (
            await crud_vector_store.get(filters=FilterVectorStore(id=vector_store_id))
        ):
            print("Vector store doesn't exist: %s", vector_store_id)
            logging.error("Vector store doesn't exist: %s", vector_store_id)
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
                    usage_bytes=0,
                    vector_store_id=vector_store_id,
                )
                return await crud_vector_store_file.create(object_=vector_store_file)

            vector_store_file = VectorStoreFile(
                id=file_id,
                created_at=0,
                last_error=None,
                object="vector_store.file",
                status=VectorStoreFileStatus.IN_PROGRESS.value,
                usage_bytes=0,
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
        except Exception as e:
            vector_store_file.status = VectorStoreFileStatus.FAILED.value
            await crud_vector_store_file.update(
                id_=vector_store_file.id, object_=vector_store_file
            )
            raise e

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
                logging.info("File %s already exists and cannot be re-indexed", file_id)
                continue
            except Exception as exc:
                raise exc

        return responses

    async def create_new_vector_store(
        self, request: CreateVectorStoreRequest
    ) -> VectorStore:
        """Create a new vector store given a set of file ids"""
        crud_vector_store = CRUDVectorStore(db=self.db)

        last_active_at = int(time.time())

        expires_after, expires_at = request.get_expiry(last_active_at)

        vector_store = VectorStore(
            id="",  # Leave blank to have Postgres generate a UUID
            usage_bytes=0,  # Automatically calculated by DB
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
        new_vector_store = await crud_vector_store.create(object_=vector_store)
        if request.file_ids != []:
            responses = await self.index_files(new_vector_store.id, request.file_ids)

            for response in responses:
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

    async def file_ids_are_valid(self, file_ids: str | list[str]) -> bool:
        crud_file_object = CRUDFileObject(db=self.db)

        if not isinstance(file_ids, list):
            file_ids = [file_ids]

        try:
            for file_id in file_ids:
                await crud_file_object.get(filters=FilterFileObject(id=file_id))
        except Exception:
            return False

        return True

    async def modify_existing_vector_store(
        self,
        vector_store_id: str,
        request: ModifyVectorStoreRequest,
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
                responses = await self.index_files(
                    new_vector_store.id, request.file_ids
                )

                for response in responses:
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
            new_vector_store.last_active_at = (
                last_active_at  # Update after indexing files
            )
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

    async def adelete_file(self, vector_store_id: str, file_id: str) -> bool:
        """Delete a file from the vector store.

        Args:
            vector_store_id (str): The ID of the vector store.
            file_id (str): The ID of the file to be deleted.

        Returns:
            dict: The response from the database after deleting the file.

        """
        data, _count = (
            await self.db.from_(self.table_name)
            .delete()
            .eq("vector_store_id", vector_store_id)
            .eq("file_id", file_id)
            .execute()
        )

        _, response = data

        return bool(response)

    async def aadd_documents(
        self,
        documents: list[Document],
        vector_store_id: str,
        file_id: str,
    ) -> list[str]:
        """Adds documents to the vector store.

        Args:
            documents (list[Document]): A list of Langchain Document objects to be added.
            vector_store_id (str): The ID of the vector store where the documents will be added.
            file_id (str): The ID of the file associated with the documents.

        Returns:
            List[str]: A list of IDs assigned to the added documents.

        Raises:
            Any exceptions that may occur during the execution of the method.

        """
        ids = []  # Initialize the ids list
        embeddings = await self.embeddings.aembed_documents(
            texts=[document.page_content for document in documents]
        )

        for document, embedding in zip(documents, embeddings):
            response = await self._aadd_vector(
                vector_store_id=vector_store_id,
                file_id=file_id,
                content=document.page_content,
                metadata=document.metadata,
                embedding=embedding,
            )
            ids.append(response.data[0]["id"])

        return ids

    async def asimilarity_search(self, query: str, vector_store_id: str, k: int = 4):
        """Searches for similar documents.

        Args:
            query (str): The query string.
            vector_store_id (str): The ID of the vector store to search in.
            k (int, optional): The number of similar documents to retrieve. Defaults to 4.

        Returns:
            The response from the database after executing the similarity search.

        """
        vector = await self.embeddings.aembed_query(query)

        user_id: str = (await self.db.auth.get_user()).user.id

        params = {
            "query_embedding": vector,
            "match_limit": k,
            "vs_id": vector_store_id,
            "user_id": user_id,
        }

        query_builder = self.db.rpc(self.query_name, params=params)

        response = await query_builder.execute()

        return response

    async def _adelete_vector(
        self,
        vector_store_id: str,
        file_id: str,
    ) -> dict:
        """Delete a vector from the vector store.

        Args:
            vector_store_id (str): The ID of the vector store.
            file_id (str): The ID of the file associated with the vector.

        Returns:
            dict: The response from the database after deleting the vector.

        """
        response = (
            await self.db.from_(self.table_name)
            .delete()
            .eq("vector_store_id", vector_store_id)
            .eq("file_id", file_id)
            .execute()
        )
        return response

    async def _aadd_vector(
        self,
        vector_store_id: str,
        file_id: str,
        content: str,
        metadata: str,
        embedding: list[float],
    ) -> dict:
        """Add a vector to the vector store.

        Args:
            vector_store_id (str): The ID of the vector store.
            file_id (str): The ID of the file associated with the vector.
            content (str): The content of the vector.
            metadata (str): The metadata associated with the vector.
            embedding (list[float]): The embedding of the vector.

        Returns:
            dict: The response from the database after inserting the vector.

        """

        user_id: str = (await self.db.auth.get_user()).user.id

        row: dict[str, any] = {
            "user_id": user_id,
            "vector_store_id": vector_store_id,
            "file_id": file_id,
            "content": content,
            "metadata": metadata,
            "embedding": embedding,
        }
        response = await self.db.from_(self.table_name).insert(row).execute()
        return response

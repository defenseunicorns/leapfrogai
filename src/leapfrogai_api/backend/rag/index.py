"""Indexing service for RAG files."""

import logging
import tempfile

from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from openai.types.beta.vector_stores import VectorStoreFile
from openai.types.beta.vector_stores.vector_store_file import LastError
from supabase_py_async import AsyncClient
from leapfrogai_api.backend.rag.document_loader import load_file, split
from leapfrogai_api.backend.rag.leapfrogai_embeddings import LeapfrogAIEmbeddings
from leapfrogai_api.backend.types import VectorStoreFileStatus
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.data.crud_file_object import CRUDFileObject, FilterFileObject
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore, FilterVectorStore
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
                    vector_store_id=vector_store_id,
                )
                return await crud_vector_store_file.create(object_=vector_store_file)

            vector_store_file = VectorStoreFile(
                id=file_id,
                created_at=0,
                last_error=None,
                object="vector_store.file",
                status=VectorStoreFileStatus.IN_PROGRESS.value,
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

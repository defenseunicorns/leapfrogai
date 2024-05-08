"""Indexing service for RAG files."""

import tempfile
import time
from fastapi import UploadFile
from openai.types import FileObject
from openai.types.beta.vector_stores import VectorStoreFile
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.data.crud_file_object import CRUDFileObject
from leapfrogai_api.data.crud_vector_store_file import CRUDVectorStoreFile
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.backend.rag.document_loader import load_file, split, embed_chunks


class IndexingService:
    """Service for indexing files into a vector store."""

    def __init__(self, session: Session):
        self.session = session

    async def _get_vector_store_file(
        self, vector_store_id: str, file_id: str
    ) -> VectorStoreFile | None:
        crud_vector_store = CRUDVectorStoreFile(model=VectorStoreFile)
        return await crud_vector_store.get(
            db=self.session, vector_store_id_=vector_store_id, file_id=file_id
        )

    async def _get_file_object(self, file_id: str):
        crud_file_object = CRUDFileObject(model=FileObject)
        file_object = await crud_file_object.get(db=self.session, id_=file_id)
        if not file_object:
            raise ValueError("File object not found")
        return file_object

    async def _get_file_bytes(self, file_id: str):
        crud_file_bucket = CRUDFileBucket(model=UploadFile)
        file_bytes = await crud_file_bucket.download(client=self.session, id_=file_id)
        if not file_bytes:
            raise ValueError("File bucket not found")
        return file_bytes

    async def index_file(self, vector_store_id: str, file_id: str) -> VectorStoreFile:
        """Index a file into a vector store."""
        vector_store_file = await self._get_vector_store_file(vector_store_id, file_id)

        if vector_store_file:
            print(
                f"ERROR: Duplicating index file {file_id} into vector store {vector_store_id}!"
            )
            raise ValueError("File already indexed")

        file_object = await self._get_file_object(file_id)
        file_bytes = await self._get_file_bytes(file_id)

        with tempfile.NamedTemporaryFile(suffix=file_object.filename) as temp_file:
            temp_file.write(file_bytes)
            temp_file.seek(0)
            documents = await load_file(temp_file.name)
            chunks = await split(documents)
            embeddings = await embed_chunks(chunks)

            print(f"Chunks: {len(chunks)}")
            print(f"Embeddings: {len(embeddings)}")
            print(f"Embeddings size: {len(embeddings[0])}")

            vector_store_file = VectorStoreFile(
                id=file_id,
                created_at=int(time.time()),
                last_error=None,
                object="vector_store.file",
                status="in_progress",
                vector_store_id=vector_store_id,
            )

            crud_vector_store_file = CRUDVectorStoreFile(model=VectorStoreFile)
            vector_store_file = await crud_vector_store_file.create(
                db=self.session, object_=vector_store_file
            )

            return await self._get_vector_store_file(vector_store_id, file_id)

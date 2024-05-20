"""Indexing service for RAG files."""

import tempfile
from fastapi import UploadFile
from openai.types import FileObject
from openai.types.beta.vector_stores import VectorStoreFile
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.data.crud_file_object import CRUDFileObject
from leapfrogai_api.data.crud_vector_store_file import CRUDVectorStoreFile
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.backend.rag.document_loader import load_file, split
from leapfrogai_api.data.supabase_vector_store import AsyncSupabaseVectorStore
from leapfrogai_api.backend.leapfrogai_embeddings import LeapfrogAIEmbeddings


class IndexingService:
    """Service for indexing files into a vector store."""

    def __init__(self, session: Session):
        self.session = session

    async def index_file(self, vector_store_id: str, file_id: str) -> VectorStoreFile:
        """Index a file into a vector store."""
        crud_vector_store_file = CRUDVectorStoreFile(model=VectorStoreFile)
        vector_store_file = await crud_vector_store_file.get(
            db=self.session, vector_store_id=vector_store_id, file_id=file_id
        )

        if vector_store_file:
            raise ValueError("File already indexed")

        crud_file_object = CRUDFileObject(model=FileObject)
        crud_file_bucket = CRUDFileBucket(model=UploadFile)

        file_object = await crud_file_object.get(db=self.session, id_=file_id)

        if not file_object:
            raise ValueError("File not found")

        file_bytes = await crud_file_bucket.download(client=self.session, id_=file_id)

        with tempfile.NamedTemporaryFile(suffix=file_object.filename) as temp_file:
            temp_file.write(file_bytes)
            temp_file.seek(0)
            documents = await load_file(temp_file.name)
            chunks = await split(documents)

            vector_store_file = VectorStoreFile(
                id=file_id,
                created_at=0,
                last_error=None,
                object="vector_store.file",
                status="in_progress",
                vector_store_id=vector_store_id,
            )

            vector_store_file = await crud_vector_store_file.create(
                db=self.session, object_=vector_store_file
            )

            try:
                embeddings_function = LeapfrogAIEmbeddings()
                vector_store_client = AsyncSupabaseVectorStore(
                    client=self.session, embedding=embeddings_function
                )

                ids = await vector_store_client.aadd_documents(
                    documents=chunks,
                    vector_store_id=vector_store_id,
                    file_id=file_id,
                )

                if len(ids) == 0:
                    vector_store_file.status = "failed"
                else:
                    vector_store_file.status = "completed"

                await crud_vector_store_file.update(
                    db=self.session, id_=vector_store_file.id, object_=vector_store_file
                )
            except:
                vector_store_file.status = "failed"
                await crud_vector_store_file.update(
                    db=self.session, id_=vector_store_file.id, object_=vector_store_file
                )
                raise

            return await crud_vector_store_file.get(
                db=self.session, vector_store_id=vector_store_id, file_id=file_id
            )

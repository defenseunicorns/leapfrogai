import tempfile
from fastapi import UploadFile
from openai.types import FileObject
from openai.types.beta import VectorStore
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.data.crud_file_object import CRUDFileObject
from leapfrogai_api.data.crud_vector_store_object import CRUDVectorStore
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.backend.rag.document_loader import load_file, split, embed_chunks


class IndexingService:

    def __init__(self, session: Session):
        self.session = session

    async def _validate_vector_store_id(self, vector_store_id: str):
        crud_vector_store = CRUDVectorStore(model=VectorStore)
        vector_store = await crud_vector_store.get(
            db=self.session, id_=vector_store_id
        )
        if not vector_store:
            raise ValueError("Vector store not found")
        return vector_store

    async def index_file(self, vector_store_id: str, file_id: str):
        """"""
        self._validate_vector_store_id(vector_store_id)

        crud_file_bucket = CRUDFileBucket(model=UploadFile)
        crud_file_object = CRUDFileObject(model=FileObject)

        file_object = await crud_file_object.get(db=self.session, id_=file_id)
        file_bytes = await crud_file_bucket.download(client=self.session, id_=file_id)

        with tempfile.NamedTemporaryFile(suffix=file_object.filename) as temp_file:
            temp_file.write(file_bytes)
            temp_file.seek(0)
            docs = await load_file(temp_file.name)
            chunks = await split(docs)
            # for chunk in chunks:
            #     print(f"{chunk}\n")

            embeddings = await embed_chunks(chunks)
            # print(embeddings[0])
            print(len(embeddings[0]))
            print(f"Chunks: {len(chunks)}")
            print(f"Embeddings: {len(embeddings)}")

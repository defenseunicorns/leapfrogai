"""CRUD Operations for VectorStore."""

from openai.types.beta import VectorStore
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class CRUDVectorStore(CRUDBase[VectorStore]):
    """CRUD Operations for VectorStore"""

    def __init__(
        self, model: type[VectorStore], table_name: str = "vector_store_objects"
    ):
        super().__init__(model=model, table_name=table_name)

    async def create(self, db: AsyncClient, object_: VectorStore) -> VectorStore | None:
        """Create new vector store."""
        return await super().create(db=db, object_=object_)

    async def get(self, id_: str, db: AsyncClient) -> VectorStore | None:
        """Get a vector store by its ID."""
        return await super().get(db=db, id_=id_)

    async def list(self, db: AsyncClient) -> list[VectorStore] | None:
        """List all vector stores."""
        return await super().list(db=db)

    async def update(
        self, id_: str, db: AsyncClient, object_: VectorStore
    ) -> VectorStore | None:
        """Update a vector store by its ID."""

        dict_ = object_.model_dump()
        del dict_["bytes"]  # Automatically calculated by DB

        data, _count = (
            await db.table(self.table_name).update(dict_).eq("id", id_).execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, id_: str, db: AsyncClient) -> bool:
        """Delete a vector store by its ID."""
        return await super().delete(id_=id_, db=db)

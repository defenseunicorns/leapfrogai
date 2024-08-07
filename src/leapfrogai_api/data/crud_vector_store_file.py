"""CRUD Operations for VectorStoreFile."""

from pydantic import BaseModel
from openai.types.beta.vector_stores import VectorStoreFile
from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class FilterVectorStoreFile(BaseModel):
    vector_store_id: str
    id: str | None = None


class CRUDVectorStoreFile(CRUDBase[VectorStoreFile]):
    """CRUD Operations for VectorStoreFile"""

    def __init__(self, db: AsyncClient, table_name: str = "vector_store_file"):
        super().__init__(db=db, model=VectorStoreFile, table_name=table_name)

    async def get(
        self, filters: FilterVectorStoreFile | None = None
    ) -> VectorStoreFile | None:
        """Get vector store file by filters."""
        return await super().get(filters=filters.model_dump() if filters else None)

    async def list(
        self, filters: FilterVectorStoreFile | None = None
    ) -> list[VectorStoreFile] | None:
        """List all vector store files."""
        return await super().list(filters={"vector_store_id": filters.vector_store_id})

    async def update(
        self, id_: str, object_: VectorStoreFile
    ) -> VectorStoreFile | None:
        """Update a vector store file by its ID.
        Args:
            id_ (str): The file id.
            db (AsyncClient): The Supabase async client.
            object_ (VectorStoreFile): The vector store file object (contains vector store id).
        """
        dict_ = object_.model_dump()
        del dict_["usage_bytes"]

        data, _count = (
            await self.db.table(self.table_name)
            .update(dict_)
            .eq("id", id_)
            .eq("vector_store_id", object_.vector_store_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, filters: FilterVectorStoreFile | None = None) -> bool:
        """Delete a vector store file by its ID."""
        return await super().delete(filters=filters.model_dump() if filters else None)

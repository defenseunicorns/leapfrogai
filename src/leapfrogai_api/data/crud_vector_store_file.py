"""CRUD Operations for VectorStoreFile."""

from pydantic import BaseModel, Field
from openai.types.beta.vector_stores import VectorStoreFile
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class AuthVectorStoreFile(VectorStoreFile):
    """A wrapper for the VectorStoreFile that includes a user_id for auth"""

    user_id: str = Field(default="")


class FilterVectorStoreFile(BaseModel):
    vector_store_id: str
    id: str | None = None


class CRUDVectorStoreFile(CRUDBase[AuthVectorStoreFile]):
    """CRUD Operations for VectorStoreFile"""

    def __init__(self, db: AsyncClient, table_name: str = "vector_store_file"):
        super().__init__(db=db, model=AuthVectorStoreFile, table_name=table_name)

    async def create(self, object_: VectorStoreFile) -> VectorStoreFile | None:
        """Create a new vector store file."""
        user_id: str = (await self.db.auth.get_user()).user.id
        return await super().create(
            object_=AuthVectorStoreFile(user_id=user_id, **object_.model_dump())
        )

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
        data, _count = (
            await self.db.table(self.table_name)
            .update(object_.model_dump())
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
        return await super().delete(filters=filters)

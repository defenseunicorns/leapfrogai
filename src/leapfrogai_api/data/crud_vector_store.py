"""CRUD Operations for VectorStore."""

from pydantic import Field
from openai.types.beta import VectorStore
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class AuthVectorStore(VectorStore):
    """A wrapper for the VectorStore that includes a user_id for auth"""

    user_id: str = Field(default="")


class CRUDVectorStore(CRUDBase[AuthVectorStore]):
    """CRUD Operations for VectorStore"""

    def __init__(self, db: AsyncClient, table_name: str = "vector_store"):
        super().__init__(db=db, model=AuthVectorStore, table_name=table_name)

    async def create(self, object_: VectorStore) -> AuthVectorStore | None:
        """Create new vector store."""
        user_id: str = (await self.db.auth.get_user()).user.id
        return await super().create(
            object_=AuthVectorStore(user_id=user_id, **object_.model_dump())
        )

    async def get(self, id_: str) -> AuthVectorStore | None:
        """Get a vector store by its ID."""
        return await super().get(id_=id_)

    async def list(self) -> list[AuthVectorStore] | None:
        """List all vector stores."""
        return await super().list()

    async def update(self, id_: str, object_: VectorStore) -> AuthVectorStore | None:
        """Update a vector store by its ID."""

        dict_ = object_.model_dump()
        del dict_["bytes"]  # Automatically calculated by DB

        data, _count = (
            await self.db.table(self.table_name).update(dict_).eq("id", id_).execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, id_: str) -> bool:
        """Delete a vector store by its ID."""
        return await super().delete(id_=id_)

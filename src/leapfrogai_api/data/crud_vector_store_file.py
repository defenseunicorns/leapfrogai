"""CRUD Operations for VectorStoreFile."""

from pydantic import Field
from openai.types.beta.vector_stores import VectorStoreFile
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class AuthVectorStoreFile(VectorStoreFile):
    """A wrapper for the VectorStoreFile that includes a user_id for auth"""

    user_id: str = Field(default="")


class CRUDVectorStoreFile(CRUDBase[AuthVectorStoreFile]):
    """CRUD Operations for VectorStoreFile"""

    def __init__(self, db: AsyncClient, table_name: str = "vector_store_file"):
        super().__init__(db=db, model=AuthVectorStoreFile, table_name=table_name)

    async def create(self, object_: VectorStoreFile) -> AuthVectorStoreFile | None:
        """Create a new vector store file."""
        user_id: str = (await self.db.auth.get_user()).user.id
        return await super().create(
            object_=AuthVectorStoreFile(user_id=user_id, **object_.model_dump())
        )

    async def get(  # pylint: disable=arguments-differ
        self, vector_store_id: str, file_id: str
    ) -> AuthVectorStoreFile | None:
        """Get a vector store file by its ID."""
        data, _count = (
            await self.db.table(self.table_name)
            .select("*")
            .eq("vector_store_id", vector_store_id)
            .eq("id", file_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def list(  # pylint: disable=arguments-differ
        self, vector_store_id: str
    ) -> list[AuthVectorStoreFile] | None:
        """List all vector store files."""
        data, _count = (
            await self.db.table(self.table_name)
            .select("*")
            .eq("vector_store_id", vector_store_id)
            .execute()
        )

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(
        self, id_: str, object_: VectorStoreFile
    ) -> AuthVectorStoreFile | None:
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

    async def delete(self, vector_store_id: str, file_id: str) -> bool:  # pylint: disable=arguments-differ
        """Delete a vector store file by its ID."""

        data, _count = (
            await self.db.table(self.table_name)
            .delete()
            .eq("vector_store_id", vector_store_id)
            .eq("id", file_id)
            .execute()
        )

        _, response = data

        return bool(response)

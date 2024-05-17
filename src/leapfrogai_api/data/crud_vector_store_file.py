"""CRUD Operations for VectorStoreFile."""

from openai.types.beta.vector_stores import VectorStoreFile
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class CRUDVectorStoreFile(CRUDBase[VectorStoreFile]):
    """CRUD Operations for VectorStoreFile"""

    def __init__(
        self,
        model: type[VectorStoreFile],
        table_name: str = "vector_store_file_objects",
    ):
        super().__init__(model=model, table_name=table_name)

    async def create(
        self, db: AsyncClient, object_: VectorStoreFile
    ) -> VectorStoreFile | None:
        """Create a new vector store file."""
        return await super().create(db=db, object_=object_)

    async def get(  # pylint: disable=arguments-differ
        self, vector_store_id: str, file_id: str, db: AsyncClient
    ) -> VectorStoreFile | None:
        """Get a vector store file by its ID."""
        data, _count = (
            await db.table(self.table_name)
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
        self, vector_store_id: str, db: AsyncClient
    ) -> list[VectorStoreFile] | None:
        """List all vector store files."""
        data, _count = (
            await db.table(self.table_name)
            .select("*")
            .eq("vector_store_id", vector_store_id)
            .execute()
        )

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(
        self, id_: str, db: AsyncClient, object_: VectorStoreFile
    ) -> VectorStoreFile | None:
        """Update a vector store file by its ID.
        Args:
            id_ (str): The file id.
            db (AsyncClient): The Supabase async client.
            object_ (VectorStoreFile): The vector store file object (contains vector store id).
        """
        data, _count = (
            await db.table(self.table_name)
            .update(object_.model_dump())
            .eq("id", id_)
            .eq("vector_store_id", object_.vector_store_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, vector_store_id: str, file_id: str, db: AsyncClient) -> bool:  # pylint: disable=arguments-differ
        """Delete a vector store file by its ID."""

        data, _count = (
            await db.table(self.table_name)
            .delete()
            .eq("vector_store_id", vector_store_id)
            .eq("id", file_id)
            .execute()
        )

        _, response = data

        return bool(response)

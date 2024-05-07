"""CRUD Operations for VectorStore."""

from supabase_py_async import AsyncClient
from openai.types.beta import VectorStore, VectorStoreDeleted


class CRUDVectorStore:
    """CRUD Operations for VectorStore"""

    def __init__(self, model: type[VectorStore]):
        self.model = model
        self.table_name = "vector_store_objects"

    async def create(
        self, client: AsyncClient, vector_store: VectorStore
    ) -> VectorStore | None:
        """Create a new vector store."""
        vector_store_dict = vector_store.model_dump()
        if vector_store_dict.get("id") == "":
            del vector_store_dict["id"]
        data, _count = (
            await client.table(self.table_name).insert(vector_store_dict).execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def get(
        self, client: AsyncClient, vector_store_id: str
    ) -> VectorStore | None:
        """Get a vector store by its ID."""
        data, _count = (
            await client.table(self.table_name)
            .select("*")
            .eq("id", vector_store_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def list(self, client: AsyncClient) -> list[VectorStore] | None:
        """List all vector stores."""
        data, _count = await client.table(self.table_name).select("*").execute()

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(
        self, client: AsyncClient, vector_store_id: str, vector_store: VectorStore
    ) -> VectorStore | None:
        """Update a vector store by its ID."""
        data, _count = (
            await client.table(self.table_name)
            .update(vector_store.model_dump())
            .eq("id", vector_store_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(
        self, client: AsyncClient, vector_store_id: str
    ) -> VectorStoreDeleted | None:
        """Delete a vector store by its ID."""
        data, _count = (
            await client.table(self.table_name)
            .delete()
            .eq("id", vector_store_id)
            .execute()
        )

        _, response = data

        return VectorStoreDeleted(
            id=vector_store_id,
            deleted=bool(response),
            object="vector_store.deleted",
        )

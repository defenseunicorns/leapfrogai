"""CRUD Operations for VectorStore."""

import time

from pydantic import BaseModel
from openai.types.beta import VectorStore
from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class FilterVectorStore(BaseModel):
    """Validation for VectorStore filter."""

    id: str


class CRUDVectorStore(CRUDBase[VectorStore]):
    """CRUD Operations for VectorStore"""

    def __init__(self, db: AsyncClient):
        super().__init__(db=db, model=VectorStore, table_name="vector_store")

    async def get(self, filters: FilterVectorStore | None = None) -> VectorStore | None:
        """Get vector store by filters."""

        vector_store: VectorStore | None = await super().get(
            filters=filters.model_dump() if filters else None
        )

        if await self.delete_when_expired(vector_store):
            return None

        return vector_store

    async def list(
        self, filters: FilterVectorStore | None = None
    ) -> list[VectorStore] | None:
        """List all vector stores."""

        vector_stores: list[VectorStore] | None = await super().list(
            filters=filters.model_dump() if filters else None
        )
        non_expired_vector_stores: list[VectorStore] | None = None

        if vector_stores:
            # Iterate through each vector store and delete expired entries
            for vector_store in vector_stores:
                vector_store_deleted: bool = await self.delete_when_expired(
                    vector_store
                )

                if vector_store_deleted:
                    continue
                else:
                    if non_expired_vector_stores:
                        non_expired_vector_stores.append(vector_store)
                    else:
                        non_expired_vector_stores = [vector_store]

        return non_expired_vector_stores

    async def update(self, id_: str, object_: VectorStore) -> VectorStore | None:
        """Update a vector store by its ID."""

        dict_ = object_.model_dump()
        del dict_["usage_bytes"]  # Automatically calculated by DB

        data, _count = (
            await self.db.table(self.table_name).update(dict_).eq("id", id_).execute()
        )

        _, response = data

        if response:
            if "user_id" in response[0]:
                del response[0]["user_id"]
            return self.model(**response[0])
        return None

    async def delete(self, filters: FilterVectorStore | None = None) -> bool:
        """Delete a vector store by its ID."""
        return await super().delete(filters=filters.model_dump() if filters else None)

    async def delete_when_expired(self, vector_store: VectorStore | None) -> bool:
        """Delete vector stores when they are expired"""

        if vector_store and vector_store.expires_at and vector_store.expires_after:
            current_time = int(time.time())

            if current_time > vector_store.expires_at:
                await self.delete(filters=FilterVectorStore(id=vector_store.id))
                return True
        return False

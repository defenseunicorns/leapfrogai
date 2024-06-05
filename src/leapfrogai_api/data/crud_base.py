"""CRUD Operations for VectorStore."""

from typing import Generic, TypeVar
from supabase_py_async import AsyncClient
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class CRUDBase(Generic[ModelType]):
    """CRUD Operations"""

    def __init__(self, db: AsyncClient, model: type[ModelType], table_name: str):
        self.model = model
        self.table_name = table_name
        self.db = db

    async def create(self, object_: ModelType) -> ModelType | None:
        """Create new row."""
        dict_ = object_.model_dump()
        del dict_["id"]  # Ensure this is created by the database
        del dict_["created_at"]  # Ensure this is created by the database
        data, _count = await self.db.table(self.table_name).insert(dict_).execute()

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def get(self, id_: str) -> ModelType | None:
        """Get row by ID."""
        data, _count = (
            await self.db.table(self.table_name).select("*").eq("id", id_).execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def list(self) -> list[ModelType] | None:
        """List all rows."""
        data, _count = await self.db.table(self.table_name).select("*").execute()

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(self, id_: str, object_: ModelType) -> ModelType | None:
        """Update a vector store by its ID."""
        data, _count = (
            await self.db.table(self.table_name)
            .update(object_.model_dump())
            .eq("id", id_)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, id_: str) -> bool:
        """Delete a vector store by its ID."""
        data, _count = (
            await self.db.table(self.table_name).delete().eq("id", id_).execute()
        )

        _, response = data

        return bool(response)

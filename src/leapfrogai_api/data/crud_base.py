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
        if "id" in dict_ and not dict_.get(
            "id"
        ):  # There are cases where the id is provided
            del dict_["id"]
        if "created_at" in dict_:
            del dict_["created_at"]
        data, _count = await self.db.table(self.table_name).insert(dict_).execute()

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def get(self, filters: dict | None = None) -> ModelType | None:
        """Get row by filters."""
        query = self.db.table(self.table_name).select("*")

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        data, _count = await query.execute()

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def list(self, filters: dict | None = None) -> list[ModelType] | None:
        """List all rows."""
        query = self.db.table(self.table_name).select("*")

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        data, _count = await query.execute()

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(self, id_: str, object_: ModelType) -> ModelType | None:
        """Update a row by its ID."""
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

    async def delete(self, filters: dict | None = None) -> bool:
        """Delete a row by filters."""
        query = self.db.table(self.table_name).delete()

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        data, _count = await query.execute()

        _, response = data

        if response:
            return True
        return False

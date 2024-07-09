"""CRUD Operations for VectorStore."""

from typing import Generic, TypeVar
from supabase import AClient as AsyncClient
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
        dict_["user_id"] = await self._get_user_id()

        if "id" in dict_ and not dict_.get(
            "id"
        ):  # There are cases where the id is provided
            del dict_["id"]
        # Only delete created_at if it is <= 0, the db time is not adequate for message ordering
        if "created_at" in dict_ and not (
            isinstance(dict_["created_at"], int) and dict_["created_at"] > 0
        ):
            del dict_["created_at"]

        result = await self.db.table(self.table_name).insert(dict_).execute()

        try:
            response = result.data
            if "user_id" in response[0]:
                del response[0]["user_id"]
            return self.model(**response[0])
        except Exception:
            return None

    async def get(self, filters: dict | None = None) -> ModelType | None:
        """Get row by filters."""
        query = self.db.table(self.table_name).select("*")

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        result = await query.execute()

        try:
            response = result.data
            if "user_id" in response[0]:
                del response[0]["user_id"]
            return self.model(**response[0])
        except Exception:
            return None

    async def list(self, filters: dict | None = None) -> list[ModelType] | None:
        """List all rows."""
        query = self.db.table(self.table_name).select("*")

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        result = await query.execute()

        try:
            response = result.data
            for item in response:
                if "user_id" in item:
                    del item["user_id"]
            return [self.model(**item) for item in response] or None
        except Exception:
            return None

    async def update(self, id_: str, object_: ModelType) -> ModelType | None:
        """Update a row by its ID."""

        dict_ = object_.model_dump()
        dict_["user_id"] = await self._get_user_id()

        result = (
            await self.db.table(self.table_name).update(dict_).eq("id", id_).execute()
        )

        try:
            response = result.data
            if "user_id" in response[0]:
                del response[0]["user_id"]
            return self.model(**response[0])
        except Exception:
            return None

    async def delete(self, filters: dict | None = None) -> bool:
        """Delete a row by filters."""
        query = self.db.table(self.table_name).delete()

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        result = await query.execute()

        try:
            return True if result.data else False
        except Exception:
            return False

    async def _get_user_id(self) -> str:
        """Get the user_id from the API key."""

        if self.db.options.headers.get("x-custom-api-key"):
            data, _count = await self.db.table("api_keys").select("user_id").execute()
            _, tmp = data
            user_id: str = tmp[0]["user_id"]
        else:
            user_id = (await self.db.auth.get_user()).user.id

        return user_id

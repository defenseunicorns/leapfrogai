"""CRUD Operations for Thread."""

from pydantic import Field
from openai.types.beta import Thread
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class AuthThread(Thread):
    """A wrapper for the thread that includes a user_id for auth"""

    user_id: str = Field(default="")


class CRUDThread(CRUDBase[AuthThread]):
    """CRUD Operations for thread"""

    def __init__(self, db: AsyncClient):
        super().__init__(db=db, model=AuthThread, table_name="thread_objects")

    async def create(self, object_: Thread) -> Thread | None:
        """Create new thread."""
        user_id: str = (await self.db.auth.get_user()).user.id
        return await super().create(
            object_=AuthThread(user_id=user_id, **object_.model_dump())
        )

    async def get(self, filters: dict | None = None) -> Thread | None:
        """Get a vector store by its ID."""

        return await super().get(filters=filters)

    async def list(self, filters: dict | None = None) -> list[Thread] | None:
        """List all threads."""

        return await super().list(filters=filters)

    async def update(self, id_: str, object_: Thread) -> Thread | None:
        """Update a thread by its ID."""
        return await super().update(id_=id_, object_=object_)

    async def delete(self, filters: dict | None = None) -> bool:
        """Delete a thread by its ID."""
        return await super().delete(filters=filters)

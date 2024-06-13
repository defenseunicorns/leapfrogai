"""CRUD Operations for Run."""

from pydantic import Field
from openai.types.beta.threads import Run
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class AuthRun(Run):
    """A wrapper for the run that includes a user_id for auth"""

    user_id: str = Field(default="")


class CRUDRun(CRUDBase[AuthRun]):
    """CRUD Operations for run"""

    def __init__(self, db: AsyncClient):
        super().__init__(db=db, model=AuthRun, table_name="run_objects")

    async def create(self, object_: Run) -> Run | None:
        """Create new run."""
        user_id: str = (await self.db.auth.get_user()).user.id
        return await super().create(
            object_=AuthRun(user_id=user_id, **object_.model_dump())
        )

    async def get(self, filters: dict | None = None) -> Run | None:
        """Get a vector store by its ID."""

        return await super().get(filters)

    async def list(self, filters: dict | None = None) -> list[Run] | None:
        """List all runs."""
        return await super().list(filters=filters)

    async def update(self, id_: str, object_: Run) -> Run | None:
        """Update a run by its ID."""

        dict_ = object_.model_dump()

        data, _count = (
            await self.db.table(self.table_name).update(dict_).eq("id", id_).execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, filters: dict | None = None) -> bool:
        """Delete a run by its ID."""
        return await super().delete(filters=filters)

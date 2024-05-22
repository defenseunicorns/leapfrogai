"""CRUD Operations for Assistant."""

from pydantic import Field
from openai.types.beta import Assistant
from supabase_py_async import AsyncClient

from leapfrogai_api.data.async_mixin import AsyncMixin
from leapfrogai_api.data.crud_base import CRUDBase
from leapfrogai_api.routers.supabase_session import get_user_session


class AuthAssistant(Assistant):
    """A wrapper for the Assistant that includes a user_id for auth"""

    user_id: str = Field(default="")


class CRUDAssistant(CRUDBase[AuthAssistant], AsyncMixin):
    """CRUD Operations for Assistant"""

    async def __ainit__(self, jwt: str, table_name: str = "assistant_objects"):
        db: AsyncClient = await get_user_session(jwt)
        super(CRUDAssistant, self).__init__(
            jwt=jwt, db=db, model=AuthAssistant, table_name=table_name
        )

    async def create(self, object_: Assistant) -> Assistant | None:
        """Create a new assistant."""
        user_id: str = (await self.db.auth.get_user(self.jwt)).user.id
        return await super().create(
            object_=AuthAssistant(user_id=user_id, **object_.dict())
        )

    async def get(self, id_: str) -> AuthAssistant | None:
        """Get an assistant by its ID."""
        return await super().get(id_=id_)

    async def list(self) -> list[AuthAssistant] | None:
        """List all assistants."""
        return await super().list()

    async def update(self, id_: str, object_: Assistant) -> AuthAssistant | None:
        """Update an assistant by its ID."""
        user_id: str = (await self.db.auth.get_user(self.jwt)).user.id
        return await super().update(
            id_=id_, object_=AuthAssistant(user_id=user_id, **object_.dict())
        )

    async def delete(self, id_: str) -> bool:
        """Delete an assistant by its ID."""
        return await super().delete(id_=id_)

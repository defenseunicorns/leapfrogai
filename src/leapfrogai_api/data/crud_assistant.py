"""CRUD Operations for Assistant."""

from pydantic import BaseModel, Field
from openai.types.beta import Assistant
from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class AuthAssistant(Assistant):
    """A wrapper for the Assistant that includes a user_id for auth"""

    user_id: str = Field(default="")


class FilterAssistant(BaseModel):
    """Validation for Assistant filter."""

    id: str


class CRUDAssistant(CRUDBase[AuthAssistant]):
    """CRUD Operations for Assistant"""

    def __init__(
        self,
        db: AsyncClient,
        table_name: str = "assistant_objects",
    ):
        super().__init__(db=db, model=AuthAssistant, table_name=table_name)

    async def create(self, object_: Assistant) -> Assistant | None:
        """Create a new assistant."""
        if self.db.options.headers.get("x-custom-api-key"):
            data, _count = await self.db.table("api_keys").select("user_id").execute()
            _, tmp = data
            user_id: str = tmp[0]["user_id"]
            print(user_id)
        else:
            user_id: str = (await self.db.auth.get_user()).user.id

        return await super().create(
            object_=AuthAssistant(user_id=user_id, **object_.model_dump())
        )

    async def get(self, filters: FilterAssistant | None = None) -> Assistant | None:
        """Get assistant by filters."""
        return await super().get(filters=filters.model_dump() if filters else None)

    async def list(
        self, filters: FilterAssistant | None = None
    ) -> list[Assistant] | None:
        """List all assistants."""
        return await super().list(filters=filters.model_dump() if filters else None)

    async def update(self, id_: str, object_: Assistant) -> Assistant | None:
        """Update an assistant by its ID."""
        user_id: str = (await self.db.auth.get_user()).user.id
        return await super().update(
            id_=id_, object_=AuthAssistant(user_id=user_id, **object_.model_dump())
        )

    async def delete(self, filters: FilterAssistant | None = None) -> bool:
        """Delete an assistant by its ID."""
        return await super().delete(filters=filters.model_dump() if filters else None)

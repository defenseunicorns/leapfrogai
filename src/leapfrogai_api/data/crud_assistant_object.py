"""CRUD Operations for Assistant."""

from pydantic import Field

from openai.types.beta import Assistant
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class AuthAssistant(Assistant):
    user_id: str = Field(default="")


class CRUDAssistant(CRUDBase[AuthAssistant]):
    """CRUD Operations for Assistant"""

    def __init__(self, table_name: str = "assistant_objects"):
        super().__init__(model=AuthAssistant, table_name=table_name)

    async def create(self, db: AsyncClient, object_: Assistant) -> Assistant | None:
        """Create a new assistant."""
        auth_assistant: AuthAssistant = AuthAssistant(
            user_id=db.auth.get_user().user.id, **object_.dict()
        )
        print("********* userid" + db.auth.get_user().user.id)
        return await super().create(db=db, object_=auth_assistant)

    async def get(self, id_: str, db: AsyncClient) -> AuthAssistant | None:
        """Get an assistant by its ID."""
        return await super().get(db=db, id_=id_)

    async def list(self, db: AsyncClient) -> list[AuthAssistant] | None:
        """List all assistants."""
        return await super().list(db=db)

    async def update(
        self, id_: str, db: AsyncClient, object_: Assistant
    ) -> AuthAssistant | None:
        """Update an assistant by its ID."""
        auth_assistant: AuthAssistant = AuthAssistant(
            user_id=db.auth.get_user().user.id, **object_.dict()
        )
        return await super().update(id_=id_, db=db, object_=auth_assistant)

    async def delete(self, id_: str, db: AsyncClient) -> bool:
        """Delete an assistant by its ID."""
        return await super().delete(id_=id_, db=db)

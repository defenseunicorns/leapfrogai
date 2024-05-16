"""CRUD Operations for Assistant."""

from openai.types.beta import Assistant
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class CRUDAssistant(CRUDBase[Assistant]):
    """CRUD Operations for Assistant"""

    def __init__(self, model: type[Assistant], table_name: str = "assistant_objects"):
        super().__init__(model=model, table_name=table_name)

    async def create(self, db: AsyncClient, object_: Assistant) -> Assistant | None:
        """Create a new assistant."""
        return await super().create(db=db, object_=object_)

    async def get(self, id_: str, db: AsyncClient) -> Assistant | None:
        """Get an assistant by its ID."""
        return await super().get(db=db, id_=id_)

    async def list(self, db: AsyncClient) -> list[Assistant] | None:
        """List all assistants."""
        return await super().list(db=db)

    async def update(
        self, id_: str, db: AsyncClient, object_: Assistant
    ) -> Assistant | None:
        """Update an assistant by its ID."""
        return await super().update(id_=id_, db=db, object_=object_)

    async def delete(self, id_: str, db: AsyncClient) -> bool:
        """Delete an assistant by its ID."""
        return await super().delete(id_=id_, db=db)

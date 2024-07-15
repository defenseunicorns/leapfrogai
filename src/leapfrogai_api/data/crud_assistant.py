"""CRUD Operations for Assistant."""

from pydantic import BaseModel
from openai.types.beta import Assistant
from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class FilterAssistant(BaseModel):
    """Validation for Assistant filter."""

    id: str


class CRUDAssistant(CRUDBase[Assistant]):
    """CRUD Operations for Assistant"""

    def __init__(
        self,
        db: AsyncClient,
        table_name: str = "assistant_objects",
    ):
        super().__init__(db=db, model=Assistant, table_name=table_name)

    async def get(self, filters: FilterAssistant | None = None) -> Assistant | None:
        """Get assistant by filters."""
        return await super().get(filters=filters.model_dump() if filters else None)

    async def list(
        self, filters: FilterAssistant | None = None
    ) -> list[Assistant] | None:
        """List all assistants."""
        return await super().list(filters=filters.model_dump() if filters else None)

    async def delete(self, filters: FilterAssistant | None = None) -> bool:
        """Delete an assistant by its ID."""
        return await super().delete(filters=filters.model_dump() if filters else None)

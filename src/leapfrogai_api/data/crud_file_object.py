"""CRUD Operations for FileObject"""

from pydantic import BaseModel
from openai.types import FileObject
from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class FilterFileObject(BaseModel):
    """Validation for FileObject filter."""

    id: str


class CRUDFileObject(CRUDBase[FileObject]):
    """CRUD Operations for FileObject"""

    def __init__(self, db: AsyncClient, table_name: str = "file_objects"):
        super().__init__(db=db, model=FileObject, table_name=table_name)

    async def get(self, filters: FilterFileObject | None = None) -> FileObject | None:
        """Get file object by filters."""
        return await super().get(filters=filters.model_dump() if filters else None)

    async def list(
        self, filters: FilterFileObject | None = None
    ) -> list[FileObject] | None:
        """List all file objects."""
        return await super().list(filters=filters.model_dump() if filters else None)

    async def delete(self, filters: FilterFileObject | None = None) -> bool:
        """Delete a file object by its ID."""
        return await super().delete(filters=filters.model_dump() if filters else None)

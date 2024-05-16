"""CRUD Operations for FileObject"""

from openai.types import FileObject
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class CRUDFileObject(CRUDBase[FileObject]):
    """CRUD Operations for FileObject"""

    def __init__(self, model: type[FileObject], table_name: str = "file_objects"):
        super().__init__(model=model, table_name=table_name)

    async def create(self, db: AsyncClient, object_: FileObject) -> FileObject | None:
        """Create a new file object."""
        return await super().create(db=db, object_=object_)

    async def get(self, id_: str, db: AsyncClient) -> FileObject | None:
        """Get a file object by its ID."""
        return await super().get(db=db, id_=id_)

    async def list(self, db: AsyncClient) -> list[FileObject] | None:
        """List all file objects."""
        return await super().list(db=db)

    async def update(
        self, id_: str, db: AsyncClient, object_: FileObject
    ) -> FileObject | None:
        """Update a file object by its ID."""
        return await super().update(id_=id_, db=db, object_=object_)

    async def delete(self, id_: str, db: AsyncClient) -> bool:
        """Delete a file object by its ID."""
        return await super().delete(id_=id_, db=db)

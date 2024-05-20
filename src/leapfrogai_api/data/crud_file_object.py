"""CRUD Operations for FileObject"""

from pydantic import Field

from openai.types import FileObject
from supabase_py_async import AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class AuthFileObject(FileObject):
    user_id: str = Field(default="")


class CRUDFileObject(CRUDBase[AuthFileObject]):
    """CRUD Operations for FileObject"""

    def __init__(self, table_name: str = "file_objects"):
        super().__init__(model=AuthFileObject, table_name=table_name)

    async def create(
        self, db: AsyncClient, object_: FileObject
    ) -> AuthFileObject | None:
        """Create a new file object."""
        auth_file_object: AuthFileObject = AuthFileObject(
            user_id=db.auth.get_user().user.id, **object_.dict()
        )
        return await super().create(db=db, object_=auth_file_object)

    async def get(self, id_: str, db: AsyncClient) -> AuthFileObject | None:
        """Get a file object by its ID."""
        return await super().get(db=db, id_=id_)

    async def list(self, db: AsyncClient) -> list[AuthFileObject] | None:
        """List all file objects."""
        return await super().list(db=db)

    async def update(
        self, id_: str, db: AsyncClient, object_: FileObject
    ) -> AuthFileObject | None:
        """Update a file object by its ID."""
        auth_file_object: AuthFileObject = AuthFileObject(
            user_id=db.auth.get_user().user.id, **object_.dict()
        )
        return await super().update(id_=id_, db=db, object_=auth_file_object)

    async def delete(self, id_: str, db: AsyncClient) -> bool:
        """Delete a file object by its ID."""
        return await super().delete(id_=id_, db=db)

"""CRUD Operations for Thread."""

from openai.types.beta import Thread
from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class CRUDThread(CRUDBase[Thread]):
    """CRUD Operations for thread"""

    def __init__(self, db: AsyncClient):
        super().__init__(db=db, model=Thread, table_name="thread_objects")

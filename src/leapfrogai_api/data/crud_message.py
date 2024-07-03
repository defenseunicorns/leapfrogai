"""CRUD Operations for Message."""

from openai.types.beta.threads import Message
from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import CRUDBase


class CRUDMessage(CRUDBase[Message]):
    """CRUD Operations for message"""

    def __init__(self, db: AsyncClient):
        super().__init__(db=db, model=Message, table_name="message_objects")

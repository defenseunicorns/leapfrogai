"""Supabase session dependency."""

import os
from typing import Annotated
from fastapi import Depends
from supabase_py_async import AsyncClient, create_client


async def init_supabase_client() -> AsyncClient:
    """Initialize a Supabase client."""
    return await create_client(
        supabase_key=os.getenv("SUPABASE_SERVICE_KEY"),
        supabase_url=os.getenv("SUPABASE_URL"),
    )


Session = Annotated[AsyncClient, Depends(init_supabase_client)]


def get_user(session: Session, authorization: str) -> Session:
    api_key: str = authorization.replace("Bearer ", "")
    return session.auth.get_user(jwt=api_key)

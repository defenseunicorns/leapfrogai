"""Supabase session dependency."""

import os
from typing import Annotated
from fastapi import Depends
from supabase_py_async import AsyncClient, create_client


async def init_supabase_client() -> AsyncClient:
    """Initialize a Supabase client."""
    return await create_client(
        supabase_key=os.getenv("SUPABASE_ANON_KEY"),
        supabase_url=os.getenv("SUPABASE_URL"),
    )


Session = Annotated[AsyncClient, Depends(init_supabase_client)]


async def get_user_session(session: Session, authorization: str) -> AsyncClient:
    if authorization is None:
        return session

    api_key: str = authorization.replace("Bearer ", "")
    return await create_client(
        supabase_key=os.getenv("SUPABASE_ANON_KEY"),
        supabase_url=os.getenv("SUPABASE_URL"),
        access_token=api_key
    )

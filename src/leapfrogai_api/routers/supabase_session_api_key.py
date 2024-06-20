"""Supabase session dependency."""

import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase_py_async import AsyncClient, ClientOptions, create_client

security = HTTPBearer()

# TODO: This is a work in progress file to figure out how to validate the API key via request header.


async def init_supabase_client(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> AsyncClient:
    """
    Returns an authenticated Supabase client using the provided user's JWT token

    Parameters:
        auth_creds (HTTPAuthorizationCredentials): the auth credentials for the user that include the bearer token

    Returns:
        user_client (AsyncClient): a client instantiated with a session associated with the JWT token
    """

    if not await validate_api_authorization(auth_creds.credentials):
        raise HTTPException(
            detail="Token has expired or is not valid. Generate a new token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    client: AsyncClient = await create_client(
        supabase_key=os.getenv("SUPABASE_ANON_KEY"),
        supabase_url=os.getenv("SUPABASE_URL"),
        options=ClientOptions(auto_refresh_token=False),
    )

    return client


# This variable needs to be added to each endpoint even if it's not used to ensure auth is required for the endpoint
Session = Annotated[AsyncClient, Depends(init_supabase_client)]


async def validate_api_authorization(api_key: str) -> bool:
    """
    Check if the provided API key is valid, raises a 403 if not

    Parameters:
        session (Session): the default anonymous session
        api_key (str): the API key for the user
    """

    authorized = True

    if api_key:
        session = await create_client(
            supabase_key=os.getenv("SUPABASE_ANON_KEY"),
            supabase_url=os.getenv("SUPABASE_URL"),
            options=ClientOptions(auto_refresh_token=False),
        )
        await session.rpc("set_config", {"key": "role", "value": "validator_role"})
        response = (
            await session.table("api_keys").select("*").eq("api_key", api_key).execute()
        )
        await session.rpc("reset_config", {"key": "role"})

        if not response.data:
            authorized = False

    return authorized

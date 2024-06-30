"""Supabase session dependency."""

import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import AClient as AsyncClient
from supabase import ClientOptions, acreate_client
from leapfrogai_api.backend.security.api_key import encode_unique_key, parse

security = HTTPBearer()

# TODO: This is a work in progress file to figure out how to validate the API key via request header.


def get_vars() -> tuple[str, str]:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise HTTPException(
            detail="Supabase URL or Supabase Anon Key is not set",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return supabase_url, supabase_key


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

    client: AsyncClient = await acreate_client(
        supabase_key=get_vars()[1],
        supabase_url=get_vars()[0],
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
    supabase_service_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_service_key:
        raise HTTPException(
            detail="Supabase Service Key is not set",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if api_key:
        _, key, _ = parse(api_key)

        api_key = encode_unique_key(key)

        headers = {"x-custom-api-key": api_key}

        session = await acreate_client(
            supabase_key=supabase_service_key,
            supabase_url=get_vars()[0],
            options=ClientOptions(auto_refresh_token=False, headers=headers),
        )

        response = await session.table("api_keys").select("*").execute()

        if not response.data[0]["api_key"] == api_key:
            authorized = False

    return authorized

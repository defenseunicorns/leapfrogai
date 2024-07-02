"""Supabase session dependency."""

import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import AClient as AsyncClient
from supabase import acreate_client
from supabase.client import ClientOptions
from leapfrogai_api.backend.security.api_key import (
    encode_unique_key,
    parse_api_key,
    validate_api_key,
)

security = HTTPBearer()

# TODO: This is a work in progress file to figure out how to validate the API key via request header.


def get_supabase_vars() -> tuple[str, str]:
    """Gets the Supabase URL and Supabase Anon Key from the environment variables

    Returns:
        tuple[str, str]: the Supabase URL and Supabase Anon Key
    """

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise HTTPException(
            detail="Supabase URL or Supabase Anon Key is not set",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return supabase_url, supabase_key


def validate_jtw_token(token: str) -> bool:
    """Validates the JWT token

    Parameters:
        token (str): the JWT token

    Returns:
        bool: True if the token is valid, False otherwise
    """

    try:
        _header, _payload, _signature = token.split(".")
        return True
    except ValueError:
        return False


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

    supabase_url, supabase_key = get_supabase_vars()

    if validate_api_key(auth_creds.credentials):
        _, key, _ = parse_api_key(auth_creds.credentials)

        api_key = encode_unique_key(key)

        if not await validate_api_authorization(api_key):
            raise HTTPException(
                detail="Token has expired or is not valid. Generate a new token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        client: AsyncClient = await acreate_client(
            supabase_url=supabase_url,
            supabase_key=supabase_key,
            options=ClientOptions(
                auto_refresh_token=False, headers={"x-custom-api-key": api_key}
            ),
        )

        return client

    if validate_jtw_token(auth_creds.credentials):
        client = await acreate_client(
            supabase_key=supabase_key,
            supabase_url=supabase_url,
        )

        await client.auth.set_session(
            access_token=auth_creds.credentials, refresh_token="dummy"
        )

        return client

    raise HTTPException(
        detail="Invalid credentials provided",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


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
        headers = {"x-custom-api-key": api_key}

        session = await acreate_client(
            supabase_key=supabase_service_key,
            supabase_url=get_supabase_vars()[0],
            options=ClientOptions(auto_refresh_token=False, headers=headers),
        )

        response = await session.table("api_keys").select("*").execute()

        if not response or not response.data:
            return False
        if not response.data[0]["api_key"] == api_key:
            authorized = False

    return authorized

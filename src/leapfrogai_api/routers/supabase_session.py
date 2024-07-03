"""Supabase session dependency."""

import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import HTTPStatusError
from supabase import AClient as AsyncClient
from supabase import acreate_client
import gotrue
from leapfrogai_api.backend.security.api_key import validate_and_encode_api_key

security = HTTPBearer()


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

    client: AsyncClient = await acreate_client(
        supabase_key=supabase_key,
        supabase_url=supabase_url,
    )

    # Try API Key Auth first
    valid, api_key = validate_and_encode_api_key(auth_creds.credentials)

    if valid and api_key:
        client.options.headers = {"x-custom-api-key": api_key}
        client.options.auto_refresh_token = False

        if not await _validate_api_authorization(client):
            raise HTTPException(
                detail="API Key has expired or is not valid. Generate a new token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return client

    # If API Key Auth fails, try JWT Auth
    if _validate_jwt_token(auth_creds.credentials):
        await client.auth.set_session(
            access_token=auth_creds.credentials, refresh_token="dummy"
        )

        return client

    # If both API Key and JWT Auth fail, raise an error
    raise HTTPException(
        detail="Invalid credentials provided",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


# This variable needs to be added to each endpoint even if it's not used to ensure auth is required for the endpoint
Session = Annotated[AsyncClient, Depends(init_supabase_client)]


async def _validate_api_authorization(session: AsyncClient) -> bool:
    """
    Check if the provided API key is valid

    Parameters:
        session (Session): an anonymous session with x-custom-api-key header

    Returns:
        bool: True if the API key is valid, False otherwise
    """

    response = await session.table("api_keys").select("*").execute()

    if not response or not response.data:
        return False

    return True


async def _validate_jwt_authorization(session, authorization: str) -> bool:
    """
    Check if the provided user's JWT token is valid, raises a 403 if not

    Parameters:
        session (Session): the default anonymous session
        authorization (str): the JWT token for the user
    """

    authorized = True

    if authorization:
        api_key: str = authorization.replace("Bearer ", "")

        try:
            user_response: gotrue.types.UserResponse = await session.auth.get_user(
                api_key
            )

            if user_response is None:
                authorized = False
        except HTTPStatusError:
            authorized = False
        except gotrue.errors.AuthApiError:
            authorized = False
    else:
        authorized = False

    return authorized


def _validate_jwt_token(token: str) -> bool:
    """
    Check if the provided JWT token is valid

    Parameters:
        token (str): the JWT token

    Returns:
        bool: True if the token is valid, False otherwise
    """

    try:
        _header, _payload, _signature = token.split(".")
        if not _header or not _payload or not _signature:
            return False
        return True
    except ValueError:
        return False

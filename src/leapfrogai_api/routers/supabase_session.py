"""Supabase session dependency."""

from base64 import binascii
import logging
import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import HTTPStatusError
from supabase import AClient as AsyncClient
from supabase import acreate_client
import gotrue
from leapfrogai_api.backend.security.api_key import APIKey

from leapfrogai_api.data.crud_api_key import CRUDAPIKey, APIKeyItem
import time

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
    use_jwt_directly: bool = False,
) -> AsyncClient:
    """
    Returns an authenticated Supabase client using the provided user's JWT token or API key

    Parameters:
        auth_creds (HTTPAuthorizationCredentials): the auth credentials for the user that include the bearer token or API key

    Returns:
        user_client (AsyncClient): a client instantiated with a session associated with the JWT token or API key
    """

    supabase_url, supabase_key = get_supabase_vars()
    client: AsyncClient = await acreate_client(
        supabase_key=supabase_key, supabase_url=supabase_url
    )

    try:
        if _validate_jwt_token(auth_creds.credentials):
            if use_jwt_directly:
                await client.auth.set_session(
                    access_token=auth_creds.credentials, refresh_token="dummy"
                )
            else:
                await _handle_jwt_auth(client, auth_creds.credentials)
        else:
            await _handle_api_key_auth(client, auth_creds.credentials)
        return client
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("\t%s", e)
        raise HTTPException(
            detail="Failed to create Supabase session",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


async def _handle_jwt_auth(client: AsyncClient, token: str) -> None:
    try:
        await client.auth.set_session(access_token=token, refresh_token="dummy")
        if await _validate_jwt_authorization(client, token):
            new_api_key_item = await _create_new_api_key(client)
            client.options.auto_refresh_token = False
            client.options.headers.update(
                {"x-custom-api-key": new_api_key_item.api_key}
            )
    except gotrue.errors.AuthApiError as e:
        raise HTTPException(
            detail="Token has expired or is not valid. Generate a new token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        ) from e
    except binascii.Error as e:
        raise HTTPException(
            detail="Failed to validate Authentication Token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        ) from e


async def _handle_api_key_auth(client: AsyncClient, api_key_str: str) -> None:
    try:
        api_key = APIKey.parse(api_key_str)
        client.options.auto_refresh_token = False
        client.options.headers.update({"x-custom-api-key": api_key.unique_key})
        if not await _validate_api_authorization(client):
            raise HTTPException(
                detail="API Key has expired or is not valid. Generate a new token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    except ValueError as e:
        raise HTTPException(
            detail="Failed to validate API Key",
            status_code=status.HTTP_401_UNAUTHORIZED,
        ) from e


async def _create_new_api_key(client: AsyncClient) -> APIKeyItem:
    """
    Generate a short-lived API key that expires in 10 minutes.
    This is used for temporary authentication after JWT validation.
    """
    crud_api_key = CRUDAPIKey(client)
    return await crud_api_key.create(
        APIKeyItem(
            name="Generated Short-Lived API Key",
            id="",
            api_key="",
            created_at=0,
            expires_at=int(time.time()) + 10 * 60,  # 10 minutes from now
        )
    )


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


async def _validate_jwt_authorization(session: AsyncClient, authorization: str) -> bool:
    """
    Check if the provided user's JWT token is valid, raises a 403 if not

    Parameters:
        session (Session): the default anonymous session
        authorization (str): the JWT token for the user
    """

    authorized: bool = False

    if authorization:
        try:
            user_response: gotrue.types.UserResponse = await session.auth.get_user(
                authorization.replace("Bearer ", "")
            )

            if user_response:
                authorized = True

        except HTTPStatusError:
            authorized = False
        except gotrue.errors.AuthApiError:
            authorized = False

    if not authorized:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

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


# This variable needs to be added to each endpoint even if it's not used to ensure auth is required for the endpoint
Session = Annotated[AsyncClient, Depends(init_supabase_client)]

"""Supabase session dependency."""

import logging
import os
from base64 import binascii
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from gotrue import errors, types
from httpx import HTTPStatusError
from supabase_py_async import AsyncClient, ClientOptions, create_client

security = HTTPBearer()


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

    client: AsyncClient = await create_client(
        supabase_key=os.getenv("SUPABASE_ANON_KEY"),
        supabase_url=os.getenv("SUPABASE_URL"),
        access_token=auth_creds.credentials,
        options=ClientOptions(auto_refresh_token=False),
    )

    try:
        # Set up a session for this client, a dummy refresh_token is used to prevent validation errors
        await client.auth.set_session(
            access_token=auth_creds.credentials, refresh_token="dummy"
        )
    except errors.AuthApiError as e:
        logging.exception("\t%s", e)
        raise HTTPException(
            detail="Token has expired or is not valid. Generate a new token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        ) from e
    except binascii.Error as e:
        logging.exception("\t%s", e)
        raise HTTPException(
            detail="Failed to validate Authentication Token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        ) from e
    except Exception as e:
        logging.exception("\t%s", e)
        raise HTTPException(
            detail="Failed to create Supabase session",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e

    await validate_user_authorization(
        session=client, authorization=auth_creds.credentials
    )

    return client


# This variable needs to be added to each endpoint even if it's not used to ensure auth is required for the endpoint
Session = Annotated[AsyncClient, Depends(init_supabase_client)]


async def validate_user_authorization(session: Session, authorization: str):
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
            user_response: types.UserResponse = await session.auth.get_user(api_key)

            if user_response is None:
                authorized = False
        except HTTPStatusError:
            authorized = False
        except errors.AuthApiError:
            authorized = False
    else:
        authorized = False

    if not authorized:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

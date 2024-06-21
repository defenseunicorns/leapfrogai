"""Supabase session dependency."""

import logging
import os
from base64 import binascii
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from gotrue import errors, types
from httpx import HTTPStatusError
from supabase import acreate_client, AClient


security = HTTPBearer()


async def init_supabase_client(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """
    Returns an authenticated Supabase client using the provided user's JWT token

    Parameters:
        auth_creds (HTTPAuthorizationCredentials): the auth credentials for the user that include the bearer token

    Returns:
        user_client (AsyncClient): a client instantiated with a session associated with the JWT token
    """

    # TODO: auth_creds is expecting to be decoded as jwt token, but our API key is not a jwt token

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise HTTPException(
            detail="Supabase URL or Supabase Anon Key is not set",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    client: AClient = await acreate_client(
        supabase_url=supabase_url, supabase_key=supabase_key
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
Session = Annotated[AClient, Depends(init_supabase_client)]


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
        # TODO: Once we sort out the API key, we can use the following code to check if the user is authorized
        # await session.rpc('set_config', {'key': 'role', 'value': 'validator_role'})
        # response = await session.table('api_keys').select('*').eq('api_key', api_key).execute()
        # await session.rpc('reset_config', {'key': 'role'})

        # if response.data:
        #     authorized = True

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

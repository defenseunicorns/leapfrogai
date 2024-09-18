import json
import logging
import os
import traceback
import pytest
import requests

# This is the anon_key for supabase, it provides access to the endpoints that would otherwise be inaccessible
ANON_KEY = os.environ["ANON_KEY"]
SERVICE_KEY = os.environ["SERVICE_KEY"]
DEFAULT_TEST_EMAIL = "fakeuser1@test.com"
DEFAULT_TEST_PASSWORD = "password"


def create_test_user(
    anon_key: str = ANON_KEY,
    email: str = DEFAULT_TEST_EMAIL,
    password: str = DEFAULT_TEST_PASSWORD,
) -> str:
    headers = {
        "apikey": f"{anon_key}",
        "Authorization": f"Bearer {anon_key}",
        "Content-Type": "application/json",
    }

    try:
        requests.post(
            url="https://supabase-kong.uds.dev/auth/v1/signup",
            headers=headers,
            json={
                "email": email,
                "password": password,
                "confirmPassword": password,
            },
        )
    except Exception:
        logging.error(
            "Error creating user (likely because the user already exists): %s",
            traceback.format_exc(),
        )

    return get_jwt_token(anon_key, email, password)


def get_jwt_token(
    api_key: str,
    test_email: str = DEFAULT_TEST_EMAIL,
    test_password: str = DEFAULT_TEST_PASSWORD,
) -> str:
    url = "https://supabase-kong.uds.dev/auth/v1/token?grant_type=password"
    headers = {"apikey": f"{api_key}", "Content-Type": "application/json"}
    data = {"email": test_email, "password": test_password}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        pytest.fail(
            f"Request for the JWT token failed with status code {response.status_code} expected 200",
            False,
        )

    return json.loads(response.content)["access_token"]

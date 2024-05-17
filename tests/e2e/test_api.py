import logging
import uuid
import random

import pytest as pytest
import requests
import os
import json

logger = logging.getLogger(__name__)
test_id = str(uuid.uuid4())

get_urls = {
    "assistants_url": "http://leapfrogai-api.uds.dev/openai/v1/assistants",
    "assistants_id_url": f"http://leapfrogai-api.uds.dev/openai/v1/assistants/{test_id}",
    "files_url": "http://leapfrogai-api.uds.dev/openai/v1/files",
    "files_specific_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_id}",
    "files_specific_content_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_id}/content",
}

post_urls = {
    "assistants_url": "http://leapfrogai-api.uds.dev/openai/v1/assistants",
    "assistants_id_url": f"http://leapfrogai-api.uds.dev/openai/v1/assistants/{test_id}",
    "files_url": "http://leapfrogai-api.uds.dev/openai/v1/files",
}

delete_urls = {
    "assistants_id_url": f"http://leapfrogai-api.uds.dev/openai/v1/assistants/{test_id}",
    "files_specific_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_id}",
}

# This is the anon_key for supabase, it provides access to the endpoints that would otherwise be inaccessible
anon_key = os.environ["ANON_KEY"]


def get_jwt_token(api_key: str):
    url = "https://supabase-kong.uds.dev/auth/v1/token?grant_type=password"
    headers = {
        "apikey": f"{api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "email": "tester@test.com",
        "password": "password"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        pytest.fail(f"Request for the JWT token failed with status code {response.status_code} expected 200", False)

    return json.loads(response.content)["access_token"]


def verify_request(urls: dict[str, str], request_type: str, jwt_token: str, legitimate: True):
    fake_jwt_token: str = jwt_token[-8] + "fakefake"

    headers = {"Authorization": f"Bearer {jwt_token}"} if legitimate else {
        "Authorization": f"Bearer {fake_jwt_token}"
    }

    # Verify that legitimate requests are not forbidden
    for url in urls:
        response: requests.Response | None = None

        try:
            if request_type == "get":
                response = requests.get(
                    urls[url], headers=headers
                )
            elif request_type == "post":
                response = requests.post(
                    urls[url], headers=headers
                )
            elif request_type == "delete":
                response = requests.delete(
                    urls[url], headers=headers
                )

            if legitimate and response.status_code == 403:
                response.raise_for_status()

            if not legitimate and response.status_code != 403:
                raise Exception("An illegitimate request has been allowed")

        except requests.exceptions.RequestException:
            pytest.fail(f"Request failed with status code {response.status_code}", True)


def test_api_row_level_security():
    jwt_token = get_jwt_token(anon_key)

    # Confirm that legitimate requests are allowed
    verify_request(get_urls, "get", jwt_token, True)
    verify_request(post_urls, "post", jwt_token, True)
    verify_request(delete_urls, "delete", jwt_token, True)

    # Confirm that illegitimate requests are not
    verify_request(get_urls, "get", jwt_token, False)
    verify_request(post_urls, "post", jwt_token, False)
    verify_request(delete_urls, "delete", jwt_token, False)

import logging
import uuid

import pytest as pytest
import requests
import os
import json

logger = logging.getLogger(__name__)
test_file_id = str(uuid.uuid4())

get_urls = {
    "assistants_url": "http://leapfrogai-api.uds.dev/openai/v1/assistants",
    "files_url": "http://leapfrogai-api.uds.dev/openai/v1/files",
    "files_specific_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_file_id}",
    "files_specific_content_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_file_id}/content",
}

post_urls = {
    "assistants_url": "http://leapfrogai-api.uds.dev/openai/v1/assistants",
    "files_url": "http://leapfrogai-api.uds.dev/openai/v1/files",
    "files_specific_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_file_id}",
    "files_specific_content_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_file_id}/content",
}

delete_urls = {
    "assistants_url": "http://leapfrogai-api.uds.dev/openai/v1/assistants",
    "files_url": "http://leapfrogai-api.uds.dev/openai/v1/files",
    "files_specific_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_file_id}",
    "files_specific_content_url": f"http://leapfrogai-api.uds.dev/openai/v1/files/{test_file_id}/content",
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


def test_api():
    jwt_token = get_jwt_token(anon_key)

    try:
        for url_name in get_urls:
            response = requests.get(
                get_urls[url_name], headers={"Authorization": "Bearer " + jwt_token}
            )
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed with status code {response.status_code}", True)

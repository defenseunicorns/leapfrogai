import io
import logging
import uuid

import pytest as pytest
import requests

from tests.utils.client import create_test_user

logger = logging.getLogger(__name__)
test_id = str(uuid.uuid4())

get_urls = {
    "assistants_url": "https://leapfrogai-api.uds.dev/openai/v1/assistants",
    "assistants_id_url": f"https://leapfrogai-api.uds.dev/openai/v1/assistants/{test_id}",
    "files_url": "https://leapfrogai-api.uds.dev/openai/v1/files",
    "files_specific_url": f"https://leapfrogai-api.uds.dev/openai/v1/files/{test_id}",
    "files_specific_content_url": f"https://leapfrogai-api.uds.dev/openai/v1/files/{test_id}/content",
}

post_urls = {
    "assistants_url": "https://leapfrogai-api.uds.dev/openai/v1/assistants",
    "assistants_id_url": f"https://leapfrogai-api.uds.dev/openai/v1/assistants/{test_id}",
    "files_url": "https://leapfrogai-api.uds.dev/openai/v1/files",
}

delete_urls = {
    "assistants_id_url": f"https://leapfrogai-api.uds.dev/openai/v1/assistants/{test_id}",
    "files_specific_url": f"https://leapfrogai-api.uds.dev/openai/v1/files/{test_id}",
}


# We need a jwt token that is properly decodeable but invalid in regards to not being a token for a valid user
invalid_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

mock_assistant_body = {
    "name": "Test Assistant",
    "description": "A test assistant",
    "instructions": "Follow my instructions carefully.",
    "model": "test-model",
    "tools": [{"type": "file_search"}],
    "tool_resources": None,
    "temperature": 0.7,
    "top_p": 1.0,
    "metadata": {},
    "response_format": "auto",
}


def verify_request(
    urls: dict[str, str], request_type: str, jwt_token: str, legitimate: bool
):
    headers = (
        {"Authorization": f"Bearer {jwt_token}"}
        if legitimate
        else {"Authorization": f"Bearer {invalid_jwt_token}"}
    )

    # Verify that legitimate requests are not forbidden
    for url in urls:
        response: requests.Response | None = None

        try:
            if request_type == "get":
                response = requests.get(urls[url], headers=headers)
            elif request_type == "post":
                if url == "assistants_url":
                    response = requests.post(
                        urls[url],
                        headers=headers,
                        json={"request": mock_assistant_body},
                    )
                elif url == "files_url":
                    f = io.StringIO("test text data")
                    files = {"file": ("test.txt", f, "text/plain")}
                    response = requests.post(urls[url], headers=headers, files=files)
                elif url == "assistants_id_url":
                    response = requests.post(
                        urls[url], headers=headers, json=mock_assistant_body
                    )
            elif request_type == "delete":
                response = requests.delete(urls[url], headers=headers)

            # 'legitimate' requests should never return a 401 or a 403
            if legitimate and (
                response.status_code == 401 or response.status_code == 403
            ):
                response.raise_for_status()

            # 'illegitimate' requests should always return a 401 or a 403
            if (
                not legitimate
                and response.status_code != 401
                and response.status_code != 403
            ):
                raise Exception("An illegitimate request has been allowed")

        except requests.exceptions.RequestException:
            pytest.fail(f"Request failed with status code {response.status_code}", True)


def test_api_row_level_security():
    jwt_token = create_test_user()

    # Confirm that legitimate requests are allowed
    verify_request(get_urls, "get", jwt_token, True)
    verify_request(post_urls, "post", jwt_token, True)
    verify_request(delete_urls, "delete", jwt_token, True)

    # Confirm that illegitimate requests are not allowed
    verify_request(get_urls, "get", jwt_token, False)
    verify_request(post_urls, "post", jwt_token, False)
    verify_request(delete_urls, "delete", jwt_token, False)

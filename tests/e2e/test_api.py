import requests
import os

health_urls = {
    "assistants_url": "http://leapfrogai-api.uds.dev/openai/v1/assistants",
}

# This is the JWT token for a test user, it provides access to the endpoints that would otherwise be inaccessible
jwt_token = os.environ["API_KEY"]


def test_studio():
    try:
        for url_name in health_urls:
            response = requests.get(
                health_urls[url_name], headers={"Authentication": "Bearer " + jwt_token}
            )
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed with status code {response.status_code}")
        print(e)
        exit(1)

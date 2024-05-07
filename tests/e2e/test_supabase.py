import requests
import os

health_urls = {
    "auth_health_url": "http://localhost:8000/auth/v1/health",
    "rest_health_url": "http://localhost:8000/rest/v1/",
    "storage_health_url": "http://localhost:8000/storage/v1/status"
}
anon_api_key = os.environ["API_KEY"]


def test_studio():
    try:
        for url_name in health_urls:
            response = requests.get(health_urls[url_name], headers={
                                    "apikey": anon_api_key})
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed with status code {response.status_code}")
        print(e)
        exit(1)

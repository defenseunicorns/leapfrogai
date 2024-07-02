import requests

from .utils import ANON_KEY

health_urls = {
    "auth_health_url": "http://supabase-kong.uds.dev/auth/v1/health",
    "rest_health_url": "http://supabase-kong.uds.dev/rest/v1/",
    "storage_health_url": "http://supabase-kong.uds.dev/storage/v1/status",
}


def test_studio():
    try:
        for url_name in health_urls:
            response = requests.get(health_urls[url_name], headers={"apikey": ANON_KEY})
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed with status code {response.status_code}")
        print(e)
        exit(1)

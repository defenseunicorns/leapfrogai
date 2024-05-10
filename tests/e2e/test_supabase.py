import requests
import os

health_urls = {
    "auth_health_url": "http://supabase-kong.uds.dev/auth/v1/health",
    "rest_health_url": "http://supabase-kong.uds.dev/rest/v1/",
    "storage_health_url": "http://supabase-kong.uds.dev/storage/v1/status",
}

# This is the Supabase anon key, it provides access to the health endpoints that would otherwise be inaccessible
anon_api_key = os.environ["API_KEY"]


def test_studio():
    try:
        for url_name in health_urls:
            response = requests.get(
                health_urls[url_name], headers={"apikey": anon_api_key}
            )
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed with status code {response.status_code}")
        print(e)
        exit(1)

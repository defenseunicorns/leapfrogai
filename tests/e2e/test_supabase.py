import requests
from realtime.connection import Socket

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


def test_supabase_realtime_vector_store_indexing():
    def callback1(payload):
        print("Callback 1: ", payload)

    URL = f"wss://supabase-kong.uds.dev/realtime/v1/?apikey={ANON_KEY}&vsn=1.0.0"
    s = Socket(URL)
    s.connect()

    channel_1 = s.set_channel("realtime:*")
    channel_1.join().on("UPDATE", callback1)
    s.listen()
import requests
from realtime.connection import Socket
from realtime.channel import Channel

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
    def postgres_changes_callback(payload):
        print("postgres_changes: ", payload)

    URL = f"https://supabase-kong.uds.dev/realtime/v1"
    JWT = ANON_KEY
    s = Socket(URL, JWT, auto_reconnect=True)
    s.connect()

    channel_1: Channel = Channel(s, "postgres-vector-store-indexing-test")
    channel_1.on_postgres_changes(
        table="vector_store_file",
        schema="public",
        event="*",
        callback=postgres_changes_callback,
    ).subscribe()
    s.listen()
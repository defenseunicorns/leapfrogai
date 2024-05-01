import requests

url = "https://supabase-kong.uds.dev/"
username = "supabase-admin"
password = "testing"


def test_studio():
    try:
        response = requests.get(url, auth=(username, password))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed with status code {response.status_code}")
        print(e)
        exit(1)

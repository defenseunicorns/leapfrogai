import os
from dotenv import load_dotenv


def pytest_configure(config):
    # runs once for all tests

    load_dotenv(".jwt")

    os.environ["SUPABASE_USER_JWT"] = os.environ.get("SUPABASE_USER_JWT", "mock-data")
    os.environ["SUPABASE_URL"] = os.environ.get("SUPABASE_URL", "mock-data")
    os.environ["ANON_KEY"] = os.environ.get("SUPABASE_ANON_KEY", "mock-data")
    os.environ["API_KEY"] = os.environ.get("SUPABASE_ANON_KEY", "mock-data")
    
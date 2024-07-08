# This file will be imported by all test files
import os
from dotenv import load_dotenv


def pytest_configure(config):
    # This will run once per test run
    # before tests are collected or executed

    load_dotenv()

    os.environ["SUPABASE_USER_JWT"] = os.environ.get("SUPABASE_USER_JWT", "mock-data")
    os.environ["SUPABASE_URL"] = os.environ.get("SUPABASE_URL", "mock-data")
    os.environ["ANON_KEY"] = os.environ.get("SUPABASE_ANON_KEY", "mock-data")
    os.environ["API_KEY"] = os.environ.get("SUPABASE_ANON_KEY", "mock-data")

import asyncio
import io
import threading
import uuid
from fastapi import UploadFile
import requests
from openai.types.beta.vector_stores import VectorStoreFile
from openai.types.beta import VectorStore
from openai.types.beta.vector_store import FileCounts
import _thread

from supabase import AClient as AsyncClient, acreate_client
from realtime import Socket
from leapfrogai_api.data.crud_file_bucket import CRUDFileBucket
from leapfrogai_api.data.crud_file_object import CRUDFileObject
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore

from leapfrogai_api.data.crud_vector_store_file import CRUDVectorStoreFile

from tests.client.utils import ANON_KEY, create_test_user, SERVICE_KEY
from openai.types import FileObject

health_urls = {
    "auth_health_url": "http://supabase-kong.uds.dev/auth/v1/health",
    "rest_health_url": "http://supabase-kong.uds.dev/rest/v1/",
    "storage_health_url": "http://supabase-kong.uds.dev/storage/v1/status",
}


def test_studio():
    try:
        for url_name in health_urls:
            resp = requests.get(health_urls[url_name], headers={"apikey": ANON_KEY})
            resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed with status code {resp.status_code}")
        print(e)
        exit(1)


def test_supabase_realtime_vector_store_indexing():
    class TestCompleteException(Exception):
        pass

    def timeout_handler():
        print("Test timed out after 10 seconds")
        # This is necessary to stop the thread from hanging forever
        _thread.interrupt_main()

    async def postgres_db_changes():
        """
        This function is responsible for creating a vector store and uploading a file to it.
        """
        client: AsyncClient = await acreate_client(
            supabase_key=ANON_KEY,
            supabase_url="https://supabase-kong.uds.dev",
        )
        await client.auth.set_session(access_token=access_token, refresh_token="dummy")

        upload_file_id = await upload_file(client)
        assert upload_file_id is not None, "Failed to upload file"

        vector_store = VectorStore(
            id="",
            created_at=0,
            file_counts=FileCounts(
                cancelled=0,
                completed=0,
                failed=0,
                in_progress=0,
                total=0,
            ),
            name="test_vector_store",
            object="vector_store",
            status="completed",
            usage_bytes=0,
        )

        new_vector_store = await CRUDVectorStore(client).create(vector_store)
        assert new_vector_store is not None, "Failed to create vector store"

        vector_store_file = VectorStoreFile(
            id=upload_file_id,
            vector_store_id=new_vector_store.id,
            created_at=0,
            object="vector_store.file",
            status="completed",
            usage_bytes=0,
        )

        await CRUDVectorStoreFile(client).create(vector_store_file)

    def postgres_changes_callback(payload):
        """
        This function is responsible for listening for changes to the vector store file and signaling success if the file triggers realtime successfully.
        """
        expected_record = {
            "object": "vector_store.file",
            "status": "completed",
            "usage_bytes": 0,
        }

        all_records_match = all(
            payload.get("record", {}).get(key) == value
            for key, value in expected_record.items()
        )
        event_information_match = (
            payload.get("table") == "vector_store_file"
            and payload.get("type") == "INSERT"
        )

        if event_information_match and all_records_match:
            raise TestCompleteException("Test completed successfully")

    async def upload_file(client: AsyncClient) -> str:
        """
        This function is responsible for uploading a file to the file bucket.
        """
        empty_file_object = FileObject(
            id="",
            bytes=0,
            created_at=0,
            filename="",
            object="file",
            purpose="assistants",
            status="uploaded",
            status_details=None,
        )

        file_object = await CRUDFileObject(client).create(object_=empty_file_object)
        assert file_object is not None, "Failed to create file object"

        crud_file_bucket = CRUDFileBucket(db=client, model=UploadFile)
        await crud_file_bucket.upload(
            file=UploadFile(filename="", file=io.BytesIO(b"")), id_=file_object.id
        )
        return file_object.id

    def run_postgres_db_changes():
        """
        This function is responsible for running the postgres_db_changes function.
        """
        asyncio.run(postgres_db_changes())

    timeout_timer = None
    try:
        random_name = str(uuid.uuid4())
        access_token = create_test_user(email=f"{random_name}@fake.com")

        # Schedule postgres_db_changes to run after 5 seconds
        threading.Timer(5.0, run_postgres_db_changes).start()

        # Set a timeout of 10 seconds
        timeout_timer = threading.Timer(10.0, timeout_handler)
        timeout_timer.start()

        # Listening socket
        # The service key is needed for proper permission to listen to realtime events
        # At the time of writing this, the Supabase realtime library does not support RLS
        URL = f"wss://supabase-kong.uds.dev/realtime/v1/websocket?apikey={SERVICE_KEY}&vsn=1.0.0"
        s = Socket(URL)
        s.connect()

        # Set channel to listen for changes to the vector_store_file table
        channel_1 = s.set_channel("realtime:public:vector_store_file")
        # Listen for all events on the channel ex: INSERT, UPDATE, DELETE
        channel_1.join().on("*", postgres_changes_callback)

        # Start listening
        s.listen()
    except TestCompleteException:
        if timeout_timer is not None:
            timeout_timer.cancel()  # Cancel the timeout timer if test completes successfully

        assert True
    except Exception:
        assert False


def test_supabase_realtime_file_objects():
    class TestCompleteException(Exception):
        pass

    def timeout_handler():
        print("Test timed out after 10 seconds")
        _thread.interrupt_main()

    async def create_file_object():
        client: AsyncClient = await acreate_client(
            supabase_key=ANON_KEY,
            supabase_url="https://supabase-kong.uds.dev",
        )
        await client.auth.set_session(access_token=access_token, refresh_token="dummy")

        empty_file_object = FileObject(
            id="",
            bytes=0,
            created_at=0,
            filename="test_file.txt",
            object="file",
            purpose="assistants",
            status="uploaded",
            status_details=None,
        )

        file_object = await CRUDFileObject(client).create(object_=empty_file_object)
        assert file_object is not None, "Failed to create file object"

    def file_objects_callback(payload):
        expected_record = {
            "object": "file",
            "status": "uploaded",
            "filename": "test_file.txt",
        }

        all_records_match = all(
            payload.get("record", {}).get(key) == value
            for key, value in expected_record.items()
        )
        event_information_match = (
            payload.get("table") == "file_objects" and payload.get("type") == "INSERT"
        )

        if event_information_match and all_records_match:
            raise TestCompleteException("Test completed successfully")

    def run_create_file_object():
        asyncio.run(create_file_object())

    timeout_timer = None
    try:
        random_name = str(uuid.uuid4())
        access_token = create_test_user(email=f"{random_name}@fake.com")

        threading.Timer(5.0, run_create_file_object).start()

        timeout_timer = threading.Timer(10.0, timeout_handler)
        timeout_timer.start()

        URL = f"wss://supabase-kong.uds.dev/realtime/v1/websocket?apikey={SERVICE_KEY}&vsn=1.0.0"
        s = Socket(URL)
        s.connect()

        channel = s.set_channel("realtime:public:file_objects")
        channel.join().on("*", file_objects_callback)

        s.listen()
    except TestCompleteException:
        if timeout_timer is not None:
            timeout_timer.cancel()
        assert True
    except Exception:
        assert False

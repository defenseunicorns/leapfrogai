import mimetypes
import threading

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
from locust import HttpUser, task, between, SequentialTaskSet
import warnings
import tempfile
import uuid
from tests.utils.data_path import data_path, MP3_FILE_RUSSIAN

# Suppress SSL-related warnings
warnings.filterwarnings("ignore", category=Warning)


class MissingEnvironmentVariable(Exception):
    pass


try:
    # The default model backend is set to vllm, this can be changed but llama-cpp-python may have concurrency issues
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "vllm")
    BEARER_TOKEN = os.environ["BEARER_TOKEN"]
    API_URL = os.environ["API_URL"]
except KeyError:
    raise MissingEnvironmentVariable(
        "BEARER_TOKEN and API_URL must be defined for the test to run. "
        "Please check the loadtest README at /tests/load/README.md for instructions on setting these values."
    )


class SharedResources:
    pdf_path = None
    pdf_lock = threading.Lock()


def download_arxiv_pdf():
    with SharedResources.pdf_lock:
        if SharedResources.pdf_path is None or not os.path.exists(
            SharedResources.pdf_path
        ):
            url = "https://arxiv.org/pdf/2305.16291.pdf"
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                SharedResources.pdf_path = temp_file.name

            response = requests.get(url)
            if response.status_code == 200:
                with open(SharedResources.pdf_path, "wb") as file:
                    file.write(response.content)
                print("ArXiv PDF downloaded successfully.")
            else:
                raise Exception(
                    f"Failed to download PDF from ArXiv. Status code: {response.status_code}"
                )
        else:
            print("Using existing ArXiv PDF.")

    return SharedResources.pdf_path


def load_audio_file():
    with open(data_path(MP3_FILE_RUSSIAN), "rb") as file:
        return file.read()


class RAGTasks(SequentialTaskSet):
    """Run these tasks in order to simulate full RAG flow"""

    file_id = None
    vector_store_id = None
    assistant_id = None
    thread_id = None
    pdf_path = None

    def on_start(self):
        self.pdf_path = download_arxiv_pdf()

    @task
    def upload_file(self):
        mime_type, _ = mimetypes.guess_type(self.pdf_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        m = MultipartEncoder(
            fields={
                "file": ("arxiv_2305.16291.pdf", open(self.pdf_path, "rb"), mime_type),
                "purpose": "assistants",
            }
        )

        headers = {"Content-Type": m.content_type}
        response = self.client.post("/openai/v1/files", data=m, headers=headers)

        if response.status_code == 200:
            self.file_id = response.json()["id"]
            print(f"Uploaded file ID: {self.file_id}")

    @task
    def create_vector_store(self):
        payload = {
            "name": f"Test Vector Store {uuid.uuid4()}",
            "file_ids": [self.file_id],
            "metadata": {"test": "data"},
        }
        response = self.client.post("/openai/v1/vector_stores", json=payload)
        if response.status_code == 200:
            self.vector_store_id = response.json()["id"]
            print(f"Created vector store ID: {self.vector_store_id}")

    @task
    def create_assistant(self):
        payload = {
            "model": DEFAULT_MODEL,
            "name": f"RAG Assistant {uuid.uuid4()}",
            "instructions": "You are a helpful assistant with access to a knowledge base. Use the file_search tool to find relevant information.",
            "tools": [{"type": "file_search"}],
            "tool_resources": {
                "file_search": {"vector_store_ids": [self.vector_store_id]}
            },
        }
        response = self.client.post("/openai/v1/assistants", json=payload)
        if response.status_code == 200:
            self.assistant_id = response.json()["id"]
            print(f"Created assistant with ID: {self.assistant_id}")

    @task
    def create_thread_and_run(self):
        # Create a thread
        thread_payload = {
            "messages": [
                {
                    "role": "user",
                    "content": "What information can you provide about the capital of France?",
                }
            ]
        }
        thread_response = self.client.post("/openai/v1/threads", json=thread_payload)

        if thread_response.status_code == 200:
            self.thread_id = thread_response.json()["id"]

            # Create a run using the thread and assistant
            run_payload = {
                "assistant_id": self.assistant_id,
                "instructions": "Please use the file_search tool to find information about the capital of France and provide a detailed response.",
            }
            run_response = self.client.post(
                f"/openai/v1/threads/{self.thread_id}/runs", json=run_payload
            )

            if run_response.status_code == 200:
                run_id = run_response.json()["id"]
                print(f"Created run with ID: {run_id}")

                # Check run status
                status_response = self.client.get(
                    f"/openai/v1/threads/{self.thread_id}/runs/{run_id}"
                )
                print(f"Run status: {status_response.json()['status']}")

    @task
    def stop(self):
        self.interrupt()


class LeapfrogAIUser(HttpUser):
    """This class represents a user that will kick off tasks over the life of the test"""

    # Root url to use for all client requests
    host = API_URL
    # Add some wait time in-between kicking off tasks
    wait_time = between(1, 3)

    def on_start(self):
        # Turn off SSL verification to get rid of unnecessary TLS version issues
        self.client.verify = False
        self.client.headers.update({"Authorization": f"Bearer {BEARER_TOKEN}"})

    @task
    def perform_rag_tasks(self):
        rag_tasks = RAGTasks(self)
        rag_tasks.run()

    @task
    def test_list_api_keys(self):
        self.client.get("/leapfrogai/v1/auth/list-api-keys")

    @task
    def test_openai_models(self):
        self.client.get("/openai/v1/models")

    @task
    def test_chat_completions(self):
        payload = {
            "model": DEFAULT_MODEL,
            "messages": [{"role": "user", "content": "Hello, how are you?"}],
            "max_tokens": 50,
        }
        self.client.post("/openai/v1/chat/completions", json=payload)

    @task
    def test_embeddings(self):
        payload = {
            "model": "text-embeddings",
            "input": "The quick brown fox jumps over the lazy dog",
        }
        self.client.post("/openai/v1/embeddings", json=payload)

    @task
    def test_transcribe(self):
        audio_content = load_audio_file()
        files = {"file": (MP3_FILE_RUSSIAN, audio_content, "audio/mpeg")}
        data = {"model": "whisper", "language": "ru"}
        self.client.post("/openai/v1/audio/transcriptions", files=files, data=data)

    @task
    def test_translate(self):
        audio_content = load_audio_file()
        files = {"file": (MP3_FILE_RUSSIAN, audio_content, "audio/mpeg")}
        data = {"model": "whisper"}
        self.client.post("/openai/v1/audio/translations", files=files, data=data)

    @task
    def test_list_files(self):
        self.client.get("/openai/v1/files")

    @task
    def test_list_vector_stores(self):
        self.client.get("/openai/v1/vector_stores")

    @task
    def test_list_assistants(self):
        self.client.get("/openai/v1/assistants")

    @task
    def test_healthz(self):
        self.client.get("/healthz")

    @task
    def test_models(self):
        self.client.get("/models")

    @task
    def test_create_api_key(self):
        payload = {"name": "Test API Key"}
        self.client.post("/leapfrogai/v1/auth/create-api-key", json=payload)

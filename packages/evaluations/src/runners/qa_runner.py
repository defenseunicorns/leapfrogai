import logging
import os
import openai
import zipfile

from datasets import load_dataset
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
from tqdm import tqdm

from openai.types.beta.assistant import Assistant
from openai.types.beta.vector_store import VectorStore

load_dotenv()

DEFAULT_INSTRUCTION_TEMPLATE = """
                You are a helpful AI bot that answers questions for a user. Keep your response short and direct.
                You will receive a set of context and a question that will relate to the context.
                Do not give information outside the document or repeat your findings.
                If the information is not available in the context respond UNANSWERABLE.
                """


class QA_Runner:
    """
    A runner to handle executing Question and Answer (QA) evals for LeapfrogAI

    This runner assumes LeapfrogAI is already deployed

    The evaluation takes the following steps (by default)
    - Creates a vector store
    - Uploads the contextual documents needed to answer the questions in the dataset
    - For each question in the dataset:
        - create an assistant
        - prompt the system to answer the question
        - record the response
        - delete the assistant
    - delete documents
    - delete the vector store
    """

    def __init__(
        self,
        dataset: str = "defenseunicorns/LFAI_RAG_qa_v1",
        model: str = "vllm",
        temperature: float = 0.1,
        base_url: str = None,
        api_key: str = None,
        num_samples: int = 32,
        instruction_template: str = DEFAULT_INSTRUCTION_TEMPLATE,
    ):
        """Initialize the Assistant with an API key and the path to the text file"""

        self.qa_data = None
        self.vector_store = None
        self.file_ids = None
        self.current_assistant = None
        self.model = model
        self.temperature = temperature
        self.instruction_template = instruction_template
        self.client = openai.OpenAI(
            base_url=base_url or os.getenv("LEAPFROGAI_API_URL"),
            api_key=api_key or os.getenv("LEAPFROGAI_API_KEY"),
        )
        logging.info(f"client url: {self.client.base_url}")
        self._load_qa_dataset(dataset_name=dataset, num_samples=num_samples)
        self._create_vector_store()
        self._upload_context(dataset_name=dataset)

    def run_experiment(self, cleanup: bool = True) -> None:
        """Prompts LFAI to answer questions from the QA dataset"""
        if cleanup:
            logging.info(
                "By default, all files and the vector store will be deleted after running the experiment. \
                         Please set `cleanup` to false when running the experiment if this is not preferred."
            )

        try:
            response_contents = []

            for row in tqdm(self.qa_data, desc="Evaluating data rows"):
                # create assistant
                self.current_assistant = self._create_assistant()

                # create thread
                thread = self.client.beta.threads.create()
                self.client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=row["input"],
                )

                # create run
                run = self.client.beta.threads.runs.create_and_poll(
                    assistant_id=self.current_assistant.id, thread_id=thread.id
                )

                # get messages
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id, run_id=run.id
                ).data

                response_messages = []
                for message in messages:
                    if message.role == "assistant":
                        response_messages.append(message)

                response_content = ""
                for response in response_messages:
                    response_content += response.content[0].text.value + "\n"

                    logging.debug(
                        f"number of annotations in response: {len(response.content[0].text.annotations)}"
                    )

                logging.info(f"Response recorded:\n{response_content}")
                response_contents.append(response_content)

                # delete the assistant
                self._delete_assistant(self.current_assistant.id)
                self.current_assistant = None

            # set the responses
            self.qa_data["actual_output"] = response_contents

            if cleanup:
                self.cleanup()

        # remove artifacts from the API if the experiment fails
        except Exception as exc:
            logging.info("Error encountered, running cleanup")
            self.cleanup()
            raise exc

    def cleanup(self) -> None:
        """
        Deletes the vector store and any remaining uploaded files

        This is run by default after completing a run and in case a run fails
        """
        logging.info("Cleaning up runtime artifacts...")
        if self.current_assistant:
            self._delete_assistant(assistant_id=self.current_assistant.id)
            self.current_assistant = None
        if self.file_ids:
            self._delete_context()
            self.file_ids = None
        if self.vector_store:
            self._delete_vector_store(vector_store_id=self.vector_store.id)
            self.vector_store = None

    def _load_qa_dataset(self, dataset_name: str, num_samples: int):
        """
        Load the Defense Unicorns LFAI QA dataset with the requested constraints

        By default, the dataset will contain 32 elements
        """
        logging.info(f"Downloading dataset: {dataset_name} from HuggingFace")
        qa_dataset = load_dataset(dataset_name)["eval"].select(range(num_samples))

        logging.info(f"Dataset downloaded: \n{qa_dataset}")
        self.qa_data = qa_dataset

    def _create_assistant(self) -> Assistant:
        """Create an assistant for running the QA evaluation"""
        logging.info("Creating new assistant...")
        assistant = self.client.beta.assistants.create(
            name="LFAI QA Assistant",
            instructions=self.instruction_template,
            model=self.model,
            temperature=self.temperature,
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {"vector_store_ids": [self.vector_store.id]}
            },
        )
        return assistant

    def _delete_assistant(self, assistant_id: str) -> None:
        """Deletes the current assistant"""
        logging.info("deleting assistant...")
        self.client.beta.assistants.delete(assistant_id=assistant_id)
        pass

    def _create_vector_store(self) -> VectorStore:
        logging.info("Creating vector store...")
        vector_store = self.client.beta.vector_stores.create(
            name="Question/Answer Store",
            file_ids=[],
            expires_after={"anchor": "last_active_at", "days": 1},
            metadata={"project": "QA Evaluation", "version": "0.1"},
        )
        self.vector_store = vector_store
        logging.info("Uploading context to vector store...")

    def _delete_vector_store(self, vector_store_id: str) -> None:
        """Deletes the vector store used for all QA evaluations"""
        logging.info("Deleting vector store...")
        _ = self.client.beta.vector_stores.delete(vector_store_id=vector_store_id)
        self.vector_store = None

    def _upload_context(self, dataset_name: str) -> None:
        """Uploads the full-text context documents to the vector store"""
        file_ids = []
        zip_path = hf_hub_download(
            repo_id=dataset_name, repo_type="dataset", filename="document_context.zip"
        )
        output_dir = "temp_data"
        # make a temporary directory to store documents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
            doc_list = zip_ref.namelist()

        logging.info("Uploading context documents")
        for doc in tqdm(doc_list):
            vector_store_file = self.client.beta.vector_stores.files.upload(
                vector_store_id=self.vector_store.id, file=f"{output_dir}/{doc}"
            )
            file_ids.append(vector_store_file.id)

        os.remove("temp_data")
        logging.debug(
            f"data in vector store: {self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id).data}"
        )

    def _delete_context(self) -> None:
        """Deletes the context files uploaded to the vector store"""
        logging.info("Deleting uploaded context files...")
        for file_id in self.file_ids:
            self.client.files.delete(file_id=file_id)

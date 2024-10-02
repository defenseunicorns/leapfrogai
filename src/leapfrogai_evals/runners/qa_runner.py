import ast
import logging
import os
import openai
import requests
import shutil
import zipfile

from datasets import load_dataset
from distutils.util import strtobool
from huggingface_hub import hf_hub_download
from tqdm import tqdm

from openai.types.beta.assistant import Assistant
from openai.types.beta.vector_store import VectorStore

from utils.defaults import DEFAULT_INSTRUCTION_TEMPLATE


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
        num_documents: int = 5,
        instruction_template: str = DEFAULT_INSTRUCTION_TEMPLATE,
        vector_store_id: str = None,
        cleanup: bool = True,
    ):
        """Initialize the Assistant with an API key and the path to the text file"""

        self.qa_data = None
        self.vector_store = None
        self.file_dict = None
        self.current_assistant = None
        self.api_key = api_key or os.getenv("LEAPFROGAI_API_KEY")
        self.dataset_name = os.environ.get("QA_DATASET", dataset)
        self.model = os.environ.get("MODEL_TO_EVALUATE", model)
        self.temperature = float(os.environ.get("TEMPERATURE", temperature))
        self.num_documents = int(os.environ.get("QA_NUM_DOCUMENTS", num_documents))
        self.cleanup_after = (
            bool(strtobool(os.environ.get("QA_CLEANUP_VECTOR_STORE")))
            if os.environ.get("QA_CLEANUP_VECTOR_STORE") is not None
            else cleanup
        )
        try:
            self.instruction_template = globals()[
                os.environ.get("QA_INSTRUCTION_TEMPLATE")
            ]
        except KeyError:
            logging.debug("Instruction template not in globals; setting as a string")
            self.instruction_template = os.environ.get(
                "QA_INSTRUCTION_TEMPLATE", instruction_template
            )

        self.client = openai.OpenAI(
            base_url=base_url or os.getenv("LEAPFROGAI_API_URL"),
            api_key=self.api_key,
        )
        logging.info(f"client url: {self.client.base_url}")
        try:  # use existing vector store if supplied
            self.vector_store = self._get_vector_store(
                os.environ.get("QA_VECTOR_STORE_ID", vector_store_id)
            )
        except Exception:  # otherwise create a new one
            self.vector_store = self._create_vector_store()
        if not os.environ.get("QA_VECTOR_STORE_ID") and not vector_store_id:
            self._upload_context(
                dataset_name=self.dataset_name, num_documents=self.num_documents
            )
        self._load_qa_dataset(
            dataset_name=self.dataset_name,
            num_samples=int(os.environ.get("QA_NUM_SAMPLES", num_samples)),
        )

    def run_experiment(self) -> None:
        """Prompts LFAI to answer questions from the QA dataset"""
        if self.cleanup_after:
            logging.info(
                "By default, all files and the vector store will be deleted after running the experiment. \
                         Please set `self.cleanup_after` to false if this is not preferred."
            )

        try:
            response_contents = []
            retrieved_contexts = []
            expected_annotations = []
            actual_annotations = []

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
                retrieved_context = []
                response_annotations = []
                for response in response_messages:
                    response_content += response.content[0].text.value + "\n"
                    chunk_ids = ast.literal_eval(response.metadata["vector_ids"])

                    # retrieve context used to generate response
                    for chunk_id in chunk_ids:
                        vector_response = requests.get(
                            url=os.getenv("LEAPFROGAI_API_LFAI_URL")
                            + "/vector_stores/vector/"
                            + chunk_id,
                            headers={
                                "accept": "application/json",
                                "Authorization": "Bearer " + self.api_key,
                            },
                        ).json()
                        retrieved_context.append(vector_response["content"])

                    for annotation in response.content[0].text.annotations:
                        annotation_id = annotation.file_citation.file_id
                        response_annotations.append(annotation_id)

                    logging.info(
                        f"number of annotations in response: {len(response.content[0].text.annotations)}"
                    )

                expected_annotations.append([self.file_dict[row["source_file"]]])
                actual_annotations.append(response_annotations)

                logging.info(
                    f"Retrieved context recorded: {vector_response['content']}"
                )
                retrieved_contexts.append(retrieved_context)
                logging.info(f"Response recorded:\n{response_content}")
                response_contents.append(response_content)

                # delete the assistant
                self._delete_assistant(self.current_assistant.id)
                self.current_assistant = None

            # set the responses
            self.qa_data = self.qa_data.remove_columns("actual_output")
            self.qa_data = self.qa_data.add_column(
                name="actual_output", column=response_contents
            )
            self.qa_data = self.qa_data.add_column(
                name="retrieval_context", column=retrieved_contexts
            )
            self.qa_data = self.qa_data.add_column(
                name="expected_annotations", column=expected_annotations
            )
            self.qa_data = self.qa_data.add_column(
                name="actual_annotations", column=actual_annotations
            )

            if self.cleanup_after:
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
        if self.file_dict:
            self._delete_context()
            self.file_dict = None
        if self.vector_store:
            self._delete_vector_store(vector_store_id=self.vector_store.id)
            self.vector_store = None

    def _load_qa_dataset(self, dataset_name: str, num_samples: int):
        """
        Load the Defense Unicorns LFAI QA dataset with the requested constraints

        By default, the dataset will contain 32 elements
        """
        logging.info(f"Downloading dataset: {dataset_name} from HuggingFace")
        qa_dataset = load_dataset(dataset_name)["eval"]
        qa_dataset = qa_dataset.select(
            (
                i
                for i in range(len(qa_dataset))
                if (qa_dataset[i]["source_file"] in self.doc_list)
            )
        )

        logging.info(f"Dataset downloaded: \n{qa_dataset}")
        if num_samples < len(qa_dataset):
            qa_dataset = qa_dataset.select(range(num_samples))

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
        return vector_store

    def _get_vector_store(self, vector_store_id: str) -> VectorStore:
        logging.info("Retrieving vector store...")
        vector_store = self.client.beta.vector_stores.retrieve(
            vector_store_id=vector_store_id
        )
        return vector_store

    def _delete_vector_store(self, vector_store_id: str) -> None:
        """Deletes the vector store used for all QA evaluations"""
        logging.info("Deleting vector store...")
        _ = self.client.beta.vector_stores.delete(vector_store_id=vector_store_id)
        self.vector_store = None

    def _upload_context(
        self, dataset_name: str, num_documents: int | None = None
    ) -> None:
        """Uploads the full-text context documents to the vector store"""
        self.file_dict = dict()
        zip_path = hf_hub_download(
            repo_id=dataset_name, repo_type="dataset", filename="documents_partial.zip"
        )
        # make a temporary directory to store documents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(".")
            doc_list = zip_ref.namelist()
            context_dir = doc_list.pop(0)  # first entry is the parent dir

        if num_documents:
            try:
                doc_list = doc_list[0:num_documents]
            except Exception:
                logging.info(
                    f"The number of documents requested was invalid ({num_documents}), defaulting to all documents ({len(doc_list)})"
                )

        logging.info(f"doc list: {doc_list}")

        logging.info("Uploading context documents")
        for doc in tqdm(doc_list):
            with open(doc, "rb") as pdf_file:
                vector_store_file = self.client.beta.vector_stores.files.upload(
                    vector_store_id=self.vector_store.id, file=pdf_file
                )
            self.file_dict[doc] = vector_store_file.id

        shutil.rmtree(context_dir)
        logging.debug(
            f"data in vector store: {self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id).data}"
        )

        self.doc_list = doc_list

    def _delete_context(self) -> None:
        """Deletes the context files uploaded to the vector store"""
        logging.info("Deleting uploaded context files...")
        for _, file_id in self.file_dict.items():
            self.client.files.delete(file_id=file_id)

import logging
import numpy as np
import os
import openai

from datasets import load_dataset, concatenate_datasets
from distutils.util import strtobool
from tqdm import tqdm

from openai.types.beta.assistant import Assistant
from openai.types.beta.vector_store import VectorStore

from utils.defaults import DEFAULT_INSTRUCTION_TEMPLATE


class NIAH_Runner:
    """
    A runner to handle executing Needle in a Haystack (NIAH) evals for LeapfrogAI

    This runner assumes LeapfrogAI is already deployed

    The evaluation takes the following steps (by default)
    - Creates a vector store
    - Uploads 10 noncontextual documents (around 4000 characters long) to the vector store as haystack padding
    - Takes a subset of context-containing documents (by default 5 texts of 4000 character length containing a secret code word)
    - For each contextual document:
        - create an assistant
        - upload doc to the vector store
        - request the secret code via RAG retrieval
        - determine if the code was retrieved (score 1 else 0)
        - determine if the code was given in the final response (score 1 else 0)
        - delete the document (from the vector store and outright)
    - delete the noncontextual documents
    - delete the vector store
    - Average all the retrieval scores
    - Average all the response scores
    """

    def __init__(
        self,
        dataset: str = "defenseunicorns/LFAI_RAG_niah_v1",
        temperature: float = 0.1,
        add_padding: bool = True,
        base_url: str = None,
        api_key: str = None,
        model: str = "vllm",
        message_prompt: str = "What is the secret code?",
        instruction_template: str = DEFAULT_INSTRUCTION_TEMPLATE,
        min_doc_length: int = 4096,
        max_doc_length: int = 4096,
        min_depth: float = 0.0,
        max_depth: float = 1.0,
        num_copies: int = 3,
    ):
        """Initialize the Assistant with an API key and the path to the text file"""

        self.padding = None
        self.niah_data = None
        self.vector_store = None
        self.current_file = None
        self.current_assistant = None
        self.message_prompt = os.environ.get("NIAH_MESSAGE_PROMPT", message_prompt)
        self.model = os.environ.get("MODEL_TO_EVALUATE", model)
        self.temperature = float(os.environ.get("TEMPERATURE", temperature))
        self.add_padding = (
            bool(strtobool(os.environ.get("NIAH_ADD_PADDING")))
            if os.environ.get("NIAH_ADD_PADDING") is not None
            else add_padding
        )
        try:
            self.instruction_template = globals()[
                os.environ.get("NIAH_INSTRUCTION_TEMPLATE")
            ]
        except KeyError:
            logging.debug("Instruction template not in globals; setting as a string")
            self.instruction_template = os.environ.get(
                "NIAH_INSTRUCTION_TEMPLATE", instruction_template
            )

        self.client = openai.OpenAI(
            base_url=base_url or os.environ.get("LEAPFROGAI_API_URL"),
            api_key=api_key or os.environ.get("LEAPFROGAI_API_KEY"),
        )
        logging.info(f"client url: {self.client.base_url}")
        self._load_niah_dataset(
            dataset_name=os.environ.get("NIAH_DATASET", dataset),
            min_doc_length=int(os.environ.get("NIAH_MIN_DOC_LENGTH", min_doc_length)),
            max_doc_length=int(os.environ.get("NIAH_MAX_DOC_LENGTH", max_doc_length)),
            min_depth=float(os.environ.get("NIAH_MIN_DEPTH", min_depth)),
            max_depth=float(os.environ.get("NIAH_MAX_DEPTH", max_depth)),
            num_copies=int(os.environ.get("NIAH_NUM_COPIES", num_copies)),
        )
        self._create_vector_store()
        self.retrieval_score = None
        self.response_score = None

    def run_experiment(self, cleanup: bool = True) -> None:
        """
        Runs the Needle in a Haystack evaluation

        if cleanup == True, then the following will be deleted from the API following the experiment:
        - assistants
        - contextual files
        - noncontextual padding files
        - the vector store

        In the event of an error, the cleanup function will be run regardless
        """

        try:
            retrieval_scores = []
            response_scores = []
            response_contents = []

            for row in tqdm(self.niah_data, desc="Evaluating data rows"):
                logging.debug(
                    f"length: {row['context_length']}\n depth: {row['context_depth']}\n secret_code: {row['secret_code']}"
                )
                # add file to vector_store
                # TODO: there has to be a more efficient way to add this file
                with open("context.txt", "wb") as context_file:
                    context_file.write(row["context"].encode("utf-8"))
                with open("context.txt", "rb") as context_file:
                    vector_store_file = self.client.beta.vector_stores.files.upload(
                        vector_store_id=self.vector_store.id, file=context_file
                    )
                os.remove("context.txt")
                self.current_file = vector_store_file.id

                logging.debug(
                    f"data in vector store: {self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id).data}"
                )
                logging.debug(
                    f"There are now {len(self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id).data)} files in the vector store"
                )

                # create assistant
                self.current_assistant = self._create_assistant()

                # create thread
                thread = self.client.beta.threads.create()
                self.client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=self.message_prompt,
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

                retrieval_score = 0.0
                response_score = 0.0
                response_content = ""

                for response in response_messages:
                    response_content += response.content[0].text.value + "\n"

                    # retrieval_score
                    # 1 if needle text was returned by the retrieval step of RAG else 0
                    logging.debug(
                        f"number of annotations in response: {len(response.content[0].text.annotations)}"
                    )
                    for annotation in response.content[0].text.annotations:
                        annotation_id = annotation.file_citation.file_id
                        if annotation_id == self.current_file:
                            logging.debug("Setting retrieval_score to 1.0")
                            retrieval_score = 1.0

                    # # response_score
                    # # 1 if needle text was returned by the LLM's final response else 0
                    secret_code = row["secret_code"]
                    logging.info(f"Response message: {response.content[0].text.value}")
                    if secret_code in response.content[0].text.value:
                        logging.debug("Setting response_score to 1.0")
                        response_score = 1.0

                retrieval_scores.append(retrieval_score)
                response_scores.append(response_score)
                response_contents.append(response_content)

                # delete file to clean up the vector store
                self._delete_file(self.current_file)
                self.current_file = None
                logging.debug(
                    f"There are now {len(self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id).data)} files in the vector store"
                )

                # delete the assistant
                self._delete_assistant(self.current_assistant.id)
                self.current_assistant = None

            # remove any remaining artifacts from the experiment
            self.cleanup()

            self.niah_data = self.niah_data.add_column(
                name="retrieval_score", column=retrieval_scores
            )
            self.niah_data = self.niah_data.add_column(
                name="response_score", column=response_scores
            )
            self.niah_data = self.niah_data.add_column(
                name="response", column=response_contents
            )

            self.retrieval_score = np.mean(retrieval_scores)
            self.response_score = np.mean(response_scores)

            logging.info(f"Retrieval Score {self.retrieval_score}")
            logging.info(f"Response Score {self.response_score}")

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
        if self.current_file:
            self._delete_file(file_id=self.current_file)
            self.current_file = None
        if self.padding:
            logging.info("Removing haystack padding files...")
            for row in self.padding:
                _ = self.client.files.delete(file_id=row["padding_id"])
            self.padding = None
        if self.vector_store:
            self._delete_vector_store(vector_store_id=self.vector_store.id)
            self.vector_store = None

    def _load_niah_dataset(
        self,
        dataset_name: str,
        min_doc_length: int,
        max_doc_length: int,
        min_depth: float,
        max_depth: float,
        num_copies: int,
    ):
        """
        Load the Defense Unicorns LFAI NIAH dataset with the requested constraints

        By default, the dataset will contain 10 elements
        """
        logging.info(f"Downloading dataset: {dataset_name} from HuggingFace")
        niah_dataset = load_dataset(dataset_name)
        self.padding = niah_dataset["padding"]
        niah_dataset = concatenate_datasets(
            [
                niah_dataset["base_eval"],
                niah_dataset["64k_eval"],
                niah_dataset["128k_eval"],
            ]
        )
        _copies = [i for i in range(num_copies)]
        niah_dataset = niah_dataset.select(
            (
                i
                for i in range(len(niah_dataset))
                if (
                    niah_dataset[i]["context_length"] >= min_doc_length
                    and niah_dataset[i]["context_length"] <= max_doc_length
                    and niah_dataset[i]["context_depth"] >= min_depth
                    and niah_dataset[i]["context_depth"] <= max_depth
                    and niah_dataset[i]["copy"] in _copies
                )
            )
        )

        logging.info(f"Dataset downloaded: \n{niah_dataset}")
        self.niah_data = niah_dataset

    def _create_assistant(self) -> Assistant:
        """Create an assistant for a given round of the NIAH test"""
        logging.info("Creating new assistant...")
        if self.model is None:
            raise AttributeError(
                "No 'model' has been set. Either provide a model at runner creation time with 'model=' or set the 'MODEL_TO_EVALUATE' env var"
            )
        assistant = self.client.beta.assistants.create(
            name="LFAI NIAH Assistant",
            instructions=self.instruction_template,
            model=self.model,
            temperature=self.temperature,
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {"vector_store_ids": [self.vector_store.id]}
            },
        )
        logging.info(f"Created assistant: {assistant}")
        return assistant

    def _delete_assistant(self, assistant_id: str) -> None:
        """Deletes the current assistant"""
        logging.info("deleting assistant...")
        self.client.beta.assistants.delete(assistant_id=assistant_id)
        pass

    def _create_vector_store(self) -> VectorStore:
        logging.info("Creating vector store...")
        vector_store = self.client.beta.vector_stores.create(
            name="Haystack",
            file_ids=[],
            expires_after={"anchor": "last_active_at", "days": 1},
            metadata={"project": "Needle in a Haystack Evaluation", "version": "0.1"},
        )
        if self.add_padding:  # add the extra documents as padding for the haystack
            logging.info("Uploading haystack padding to the vector store...")
            padding_ids = []
            for count, row in tqdm(enumerate(self.padding)):
                with open(f"padding_{count}.txt", "wb") as context_file:
                    context_file.write(row["context"].encode("utf-8"))
                with open(f"padding_{count}.txt", "rb") as context_file:
                    padding_file = self.client.beta.vector_stores.files.upload(
                        vector_store_id=vector_store.id, file=context_file
                    )
                padding_ids.append(padding_file.id)
                os.remove(f"padding_{count}.txt")
            logging.debug(
                f"Added {len(self.padding)} files as padding to the haystack vector store"
            )
        self.vector_store = vector_store
        self.padding = self.padding.add_column(name="padding_id", column=padding_ids)

    def _delete_vector_store(self, vector_store_id: str) -> None:
        """Deletes the vector store used for all NIAH evaluations"""
        logging.info("Deleting vector store...")
        _ = self.client.beta.vector_stores.delete(vector_store_id=vector_store_id)
        self.vector_store = None

    def _delete_file(self, file_id: str) -> None:
        """
        Deletes a file from the file store given its id

        If the vectore store exists, it will be removed from the vector store as well
        """
        logging.info(f"Deleting file with id: {file_id}")
        if self.vector_store:
            self.client.beta.vector_stores.files.delete(
                file_id=file_id, vector_store_id=self.vector_store.id
            )
        self.client.files.delete(file_id=file_id)

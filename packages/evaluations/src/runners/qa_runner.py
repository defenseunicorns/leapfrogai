import datetime
import logging
import os
import openai
import seaborn as sns
import zipfile

from datasets import load_dataset
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
import matplotlib.pyplot as plt
from tqdm import tqdm

from openai.types.beta.assistant import Assistant
from openai.types.beta.vector_store import VectorStore

load_dotenv()

INSTRUCTION_TEMPLATE = """
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
    ):
        """Initialize the Assistant with an API key and the path to the text file"""

        self.qa_data = None
        self.vector_store = None
        self.file_ids = None
        self.model = model
        self.temperature = temperature
        self.client = openai.OpenAI(
            base_url=base_url or os.getenv("LEAPFROGAI_API_URL"),
            api_key=api_key or os.getenv("LEAPFROGAI_API_KEY"),
        )
        logging.info(f"client url: {self.client.base_url}")
        self._load_qa_dataset(dataset_name=dataset, num_samples=num_samples)
        self._create_vector_store()
        self._upload_context(dataset_name=dataset)
        self.retrieval_score = None
        self.response_score = None

    def run_experiment(self, clean_up_after: bool = True) -> None:
        """Prompts LFAI to answer questions from the QA dataset"""
        if clean_up_after:
            logging.info(
                "By default, all files and the vector store will be deleted after running the experiment. \
                         Please set `clean_up_after` to false when running the experiment if this is not preferred."
            )

        response_contents = []

        for row in tqdm(self.qa_data, desc="Evaluating data rows"):
            # create assistant
            assistant = self._create_assistant()

            # create thread
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=row["input"],
            )

            # create run
            run = self.client.beta.threads.runs.create_and_poll(
                assistant_id=assistant.id, thread_id=thread.id
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
            self._delete_assistant(assistant.id)

        # set the responses
        self.qa_data["actual_output"] = response_contents

        if clean_up_after:
            self.clean_up()

    def generate_report(self) -> None:
        """Creates two heatmaps for the retrieval and response scores respectively"""
        logging.info("Creating evaluation report...")

        niah_df = self.niah_data.to_pandas()

        # average the scores across context depths and context lengths
        mean_retrieval_scores = (
            niah_df.groupby(["context_depth", "context_length"])["retrieval_score"]
            .mean()
            .reset_index()
        )
        mean_response_scores = (
            niah_df.groupby(["context_depth", "context_length"])["response_score"]
            .mean()
            .reset_index()
        )

        mean_retrieval_pivot = mean_retrieval_scores.pivot(
            index="context_depth", columns="context_length", values="retrieval_score"
        )
        mean_response_pivot = mean_response_scores.pivot(
            index="context_depth", columns="context_length", values="response_score"
        )

        logging.info("--- Scores ---")
        logging.info(f"Retrieval:\n {mean_retrieval_pivot}")
        logging.info(f"Response:\n {mean_response_pivot}")

        color_map = self._get_color_map()
        fig, axes = plt.subplots(1, 2)
        fig.suptitle("Needle in a Haystack (NIAH) Evaluation Scores")

        sns.heatmap(
            mean_retrieval_pivot, ax=axes[0], annot=True, cmap=color_map, vmin=0, vmax=1
        )
        axes[0].set_xlabel("Context Length")
        axes[0].set_ylabel("Context Depth (%)")
        axes[0].set_title("Retrieval Scores")

        sns.heatmap(
            mean_response_pivot, ax=axes[1], annot=True, cmap=color_map, vmin=0, vmax=1
        )
        axes[1].set_xlabel("Context Length")
        axes[1].set_ylabel("Context Depth (%)")
        axes[1].set_title("Response Scores")

        fig.tight_layout(rect=[0, 0, 1, 0.95])
        fig.savefig(f"niah_heatmaps_{self.model}_{datetime.date.today()}.png", dpi=600)

        logging.info("Evaluation heatmaps finished!")

    def clean_up(self) -> None:
        """Deletes files and the vector store following a successful run"""
        logging.info("Cleaning up...")
        self._delete_context()
        self._delete_vector_store()

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
            instructions=INSTRUCTION_TEMPLATE,
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
            name="Haystack",
            file_ids=[],
            expires_after={"anchor": "last_active_at", "days": 1},
            metadata={"project": "Needle in a Haystack Evaluation", "version": "0.1"},
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

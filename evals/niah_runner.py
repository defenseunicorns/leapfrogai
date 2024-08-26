import datetime
import logging
import os
import openai
import seaborn as sns

from datasets import load_dataset, concatenate_datasets
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from tqdm import tqdm

from datasets.arrow_dataset import Dataset
from matplotlib.colors import LinearSegmentedColormap
from openai.types.beta.assistant import Assistant
from openai.types.beta.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)

load_dotenv()

INSTRUCTION_TEMPLATE = """
                You are a helpful AI bot that answers questions for a user. Keep your response short and direct.
                You will receive a set of context and a question that will relate to the context.
                Do not give information outside the document or repeat your findings.
                If the information is not available in the context respond UNANSWERABLE.
                """


class NIAH_Runner:
    """
    A runner to handle executing Needle in a Haystack (NIAH) evals for LeapfrogAI

    This runner assumes LeapfrogAI is already deployed
    """

    def __init__(
        self,
        min_context: int = 0,
        max_context: int = 32768,
        dataset: str = "defenseunicorns/LFAI_RAG_niah_v1",
        model: str = "vllm",
    ):
        """Initialize the Assistant with an API key and the path to the text file"""

        self.padding = None
        self.model = model
        self.client = openai.OpenAI(
            base_url=os.getenv("LEAPFROGAI_API_URL"),
            api_key=os.getenv("LEAPFROGAI_API_KEY"),
        )
        logging.info(f"client url: {self.client.base_url}")
        self.niah_data = self._load_niah_dataset(dataset, min_context, max_context)
        self.vector_store = self._create_vector_store()

    def evaluate(self) -> None:
        """Runs the Needle in a Haystack evaluation"""

        retrieval_scores = []
        response_scores = []

        for row in tqdm(self.niah_data, desc="Evaluating data rows"):
            logging.info(
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
            file_id = vector_store_file.id

            logging.info(
                f"data in vector store: {self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id).data}"
            )
            logging.info(
                f"There are now {len(self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id).data)} files in the vector store"
            )

            # create assistant
            assistant = self._create_assistant()

            # create thread
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content="What is Doug's secret code?",
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

            retrieval_score = 0.0
            response_score = 0.0

            for response in response_messages:
                # retrieval_score
                # 1 if needle text was returned by the retrieval step of RAG else 0
                logging.info(
                    f"number of annotations in response: {len(response.content[0].text.annotations)}"
                )
                for annotation in response.content[0].text.annotations:
                    annotation_id = annotation.file_citation.file_id
                    if annotation_id == file_id:
                        logging.info("Setting retrieval_score to 1.0")
                        retrieval_score = 1.0

                # # response_score
                # # 1 if needle text was returned by the LLM's final response else 0
                secret_code = row["secret_code"]
                logging.info(f"Response message: {response.content[0].text.value}")
                if secret_code in response.content[0].text.value:
                    logging.info("Setting response_score to 1.0")
                    response_score = 1.0

            retrieval_scores.append(retrieval_score)
            response_scores.append(response_score)

            # delete file to clean up the vector store
            logging.info("Deleting files")
            self.client.beta.vector_stores.files.delete(
                file_id=file_id, vector_store_id=self.vector_store.id
            )
            self.client.files.delete(file_id=file_id)
            logging.info(
                f"There are now {len(self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id).data)} files in the vector store"
            )

            # delete the assistant
            self._delete_assistant(assistant.id)

        self._delete_vector_store(self.vector_store.id)

        self.niah_data = self.niah_data.add_column(
            name="retrieval_score", column=retrieval_scores
        )
        self.niah_data = self.niah_data.add_column(
            name="response_score", column=response_scores
        )

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

    def _load_niah_dataset(
        self, dataset_name: str, min_context: int, max_context: int
    ) -> Dataset:
        """Load the Defense Unicorns LFAI NIAH dataset with the requested context length constraints"""
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
        niah_dataset = niah_dataset.select(
            (
                i
                for i in range(len(niah_dataset))
                if (
                    niah_dataset[i]["context_length"] >= min_context
                    and niah_dataset[i]["context_length"] <= max_context
                )
            )
        )

        return niah_dataset

    def _create_assistant(self, temperature: float = 0.1) -> Assistant:
        """Create an assistant for a given round of the NIAH test"""
        logging.info("Creating new assistant...")
        assistant = self.client.beta.assistants.create(
            name="LFAI NIAH Assistant",
            instructions=INSTRUCTION_TEMPLATE,
            model=self.model,
            temperature=temperature,
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

    def _create_vector_store(self, add_padding: bool = True) -> VectorStore:
        logging.info("Creating vector store...")
        vector_store = self.client.beta.vector_stores.create(
            name="Haystack",
            file_ids=[],
            expires_after={"anchor": "last_active_at", "days": 1},
            metadata={"project": "Needle in a Haystack Evaluation", "version": "0.1"},
        )
        if add_padding:  # add the extra documents as padding for the haystack
            logging.info("Uploading haystack padding to the vector store...")
            for count, row in tqdm(enumerate(self.padding)):
                with open(f"padding_{count}.txt", "wb") as context_file:
                    context_file.write(row["context"].encode("utf-8"))
                with open(f"padding_{count}.txt", "rb") as context_file:
                    self.client.beta.vector_stores.files.upload(
                        vector_store_id=vector_store.id, file=context_file
                    )
                os.remove(f"padding_{count}.txt")
            logging.info(
                f"Added {len(self.padding)} files as padding to the haystack vector store"
            )
        return vector_store

    def _delete_vector_store(self, vector_store_id: str) -> None:
        """Deletes the vector store used for all NIAH evaluations"""
        logging.info("Deleting vector store...")
        _ = self.client.beta.vector_stores.delete(vector_store_id=vector_store_id)
        self.vector_store = None

    def _get_color_map(self) -> LinearSegmentedColormap:
        """Builds a custom colormap for the heatmap figure"""
        return LinearSegmentedColormap.from_list("rg", ["r", "y", "g"], N=256)

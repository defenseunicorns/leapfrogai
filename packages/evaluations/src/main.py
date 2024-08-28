import deepeval
from deepeval.test_case import LLMTestCase

# from deepeval.metrics import ContextualRecallMetric, FaithfulnessMetric
import logging

from runners.niah_runner import NIAH_Runner
from metrics.niah_metrics import NIAH_Retrieval, NIAH_Response
# from metrics.correctness import CorrectnessMetric

logging.basicConfig(level=logging.INFO)  # for testing

ALL_EVALS = ["LFAI_NIAH", "LFAI_QA"]

ALL_METRICS = [
    "NIAH_RETRIEVAL",
    "NIAH_RESPONSE",
    "CORRECTNESS",
    "CONTEXTUAL_RECALL",
    "FAITHFULNESS",
]


class RAGEvaluator:
    """A class that handles running all of the LeapfrogAI RAG evaluations"""

    def __init__(self):
        self.eval_list = None
        self.test_case_dict = None
        self.niah_test_cases = None

    def set_evaluations(self, eval_list=[]) -> None:
        """Set the evaluations that will be run via a list"""
        if len(eval_list) == 0:
            logging.info("Setting eval list to ALL")
            self.eval_list = ALL_EVALS
        else:
            for item in eval_list:
                if item not in ALL_EVALS:
                    raise AttributeError(
                        f"'{item}' is not an available evaluation. Please limit the list to one of the following: {ALL_EVALS}"
                    )
            self.eval_list = eval_list

    def run_evals(self, *args, **kwargs) -> None:
        """Run all of the selected evaluations"""
        if self.eval_list is None:
            raise AttributeError(
                "the list of evaluations has not been set. Please do so by running the 'set_evaluations()' function"
            )

        logging.info("Running the following evaluations:")
        for eval in self.eval_list:
            logging.info(f" -{eval}")
        if "LFAI_NIAH" in self.eval_list:
            self._niah_evaluation(*args, **kwargs)
        # TODO: add more evaluations

    def _niah_evaluation(self, *args, **kwargs) -> None:
        """Run the Needle in a Haystack evaluation"""
        self.niah_test_cases = []

        niah_runner = NIAH_Runner(*args, **kwargs)
        niah_runner.run_experiment()

        # build test cases out of the niah_dataset
        for row in niah_runner.niah_data:
            self.niah_test_cases.append(
                LLMTestCase(
                    input=niah_runner.message_prompt,
                    actual_output=row["response"],
                    context=[row["context"]],
                    additional_metadata={
                        "retrieval_score": row["retrieval_score"],
                        "response_score": row["response_score"],
                    },
                )
            )

        # run metrics
        retrieval_metric = NIAH_Retrieval()
        response_metric = NIAH_Response()

        deepeval.evaluate(
            test_cases=self.niah_test_cases, metrics=[retrieval_metric, response_metric]
        )

    def _qa_evaluation(self, *args, **kwargs) -> None:
        """Runs the Question/Answer evaluation"""
        pass


if __name__ == "__main__":
    evaluator = RAGEvaluator()
    evaluator.set_evaluations()
    evaluator.run_evals()

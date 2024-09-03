import deepeval
from deepeval.test_case import LLMTestCase
import logging

from leapfrogai_evals.runners.niah_runner import NIAH_Runner
from leapfrogai_evals.metrics.niah_metrics import NIAH_Retrieval, NIAH_Response

ALL_EVALS = ["LFAI_NIAH"]


class RAGEvaluator:
    """A class that handles running all of the LeapfrogAI RAG evaluations"""

    def __init__(self):
        self.eval_list = None
        self.test_case_dict = None
        self.niah_test_cases = None
        self.eval_options = ALL_EVALS

    def set_evaluations(self, evals_list=[]) -> None:
        """Set the evaluations that will be run via a list"""
        if len(evals_list) == 0:
            logging.info("Setting eval list to ALL")
            self.eval_list = ALL_EVALS
        # TODO: Add other evals options

    def run_evals(self, *args, **kwargs) -> None:
        """Run all of the selected evaluations"""
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    evaluator = RAGEvaluator()
    evaluator.set_evaluations()
    evaluator.run_evals()

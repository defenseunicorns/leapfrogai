import deepeval
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    FaithfulnessMetric,
)  # , ContextualRecallMetric TODO: enable this metric
import logging
from typing import Optional, List

from metrics.correctness import CorrectnessMetric
from metrics.niah_metrics import NIAH_Retrieval, NIAH_Response
from runners.niah_runner import NIAH_Runner
from runners.qa_runner import QA_Runner

logging.basicConfig(level=logging.INFO)  # for testing

ALL_EVALS = ["LFAI_NIAH", "LFAI_QA"]
# QA_METRICS = ["CORRECTNESS", "CONTEXTUAL_RECALL", "FAITHFULNESS"]
# NIAH_METRICS = ["NIAH_RETRIEVAL", "NIAH_RESPONSE"]
# ALL_METRICS = QA_METRICS + NIAH_METRICS


class RAGEvaluator:
    """A class that handles running all of the LeapfrogAI RAG evaluations"""

    def __init__(
        self,
        eval_list: Optional[List[str]] = None,
        # metric_list: Optional[List[str]] = None,
    ):
        self.eval_list = eval_list
        # self.metric_list = metric_list
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
            logging.info("Beginning Needle in a Haystack Evaluation...")
            self._niah_evaluation(*args, **kwargs)

        if "LFAI_QA" in self.eval_list:
            logging.info("Beginning Question/Answer Evaluation...")
            self._qa_evaluation(*args, **kwargs)

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
        # TODO: Give ability to choose which metrics to run
        retrieval_metric = NIAH_Retrieval()
        response_metric = NIAH_Response()

        deepeval.evaluate(
            test_cases=self.niah_test_cases, metrics=[retrieval_metric, response_metric]
        )

    def _qa_evaluation(self, *args, **kwargs) -> None:
        """Runs the Question/Answer evaluation"""
        self.qa_test_cases = []

        qa_runner = QA_Runner(*args, **kwargs)
        qa_runner.run_experiment()

        # build test cases out of the qa_dataset
        for row in qa_runner.qa_data:
            self.qa_test_cases.append(
                LLMTestCase(
                    input=row["input"],
                    actual_output=row["actual_output"],
                    context=[row["context"]],
                    expected_output=row["expected_output"],
                    # retrieval_context = row['retrieval_context'] # TODO: add this for more metrics
                )
            )

        # run metrics
        # TODO: Give ability to choose which metrics to run
        correctness_metric = CorrectnessMetric()
        faithfulness_metric = FaithfulnessMetric()

        deepeval.evaluate(
            test_cases=self.qa_test_cases,
            metrics=[correctness_metric, faithfulness_metric],
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    evaluator = RAGEvaluator()
    evaluator.set_evaluations(eval_list=["LFAI_QA"])
    evaluator.run_evals()

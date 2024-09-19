from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.benchmarks import MMLU
from deepeval.benchmarks.tasks import MMLUTask

import logging
import numpy as np
import os
from dotenv import load_dotenv
import time
from typing import Optional, List

from leapfrogai_evals.models.claude_sonnet import ClaudeSonnet  # noqa
from leapfrogai_evals.models.lfai import LFAI_Model
from leapfrogai_evals.metrics.annotation_relevancy import AnnotationRelevancyMetric
from leapfrogai_evals.metrics.correctness import CorrectnessMetric
from leapfrogai_evals.metrics.niah_metrics import NIAH_Retrieval, NIAH_Response
from leapfrogai_evals.runners.niah_runner import NIAH_Runner
from leapfrogai_evals.runners.qa_runner import QA_Runner

ALL_EVALS = ["niah_eval", "qa_eval", "mmlu"]


class RAGEvaluator:
    """A class that handles running all of the LeapfrogAI RAG evaluations"""

    def __init__(
        self,
        eval_list: Optional[List[str]] = None,
    ):
        self.eval_list = eval_list
        self.test_case_dict = None
        self.niah_test_cases = None
        self.eval_results = dict()

    def set_evaluations(self, eval_list: List[str] = None) -> None:
        """Set the evaluations that will be run via a list"""
        if not eval_list:
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
        logging.info("".join([f"\n - {eval_name}" for eval_name in self.eval_list]))

        start_time = time.time()
        for eval_name in self.eval_list:
            eval = getattr(self, eval_name)
            eval(*args, **kwargs)
        end_time = time.time()

        self.eval_results["Eval Execution Runtime (seconds)"] = end_time - start_time

        logging.info("\n\nFinal Results:")
        for key, value in self.eval_results.items():
            logging.info(f"{key}: {value}")

    def niah_eval(self, *args, **kwargs) -> None:
        """Run the Needle in a Haystack evaluation"""
        logging.info("Beginning Needle in a Haystack Evaluation...")
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
        metrics = [retrieval_metric, response_metric]

        for metric in metrics:
            scores = []
            successes = []
            for test_case in self.niah_test_cases:
                metric.measure(test_case)
                scores.append(metric.score)
                successes.append(metric.is_successful())
            self.eval_results[f"Average {metric.__name__}"] = np.mean(scores)
            logging.info(f"{metric.__name__} Results:")
            logging.info(f"average score: {np.mean(scores)}")
            logging.info(f"scores: {scores}")
            logging.info(f"successes: {successes}")

    def qa_eval(self, *args, **kwargs) -> None:
        """Runs the Question/Answer evaluation"""
        logging.info("Beginning Question/Answer Evaluation...")
        self.qa_test_cases = []

        qa_runner = QA_Runner(*args, **kwargs)
        qa_runner.run_experiment()

        # build test cases out of the qa_dataset
        for row in qa_runner.qa_data:
            self.qa_test_cases.append(
                LLMTestCase(
                    input=row["input"],
                    actual_output=row["actual_output"],
                    context=row["context"],
                    expected_output=row["expected_output"],
                    additional_metadata={
                        "actual_annotations": row["actual_annotations"],
                        "expected_annotations": row["expected_annotations"],
                    },
                    # retrieval_context = row['retrieval_context'] # TODO: add this for more metrics
                )
            )

        # Create judge llm
        try:
            judge_model = globals()[os.environ.get("LLM_JUDGE")]()
        except KeyError:
            judge_model = os.environ.get("LLM_JUDGE")

        # run metrics
        # TODO: Give ability to choose which metrics to run
        correctness_metric = CorrectnessMetric(model=judge_model)
        answer_relevancy_metric = AnswerRelevancyMetric(model=judge_model)
        annotation_relevancy_metric = AnnotationRelevancyMetric()
        metrics = [
            correctness_metric,
            answer_relevancy_metric,
            annotation_relevancy_metric,
        ]

        for metric in metrics:
            scores = []
            successes = []
            reasons = []
            for test_case in self.qa_test_cases:
                metric.measure(test_case)
                scores.append(metric.score)
                successes.append(metric.is_successful())
                reasons.append(metric.reason)
            self.eval_results[f"Average {metric.__name__}"] = np.mean(scores)
            logging.info(f"{metric.__name__} Results:")
            logging.info(f"average score: {np.mean(scores)}")
            logging.info(f"scores: {scores}")
            logging.info(f"successes: {successes}")
            logging.info(f"reasons: {reasons}")

    def mmlu(self, n_shots: Optional[int] = None):
        """Runs the Massive Multitask Language Understanding (MMLU) benchmark on a subset of tasks"""
        tasks = [
            MMLUTask.COLLEGE_COMPUTER_SCIENCE,
            MMLUTask.US_FOREIGN_POLICY,
            MMLUTask.HIGH_SCHOOL_GOVERNMENT_AND_POLITICS,
            MMLUTask.FORMAL_LOGIC,
            MMLUTask.COMPUTER_SECURITY,
            MMLUTask.SECURITY_STUDIES,
        ]
        mmlu_benchmark = MMLU(
            tasks=tasks, n_shots=n_shots or int(os.getenv("MMLU_NUM_SHOTS"))
        )
        mmlu_benchmark.evaluate(model=LFAI_Model())
        logging.info(f"MMLU overall score: {mmlu_benchmark.overall_score}")
        logging.info(f"MMLU task scores:\n {mmlu_benchmark.task_scores}")

        # add the evaluation score to the final results
        self.eval_results["MMLU"] = mmlu_benchmark.overall_score


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    evaluator = RAGEvaluator()
    evaluator.set_evaluations(eval_list=["human_eval"])
    evaluator.run_evals()

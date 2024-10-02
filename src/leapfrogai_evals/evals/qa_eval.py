import logging
import numpy as np
import os

from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
)
from deepeval.test_case import LLMTestCase

from leapfrogai_evals.metrics import AnnotationRelevancyMetric, CorrectnessMetric
from leapfrogai_evals.models import *  # noqa (imports all models)
from leapfrogai_evals.runners import QA_Runner


def qa_eval(*args, **kwargs) -> dict:
    """Runs the Question/Answer evaluation"""
    logging.info("Beginning Question/Answer Evaluation...")
    eval_results = dict()
    qa_test_cases = []

    qa_runner = QA_Runner(*args, **kwargs)
    qa_runner.run_experiment()

    # build test cases out of the qa_dataset
    for row in qa_runner.qa_data:
        qa_test_cases.append(
            LLMTestCase(
                input=row["input"],
                actual_output=row["actual_output"],
                context=row["context"],
                expected_output=row["expected_output"],
                retrieval_context=row["retrieval_context"],
                additional_metadata={
                    "actual_annotations": row["actual_annotations"],
                    "expected_annotations": row["expected_annotations"],
                },
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
    contextual_relevancy_metric = ContextualRelevancyMetric(model=judge_model)
    faithfulness_metric = FaithfulnessMetric(model=judge_model)
    annotation_relevancy_metric = AnnotationRelevancyMetric()
    metrics = [
        correctness_metric,
        answer_relevancy_metric,
        contextual_relevancy_metric,
        faithfulness_metric,
        annotation_relevancy_metric,
    ]

    # record scores and return results
    for metric in metrics:
        scores = []
        successes = []
        reasons = []
        for test_case in qa_test_cases:
            metric.measure(test_case)
            scores.append(metric.score)
            successes.append(metric.is_successful())
            reasons.append(metric.reason)
        eval_results[f"Average {metric.__name__}"] = np.mean(scores)
        logging.info(f"{metric.__name__} Results:")
        logging.info(f"average score: {np.mean(scores)}")
        logging.info(f"scores: {scores}")
        logging.info(f"successes: {successes}")
        logging.info(f"reasons: {reasons}")

    return eval_results

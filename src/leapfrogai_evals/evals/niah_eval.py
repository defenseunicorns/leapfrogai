import logging
import numpy as np

from deepeval.test_case import LLMTestCase

from leapfrogai_evals.metrics import NIAH_Retrieval, NIAH_Response
from leapfrogai_evals.runners import NIAH_Runner


def niah_eval(*args, **kwargs) -> dict:
    """Run the Needle in a Haystack evaluation"""
    logging.info("Beginning Needle in a Haystack Evaluation...")
    eval_results = dict()
    niah_test_cases = []

    niah_runner = NIAH_Runner(*args, **kwargs)
    niah_runner.run_experiment()

    # build test cases out of the niah_dataset
    for row in niah_runner.niah_data:
        niah_test_cases.append(
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

    # record scores and return results
    for metric in metrics:
        scores = []
        successes = []
        for test_case in niah_test_cases:
            metric.measure(test_case)
            scores.append(metric.score)
            successes.append(metric.is_successful())
        eval_results[f"Average {metric.__name__}"] = np.mean(scores)
        logging.info(f"{metric.__name__} Results:")
        logging.info(f"average score: {np.mean(scores)}")
        logging.info(f"scores: {scores}")
        logging.info(f"successes: {successes}")

    return eval_results

import logging
import os

from deepeval.benchmarks import MMLU
from deepeval.benchmarks.tasks import MMLUTask
from typing import Optional

from leapfrogai_evals.models import LFAI_Model


def mmlu(self, num_tasks: Optional[int] = None, n_shots: Optional[int] = None) -> dict:
    """Runs the Massive Multitask Language Understanding (MMLU) benchmark on a subset of tasks"""
    eval_results = dict()
    num_tasks = num_tasks or int(
        os.getenv("MMLU_NUM_TASKS", default=len(list(MMLUTask)))
    )
    logging.info(f"Running the MMLU benchmark on {num_tasks} tasks")
    tasks = list(MMLUTask)[:num_tasks]
    mmlu_benchmark = MMLU(
        tasks=tasks, n_shots=n_shots or int(os.getenv("MMLU_NUM_SHOTS"))
    )
    mmlu_benchmark.evaluate(model=LFAI_Model())
    logging.info(f"MMLU overall score: {mmlu_benchmark.overall_score}")
    logging.info(f"MMLU task scores:\n {mmlu_benchmark.task_scores}")

    # add the evaluation score to the final results
    eval_results["MMLU"] = mmlu_benchmark.overall_score
    return eval_results

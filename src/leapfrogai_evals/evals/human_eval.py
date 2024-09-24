import logging
import numpy as np
import os

from deepeval.benchmarks import HumanEval
from deepeval.benchmarks.tasks import HumanEvalTask
from tqdm import tqdm
from typing import Optional

from leapfrogai_evals.models import LFAI_Model


def human_eval(
    num_samples: Optional[int] = None,
    k: Optional[int] = None,
    num_tasks: Optional[int] = None,
) -> dict:
    """Runs the HumanEval benchmark on a subset of tasks"""
    eval_results = dict()
    task_scores = dict()
    num_tasks = num_tasks or int(
        os.getenv("HUMAN_EVAL_NUM_TASKS", default=len(list(HumanEvalTask)))
    )
    logging.info(f"Running the HumanEval benchmark on {num_tasks} tasks")
    failed_tasks = 0
    for task in tqdm(list(HumanEvalTask)[:num_tasks]):
        task_benchmark = HumanEval(
            n=num_samples or int(os.getenv("HUMAN_EVAL_NUM_SAMPLES_PER_TASK")),
            tasks=[task],
        )
        try:
            task_benchmark.evaluate(
                model=LFAI_Model(), k=k or int(os.getenv("HUMAN_EVAL_K"))
            )
            task_scores[task.name] = task_benchmark.overall_score
        except Exception as exc:
            logging.info(
                f"HumanEval task {task.name} failed with error {exc}", exc_info=exc
            )
            task_scores[task.name] = 0.0
            failed_tasks += 1

    human_eval_avg_score = np.mean(list(task_scores.values()))
    logging.info(f"HumanEval overall score: {human_eval_avg_score}")
    logging.info(f"HumanEval failed task count: {failed_tasks}")
    logging.info(f"HumanEval task scores:\n {task_scores}")

    # add the evaluation score to the final results
    eval_results["HumanEval"] = human_eval_avg_score
    return eval_results

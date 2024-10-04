import logging
import time
from dotenv import load_dotenv
from typing import Optional, List

from leapfrogai_evals.evals import human_eval, mmlu, niah_eval, qa_eval  # noqa

ALL_EVALS = ["niah_eval", "qa_eval", "mmlu", "human_eval"]


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
            eval = globals()[eval_name]
            eval_result = eval(*args, **kwargs)
            self.eval_results.update(eval_result)
        end_time = time.time()

        self.eval_results["Eval Execution Runtime (seconds)"] = end_time - start_time

        logging.info("\n\nFinal Results:")
        for key, value in self.eval_results.items():
            logging.info(f"{key}: {value}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    evaluator = RAGEvaluator()
    evaluator.set_evaluations(eval_list=["mmlu"])
    evaluator.run_evals()

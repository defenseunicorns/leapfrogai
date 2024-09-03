from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams


class CorrectnessMetric(GEval):
    """A custom metric that determines if the actual output matches an expected output"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            name="Correctness",
            criteria="Determine whether the actual output is factually correct based on the expected output.",
            evaluation_steps=[
                "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
                "You should also heavily penalize omission of detail",
                "Vague language, or contradicting OPINIONS, are OK",
            ],
            evaluation_params=[
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT,
            ],
            *args,
            **kwargs,
        )

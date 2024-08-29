from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
import asyncio


class NIAH_Retrieval(BaseMetric):
    """A metric for measuring the retrieval score from the LFAI Needle in a Haystack Evaluation"""

    def __init__(
        self,
        threshold: float = 1.0,
        async_mode: bool = True,
    ):
        self.threshold = threshold
        self.async_mode = async_mode

    def measure(self, test_case: LLMTestCase) -> int:
        """Records the niah retrieval score from the test case"""
        self.success = (
            test_case.additional_metadata["retrieval_score"] >= self.threshold
        )
        if self.success:
            self.score = 1
            self.reason = f"Retrieval in the NIAH evaluation scored greater than or equal to the threshold score of {self.threshold}"
        else:
            self.score = 0
            self.reason = f"Retrieval in the NIAH evaluation scored less than the threshold score of {self.threshold}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> int:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.measure, test_case)

    def is_successful(self) -> bool:
        return self.success

    @property
    def __name__(self):
        return "Needle in a Haystack (NIAH) Retrieval"


class NIAH_Response(BaseMetric):
    """A metric for measuring the response score from the LFAI Needle in a Haystack Evaluation"""

    def __init__(
        self,
        threshold: float = 1.0,
        async_mode: bool = True,
    ):
        self.threshold = threshold
        self.async_mode = async_mode

    def measure(self, test_case: LLMTestCase) -> int:
        """Records the niah response score from the test case"""
        self.success = test_case.additional_metadata["response_score"] >= self.threshold
        if self.success:
            self.score = 1
            self.reason = f"Response in the NIAH evaluation scored greater than or equal to the threshold score of {self.threshold}"
        else:
            self.score = 0
            self.reason = f"Response in the NIAH evaluation scored less than the threshold score of {self.threshold}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> int:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.measure, test_case)

    def is_successful(self) -> bool:
        return self.success

    @property
    def __name__(self):
        return "Needle in a Haystack (NIAH) Response"

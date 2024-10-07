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
        """
        Records the niah retrieval score from the test case

        This function checks for the presence of a retrieval_score (provided by the niah_runner)
        and sets a boolean determined by said score. The score is calculated in the runner to keep the
        runner self-contained as a means of running the entire evaluation on its own. For simplicity,
        the score is copied here for integration with DeepEval.

        params:
        -------
        test_case: LLMTestCase
            A test case object built from the results of a needle in a haystack evaluation run.
            test_case should contain an additional metadata field that returns a dictionary with
            the field "retrieval_score"

        returns:
        -------
        int
            A score that is equal to the "retrieval_score" from the test_case
        """
        self.score = test_case.additional_metadata["retrieval_score"]
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"Retrieval in the NIAH evaluation scored greater than or equal to the threshold score of {self.threshold}"
        else:
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
        """
        Records the niah response score from the test case

        This function checks for the presence of a response_score (provided by the niah_runner)
        and sets a boolean determined by said score. The score is calculated in the runner to keep the
        runner self-contained as a means of running the entire evaluation on its own. For simplicity,
        the score is copied here for integration with DeepEval.

        params:
        -------
        test_case: LLMTestCase
            A test case object built from the results of a needle in a haystack evaluation run.
            test_case should contain an additional metadata field that returns a dictionary with
            the field "response_score"

        returns:
        -------
        int
            A score that is equal to the "response_score" from the test_case
        """
        self.score = test_case.additional_metadata["response_score"]
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"Response in the NIAH evaluation scored greater than or equal to the threshold score of {self.threshold}"
        else:
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


class NIAH_Chunk_Rank(BaseMetric):
    """A metric for measuring the chunk rank score from the LFAI Needle in a Haystack Evaluation"""

    def __init__(
        self,
        threshold: float = 1.0,
        async_mode: bool = True,
    ):
        self.threshold = threshold
        self.async_mode = async_mode

    def measure(self, test_case: LLMTestCase) -> int:
        """
        Records the niah chunk_rank from the test case

        This function checks for the presence of a chunk rank (provided by the niah_runner)
        and sets a boolean determined by said score. The score is calculated in the runner to keep the
        runner self-contained as a means of running the entire evaluation on its own. For simplicity,
        the score is copied here for integration with DeepEval.

        params:
        -------
        test_case: LLMTestCase
            A test case object built from the results of a needle in a haystack evaluation run.
            test_case should contain an additional metadata field that returns a dictionary with
            the field "chunk_rank"

        returns:
        -------
        int
            A score that is equal to the "chunk_rank" from the test_case
        """
        self.score = test_case.additional_metadata["chunk_rank"]
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"Response in the NIAH evaluation scored greater than or equal to the threshold score of {self.threshold}"
        else:
            self.reason = f"Response in the NIAH evaluation scored less than the threshold score of {self.threshold}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> int:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.measure, test_case)

    def is_successful(self) -> bool:
        return self.success

    @property
    def __name__(self):
        return "Needle in a Haystack (NIAH) Chunk Rank"

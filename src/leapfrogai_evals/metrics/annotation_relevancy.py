from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
import asyncio


class AnnotationRelevancyMetric(BaseMetric):
    """A heuristic (non-LLM) metric for measuring how relevant the annotated documents are to the needed context"""

    def __init__(
        self,
        threshold: float = 0.75,
        async_mode: bool = True,
    ):
        self.threshold = threshold
        self.async_mode = async_mode

    def measure(self, test_case: LLMTestCase) -> int:
        """
        Calculates the number of relevant annotations out of the total annotations

        This function calculates a simple fraction of the number of relevant annotations (usually 1)
        divided by the total number of annotations (number of documents referenced) returned by RAG.
        An annotation is considered relevant if it is in the listed of provided annotations and is expected

        score = # of relevant annotations / # of total annotations

        params:
        -------
        test_case: LLMTestCase
            A test case object built from the results of a question/answer evaluation run.
            test_case should contain an additional metadata field that returns a dictionary with
            the fields "expected_annotations" and "actual_annotations" which both contain lists of strings (file ids)

        returns:
        -------
        float
            A score from 0-1 that represents the fraction of relevant annotations out of all annotations
        """

        relevant_annotations = 0
        total_annotations = len(test_case.additional_metadata["actual_annotations"])
        for annotation in test_case.additional_metadata["actual_annotations"]:
            if annotation in test_case.additional_metadata["expected_annotations"]:
                relevant_annotations += 1

        self.score = float(relevant_annotations / total_annotations)
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"The fraction of relevant annotations out of the total number of annotations ({self.score}) is greater than or equal to the threshold of {self.threshold}"
        else:
            self.reason = f"The fraction of relevant annotations out of the total number of annotations ({self.score}) is less than the threshold of {self.threshold}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> int:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.measure, test_case)

    def is_successful(self) -> bool:
        return self.success

    @property
    def __name__(self):
        return "Annotation Relevancy"

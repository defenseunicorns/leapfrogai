ALL_EVALS = ["LFAI_NIAH"]


class RAGEvaluator:
    def __init__(self):
        self.eval_list = None

    def set_evaluations(self, evals_list=[]) -> None:
        if len(evals_list) == 0:
            self.eval_list = ALL_EVALS
        # TODO: Add other evals options

    def evaluate(self):
        pass

    def report_scores(self):
        pass

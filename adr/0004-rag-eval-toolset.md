# LeapfrogAI RAG Evaluation Toolset

## Table of Contents

- [LeapfrogAI RAG Evaluation Toolset](#leapfrogai-rag-evaluation-toolset)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
  - [Context](#context)
  - [Decision](#decision)
  - [Rationale](#rationale)
  - [Alternatives](#alternatives)
  - [Related ADRs](#related-adrs)
  - [References](#references)

## Status

ACCEPTED

## Context

LeapfrogAI uses RAG to provide context-aware responses to users who have specific data they need to reference. In order to make sure RAG is operating at the levels we need it to, we need to get measurable feedback from our RAG pipeline to make it better. We also need a standard to show to mission heroes that we are in fact operating at that level. We do this with RAG-focused evaluations. This ADR Proposes **[DeepEval](https://docs.confident-ai.com/)** as the toolset of choice for handling RAG evaluations.

## Decision

Handle RAG evaluation test cases using DeepEval.

With this toolset in mind, the following steps can be taken to incorporate evals into LeapfrogAI:

- Determine what types of tasks will help improve RAG
  - What kinds of heuristics should be evaluated on?
  - What do mission heroes care about?
- Build a representative dataset
  - What documents can be used as the basis for an eval dataset?
  - Use those documents to generate questions/ground truth statements using DeepEval tools
  - Refine those question/ground truth pairs
- Begin regularly using Evals
  - Which tests serve what purpose?
    - e2e testing (e.g deployments are only allowed on passing evals)
    - Baseline for performance (tracking how tests perform over time)
    - Showing to mission heroes (what performance factors do they care about/need to see?)
  - How are evals tracked/delivered?
    - How are eval results conveyed?
    - What internal tools are used to track evals over time?

## Rationale
The major RAG evaluation toolsets all revolve around LLM-enabled evaluations. While these are fast to get running and offer a lot of flexibility, our use case will likely demand custom evaluation metrics, likely consisting of heuristics testing that do not leverage LLMs for evaluation. Among the toolsets reviewed (see [Alernatives](#alternatives)), DeepEval was found to have the most flexibility in terms of custom evaluation metrics (llm-based and non-llm), as well as what models we want to use for evaluations. DeepEval has built-in metrics for llm-based evaluations, which utilize an LLM (external to the one being evaluated) to act as a judge for specific evaluation metrics. DeepEval also provides clear [documentation](https://docs.confident-ai.com/docs/metrics-custom) on the implementation of heuristic-based evaluations which do not require an LLM-as-a-judge. DeepEval also contains benchmarks and tools for evaluating other LLM metrics, so DeepEval is capable of being the toolset of choice for the general evaluation of LLMs. DeepEval offers a toolset for generating evaluation datasets from documentation, which will assist in setting up the datasets used for evaluations. Lastly, DeepEval's test-focused approach will integrate well with the testing workflows in LeapfrogAI.

## Alternatives
**RAGAS**: A more lightweight alternative to DeepEval, [RAGAS](https://docs.ragas.io/en/latest/index.html) as a toolset is easy to run and straightforward. However, RAGAS is limited to a small set of LLM-only metrics that would require us to use an additional framework on top of to utilize custom metrics. Metrics from RAGAS are implemented directly in DeepEval, so they can still be utilized with DeepEval.

**Arize Phoenix**: [Phoenix](https://phoenix.arize.com/) is another toolset focused on both evaluation and observability. Phoenix has a lot to offer in terms of visualizations and LLM tracing, but it's included evaluation tools were a little more limited in comparison to the other toolsets. These visualization and tracing tools are useful for investigating individual traces from a developer perspective, but don't provide direct advantages for sharing evaluation results/decisions with mission heroes. Additionally, considering that the source of your evaluations in Phoenix do not necessarily need to come from Phoenix, if llm tracing is a desired feature for developers or mission heroes, any source of evals can be integrated with this toolset.

**LangChain/LangSmith**: [LangChain](https://python.langchain.com/v0.1/docs/get_started/introduction/) is a framework for the development of LLM applications. LangChain provides tools for each stage of the development process, including development, productionization, and deployment. [LangSmith](https://python.langchain.com/v0.1/docs/langsmith/) is an observability tool using LangChain that assists with tracing and evaluating LLM applications. LangSmith provides built-in evaluators and flexibility for custom evaluators. However, it is heavily reliant on the LangChain ecosystem. Getting the most out of this approach would require sizeable refactoring of the LFAI codebase. Since LangChain/LangSmith are able to incorporate each of above toolsets directly (the other alternatives and the chosen toolset), we should be able to pivot to using LangChain/LangSmith for better model traceability in the future without having to pivot away from using DeepEval.

## Related ADRs
This ADR will eventually influence the ADR for overall LLM evaluations.

## References
- [DeepEval](https://docs.confident-ai.com/)
- [RAGAS](https://docs.ragas.io/en/latest/index.html)
- [Phoenix](https://phoenix.arize.com/)
- [LangChain](https://python.langchain.com/v0.1/docs/get_started/introduction/)
- [LangSmith](https://python.langchain.com/v0.1/docs/langsmith/)

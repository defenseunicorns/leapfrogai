# LeapfrogAI RAG Evaluations

## Table of Contents

- [LeapfrogAI RAG Evaluations](#leapfrogai-rag-evaluations)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
  - [Background](#background)
  - [Decision](#decision)
  - [Rationale](#rationale)
  - [Alternatives](#alternatives)
  - [Related ADRs](#related-adrs)
  - [References](#references)

## Status

PROPOSED

## Context

LeapfrogAI uses RAG to provide context-aware responses to users who have specific data they need to reference. In order to make sure RAG is operating at the levels we need it to, we need to get measurable feedback from our RAG pipeline to make it better. We also need a standard to show to mission heroes that we are in fact operating at that level. We do this with RAG-focused evaluations. This ADR Proposes **[DeepEval](https://docs.confident-ai.com/)** as the framework of choice for handling RAG evaluations.

## Decision

Handle RAG evaluation test cases using DeepEval.

## Rationale
The major RAG evaluation frameworks all revolve around LLM-enabled evaluations. While these are fast to get running and offer a lot of flexibility, our use case will likely demand custom evaluation metrics, likely consisting of heuristics testing that do not leverage LLMs for evaluation. Among the frameworks reviewed (see [Alernatives](#alternatives)), DeepEval was found to have the most flexibility in terms of custom evaluation metrics (llm-based and non-llm), as well as what models we want to use for evaluations. DeepEval also offers a toolset for generating evaluation datasets from documentation, which will assist in setting up the datasets used for evaluations. Lastly, DeepEval's test-focused approach will integrate well with the testing workflows in LeapfrogAI.

## Alternatives
**RAGAS**: A more lightweight alternative to DeepEval, [RAGAS](https://docs.ragas.io/en/latest/index.html) as a framework is easy to run and straightforward. However, RAGAS is limited to a small set of LLM-only metrics that would require us to use an additional framework on top of to utilize custom metrics. Metrics from RAGAS are implemented directly in DeepEval, so they can still be utilized with DeepEval.

**Arize Phoenix**: [Phoenix](https://phoenix.arize.com/) is another framework focused on both evaluation and observability. Phoenix has a lot to offer in terms of visualizations and LLM tracing, but it's included evaluation tools were a little more limited in comparison to the other frameworks. Considering that the source of your evaluations in Phoenix do not necessarily need to come from Phoenix, if llm tracing is a desired feature for developers or mission heroes, any source of evals can be integrated with this toolset.

## Related ADRs
This ADR will eventually influence the ADR for overall LLM evaluations.

## References
- [DeepEval](https://docs.confident-ai.com/)
- [RAGAS](https://docs.ragas.io/en/latest/index.html)
- [Phoenix](https://phoenix.arize.com/)

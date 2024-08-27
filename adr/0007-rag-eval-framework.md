# LeapfrogAI RAG Evaluation Framework

## Table of Contents

- [LeapfrogAI RAG Evaluation Framework](#leapfrogai-rag-evaluation-framework)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
  - [Context](#context)
  - [Decisions and Rationale](#decisions-and-rationale)
    - [Tools](#tools)
    - [Datasets](#datasets)
    - [Models to Evaluate](#models-to-evaluate)
    - [LLM-as-Judge / LLMs-as-Jury](#llm-as-judge--llms-as-jury)
    - [Metrics / Evaluations](#metrics--evaluations)
    - [Execution](#execution)
    - [Delivery](#delivery)
  - [Rationale](#rationale)
  - [Alternatives](#alternatives)
  - [Related ADRs](#related-adrs)
  - [References](#references)

## Status

DRAFT

## Context

LeapfrogAI uses RAG to provide context-aware responses to users who have specific data they need to reference. In order to make sure RAG is operating at the levels we need it to, we need to get measurable feedback from our RAG pipeline to make it better. We also need a standard to show to mission heroes that we are in fact operating at that level. We do this with RAG-focused evaluations. This ADR documents all of the decisions and lessons learned for enabling a full-scale RAG evaluations pipeline MVP.

## Decisions and Rationale

This section covers all of the decision points that needed to be made along side an explanation of how those decisions were made. Each section covers a different aspect of the RAG evaluations framework.

### Tools
<details>
  <summary>Details</summary>

  #### Decision
  The primary toolset for architecting RAG evaluations will be **[DeepEval](https://docs.confident-ai.com/)**.
  #### Rationale
  Please see the the [RAG Evaluations Toolset](/adr/0004-rag-eval-toolset.md) ADR for an in-depth discussion of why DeepEval was chosen over other alternatives.

</details>

### Datasets
<details>
  <summary>Details</summary>

  #### Decision
  To handle RAG evaluations, two types of datasets were determined to be needed:
  - Question/Answer (QA)
  - Needle in a Haystack (NIAH)

  A QA dataset should contain a set of [test cases](https://docs.confident-ai.com/docs/evaluation-test-cases) that have:
  - Questions, which will be prompted to the LLM
  - Ground truth answers, which will be used to compare against the generated answer by the LLM
  - Context, which will contain the correct piece of source documentation that supports the true answer
  - The full source documentation from which the context is derived

  A dataset for [NIAH Testing](https://arize.com/blog-course/the-needle-in-a-haystack-test-evaluating-the-performance-of-llm-rag-systems/) should contain:
  - A series of irrelevant texts of varying context length that have one point of information hidden within

  To support these needs, two datasets were created:
  - [LFAI_RAG_qa_v1](https://huggingface.co/datasets/defenseunicorns/LFAI_RAG_qa_v1)
  - [LFAI_RAG_niah_v1](https://huggingface.co/datasets/defenseunicorns/LFAI_RAG_niah_v1)

  These two datasets will be used as the basis for LFAI RAG evaluations that require data sources.

  #### Rationale

  These datasets were created because it filled a gap in the openly available datasets that could have been used. For example, in QA datasets, there did not exist any dataset that had all **4** components listed above. Many had the questions, answers, and context, but none also included the source documents in a readily accessible manner. Therefore, the fastest and most effective course of action was to generate a QA dataset from source documentation using the [DeepEval Synthesizer](https://docs.confident-ai.com/docs/evaluation-datasets-synthetic-data).

  As for the NIAH dataset, there was a similar "incompleteness" problem that was observed. While other iterations of NIAH datasets are more readily available than QA datasets, some [datasets](https://huggingface.co/datasets/nanotron/simple_needle_in_a_hay_stack) had haystacks constructed of small repeating sentences, which did not mirror what a deployment context is more likely to look like. Other implementations mirrored the original [NIAH experiment](https://x.com/GregKamradt/status/1722386725635580292?lang=en) using [Paul Graham essays](https://paulgraham.com/articles.html), but did not release their specific datasets. Therefore, it made sense to quickly generate a dataset that uses the same Paul Graham essays as context, while inserting individual "needles" into certain context lengths to create a custom dataset. LFAI_RAG_niah_v1 includes context lengths from 512 to 128k characters.

</details>

### Models to Evaluate
<details>
  <summary>Details</summary>

  #### Decision

  #### Rationale

</details>

### LLM-as-Judge / LLMs-as-Jury
<details>
  <summary>Details</summary>

  #### Decision

  #### Rationale

</details>

### Metrics / Evaluations
<details>
  <summary>Details</summary>

  #### Decision

  #### Rationale

</details>

### Execution
<details>
  <summary>Details</summary>

  #### Decision

  #### Rationale

</details>

### Delivery
<details>
  <summary>Details</summary>

  #### Decision

  #### Rationale

</details>

## Related ADRs
This ADR was influenced by the [RAG Evaluations Toolset](/adr/0004-rag-eval-toolset.md) ADR.

## References
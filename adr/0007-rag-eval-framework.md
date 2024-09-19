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
  - [Related ADRs](#related-adrs)
  - [References](#references)

## Status

DRAFT

## Context

LeapfrogAI uses RAG to provide context-aware responses to users who have specific data they need to reference. In order to make sure RAG is operating at the levels we need it to, we need to get measurable feedback from our RAG pipeline to make it better. We also need a standard to show to mission heroes that we are in fact operating at that level. We do this with RAG-focused evaluations. Additionally, utilizing evaluations as a whole and developing a standard approach will allow customizations of RAG and its components (for various deployment scenarios) to be better tested and evaluated against. This ADR documents all of the decisions and lessons learned for enabling a full-scale RAG evaluations pipeline MVP.

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

  These datasets were created because it filled a gap in the openly available datasets that could have been used. For example, in QA datasets, there did not exist any dataset that had all **4** components listed above. Many had the questions, answers, and context, but none also included the source documents in a readily accessible manner. Therefore, the fastest and most effective course of action was to generate a QA dataset from source documentation using the [DeepEval Synthesizer](https://docs.confident-ai.com/docs/evaluation-datasets-synthetic-data). The documentation that was used to create the QA dataset was chosen to be both representative of deployment needs (by including some DoD specific documentation) and a variety of topics (including technical documents and financial reports).

  As for the NIAH dataset, there was a similar "incompleteness" problem that was observed. While other iterations of NIAH datasets are more readily available than QA datasets, some [datasets](https://huggingface.co/datasets/nanotron/simple_needle_in_a_hay_stack) had haystacks constructed of small repeating sentences, which did not mirror what a deployment context is more likely to look like. Other implementations mirrored the original [NIAH experiment](https://x.com/GregKamradt/status/1722386725635580292?lang=en) using [Paul Graham essays](https://paulgraham.com/articles.html), but did not release their specific datasets. Therefore, it made sense to quickly generate a dataset that uses the same Paul Graham essays as context, while inserting individual "needles" into certain context lengths to create a custom dataset. LFAI_RAG_niah_v1 includes context lengths from 512 to 128k characters.

</details>

### Models to Evaluate
<details>
  <summary>Details</summary>

  #### Decision

  The three models that will initially be evaluated are going to be:

  - [SynthIA-7B](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GPTQ) (the initial default model for LeapfrogAI)
  - [Hermes 2 Pro](https://huggingface.co/defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g-GPTQ) (Defense Unicorns quantization)
  - [Llama3.1-8B](https://huggingface.co/unsloth/Meta-Llama-3.1-8B-bnb-4bit) (using a 4 bit quantization)

  GPT-4o will also be used as a point of comparison in the results.

  #### Rationale
  Three models were chosen to evaluate against initially in order to balance the scale between complexity and variety. There are endless variations of models that could be evaluated against, but these ones were chosen with specific reasons in mind.
  - **SynthIA-7B**: This model has been the default backbone of LeapfrogAI since the beginning and (at the time of writing this ADR) is still the default model deployment choice. It is a 4 bit QPTQ quantization, so it is small enough to load on edge deployments. It is also compatible with both backend deployment options: llama-cpp-python and vllm. As it is still the default model choice, it should be evaluated on to see how it performs as time has gone on.
  - **Hermes 2 Pro**: This model is a fine-tune of the Mistral-7b-Instruct model using the [OpenHermes-2.5](https://huggingface.co/datasets/teknium/OpenHermes-2.5) dataset. Hermes 2 Pro also includes [Hermes Function Calling](https://github.com/NousResearch/Hermes-Function-Calling). This particular model is a 4 bit GPTQ quantization on the [VMWare Open Instruct](https://huggingface.co/datasets/vmware/open-instruct) dataset that was generated by Defense Unicorns. Hermes 2 Pro advances on Mistral 7b with excellent general task and conversation capabilities and enhanced function calling and generation of JSON structured outputs. This model also meets the requirements of being small enough to load in edge deployment scenarios.
  - **Llama3.1-8B**: This model has been shown to be an exemplary addition to the small model space [(Model Card)](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md). With additional language capabilities (trained on 8 languages), the Llama3.1 family of models offers high performance under a variety of scenarios. The model that will be evaluated against is a 4 bit bnb quanitzation of LLama3.1-8B. This quantization again allows for smaller deployment scenarios and makes a more relevant comparison point to the models already in use within LeapfrogAI.

As time goes on, additional models will be considered and added as comparison points.

</details>

### LLM-as-Judge / LLMs-as-Jury
<details>
  <summary>Details</summary>

  #### Decision
  
  For the RAG Evals MVP, [Claude 3.5 Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet) by Anthropic will be used as a single LLM-as-Judge.

  #### Rationale
  
  There are two points to rationalize; the model choice and the decision to use a single judge.

  In order to reach an MVP product, a single LLM judge will be utilized for the evaluations that require it. This will be the first stage so that the evaluation framework can begin receiving results. As progress is made, additional LLM-based judges will be incorporated to develop an LLM-jury styled approach. For context, please see the following [paper](https://arxiv.org/pdf/2404.18796).

  Claude 3.5 Sonnet was chosen to be used as the first judge due to it's high levels of [performance](https://artificialanalysis.ai/models/claude-35-sonnet), which is crucial when utilizing an LLM judge. Additionally, it exists outside the family of models that will be evaluated against, which has been shown to be effective in comparison to using models of the same family due to [self-enhancement bias](https://arxiv.org/pdf/2306.05685).

</details>

### Metrics / Evaluations
<details>
  <summary>Details</summary>

  #### Decision
  
  The LeapfrogAI RAG evaluation framework will utilize the following evaluations:

  LLM-as-a-judge metrics to use:
  - [Contextual Recall](https://docs.confident-ai.com/docs/metrics-contextual-recall) (for evaluating retrieval)
  - [Answer Correctness](https://docs.confident-ai.com/docs/metrics-llm-evals) (for evaluating generation)
  - [Faithfulness](https://docs.confident-ai.com/docs/metrics-faithfulness) (for evaluating generation)
  
  Non-llm-enabled evaluations:
  - Needle in a Haystack (for evaluating retrieval and generation)
  - Annotation Relevancy (for evaluating retrieval)

  Performance Metrics:
  - Total Execution Runtime
  
  Non-RAG LLM benchmarks:
  - [HumanEval](https://docs.confident-ai.com/docs/benchmarks-human-eval) (for evaluating generation)

  #### Rationale

  These metrics were chosen to balance the explainability/understandability of non-LLM based evaluations and the flexibility/scalability of LLM-as-judge evaluations.
  - Contextual Recall: evaluates the extent to which the context retrieved by RAG corresponds to an expected output
  - Answer Correctness: evaluates if an answer generated by an LLM is accurate when compared to the question asked and its context
  - Faithfulness: evaluates whether an answer generated by an LLM factually aligns with the context provided
  - Needle in a Haystack (retrieval): determines if a needle of information is correctly retrieved from the vector store by RAG
  - Needle in a Haystack (response): determines if a needle of information is correctly given in the final response of the LLM in a RAG pipeline
  - HumanEval: Evaluates an LLM's code generation abilities (not RAG-enabled, but it useful as an established baseline to compare against)
  - Annotation Relevancy: A custom metric that measures how often documents that have nothing to do with the question are cited in the annotations. Higher is better

  While these metrics are going to be utilized first to balance value-gained and time to implement, we will be adding additional evaluation metrics soon following MVP status. Potential options include:
  - RAG retrieval Hit Rate: non-LLM metric that evaluates how often a retrieved context matches the expected context for a question/answer scenario
  - Performance metrics: non-LLM metrics that measure performance targets such as runtime, compute (cpu and gpu), etc. (requires a standarized deployment context)

</details>

### Execution/Delivery
<details>
  <summary>Details</summary>

  #### Decision
  For MVP status, we will be running the evaluation framework in one-off instances utilizing the `leapfrogai_evals` module. This module contains the runners for the current evaluations and measures the metrics that have been established thus far.

  #### Rationale
  In order to start getting feedback from evaluations, we simply need to get the results in whatever form we can. Since there is not an established cadence for how often evals will be run (a determination for post MVP), the storage of said evals does not need to be consistent at this time.

  The next steps for the execution and delivery of evals will likely be the following:
  - Using the `leapfrogai_evals` module, evaluations will be run at a regular cadence in a Github workflow so that we have a standardized way of running evaluations that we can compare against.
  - These evaluation results will be stored as artifacts in Github so that peformance can be tracked over time across version releases.

</details>

### Model Card
<details>
  <summary>Details</summary>

  #### Decision

  #### Rationale

</details>

## Related ADRs
This ADR was influenced by the [RAG Evaluations Toolset](/adr/0004-rag-eval-toolset.md) ADR.

## References

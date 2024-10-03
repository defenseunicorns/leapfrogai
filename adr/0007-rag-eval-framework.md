# LeapfrogAI RAG Evaluation Framework MVP

## Table of Contents

- [LeapfrogAI RAG Evaluation Framework MVP](#leapfrogai-rag-evaluation-framework-mvp)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
  - [Context](#context)
  - [Decisions and Rationale](#decisions-and-rationale)
    - [Tools](#tools)
    - [Datasets](#datasets)
    - [Models to Evaluate](#models-to-evaluate)
    - [LLM-as-Judge / LLMs-as-Jury](#llm-as-judge--llms-as-jury)
    - [Metrics / Evaluations](#metrics--evaluations)
    - [Execution / Delivery](#execution--delivery)
    - [Model Card](#model-card)
  - [Related ADRs](#related-adrs)
  - [References](#references)

## Status

APPROVED

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

  These two datasets will be used as the basis for MVP LeapfrogAI RAG evaluations that require data sources.

  Advanced versions of these datasets will be needed after MVP status as LeapfrogAI baseline performance grows. If baseline LeapfrogAI can pass all tests and score top marks on all metrics for these tests, then the tests lose their ability to assist in tracking growth over time.
  
  An advanced QA dataset differs in the following ways:
  - More documents to use as the basis for questions. This provides a larger pool that RAG has to perform retrieval on and provides more opportunities for question types
  - Narrow the scope of the types of documents used. By keeping the topics of each document more similar to each other, this makes retrieval a more difficult task

  An advanced NIAH dataset has the following:
  - A collection of documents (the haystack) where one document contains a target piece of information (the needle) hidden somewhere within
    - The documents should be of the same topic (or in other words, be semantically similar) so it's not obvious which document has the right information
    - The needle itself should also be topically related to the rest of the documents but identifiable as unique information (i.e this information should be not obvious and only exists in one location out of all the documents)

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

All of the above models have similar vRAM requirements (able to be run on < 16Gb of vRAM), similar parameter count (7-8 billion parameters), and the same quantization level (4-bit). By balancing these factors, we can verify that each of these models can be swapped out for another and the system requirements do not need to change. This will assist in being able to provide comparisons that are different by as few variables as possible.

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

  Claude 3.5 Sonnet was chosen to be used as the first judge due to it's high levels of [performance](https://artificialanalysis.ai/models/claude-35-sonnet), which is crucial when utilizing an LLM judge. Claude 3.5 Sonnet as compared to other models (as seen in it's [model card](https://www-cdn.anthropic.com/fed9cc193a14b84131812372d8d5857f8f304c52/Model_Card_Claude_3_Addendum.pdf)) outperforms other large models on various evaluation benchmarks. These benchmarks include:
  - MMLU (general multitask reasoning)
  - DROP (reading comprehension)
  - BIG-Bench Hard (mixed task evaluations)
  - Needle in a Haystack recall (for understanding lots of context)
  - XSTest (for testing rejection of harmful requests)

 By utilizing a model that outperforms other similarly large models on all of these tasks, we can have confidence that we are using the most capable LLM-as-judge model.

 Additionally, Claude 3.5 Sonnet exists outside the family of models that will be evaluated against, which has been shown to be effective in comparison to using models of the same family due to [self-enhancement bias](https://arxiv.org/pdf/2306.05685).

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
  
  Non-LLM-enabled evaluations:
  - Needle in a Haystack (for evaluating retrieval and generation)
  - Annotation Relevancy (for evaluating retrieval)

  Standard LLM benchmarks:
  - [HumanEval](https://docs.confident-ai.com/docs/benchmarks-human-eval) (for evaluating code generation)
  - [MMLU](https://docs.confident-ai.com/docs/benchmarks-mmlu) (for evaluating reasoning across multiple subjects; generation only)

  Performance Metrics:
  - Total Execution Runtime

  #### Rationale

  These metrics were chosen to balance the explainability/understandability of non-LLM based evaluations and the flexibility/scalability of LLM-as-judge evaluations.
  - Contextual Recall: evaluates the extent to which the context retrieved by RAG corresponds to an expected output
  - Answer Correctness: evaluates if an answer generated by an LLM is accurate when compared to the question asked and its context
  - Faithfulness: evaluates whether an answer generated by an LLM factually aligns with the context provided
  - Needle in a Haystack (retrieval): determines if a needle of information is correctly retrieved from the vector store by RAG
  - Needle in a Haystack (response): determines if a needle of information is correctly given in the final response of the LLM in a RAG pipeline
  - HumanEval: Evaluates an LLM's code generation abilities (not RAG-enabled, but useful as an established baseline to compare against)
  - MMLU: Evaluates an LLM's ability to reason on multiple task topics using multiple choice questions (not RAG-enabled, but useful as an established baseline to compare against)
  - Annotation Relevancy: A custom metric that measures how often documents that have nothing to do with the question are cited in the annotations. Higher is better

  Established LLM benchmarks (MMLU and HumanEval) are included in this MVP evaluation framework despite not requiring information from a retrieval system. It's important that this framework have a few generation-only metrics to be better at diagnosing whether issues in performance are happening due to RAG or the model. The other metrics included in this MVP evaluate either the retrieval stage on its own or the information-assisted generation. If the metrics evaluated on the information-assisted generation (e.g Faithfulness or NIAH response) are scoring low, it is difficult to parse out whether or not the low score is caused by the information retrieval, the generation itself, or both. Having these benchmarks provides a way to validate whether or not the generation works as expected, indicating a potential problem with the retrieval. These benchmarks are also standard, and therefore used across many LLMs. Therefore, these values can be used when comparing what performance is expected of these models and what is being observed in LeapfrogAI. These benchmarks can assist in diagnosing problems with both quantization (which often don't have these benchmarks) and implementation differences.

  While these metrics are going to be utilized first to balance value-gained and time to implement, we will be adding additional evaluation metrics soon following MVP status. Potential options include:
  - RAG retrieval Hit Rate: non-LLM metric that evaluates how often a retrieved context matches the expected context for a question/answer scenario
  - Performance metrics: non-LLM metrics that measure performance targets such as runtime, compute (cpu and gpu), etc. (requires a standarized deployment context)

</details>

### Execution / Delivery
<details>
  <summary>Details</summary>

  #### Decision
  For MVP status, we will be running the evaluation framework in one-off instances utilizing the `leapfrogai_evals` module. This module contains the runners for the current evaluations and measures the metrics that have been established thus far.

  #### Rationale
  In order to start getting feedback from evaluations, we simply need to get the results in whatever form we can. Since there is not an established cadence for how often evals will be run (a determination for post MVP), the storage of said evals does not need to be consistent at this time.

  The next steps for the execution and delivery of evals will likely be the following:
  - Using the `leapfrogai_evals` module, evaluations will be run at a regular cadence in a Github workflow so that we have a standardized way of running evaluations that we can compare against.
  - These evaluation results will be stored as artifacts in GitHub so that performance can be tracked over time across version releases.

</details>

### Model Card
<details>
  <summary>Details</summary>

  #### Decision
  
  The model card will ultimately exist in a few forms:

  - A tabular representation that shows for a given model (or hyperparameter configuration) as a row, the columns consist of all of the scored metrics that were applied to that configuration.
  - A deployed instance of LeapfrogAI will likely always accompany UDS runtime. The evaluation results for a deployment will live in a table under its corresponding UDS runtime page.
    - The evaluation outputs themselves will eventually be provided in `json` format for easier ingestion into observability tools or other additional frameworks.
    - This will likely become more relevant after MVP status.

  A model card report will consist of the table of evaluation metrics as well as a written summary of what the metrics mean, how they relate to specific performance considerations, as well as model recommendations. Therefore, this report can be   generalized for a wide audience, but will need to be customized for a given potential deployment scenario. A metrics table may look something like this:
  ![Screenshot from 2024-09-18 18-03-18](https://github.com/user-attachments/assets/479f385b-1d09-4842-b1f0-e2d8992b0b3d)

  #### Rationale

  The needs of the model card will likely evolve over time as the needs of delivering evaluations changes. This can be observed in three potential stages:
  - Near-term: evaluations benefit the product team to help identify new model choices for new defaults, diagnose implementation bugs, and evaluate upgrades to the RAG pipeline.
    - Data format needed: raw numbers, potentially in tabular format for ease of ingesting
  - Mid-term: evaluations on default model options for mission heroes are part of the delivery process. These recommendations are provided to assist mission heroes in selecting the models they want in their deployments.
    - Data format needed: same as near-term, but a higher emphasis on the report will be necessary
  - Long-term: evaluations are ingrained within all LeapfrogAI deployments to diagnose potential runtime issues and to evaluate multiple model options directly within the cluster
    - Data format needed: evaluations will need to be directly tied into other metrics-measuring tools, such as prometheus, to integrate directly into UDS runtime.
   
  By providing an iterable approach to delivering evaluation results, the model card's use-case will be able to evolve over time to scale to meet the needs of the product team, delivery team, and mission heroes.

</details>

## Related ADRs
This ADR was influenced by the [RAG Evaluations Toolset](/adr/0004-rag-eval-toolset.md) ADR.

## References

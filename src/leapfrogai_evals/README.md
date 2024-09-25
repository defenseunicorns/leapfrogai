# LeapfrogAI Evaluations

This covers how to use the evaluations present in LeapfrogAI. As more evaluations get added, these instructions will be updated.

## Running the Evaluations
The LeapfrogAI RAG evaluation system assumes the following:

- LeapfrogAI is deployed
- A valid LeapfrogAI API key is set (for more info, see the [API README](/src/leapfrogai_api/README.md))
- For all LLM-enabled metrics, a valid Anthropic API key is set

For the easiest setup, copy the `.env.example` file:

```bash
cp .env.example .env
```

Within `.env`, replace the necessary environment variables:

```bash
LEAPFROGAI_API_URL=<LeapfrogAI API url, usually: https://leapfrogai-api.uds.dev/openai/v1 for development>
LEAPFROGAI_API_KEY=<LeapfrogAI API key>
ANTHROPIC_API_KEY=<Anthropic API key>
```

Running `main.py` will by default run all of the evaluations currently available:

```bash
# from within the src/leapfrogai_evals dir
python -m pip install .
python main.py
```

## Question/Answer Evaluation

Question and answer pairs are a valuable setup for evaluating LLM systems as a hole. Within LeapfrogAI, this type of evaluation takes an input question, expected context, and expected output, and compares them to the retrieved context from RAG and the system's final output.

### Data
The LeapfrogAI QA evaluation uses a custom dataset available on HuggingFace: [defenseunicorns/LFAI_RAG_qa_v1](https://huggingface.co/datasets/defenseunicorns/LFAI_RAG_qa_v1)

LFAI_RAG_qa_v1 contains 36 question/answer/context entries that are intended to be used for LLM-as-a-judge enabled RAG Evaluations.

Example:

```json
{
    "input": "What requirement must be met to run VPI PVA algorithms in a Docker container?",
    "actual_output": null,
    "expected_output": "To run VPI PVA algorithms in a Docker container, the same VPI version must be installed on the Docker host.",
    "context": [
        "2.6.\nCompute\nStack\nThe\nfollowing\nDeep\nLearning-related\nissues\nare\nnoted\nin\nthis\nrelease.\nIssue\nDescription\n4564075\nTo\nrun\nVPI\nPVA\nalgorithms\nin\na\ndocker\ncontainer,\nthe\nsame\nVPI\nversion\nhas\nto\nbe\ninstalled\non \nthe\ndocker\nhost.\n2.7.\nDeepstream\nIssue\nDescription\n4325898\nThe\npipeline\ngets\nstuck\nfor\nmulti\u0000lesrc\nwhen\nusing\nnvv4l2decoder.\nDS\ndevelopers\nuse \nthe\npipeline\nto\nrun\ndecode\nand\ninfer\njpeg\nimages.\nNVIDIA\nJetson\nLinux\nRelease\nNotes\nRN_10698-r36.3\n|\n11"
    ],
    "source_file": "documents/Jetson_Linux_Release_Notes_r36.3.pdf"
}
```

### Experimental Design
The LeapfrogAI QA evaluation uses the following process:

- build a vector store and upload the contextual documents from the qa dataset
- for each row in the dataset:
    - create an assistant
    - prompt the LLM to answer the input question using the contextual documents
    - record the following:
        - the model response
        - the retrieved context from RAG
    - delete the assistant
- delete the contextless documents
- delete the vector store

Various metrics can then be calculated using these individual pieces.

## Needle in a Haystack (NIAH)

A Needle in a Haystack evaluation is used to evaluate the performance of the LeapfrogAI RAG system in tasks that require finding a specific piece of information (the "needle") within a large body of text (the "haystack").

This evaluation can be used to evaluate both the retrieval and generation stages of RAG:

- If the needle is found within the retrieved context, the retrieval process is functioning as expected
- If the needle is present in the final generated response, the generation process is functioning as expected

### Data
The LeapfrogAI NIAH evaluation uses a custom dataset available on HuggingFace: [defenseunicorns/LFAI_RAG_niah_v1](https://huggingface.co/datasets/defenseunicorns/LFAI_RAG_niah_v1)

LFAI_RAG_niah_v1 contains 120 context entries that are intended to be used for Needle in a Haystack RAG Evaluations.

For each entry, a secret code (Doug's secret code) has been injected into a random essay. This secret code is the "needle" that is the goal to be found by an LLM.

Example:

```json
{
  "context_length":512,
  "context_depth":0.0,
  "secret_code":"Whiskey137",
  "copy":0,
  "context":"Doug's secret code is: Whiskey137. Remember this. Venture funding works like gears. A typical startup goes through several rounds of funding, and at each round you want to take just enough money to reach the speed where you can shift into the next gear.\n\nFew startups get it quite right. Many are underfunded. A few are overfunded, which is like trying to start driving in third gear."
}
```

### Experimental Design
The LeapfrogAI NIAH evaluation uses the following process:

- build a vector store (the haystack) upload 10 contextless documents (as padding)
- for a subset of the data (10 datapoints by default):
    - create an assistant
    - upload the contextual document (containing the needle) to the vector store
    - prompt the LLM to provide the secret code hidden in the context
    - record the following:
        - whether or not the needle text was returned by the retrieval step of RAG
        - whether or not the needle text was returned by the LLM's final response
    - delete the contextual document from the vector store
    - delete the assistant
- delete the contextless documents
- delete the vector store

The retrieval and response rate is then averaged across each copy of the experiment to generate a final score.

## Established Benchmark Evaluations

### MMLU

The [Massive Multitask Language Understanding (MMLU)](https://arxiv.org/abs/2009.03300) benchmark is widely-used in the evaluation of large language models on academic and professional tasks. It consists of 57 tasks across disciplines including mathe, history, biology, law, etc. These tasks reflect the kind of questions students and professionals might encounter, making the benchmark a good test of a model's knowledge and reasoning abilities across different fields.

MMLU is a multiple-choice evaluation, meaning that it focuses more on the logical reasoning behind the questions and less about the specific generation process.

Within the LeapfrogAI evaluation framework, The [DeepEval Implementation of MMLU](https://docs.confident-ai.com/docs/benchmarks-mmlu) is utilized. Additionally, a default subset of 6 topically relevant tasks out of the total 57 tasks are tested against, including: College Computer Science, US Foreign Policy, High School Government and Politics, Formal Logic, Computer Security, and Security Studies. This subset was chosen as the full MMLU evaluation takes a long time to process. Larger evaluation sessions should utilize the entire task set.

### HumanEval

The [HumanEval](https://github.com/openai/human-eval) benchmark is a dataset designed to evaluate an LLM's code generation capabilities. The benchmark consists of 164 hand-crafted programming challenges comparable to simple software interview questions.

HumanEval code snippets are generated from docstrings into Python-executable code. The primary metric utilized is the pass@k metric, which measures the probability that at least one of the top k code snippets generated by the LLM passes all the test cases.

Within the LeapfrogAI evaluation framework, The [DeepEval Implementation of HumanEval](https://docs.confident-ai.com/docs/benchmarks-human-eval) is utilized. Additionally, a default subset of 50 code generation tasks out of the total 164 are tested against. This was chosen as the full HumanEval evaluation takes a long time to process. Larger evaluation sessions should utilize the entire task set.

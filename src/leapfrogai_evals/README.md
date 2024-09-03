# LeapfrogAI Evaluations

This covers how to use the evaluations present in LeapfrogAI. As more evaluations get added, these instructions will be updated.

## Running the Evaluations
The LeapfrogAI RAG evaluation system assumes the following:

- LeapfrogAI is deployed
- A valid LeapfrogAI API key is set (for more info, see the [API README](/src/leapfrogai_api/README.md))

Set the following environment variables:

```bash
LEAPFROGAI_API_URL=<LeapfrogAI API url, usually: https://leapfrogai-api.uds.dev/openai/v1 for development>
LEAPFROGAI_API_KEY=<LeapfrogAI API key>
MODEL_TO_EVALUATE="vllm" # can also be provided as "model" to the __init__ for the runner
```

Running `main.py` will by default run all of the evaluations currently available:

```bash
# from within the packages/evaluations dir
python -m pip install .
python src/main.py
```

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

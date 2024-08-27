# LeapfrogAI Evaluations

This covers how to use the evaluations present in LeapfrogAI. As more evaluations get added, these instructions will be updated.

## Running the Evaluations

Running `main.py` will by default run all of the evaluations currently available:

```bash
# from within the src/evaluations dir
python -m pip install .
python main.py
```

## Needle in a Haystack (NIAH)

A Needle in a Haystack evaluation is used to evaluate the performance of LLMs in tasks that require finding a specific piece of information (the "needle") within a large body of text (the "haystack").

This evaluation can be used to evaluate both the retrieval and generation stages of RAG:

- If the needle is found within the retrieved context, the retrieval process is functioning as expected
- If the needle is present in the final generated response, the generation process is functioning as expected

### Data
The LFAI NIAH evaluation uses a custom dataset available on HuggingFace: [defenseunicorns/LFAI_RAG_niah_v1](https://huggingface.co/datasets/defenseunicorns/LFAI_RAG_niah_v1)

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
The LFAI NIAH evaluation uses the following process:

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
- average the retrieval scores as the final retrieval score
- average the response scores as the final response score

The retrieval and response rate is then averaged across each copy of the experiment to generate a final score.

### Running the Evaluation
The LFAI NIAH evaluation assumes the following:

- LFAI is deployed
- A valid LFAI API key is set

Set the following environment variables:

```bash
LEAPFROGAI_API_URL=<lfai api url, usually: https://leapfrogai-api.uds.dev/openai/v1 for development>
LEAPFROGAI_API_KEY=<lfai api key>
```

You can then run the evaluation in a script with the following:

```python
from niah_runner import NIAH_Runner

runner = NIAH_Runner() # see input parameters

runner.evaluate() # run the evaluation

runner.generate_report() # generate a heatmap with the results
```

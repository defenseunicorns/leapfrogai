---
title: App Development with LeapfrogAI
type: docs
weight: 1
---

Prior to developing applications using LeapfrogAI, ensure that you have a valid instance of LeapfrogAI deployed in your environment. See the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/) page for more info on how to get started.

## OpenAI Compatibility in LeapfrogAI

The LeapfrogAI API is an OpenAI-compatible API, meaning that the endpoints built out within the LeapfrogAI API as what is found within the OpenAI API. **Note:** Not all endpoints/functionality in OpenAI is implemented in LeapfrogAI. To see what endpoints are implemented in your deployment, reference the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#checking-deployment) guide for how to check the API reference.

## Basic Usage of the OpenAI SDK with LeapfrogAI

### OpenAI API Reference

The best place to look for help with using the OpenAI SDK is to refer to the [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction), so it is recommended to return to this reference when understanding how specific endpoints work.

### Getting a LeapfrogAI API Key

In order to utilize the LeapfrogAI API outside of the User Interface, you'll need to get an API key. This can be done one of two ways:

#### Via the UI

The easiest way to create a LeapfrogAI API key is via the user interface. Perform the following in the UI (reference the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#checking-deployment) guide for where the UI is deployed):

- Select the **Settings** icon ⚙️ in the top-right corner
- Select **API Keys**
- Select **Create New**
  - Provide a name for the API key
  - Choose a lifespan for the API key
- Select **Create**
- Copy the API for future use

#### Via the deployment

If you prefer not use the UI (or the UI is not deployed), you can use the following guides to create an API key:

1-hour JWT via Supabase: [instructions](https://github.com/defenseunicorns/leapfrogai/blob/main/packages/supabase/README.md#troubleshooting)

Long-lived API key via the API: [instructions](https://github.com/defenseunicorns/leapfrogai/blob/main/src/leapfrogai_api/README.md#running)

### Install dependencies

It's recommended to be using Python version `3.11.6` or greater.

You'll need the pip Python package manager and the OpenAI SDK:

```bash
pip install openai
```

### Creating the Client

Now that you have your API key, you can create an OpenAI client using LeapfrogAI on the backend in a Python script:

```python
import openai

# set base url and api key (recommended that these are set as env vars)
LEAPFROGAI_API_KEY="api-key" # insert actual API key here
LEAPFROGAI_API_URL="https://leapfrogai-api.uds.dev" # the API may be at a different URL

# create an openai client
client = openai.OpenAI(api_key=LEAPFROGAI_API_KEY, base_url=LEAPFROGAI_API_URL+"/openai/v1")
```

### Running Chat Completions

Now that you have a client created, you can utilize it to handle basic chat completion requests:

```python
... # using the same code from above

completion = client.chat.completions.create(
  model="vllm", # in LFAI, the "model" refers to the backend which services the model itself
  messages=[
      {
          "role": "user",
          "content": "Please tell me a fun fact about frogs.",
      }
  ]
)
```

This is just a basic example; check out the [chat completion reference](https://platform.openai.com/docs/api-reference/chat/create) for more options!

## Building a RAG Pipeline using Assistants

Now that we've seen a basic example, let's leverage OpenAI assistants using LeapfrogAI to handle a more complex task: [**Retrieval Augmented Generation (RAG)**](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/).

We'll break this example down into a few steps:

### Requirements

Referencing the [Basic Usage](#basic-usage-of-the-openai-sdk-with-leapfrogai) section, you'll need:

- A LeapfrogAI API key
- The URL of the LeapfrogAI API instance you'll be using
- An OpenAI Client using LeapfrogAI

### Create a Vector Store

A [vector database](https://www.pinecone.io/learn/vector-database/) is a fundamental piece of RAG-enabled systems. Vector databases store vectorized representations of  and creating one is the first step to building a RAG pipeline.

Assuming you've created an OpenAI client as detailed above, create a vector store:

```python
# create a vector store
vector_store = client.beta.vector_stores.create(
    name="RAG Demo Vector Store",
    file_ids=[],
    expires_after={"anchor": "last_active_at", "days": 5},
    metadata={"project": "RAG Demo", "version": "0.1"},
)
```

### Upload a file

Now that you have a vector store, let's add some documents. For a simple example, let's assume you have two text files with the following contents:

**doc_1.txt**

```text
Joseph has a pet frog named Milo.
```

**doc_2.txt**

```text
Milo the frog's birthday is on October 7th.
```

Create these documents so you can add them to the vector store:

```python
# upload some documents
documents = ['doc_1.txt','doc_2.txt']
for doc in documents:
    with open(doc, "rb") as file: # read these files in binary mode
        _ = client.beta.vector_stores.files.upload(
            vector_store_id=vector_store.id, file=file
        )
```

When you upload files to a vector store, this creates a `VectorStoreFile` object. You can record these for later usage, but for now they aren't needed for simple chatting with your documents.

### Create an Assistant

[OpenAI Assistants](https://platform.openai.com/docs/assistants/overview) carry specific instructions and can reference specific tools to add functionality to your workflows. In this case, we'll add the ability for this assistant to search files in our vector store using the `file_search` tool:

```python
# these instructions are for example only, your use case may require different directions
INSTRUCTIONS = """
  You are a helpful AI bot that answers questions for a user. Keep your response short and direct.
  You may receive a set of context and a question that will relate to the context.
  Do not give information outside the document or repeat your findings.
"""

# create an assistant
assistant = client.beta.assistants.create(
    name="Frog Buddy",
    instructions=INSTRUCTIONS,
    model="vllm",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {"vector_store_ids": [vector_store.id]}
    },
)
```

### Create a Thread and Get Messages

Now that we have an assistant that is able to pull context from our vector store, let's query the assistant. This is done with the assistance of threads and runs (see the [assistants overview](https://platform.openai.com/docs/assistants/overview) for more info).

We'll make a query specific to the information in the documents we've uploaded:

```python
# this query can only be answered using the uploaded documents
query = "When is the birthday of Joseph's pet frog?"

# create thread
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=query,
)

# create run
run = client.beta.threads.runs.create_and_poll(
    assistant_id=assistant.id, thread_id=thread.id
)
```

You'll notice that both documents are needed in order to answer this question. One contains the actual birthday date, while the other contains the relationship information between Joseph and Milo the frog. This is one of the reasons LLMs are utilized when extracting information from documents; they can integrate specific pieces of information across multiple sources.

### View the Response

With the run executed, you can now list the messages associated with that run to get the response to our query.

```python
# get messages
messages = client.beta.threads.messages.list(
    thread_id=thread.id, run_id=run.id
).data

# print messages
print(messages[1].content[0].text.value)
# we need the second message in the list, as the first one is associated with our request to the LLM
```

The output will look something like this:

```text
The birthday of Joseph's pet frog, Milo, is on October 7th. 【4:0†doc_2.txt】 【4:0†doc_1.txt】
```

As you can see, our Frog Buddy assistant was able to recieve the contextual information it needed in order to know how to answer the query. You'll also notice that the attached annotations correspond to the files we uploaded earlier, so we know we're pulling our information from the right place!

This just scratches the surface of what you can create with the OpenAI SDK leveraging LeapfrogAI. This may be a simple example that doesn't necessarily require the added overhead of RAG, but when you need to search for information hidden in hundreds or thousands of documents, you may not be able to hand your LLM all the data at once, which is where RAG really comes in handy.

As a reminder, the [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction) has lots of information on using the OpenAI SDK, and much of it is compatible with LeapfrogAI!

## Questions/Feedback

If you have any questions, feedback, or specific update requests on this development guide, please open an issue on the [LeapfrogAI Github Repository](https://github.com/defenseunicorns/leapfrogai). Additionally, if you have specific feature requests for the LeapfrogAI API (for example, certain endpoints that are not yet compatible with OpenAI), please create an issue in Github.

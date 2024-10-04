---
title: App Development with LeapfrogAI
type: docs
weight: 1
---

Prior to developing applications using LeapfrogAI, ensure that you have a valid instance of LeapfrogAI deployed in your environment. See the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/) page for more info on how to get started.

## OpenAI Compatibility in LeapfrogAI

The LeapfrogAI API is an OpenAI-compatible API, meaning that the endpoints built out within the LeapfrogAI API as what is found within the OpenAI API. **Note:** Not all endpoints/functionality in OpenAI is implemented in LeapfrogAI. To see what endpoints are implemented in your deployment, reference the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#checking-deployment) guide for how to check the API reference.

## Using the OpenAI SDK with LeapfrogAI

### OpenAI API Reference

The best place to look for help with using the OpenAI SDK is to refer to the [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction), so it is recommended to return to this reference when understanding how specific endpoints work.

### Getting a LeapfrogAI API Key

In order to utilize the LeapfrogAI API outside of the User Interface, you'll need to get an API key. This can be done one of two ways:

#### Via the UI

To create a LeapfrogAI API key via the user interface, perform the following in the UI (reference the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#checking-deployment) guide for where the UI is deployed):
- Select the **Settings** icon ⚙️ in the top-right corner
- Select **API Keys**
- Select **Create New**
  - Provide a name for the API key
  - Choose a lifespan for the API key
- Select **Create**
- Copy the API for future use

#### Via the deployment

TODO: Write this

### Creating the Client

Now that you have your API key, you can create an OpenAI client using LeapfrogAI on the backend:

```python
import openai

# set base url and api key (recommended that these are set as env vars)
LEAPFROGAI_API_KEY="api-key" # insert actual API key here
LEAPFROGAI_API_URL="https://leapfrogai-api.uds.dev" # the API may be at a different URL

# create an openai client
client = openai.OpenAI(api_key=LEAPFROGAI_API_KEY, base_url=LEAPFROGAI_API_URL+"/openai/v1")
```

### Running Chat Completions

Now that you have a client created, you can utilize it (with LeapfrogAI on the backend) to handle basic chat completion requests:

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

### Building a RAG Pipeline using Assistants

Now that we've seen a basic example, let's leverage OpenAI assistants using LeapfrogAI to handle a more complex task: Retrieval Augmented Generation (RAG)

We'll break this example down into a few step:

#### Create a Vector Store

#### Upload a file

#### Create an Assistant

Assuming you've created an OpenAI as detailed above, create an assistant:

```python
# these instructions are for example only, your use case may require more explicit directions
instructions = """
  You are a helpful, frog-themed AI bot that answers questions for a user. Keep your response short and direct.
  You may receive a set of context and a question that will relate to the context.
  Do not give information outside the document or repeat your findings.
"""

# create an assistant
assistant = client.beta.assistants.create(
    name="Frog Buddy",
    instructions=instructions,
    model="vllm",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {"vector_store_ids": [self.vector_store.id]}
    },
)
```
#### Create a Thread and Get Messages

```python
# create thread
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=message_prompt,
)

# create run
run = client.beta.threads.runs.create_and_poll(
    assistant_id=assistant.id, thread_id=thread.id
)

# get messages
messages = self.client.beta.threads.messages.list(
    thread_id=thread.id, run_id=run.id
).data

```


## Questions/Feedback

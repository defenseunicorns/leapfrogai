# Leapfrog AI


## OpenAI Server

The OpenAI API service is hosted and then uses GRPC to talk to the embedding server and the alpaca-lora-7B instance


## Create the API Server

models should point to the embedding and the 


```python

import openai

# Put anything you want in `API key`
openai.api_key = 'Free the models'

# Point to your own url
openai.api_base = "https://leapfrogai.tom.bigbang.dev"
# openai.api_base = "http://127.0.0.1:8080"
print(openai.Model.list())
openai.Embedding.create(input="hello there what does this do",model="text-embedding-ada-002")
completion = openai.Completion.create(model="llama-7B-4b", prompt="Hello everyone this is")
print(completion)
 ```



 ```python
response = openai.Completion.create(
  model="llama-7B-4b",
  prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
  temperature=0.9,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)
```


```python
response = openai.Completion.create(
  model="llama-7B-4b",
  prompt="You: What have you been up to?\nFriend: Watching old movies.\nYou: Did you watch anything interesting?\nFriend:",
  temperature=0.5,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.5,
  presence_penalty=0.0,
  stop=["You:"]
)
print(response.choices[0].text)
```





## TODO

### Data
* add full wikipedia as datasource

### Notebooks

* Write weaviate notebook for ingesting into weaviate

### Chat

* Update the chat to use weaviate
* Update to return the docs used for the context of the chat, not just the response

### Weaviate

* Weaviate can't seem to override how to access OpenAI: https://github.com/weaviate/weaviate/blob/f6e9c715f61e7687e817980f65b76a4f69ed3867/modules/generative-openai/clients/openai.go#L42
* update the schema to also hold the URLs/filenames
* update the query to return the URLs and filenames
* Add variables to zarf package
* Set default vectorizer?  is this supposed to be the API service?
* weaviate metrics
![LeapfrogAI Logo](docs/imgs/leapfrogai.png)

## Table of Contents
1. [Project Goal](#project-goal)
2. [Why Host Your Own LLM?](#why-host-your-own-llm)
3. [Features](#features)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Project Goal <a name="project-goal"></a>

LeapfrogAI is designed to provide AI-as-a-service in egress limited environments. This project aims to bridge the gap between resource-constrained environments and the growing demand for sophisticated AI solutions, by enabling the hosting of APIs that provide AI-related services.

Our services include vector databases, completions with models like Large Language Models (LLMs), and the creation of embeddings. These AI capabilities can be easily accessed and integrated with your existing infrastructure, ensuring the power of AI can be harnessed irrespective of your environment's limitations.

## Why Host Your Own LLM? <a name="why-host-your-own-llm"></a>

Large Language Models (LLMs) are a powerful resource for AI-driven decision making, content generation, and more. However, the use of cloud-based LLMs can introduce limitations such as:

* **Data Privacy and Security**: Sending sensitive information to a third-party service may not be suitable or permissible for all types of data or organizations. By hosting your own LLM, you retain full control over your data.

* **Cost**: Pay-as-you-go AI services can become expensive, especially when large volumes of data are involved. Running your own LLM can often be a more cost-effective solution in the long run.

* **Customization and Control**: By hosting your own LLM, you have the ability to customize the model's parameters, training data, and more, tailoring the AI to your specific needs.

* **Latency**: If your application requires real-time or near-real-time responses, hosting the model locally can significantly reduce latency compared to making a round trip to a remote API.

## Features <a name="features"></a>

* LeapfrogAI provides an API that closely matches that of OpenAI's. This feature allows tools that have been built with OpenAI/ChatGPT to function seamlessly with LeapfrogAI as a backend. This compatibility greatly simplifies the transition process for developers familiar with OpenAI's API, and facilitates easy integration with existing systems.

* Vector Databases: Our vector database service allows you to perform efficient similarity searches on large scale databases. This feature can be utilized to augment prompts with responses from VectorDBs, enhancing the contextual awareness of the model.

* Fine-Tuning Models: One of the key strengths of LeapfrogAI is its ability to leverage customer specific data. We provide capabilities to fine-tune models with your data, enabling the AI to better understand your domain and provide more accurate and contextually relevant outputs.

* Embeddings Creation: Embeddings are fundamental to the working of many AI algorithms. LeapfrogAI provides services to generate embeddings which can be used for a variety of tasks such as semantic similarity, clustering, and more.

## Getting Started <a name="getting-started"></a>

### Setting up the Kubernetes Cluster

#### K3d

Zarf-k3d with custom image:

* publish this as an actual package and create install instructions
https://github.com/runyontr/zarf-package-k3d


Deployment of Leapfrog AI requires a Kubernetes environment with at least 1 GPU to handle the StableLM-3B model that is deployed by default.  To perform an installation

```shell
zarf init -a amd64
zarf package deploy oci://ghcr.io/defenseunicorns/packages/big-bang-distro-k3d/big-bang-distro-k3d:0.0.1-amd64
```


#### EKSCTL

```shell
eckctl create cluster -f config.yaml
zarf init -a amd64
zarf package deploy oci://ghcr.io/defenseunicorns/packages/big-bang-distro-k3d/big-bang-distro-k3d:0.0.1-amd64
```


### Deploy

```shell
zarf package create
zarf package deploy zarf-package-leapfrogai-amd64-0.1.1.tar.zst
```

### Configure DNS

Ensure that the DNS record for `*.bigbang.dev` points to the load balancher for Istio.  By default this DNS record points at localhost, so for the k3d deployment, this should work out of the box with the loadbalancers configured.  For a remote EKS deployment, you may need to 


The OpenAI API service is hosted and then uses GRPC to talk to the embedding server and the alpaca-lora-7B instance


## Usage <a name="usage"></a>

Reference one of the ipythonnotebooks that showcase a simple getting started.


# Leapfrog AI

Leapfrog AI is a deployable AI-as-a-service that brings the capabilities of AI models to egress limited environments by allowing teams to deploy APIs that mirror OpenAI's spec.  Teams are able to use tools built around OpenAIs models in their own environment, preventing the release of propriatary and sensive data to SaaS tools.

In addition, tools like [Weaviate](https://weaviate.io/) are deployed to allow for the creation of content augmented applications.


## Create the API Server

See the [Getting Started Notebook](notebooks/gettingstarted.ipynb) for example of using the API with the openai python module.



## TODO

### LeapfrogAI
* Turn into Helm Chart
* Make into Zarf Package

### Data
* add full wikipedia as datasource
* GitHub repos
  * all DU ones
  * K8s
  * helm charts
  * ???

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

### Model
* Add 3b model
* red pajama
* stable LLM
* repelet
* multiGPU for larger models 
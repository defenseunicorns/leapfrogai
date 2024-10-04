# LeapfrogAI API

> [!IMPORTANT]
> See the [API package documentation](../../packages/api/README.md) for general pre-requisites, dependent components, and package deployment instructions

This document is only applicable for spinning up the API in a local Python development environment.

## Local Development Setup

> [!IMPORTANT]
> Execute the following commands from this sub-directory

### Running

> [!IMPORTANT]
> The following steps assume that you already have a deployed and accessible UDS Kubernetes cluster and LeapfrogAI. Please follow the steps within the [DEVELOPMENT.md](../../docs/DEVELOPMENT.md) for details.

1. Install dependencies

    ```bash
    make install
    ```

2. Create a config.yaml using the config.example.yaml as a template.

3. Run the FastAPI application

    ```bash
    make dev API_PORT=8080
    ```

4. Create an API key with test user "leapfrogai@defenseunicorns.com" and test password "password", lasting 30 days from creation time

    ```bash
    # If the in-cluster API is up, and not testing the API workflow
    make api-key API_BASE_URL=http://localhost:8080
    ```

    To create a new 30-day API key, use the following:

    ```bash
    # If the in-cluster API is up, and not testing the API workflow
    make new-api-key API_BASE_URL=http://localhost:8080
    ```

    The newest API key will be printed to a `.env` file located within this directory.

5. Make calls to the API Swagger endpoint at `http://localhost:8080/docs` using your API token as the `HTTPBearer` token.

    - Hit `Authorize` on the Swagger page to enter your API key

### Access

See the ["Access" section of the DEVELOPMENT.md](../../docs/DEVELOPMENT.md#access) for different ways to connect the API to a model backend or Supabase.

### Tests

See the [tests directory documentation](../../tests/README.md) for more details.

### Reranking Configuration

The LeapfrogAI API includes a Retrieval Augmented Generation (RAG) pipeline for enhanced question answering. This section details how to configure its reranking options. All RAG configurations are managed through the `/leapfrogai/v1/rag/configure` API endpoint.

#### 1. Enabling/Disabling Reranking

Reranking improves the accuracy and relevance of RAG responses. You can enable or disable it using the `enable_reranking` parameter:

* **Enable Reranking:** Send a PATCH request to `/leapfrogai/v1/rag/configure` with the following JSON payload:

```json
{
  "enable_reranking": true
}
```

* **Disable Reranking:**  Send a PATCH request with:

```json
{
  "enable_reranking": false
}
```

#### 2. Selecting a Reranking Model

Multiple reranking models are supported, each offering different performance characteristics.  Choose your preferred model using the `ranking_model` parameter.  Ensure you've installed any necessary Python dependencies for your chosen model (see the [rerankers library documentation](https://github.com/AnswerDotAI/rerankers) on dependencies).

* **Supported Models:**  The system supports several models, including (but not limited to) `flashrank`, `rankllm`, `cross-encoder`, and `colbert`.  Refer to the [rerankers library documentation](https://github.com/AnswerDotAI/rerankers) for a complete list and details on their capabilities.

* **Model Selection:** Use a PATCH request to `/leapfrogai/v1/rag/configure` with the desired model:

```json
{
  "enable_reranking": true,  // Reranking must be enabled
  "ranking_model": "rankllm" // Or another supported model
}
```

#### 3. Adjusting the Number of Results Before Reranking (`rag_top_k_when_reranking`)

This parameter sets the number of top results retrieved from the vector database *before* the reranking process begins. A higher value increases the diversity of candidates considered for reranking but also increases processing time. A lower value can lead to missing relevant results if not carefully chosen. This setting is only relevant when reranking is enabled.

* **Configuration:** Use a PATCH request to `/leapfrogai/v1/rag/configure` to set this value:

```json
{
  "enable_reranking": true,
  "ranking_model": "flashrank",
  "rag_top_k_when_reranking": 150 // Adjust this value as needed
}
```

#### 4. Retrieving the Current RAG Configuration

To check the current RAG configuration (including reranking status, model, and `rag_top_k_when_reranking`), send a GET request to `/leapfrogai/v1/rag/configure`. The response will be a JSON object containing all the current settings.

#### 5.  Example Configuration Flow

1. **Initial Setup:**  Start with reranking enabled using the default `flashrank` model and a `rag_top_k_when_reranking` value of 100.

2. **Experiment with Models:**  Test different reranking models (`rankllm`, `colbert`, etc.) by changing the `ranking_model` parameter and observing the impact on response quality.  Adjust `rag_top_k_when_reranking` as needed to find the optimal balance between diversity and performance.

3. **Fine-tuning:** Once you identify a suitable model, fine-tune the `rag_top_k_when_reranking` parameter for optimal performance.  Monitor response times and quality to determine the best setting.

4. **Disabling Reranking:** If needed, disable reranking by setting `"enable_reranking": false`.

Remember to always consult the [rerankers library documentation](https://github.com/AnswerDotAI/rerankers) for information on supported models and their specific requirements.  The API documentation provides further details on request formats and potential error responses.

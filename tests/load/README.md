# LeapfrogAI Load Tests

These tests check the API's ability to handle different amounts of load. The tests simulate a specified number of users hitting the endpoints with some number of requests per second.

## Pre-Requisites

Before running the tests, ensure that your API URL and API key are properly configured in your environment variables. Follow these steps:

1. Set the API URL:

   ```bash
   export API_URL="https://leapfrogai-api.uds.dev"
   ```

2. Set the API token:

   ```bash
   export BEARER_TOKEN="<your-api-key-here>"
   ```

   **Note:** See the [API documentation](../../src/leapfrogai_api/README.md) to create an API key.

3. (Optional) - Set the model backend, this will default to `vllm` if unset:

   ```bash
   export DEFAULT_MODEL="llama-cpp-python"
   ```

## Running the Tests

To start the Locust web interface and run the tests:

1. Install dependencies from the project root.

   ```bash
   pip install ".[dev]"
   ```

2. Navigate to the directory containing `loadtest.py`.

3. Execute the following command:

   ```bash
   locust -f loadtest.py --web-port 8089
   ```

4. Open your web browser and go to `http://0.0.0.0:8089`.

5. Use the Locust web interface to configure and run your tests:
   - Set the number of users to simulate
   - Set the spawn rate (users per second)
   - Choose the host to test against (should match your `API_URL`)
   - Start the test and monitor results in real-time

# LeapfrogAI Load Tests

## Overview

These tests check the API's ability to handle different amounts of load. The tests simulate a specified number of users hitting the endpoints with some number of requests per second.

# Requirements

### Environment Setup

Before running the tests, ensure that your API URL and bearer token are properly configured in your environment variables. Follow these steps:

1. Set the API URL:
   ```bash
   export API_URL="https://leapfrogai-api.uds.dev"
   ```

2. Set the API token:
   ```bash
   export BEARER_TOKEN="<your-supabase-jwt-here>"
   ```

   **Note:** The bearer token should be your Supabase user JWT. For information on generating a JWT, please refer to the [Supabase README.md](../../packages/supabase/README.md). While an API key generated from the LeapfrogAI API endpoint can be used, it will cause the token generation load tests to fail.

3. (Optional) - Set the model backend, this will default to `vllm` if unset:
      ```bash
   export DEFAULT_MODEL="llama-cpp-python"
   ```

## Running the Tests

To start the Locust web interface and run the tests:

1. Navigate to the directory containing `loadtest.py`.

2. Execute the following command:
   ```bash
   locust -f loadtest.py --web-port 8089
   ```

3. Open your web browser and go to `http://0.0.0.0:8089`.

4. Use the Locust web interface to configure and run your tests:
   - Set the number of users to simulate
   - Set the spawn rate (users per second)
   - Choose the host to test against (should match your `API_URL`)
   - Start the test and monitor results in real-time
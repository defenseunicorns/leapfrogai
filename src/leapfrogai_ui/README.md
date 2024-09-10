# LeapfrogAI UI

> [!IMPORTANT]
> See the [UI package documentation](../../packages/UI/README.md) for general pre-requisites, dependent components, and package deployment instructions

This document is only applicable for spinning up the UI in a local Node development environment.

## Local Development Setup

> [!IMPORTANT]
> Execute the following commands from this sub-directory

### Running

1. Install dependencies

   ```bash
   npm install
   ```

2. Create a .env using the .env.example as a template.

3. Some backend functionality within the app requires libreoffice (for converting files to PDFs). While not required for 
   the app to run, if you are running the app locally without using the Dockerfile (e.g. via npm run dev), you will 
   need to install libreoffice.

   ex. ```brew install libreoffice``` or ```sudo apt install libreoffice```

3. Run the Node application and open in your default browser

   ```bash
   npm run dev -- --open
   ```

### Building

To create a production version of the app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

### Configuration Options

#### API

It is recommended to run LeapfrogAI with UDS, but if you want to run the UI locally (on localhost, e.g. for local development),
you can either:

1. Connect to a UDS deployed version of the LeapfrogAI API and Supabase

   **OR**

2. Connect to OpenAI and UDS deployed Supabase or locally running Supabase.

**NOTE:** most data CRUD operations utilize LeapfrogAI API or OpenAI, but some functionality still depends on a direct connection with Supabase.

If running the UI locally and utilizing LeapfrogAI API, **you must use the same Supabase instance that the LeapfrogAI API is utilizing**.

#### Cluster

1. Connect the UI to a UDS deployed version of Supabase and LeapfrogAI API.
   Ensure these env variables are set appropriately in your .env file:

```bash
PUBLIC_SUPABASE_URL=https://supabase-kong.uds.dev
PUBLIC_SUPABASE_ANON_KEY=<anon_key>
...
LEAPFROGAI_API_BASE_URL=https://leapfrogai-api.uds.dev
DEFAULT_MODEL=llama-cpp-python # or vllm
```

2. Run the UI migrations

   If you deploy the UI with UDS, the necessary database migrations will be applied. You can still run a local version of the UI, but the deployed version will have set up the database properly for you.

#### Standalone Supabase

1. Install [Supabase](https://supabase.com/docs/guides/cli/getting-started?platform=macos)
2. Run: `supabase start`
   The configuration files at src/leapfrogai_ui/supabase will ensure your Supabase is configured to work with Keycloak if
   you set these .env variables:

```bash
SUPABASE_AUTH_KEYCLOAK_CLIENT_ID=uds-supabase
SUPABASE_AUTH_KEYCLOAK_SECRET=<secret> #this is the client secret for the client in Keycloak
SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL=https://sso.uds.dev/realms/uds
```

After it starts, the Supabase API URL and Anon key are printed to the console. These are used in the .env file to connect to Supabase.

After starting supabase for the first time, you need to initialize the database with migrations and seed data:

`supabase db reset`

After this initial reset, if you start Supabase again it will already have the data and you don't need to run this command unless you want to restore it to the default.

Stop Supabase:

`npm run supabase:stop`

**WARNING:** if switching the application from utilizing LeapfrogAI API to OpenAI or vice versa, and you encounter this error: `Server responded with status code 431. See https://vitejs.dev/guide/troubleshooting.html#_431-request-header-fields-too-large.`, then you need to clear your browser cookies.

#### Authentication

You can choose to use Keycloak (with UDS) or turn Keycloak off and just use Supabase.

When the UI and API are deployed with UDS, everything will be configured properly automatically, but if you want to
run the UI outside of UDS on localhost (e.g. for development work), there are some manual configuration steps:

1. Modify the "GOTRUE_URI_ALLOW_LIST" within Supabase.  
   The Supabase UDS package has a ConfigMap called "supabase-auth-default".  
   Add these values to the "GOTRUE_URI_ALLOW_LIST" (no spaces!). This variable may not exist and you will need to add it.
   Restart the supabase-auth pod after updating the config:
   `http://localhost:5173/auth/callback,http://localhost:4173/auth/callback`  
   **NOTE:** Port 4173 is utilized by Playwright for E2E tests. You do not need this if you are not concerned about Playwright.

##### With KeyCloak

1. If Supabase was deployed with UDS, it will automatically configure a Keycloak Client for you. We need to modify this client to allow
   localhost URIs.  
   Within Keycloak, under the UDS Realm, edit the uds-supabase client.  
   Under "Valid redirect URIs" add:  
   http://localhost:5173/auth/callback  
   http://localhost:4173/auth/callback (for Playwright tests)
2. If you want to connect Keycloak to a locally running Supabase instance (non UDS deployed), see the "Running Supabase locally" section below.

##### Without Keycloak

1. To turn off Keycloak, set this .env variable: `PUBLIC_DISABLE_KEYCLOAK=false`

#### OpenAI

Set the following .env variables:

```bash
DEFAULT_MODEL=gpt-3.5-turbo
LEAPFROGAI_API_BASE_URL=https://api.openai.com
# If specified, app will use OpenAI instead of LeapfrogAI
OPENAI_API_KEY=<your_openai_api_key>
```

You still need Supabase, so you can connect to UDS deployed Supabase, or run Supabase locally.
To connect to UDS deployed Supabase, set these .env variables:

```bash
PUBLIC_SUPABASE_URL=https://supabase-kong.uds.dev
PUBLIC_SUPABASE_ANON_KEY=<anon_key>
```

## Notes and Troubleshooting

### Supabase

We use Supabase for authentication and a database. Application specific data
(ex. user profile images, application settings like feature flags, etc..) should be stored directly in Supabase and
would not normally utilize the LeapfrogAI API for CRUD operations.

### Playwright End-to-End Tests

1. Install Playwright

   ```bash
   npm init playwright@latest
   ```

2. Run the E2E tests:  

   ```bash
   npm run test:integration:ui
   ```

   Click the play button in the Playwright UI.
   Playwright will run it's own production build and server the app at `http://localhost:4173`. If you make server side changes,
   restart playwright for them to take effect.

Notes:

1. Playwright tests are End-To-End tests and use the "real" full stack app. If you run these tests, they will use the configuration indicated by your
   .env file. See the "Configuration Options" section above to configure which database Playwright is using.
2. If you run the tests in headless mode (`npm run test:integration`) you do not need the app running, it will build the app and run on port 4173.
3. If using Keycloak, you cannot login twice within 30 seconds. If you global.setup.ts step fails, this is likely why. The setup file also tests logout, but
   this can take a long time because of the 30 second wait in between log ins. You can disable this test by setting the environment
   variable SKIP_LOGOUT_TEST=true

### Supabase and Keycloak Integration

The Supabase docs are inadequate for properly integrating with Keycloak. Additionally, they only support integration with the Supabase Cloud SAAS offering.
Before reading the section below, first reference the [Supabase docs](https://supabase.com/docs/guides/auth/social-login/auth-keycloak).

**The following steps are required to integrate Supabase with Keycloak for local development**

The supabase/config.toml file contains configuration options for Supabase when running it locally. When running locally, the Supabase UI dashboard does not offer
all the same configuration options that the cloud version does, so you have to specify some options in this file instead.

The variables that had to be overridden were:

```toml
[auth]
site_url = "http://localhost:5173"

[auth.external.keycloak]
enabled = true
client_id = "env(SUPABASE_AUTH_KEYCLOAK_CLIENT_ID)"
secret = "env(SUPABASE_AUTH_KEYCLOAK_SECRET)"
url= "env(SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL)"

```

The variables referenced in the [auth.external.keycloak] section above are in your .env file at the root of the project.
You need to create a client in Keycloak to get these variables.
Under a realm in Keycloak that is not the master realm (if using UDS, its "uds"):

1. Create a new client (the client ID you use will be used in the env variables below)
2. Turn on "Client Authentication"
3. For "Valid redirect URLs", you need to put:
   1. `http://127.0.0.1:54321/auth/v1/callback` (or the URL for the Supabase callback, for locally running Supabase, DO NOT USE LOCALHOST, use 127.0.0.1)
   2. Put the same two URLs in for "Web Origins"
4. Copy the Client Secret under the Clients -> Credentials tab and use in the env variables below
5. You can create users under the "Users" tab and either have them verify their email (if you setup SMTP), or manually mark them as verified.

```bash
# .env
SUPABASE_AUTH_KEYCLOAK_CLIENT_ID=<client-id-for-app-from-keycloak>
SUPABASE_AUTH_KEYCLOAK_SECRET=<client-id-for-app-from-keycloak>
SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL=<URL for keycloak see notes below>
```

The `SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL` can be tricky if your Keycloak is not hosted on an actual domain.
For example, if you are running Keycloak locally, you might have it at: http://localhost:8080/auth/realms/uds
If you leave this as localhost:8080, when Supabase attempts to make a POST request to the Keycloak server during the auth process,
it will not be able to find this address and you will likely see the error "unable to exchange external code".
[This comment](https://github.com/supabase/auth/issues/516#issuecomment-1179152266) speaks to this problem, although the solutions
don't work if you are using the Supabase CLI and not running a pure [docker version of Supabase](https://supabase.com/docs/guides/self-hosting/docker).

In order to fix this, we have to edit the /etc/hosts file in the running Supabase Auth container (we can't add this through a docker compose file
because we are using the Supabase CLI to start it up, migrate the db, and seed it).

Here is an example of how you can modify the /etc/hosts of the supabase container:
`"supabase start && docker exec -u 0 supabase_auth_supabase /bin/sh -c \"echo '100.115.154.78 keycloak.admin.uds.dev' >> /etc/hosts\"`
**You must ensure the IP address used in this command is the correct IP for where you have Keycloak hosted.**
If you need to use a different Keycloak server for local development, you will need to modify this command.

If your Keycloak server is not at a hosted domain, you will also need to modify the /etc/hosts on your machine:

```bash
vim /etc/hosts

# add the following line to the opened `/etc/hosts` file
# replace beginning with the correct IP address
xxx.xxx.xx.xx  keycloak.admin.uds.dev
```

Ensure the

```bash
PUBLIC_SUPABASE_URL=
PUBLIC_SUPABASE_ANON_KEY=
```

variables in your `.env` file are pointing to the correct Supabase instance.

**NOTE:** if connecting to a hosted Supabase instance, or in a cluster with networking, you will not need to override /etc/host files.
The:

```bash
SUPABASE_AUTH_KEYCLOAK_CLIENT_ID=
SUPABASE_AUTH_KEYCLOAK_SECRET=
SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL=
```

variables will also not do anything because they are only used for locally running Supabase.
You will instead need to modify the Auth provider settings directly in the Supabase dashboard and set the appropriate
redirect URLs and client ID/secret.

If you do not use this component and need to login with a Supabase auth command directly, ensure you provide
the "openid" scope with the options parameter.

The E2E tests use a fake Keycloak user. You must create this user in Keycloak, and add the username, password, and MFA secret
to the .env file in order for the tests to pass. PUBLIC_DISABLE_KEYCLOAK must also be set to false to run the E2E tests.

To get the MFA secret, create your new Keycloak user with the normal Keycloak login flow (not manually through the Keycloak UI).
When scanning the QR code, use an app that lets you see the url of the QR code. The secret is contained in that URL.

Login flow was adapted from [this reference](https://supabase.com/docs/guides/getting-started/tutorials/with-sveltekit?database-method=sql)

### Chat Data Flow

The logic for handling regular chat messages and assistant chat messages, along with persisting that data to the database is complex and deserves a detailed explanation.

Our chat page allows the user to send messages to /api/chat ("regular chat") and /api/chat/assistants ("chat with assistant"). The messages are streamed to the client so that text is
progressively displayed on the screen. We use the Vercel [AI SDK](https://sdk.vercel.ai/docs/getting-started/svelte) to handle streaming as well as response cancellation, regeneration, message editing, error handling, and more.

Messages streamed with regular chat, use the "useChat" function.  
Assistants use the "useAssistants" function.  
These functions do not provide the same features and handle data differently, resulting in several edge cases.

Here are a few of the big issues caused by these differences:

The useChat function does not save messages with the API to the database, we have to handle that on our own.  
Messages sent with useAssistants, however, are saved to the database automatically.

Creation timestamps are handled differently depending on if they are streamed responses or if they have been saved to the database.
Streamed messages have timestamps on the "createdAt" field, saved messages have timestamps on the "created_at" field. Sometimes the dates are Date strings, unix seconds, or unix milliseconds.
Since dates can be returned in seconds, we lose some of the precision we would have for sorting the messages if they were returned in milliseconds. Due to this issue, there is logic in place to prevent the
user from sending messages too quickly, ensuring timestamps are unique.

Additionally, streamed messages have temporary ids that do not match the ids messages are assigned when they are saved to the database. This makes editing and deleting messages challenging, so we have to keep track of both streamed
messages and saved messages in client side state in the correct order. We use this state to look up the saved ids and make the appropriate API calls with the permanent ids.

While there are several automated tests for this logic, the edge cases and mocking scenarios are complex. Any modifications to this logic should be thoroughly manually tested.

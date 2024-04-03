# LeapfrogAI UI

## Getting Started

1. You will need Supabase installed before running the application:
   [Supabase](https://supabase.com/docs/guides/cli/getting-started?platform=macos)

2. Create a `.env` file at the route of the project, reference the `.env.example` file for values to put in the .env file

3. Install dependencies:

```
npm i
npm run dev -- --open
```

## Building

To create a production version of the app:

```
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.

## Developer Notes

### Tooling

#### Husky

This repository utilizes [Husky](https://typicode.github.io/husky/) for pre-commit checks (git hooks).

If you need to commit and skip the git hooks:

```
git commit -m "..." -n # Skips Git hooks
```

To commit without running tests:

```
SKIP_TEST=true git commit -m "chore: my commit msg"
```

[reference the docs](https://typicode.github.io/husky/how-to.html) for other helpful tips on using husky or configuring for CI and Docker

### Supabase

We use Supabase for authentication and a database. Playwright tests run against a running instance of Supabase that you can start locally. You need the [Supabase CLI](https://supabase.com/docs/guides/cli/getting-started) installed to do so. Before running Playwright tests, make sure Supabase and the frontend are running `npm run dev` will start both.

Run locally:

`npm run supabase:start`

After it starts, the Supabase API URL and Anon key are printed to the console. These are used in the .env file to connect to Supabase.

After starting supabase for the first time, you need to initialize the database with migrations and seed data:

`npm run supabase:reset`

After this initial reset, if you start Supabase again it will already have the data and you don't need to run this command unless you want to restore it to the default.

Note - `npm run dev` will start Supabase and the frontend, but it does not run the migrations and seeding.

Stop Supabase:

`npm run supabase:stop`

### Playwright End-to-End Tests

First install Playwright: `npm init playwright@latest`

To run the E2E tests, have the app running then:  
`npm run test:integration:ui`
Click the play button in the Playwright UI.

Notes:
1. Running the script above will reset the locally running Supabase instance and re-seed the database. You will
lose existing data.
2. if you run the tests in headless mode (```npm run test:integration```) you do not need the app running, it will build the app and run on port 4173.

# Supabase and Keycloak Integration

The Supabase docs are inadequate for properly integrating with Keycloak. Additionally, they only support integration with the Supabase Cloud SAAS offering.
Before reading the section below, first reference the [Supabase docs](https://supabase.com/docs/guides/auth/social-login/auth-keycloak).

### The following steps are required to integrate Supabase with Keycloak for local development:

The supabase/config.toml file contains configuration options for Supabase when running it locally. When running locally, the Supabase UI dashboard does not offer
all the same configuration options that the cloud version does, so you have to specify some options in this file instead.

The variables that had to be overridden were:

```
[auth]
site_url = "http://localhost:5173"
additional_redirect_urls = ["http://localhost:5173/auth/callback"]

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
   1. `http://localhost:5173/auth/callback` (or the URL for the frontend app callback)
   2. `http://127.0.0.1:54321/auth/v1/callback` (or the URL for the Supabase callback, for locally running Supabase, DO NOT USE LOCALHOST, use 127.0.0.1)
   3. Put the same two URLs in for "Web Origins"
4. Create a user under the "Users" tab and either have them verify their email, or mark it as verified.
5. Copy the Client Secret under the Clients -> Credentials tab and use in the env variables below

```
#.env
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

`npm run supabase:start` will start Supabase and modify the /etc/hosts to properly direct requests to the Keycloak server.
If you need to use a different Keycloak server for local development, you will need to modify this command.

If your Keycloak server is not at a hosted domain, you will also need to modify the /etc/hosts on your machine:

```
Example:
sudo nano /etc/hosts
*add this line (edit as required)*
100.104.70.77  keycloak.admin.uds.dev
```

Ensure the

```
PUBLIC_SUPABASE_URL=
PUBLIC_SUPABASE_ANON_KEY=
```

variables in your .env file are pointing to the correct Supabase instance.

Note - if connecting to a hosted Supabase instance, or in a cluster with networking, you will not need to override /etc/host files.
The:

```
SUPABASE_AUTH_KEYCLOAK_CLIENT_ID=
SUPABASE_AUTH_KEYCLOAK_SECRET=
SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL=
```

variables will also not do anything because they are only used for locally running Supabase.
You will instead need to modify the Auth provider settings directly in the Supabase dashboard and set the appropriate
redirect URLs and client ID/secret.

If you use the <Auth /> component from @supabase/auth-ui-shared, you must ensure you supply provider and scope props:
ex:

```
	<Auth
		supabaseClient={data.supabase}
		redirectTo={`${data.url}/auth/callback`}
		showLinks={false}
		providers={['keycloak']}
		providerScopes={{
			keycloak: 'openid'
		}}
		onlyThirdPartyProviders
		appearance={{ theme: ThemeSupa }}
	/>
```

If you do not use this component and need to login with a Supabase auth command directly, ensure you provide
the "openid" scope with the options parameter.

Login flow was adapted from [this reference](https://supabase.com/docs/guides/getting-started/tutorials/with-sveltekit?database-method=sql)

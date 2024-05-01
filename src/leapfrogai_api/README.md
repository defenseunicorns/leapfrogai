# LeapfrogAI API

A mostly OpenAI compliant API surface.

## Requirements

- Supabase

## Local Development

Create a local Supabase instance (requires [[Supabase CLI](https://supabase.com/docs/guides/cli/getting-started)):

``` bash
supabase start # from /leapfrogai

supabase db reset # clears all data and reinitializes migrations

supabase status # to check status and see your keys
```

Setup environment variables:

``` bash
export SUPABASE_URL="http://localhost:54321" # or whatever you configured it as in your Supabase config.toml
export SUPABASE_SERVICE_KEY="<YOUR_KEY>" # supabase status will show you the keys
```
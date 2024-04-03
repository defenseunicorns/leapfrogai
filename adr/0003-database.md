# LeapfrogAI Database

## Table of Contents

- [LeapfrogAI Database](#leapfrogai-database)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
  - [Background](#background)
  - [Decision](#decision)
  - [Rationale](#rationale)
  - [Alternatives](#alternatives)
  - [Related ADRs](#related-adrs)
  - [References](#references)

## Status

PROPOSED

## Context

LeapfrogAI began with a need for a basic vector store. As LeapfrogAI expands into providing a production ready front end the demands of the database expand to include authentication, user data, object storage, and additional data types for Retrieval Augmented Generation. This ADR proposes ***Supabase*** as a single database solution for all current LeapfrogAI needs.

## Decision

Move to Supabase for all current LeapfrogAI Database needs.

## Rationale

### General Features
- Open Source, Apache 2.0 license
- Integrates easily into frontend with SDK
- Easy to run Supabase locally for development 
- Row Level Security with Postgres enables protection of data at the request level
- Supabase Auth system integrates with Keycloak to enable UDS SSO (OpenID)
- [Supabase CLI](https://supabase.com/docs/guides/cli/getting-started) is user friendly and feature rich. The CLI can be used for initializing and configuring the database, then saving schemas and migrations to make our configuration easily reproducible and deployable. It can also be used to [automate tests via GitHub Actions](https://supabase.com/docs/guides/cli/github-action/testing)
- Additional features built in if we need them in the future - like realtime subscriptions and edge functions
- Well supported and adopted in the community, also supports various frameworks (Svelte, Nuxt, Next.js, React, Flutter, etc...)
- Documentation provides lots of useful examples/recipes although documentation for self-hosted situations can be outdated

### As Vector Store:

- Supabase has a pgvector extension for supporting vector storage for RAG
- Because Supabase is Postgres/pgvector under the hood, is it is compatible with a multitude of Python libraries ([LangChain](https://python.langchain.com/docs/integrations/vectorstores/supabase), [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/vector_stores/SupabaseVectorIndexDemo/), [Vecs](https://github.com/supabase/vecs), [NeumAI](https://github.com/NeumTry/NeumAI), etc.)

## Alternatives

- Per our previous ADR, [0001-vectordb-backend](0001-vectordb-backend.md), ChromaDB is a lightweight offering, but we continued to grow we discovered it doesn't offer many of the security and scaling features that Supabase provides (Row Level Security, Auth, etc.).

## Related ADRs
* [0001-vectordb-backend (Superseded)](0001-vectordb-backend.md)

## References
- [Supabase Documentation](https://supabase.com/docs/)
- [Supabase CLI Documentation](https://supabase.com/docs/guides/cli/getting-started)
- [LangChain Python Library](https://python.langchain.com/docs/integrations/vectorstores/supabase)
- [LlamaIndex Python Library](https://docs.llamaindex.ai/en/stable/examples/vector_stores/SupabaseVectorIndexDemo/)
- [Vecs Python Library](https://github.com/supabase/vecs)
- [NeumAI Python Library](https://github.com/NeumTry/NeumAI)
- [ChromaDB ADR](0001-vectordb-backend.md)
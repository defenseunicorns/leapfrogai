# VectorDB

## Table of Contents

- [VectorDB](#vectordb)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
    - [Issue](#issue)
    - [Decision](#decision)
    - [Rationale](#rationale)
    - [Status](#status)
  - [Context](#context)
    - [Important Factors](#important-factors)
    - [Options](#options)
    - [Supporting information](#supporting-information)
      - [Benchmarks](#benchmarks)
    - [Indexing](#indexing)
    - [Assumptions](#assumptions)
    - [Constraints](#constraints)
    - [Implications](#implications)

## Status

ACCEPTED (Candidate to be superseded by [0003-database.md](0003-database.md))

### Issue

We need to support a Vector DB for retrieval-augmented generation (RAG), there are many options but we need to choose between them.

### Decision

ChromaDB

### Rationale

We decided on ChromaDB due to it's simple implementation, performance, and Apache 2.0 license. At this maturity level, we expect individual capabilities on top of LeapfrogAI to maintain their own Vector DB with ChromaDB and will expand support as common themes surface.

### Status

Provisional

## Context

### Important Factors

- OpenSource
- Performance
  - Queries per second
  - Latency
- RBAC
- Self-hosted
- Portability
- Developer Experience
- Sharding
- Licensing/Fees

### Options

- [Pinecone](https://www.pinecone.io/)
- [Weaviate](https://weaviate.io/)
- [Milvus](https://milvus.io/)
- [GitHub](https://github.com/milvus-io/milvus)
- [Architecture](https://milvus.io/docs/architecture_overview.md)
- [Qdrant](https://qdrant.tech/)
- [Chroma](https://www.trychroma.com/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [PGvector](https://github.com/pgvector/pgvector)

### Supporting information

#### Benchmarks

- https://benchmark.vectorview.ai/vectordbs.html
- https://ann-benchmarks.com/index.html#algorithms
- https://github.com/milvus-io/milvus/discussions/4939

### Indexing

- https://weaviate.io/blog/ann-algorithms-vamana-vs-hnsw
- https://thedataquarry.com/posts/vector-db-3/

### Assumptions

- We will start with a single preferred VectorDB, but LeapfrogAI should be extensible to accommodate other options.
- Not bundling the vector db with the app layer is desirable

### Constraints

TBD

### Implications

TBD

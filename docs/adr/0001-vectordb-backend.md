# 1. VectorDB

Contents:

- [Summary](#summary)
  - [Issue](#issue)
  - [Decision](#decision)
  - [Rationale](#rationale)
  - [Status](#status)
- [Context](#context)
  - [Important Factors](#important-factors)
  - [Options](#options)
  - [Supporting Information](#supporting-information)
  - [Assumptions](#assumptions)
  - [Constraints](#constraints)
  - [Implications](#implications)

## Summary

### Issue

We need to support a vector db for retrieval-augmented generation (RAG), there are many options but we need to choose between them. 

### Decision 

TBD

### Rationale 
TBD

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
- [Milvus](https://milvus.io/) - [GitHub](https://github.com/milvus-io/milvus) - [Architecture](https://milvus.io/docs/architecture_overview.md)
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

- Choosing a single vector db is desirable
- Not bundling the vector db with the app layer is desirable

### Constraints

TBD

### Implications

TBD

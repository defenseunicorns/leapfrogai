-- Some of this is from https://python.langchain.com/docs/integrations/vectorstores/supabase
-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store the OpenAI Vector Store Objects
create table
  vector_store_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    bytes bigint,
    created_at bigint default extract(epoch from now()) not null,
    file_counts jsonb,
    last_active_at bigint,
    metadata jsonb,
    name text,
    object text check (object in ('vector_store')),
    status text,
    expires_after jsonb,
    expires_at bigint
  );

-- Create a table to store the OpenAI Vector Store File Objects
create table
  vector_store_file_objects (
    id uuid references file_objects (id) on delete cascade,
    created_at bigint,
    last_error jsonb,
    object text,
    status text,
    vector_store_id uuid references vector_store_objects (id) on delete cascade,
    primary key (vector_store_id, id)
  );

-- Create a table to store your documents
create table
  vector_store (
    id uuid primary key DEFAULT uuid_generate_v4(),
    vector_store_id uuid references vector_store_objects (id) on delete cascade,
    file_id uuid references file_objects (id) on delete cascade,
    content text, -- corresponds to Document.pageContent
    metadata jsonb, -- corresponds to Document.metadata
    embedding vector (768) -- Instructor-XL produces 768-length embeddings
  );

-- Create a function to search for documents
create function match_vectors (
  query_embedding vector (768), -- Instructor-XL produces 768-length embeddings
  vs_id uuid,
  match_limit int,
  filter jsonb default '{}'
) returns table (
  id uuid,
  vector_store_id uuid,
  file_id uuid,
  content text,
  metadata jsonb,
  similarity float
) language plpgsql as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    vector_store_id,
    file_id,
    content,
    metadata,
    1 - (vector_store.embedding <=> query_embedding) as similarity
  from vector_store
  where vector_store_id = vs_id
    and metadata @> filter
  order by vector_store.embedding <=> query_embedding
  limit match_limit;
end;
$$;

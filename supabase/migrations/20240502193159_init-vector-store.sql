-- Some of this is from https://python.langchain.com/docs/integrations/vectorstores/supabase
-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store the OpenAI Vector Store Objects
create table
  vector_store_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    bytes bigint,
    created_at bigint,
    file_counts jsonb,
    last_active_at bigint,
    metadata jsonb,
    name text,
    object text,
    status text,
    expires_after jsonb,
    expires_at bigint
  );

-- Create a table to store the OpenAI Vector Store File Objects
create table
  vector_store_file_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    created_at bigint,
    last_error jsonb,
    object text,
    status text,
    vector_store_object_id uuid references vector_store_objects (id) on delete cascade
  );

-- Create a table to store your documents
create table
  vector_store (
    id uuid primary key DEFAULT uuid_generate_v4(),
    vector_store_id uuid references vector_store_objects (id) on delete cascade,
    file_id uuid references vector_store_file_objects (id) on delete cascade,
    content text, -- corresponds to Document.pageContent
    metadata jsonb, -- corresponds to Document.metadata
    embedding vector (768) -- Instructor-XL produces 768-dimensional embeddings
  );

-- Create a function to search for documents
create function match_vectors (
  query_embedding vector (768), -- Instructor-XL produces 4096-dimensional embeddings
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
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding;
end;
$$;

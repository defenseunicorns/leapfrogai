-- Some of this is from https://python.langchain.com/docs/integrations/vectorstores/supabase
-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store the OpenAI Vector Store Objects
create table
  vector_store (
    id uuid primary key DEFAULT uuid_generate_v4(),
    user_id uuid references auth.users not null,
    usage_bytes bigint,
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
  vector_store_file (
    id uuid references file_objects (id) on delete cascade,
    user_id uuid references auth.users not null,
    created_at bigint default extract(epoch from now()) not null,
    last_error jsonb,
    object text check (object in ('vector_store.file')),
    status text,
    usage_bytes bigint,
    chunking_strategy jsonb,
    vector_store_id uuid references vector_store (id) on delete cascade,
    primary key (vector_store_id, id)
  );

-- Create a table to store your documents
create table
  vector_content (
    id uuid primary key DEFAULT uuid_generate_v4(),
    user_id uuid references auth.users not null,
    vector_store_id uuid references vector_store (id) on delete cascade,
    file_id uuid references file_objects (id) on delete cascade,
    content text, -- corresponds to Document.pageContent
    metadata jsonb, -- corresponds to Document.metadata
    embedding vector (768) -- Instructor-XL produces 768-length embeddings
  );

-- Create a function to update the size in bytes for vector_store_file
create or replace function calculate_vector_store_file_usage_bytes() returns trigger as $$
declare
    file_size bigint;
begin
    -- Calculate the size of the content, metadata, and embedding for the new or updated file
    select coalesce(pg_column_size(content) + pg_column_size(metadata) + pg_column_size(embedding), 0)
    into file_size
    from vector_content
    where file_id = new.file_id;

    -- Update the usage_bytes in the vector_store_file table
    update vector_store_file
    set usage_bytes = file_size + coalesce(usage_bytes, 0)
    where id = new.file_id
    and vector_store_id = new.vector_store_id;

    return new;
end;
$$ language plpgsql;

-- Create a trigger to call the function after insert or update on the vector_content table
create trigger calculate_vector_store_file_usage_bytes_trigger
after insert or update on vector_content
for each row execute function calculate_vector_store_file_usage_bytes();

-- Create a function to update the total size in bytes for vector_store
create or replace function update_vector_store_usage_bytes() returns trigger as $$
declare
    total_size bigint;
begin
    -- Calculate the total size of relevant entries in the vector_store_file table
    select coalesce(sum(usage_bytes), 0)
    into total_size
    from vector_store_file
    where vector_store_id = coalesce(new.vector_store_id, old.vector_store_id);

    -- Update the usage_bytes column in the vector_store table
    update vector_store
    set usage_bytes = total_size
    where id = coalesce(new.vector_store_id, old.vector_store_id);

    return new;
end;
$$ language plpgsql;

-- Create a trigger to call the function after insert, update, or delete on the vector_store_file table
create trigger update_vector_store_usage_bytes_trigger
after insert or update or delete on vector_store_file
for each row execute function update_vector_store_usage_bytes();

-- Create a function to search for documents
create function match_vectors (
  query_embedding vector (768), -- Instructor-XL produces 768-length embeddings
  vs_id uuid,
  user_id uuid,
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
    1 - (vector_content.embedding <=> query_embedding) as similarity
  from vector_content
  where vector_store_id = vs_id
    and user_id = user_id
    and metadata @> filter
  order by vector_content.embedding <=> query_embedding
  limit match_limit;
end;
$$;

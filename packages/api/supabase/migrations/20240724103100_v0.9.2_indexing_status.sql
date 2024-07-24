-- Create a table to store the status of the vector store file indexing
CREATE TABLE vector_store_file_status (
    id VARCHAR PRIMARY KEY,
    user_id uuid references auth.users not null,
    status VARCHAR CHECK (status IN ('processing', 'complete', 'error')),
    created_at bigint default extract(epoch from now()) not null,
    updated_at bigint default extract(epoch from now()) not null
);

-- Add an index on user_id for faster queries
CREATE INDEX idx_vector_store_file_status_user_id ON vector_store_file_status(user_id);

-- Turn on security
alter table vector_store_file_status enable row level security;

-- Allow users to CRUD their own vector_store_file_status via API key.
create policy "Individuals can CRUD their own vector_store_file_status via API key."
    on vector_store_file_status for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = vector_store_file_status.user_id
        )
    );

-- Allow users to CRUD their own vector_store_file_status
create policy "Individuals can CRUD their own vector_store_file_status" on vector_store_file_status for
    all to anon using (auth.uid() = user_id);

-- Create a function to update the updated_at column
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = extract(epoch from now());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the updated_at column
CREATE TRIGGER update_vector_store_file_status_modtime
BEFORE UPDATE ON vector_store_file_status
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Enable Supabase realtime for the vector_store_file_status table
alter publication supabase_realtime
add table vector_store_file_status;
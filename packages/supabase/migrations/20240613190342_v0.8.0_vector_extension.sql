-- Some of this is from https://python.langchain.com/docs/integrations/vectorstores/supabase
-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- If this is the first migration that has run on the database the owner of the schema_migrations table will be the user that created the table.
-- We want to ensure the standard `postgres` user is the owner.
ALTER SCHEMA supabase_migrations OWNER TO postgres;
ALTER TABLE supabase_migrations.schema_migrations OWNER TO postgres;

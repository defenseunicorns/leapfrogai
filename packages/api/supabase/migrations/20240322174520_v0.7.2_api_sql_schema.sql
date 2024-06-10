-- Create a table to store the OpenAI File Objects
create table
  file_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    bytes int,
    created_at bigint,
    -- created_at bigint default extract(epoch from now()) not null, -- This line was added post v0.7.2
    filename text,
    object text,
    -- object text check (object in ('file')), -- This line was added post v0.7.2
    purpose text,
    status text,
    status_details text
  );

-- storage bucket for the files
insert into storage.buckets
  (id, name, public)
values
  ('file_bucket', 'files', true);

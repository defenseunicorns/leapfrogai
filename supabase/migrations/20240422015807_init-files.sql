-- Create a table to store the OpenAI File Objects
create table
  file_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    bytes int,
    created_at bigint default extract(epoch from now()) not null,
    filename text,
    object text check (object in ('file')),
    purpose text,
    status text,
    status_details text
  );

-- storage bucket for the files
insert into storage.buckets
  (id, name, public)
values
  ('file_bucket', 'files', true);

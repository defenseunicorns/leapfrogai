-- Set up Storage!
insert into storage.buckets (id, name)
values ('file_uploads', 'file_uploads');

-- These are user profiles avatars, currently not used by app
insert into storage.buckets (id, name)
values ('avatars', 'avatars');



-- RLS

-- Allow a user to access files under their folder:
create policy " Allow users access to files within their folder"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'file_uploads' and
  (storage.foldername(name))[1] = (select auth.uid()::text)
);
-- Set up Storage!
insert into storage.buckets
(id, name, public)
values
    ('assistant_avatars', 'assistant_avatars', true);

-- These are user profiles avatars, currently not used by app
insert into storage.buckets (id, name)
values ('avatars', 'avatars');



-- RLS

create policy "Allow users to add assistant avatars under their uid"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'assistant_avatars' and
  (storage.foldername(name))[1] = (select auth.uid()::text)
);
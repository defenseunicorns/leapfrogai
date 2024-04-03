alter table conversations enable row level security;

alter table messages enable row level security;

alter table profiles enable row level security;

-- Policies for conversations
create policy "Individuals can create conversations." on conversations for
    insert with check (auth.uid() = user_id);
create policy "Individuals can view their own conversations. " on conversations for
    select using (auth.uid() = user_id);
create policy "Individuals can update their own conversations." on conversations for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own conversations." on conversations for
    delete using (auth.uid() = user_id);

-- Policies for messages
create policy "Individuals can view their own messages." on messages for
    select using (auth.uid() = user_id); 
create policy "Individuals can create messages." on messages for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own messages." on messages for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own messages." on messages for
    delete using (auth.uid() = user_id);

-- Policies for profiles
create policy "Public profiles are viewable by everyone." on profiles
    for select using (true);

create policy "Users can insert their own profile." on profiles
  for insert with check (auth.uid() = id);

create policy "Users can update own profile." on profiles
  for update using (auth.uid() = id);

-- Set up access controls for storage.
-- See https://supabase.com/docs/guides/storage/security/access-control#policy-examples for more details.
create policy "Avatar images are publicly accessible." on storage.objects
  for select using (bucket_id = 'avatars');

create policy "Anyone can upload an avatar." on storage.objects
  for insert with check (bucket_id = 'avatars');

create policy "Anyone can update their own avatar." on storage.objects
  for update using (auth.uid() = owner) with check (bucket_id = 'avatars');
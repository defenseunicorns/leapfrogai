-- Create tables
create table conversations (
                               id uuid primary key DEFAULT uuid_generate_v4(),
                               user_id uuid references auth.users not null,
                               label text,
                               inserted_at timestamp with time zone default timezone('utc'::text, now()) not null
);

create table messages (
                          id uuid primary key DEFAULT uuid_generate_v4(),
                          user_id uuid references auth.users not null,
                          conversation_id uuid references conversations on delete cascade not null,
                          role text check (role in ('system', 'user', 'assistant', 'function', 'data', 'tool')),
                          content text,
                          inserted_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create a table for public profiles
create table profiles (
                          id uuid references auth.users not null primary key,
                          updated_at timestamp with time zone,
                          username text unique,
                          full_name text,
                          avatar_url text,
                          website text,

                          constraint username_length check (char_length(username) >= 3)
);

-- conversations, messages, and profiles tables and RLS policies

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


-- This trigger automatically creates a profile entry when a new user signs up via Supabase Auth.
-- See https://supabase.com/docs/guides/auth/managing-user-data#using-triggers for more details.
create function public.handle_new_user()
    returns trigger as $$
begin
insert into public.profiles (id, full_name, avatar_url)
values (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
return new;
end;
$$ language plpgsql security definer;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute procedure public.handle_new_user();


CREATE TABLE assistants (
                            id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
                            object text CHECK (object in ('assistant')),
                            name VARCHAR(255),
                            description VARCHAR(512),
                            model VARCHAR(255) NOT NULL,
                            instructions TEXT,
                            tools jsonb,
                            tool_resources jsonb,
                            metadata jsonb,
                            temperature FLOAT,
                            top_p FLOAT,
                            response_format jsonb,
                            created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

alter table assistants enable row level security;

-- Policies for assistants
CREATE POLICY "Individuals can view their own assistants." ON assistants
FOR SELECT USING ((metadata ->> 'created_by') = auth.uid()::text);
create policy "Individuals can create assistants." on assistants for
    insert with check ((metadata ->> 'created_by') = auth.uid()::text);
create policy "Individuals can update their own assistants." on assistants for
update using ((metadata ->> 'created_by') = auth.uid()::text);
create policy "Individuals can delete their own assistants." on assistants for
    delete using ((metadata ->> 'created_by') = auth.uid()::text);


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
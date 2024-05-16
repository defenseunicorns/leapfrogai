-- Create tables

create table assistants (
    id TEXT primary key,
    object text check (object = 'assistant'),
    name varchar(255),
    description varchar(512),
    model varchar(255) not null,
    instructions TEXT,
    tools jsonb,
    tool_resources jsonb,
    metadata jsonb,
    temperature float,
    top_p float,
    response_format jsonb,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);


create table public.profiles (
  id uuid references auth.users not null primary key,
  full_name text,
  thread_ids text array DEFAULT '{}'
);


-- Set up Storage!
insert into storage.buckets
(id, name, public)
values
    ('assistant_avatars', 'assistant_avatars', true);

-- These are user profiles avatars, currently not used by app and will be removed soon
insert into storage.buckets (id, name)
values ('avatars', 'avatars');


-- RLS policies

alter table public.profiles enable row level security;
alter table assistants enable row level security;


-- Policies for profiles
create policy "Users can view their own profiles" on profiles
    for select using  (auth.uid() = id);
create policy "Users can insert their own profile." on profiles
  for insert with check (auth.uid() = id);
create policy "Users can update own profile." on profiles
  for update using (auth.uid() = id);

-- Policies for assistants
create policy "Individuals can view their own assistants." ON assistants
for select using ((metadata ->> 'user_id') = auth.uid()::text);
create policy "Individuals can create assistants." on assistants for
    insert with check ((metadata ->> 'user_id') = auth.uid()::text);
create policy "Individuals can update their own assistants." on assistants for
update using ((metadata ->> 'user_id') = auth.uid()::text);
create policy "Individuals can delete their own assistants." on assistants for
    delete using ((metadata ->> 'user_id') = auth.uid()::text);


-- Policies for storage.
create policy "Avatar images are publicly accessible." on storage.objects
  for select using (bucket_id = 'avatars');
create policy "Anyone can upload an avatar." on storage.objects
  for insert with check (bucket_id = 'avatars');
create policy "Anyone can update their own avatar." on storage.objects
  for update using (auth.uid() = owner) with check (bucket_id = 'avatars');


create policy "Assistant Avatar images are publicly accessible." on storage.objects
  for select using (bucket_id = 'assistant_avatars');
create policy "Anyone can upload an assistant avatar." on storage.objects
  for insert with check (bucket_id = 'assistant_avatars');
create policy "Anyone can update their own assistant avatars." on storage.objects
  for update using (auth.uid() = owner) with check (bucket_id = 'assistant_avatars');



-- This trigger automatically creates a profile entry when a new user signs up via Supabase Auth.
-- See https://supabase.com/docs/guides/auth/managing-user-data#using-triggers for more details.
create function public.handle_new_user()
    returns trigger as $$
begin
insert into public.profiles (id, full_name)
values (new.id, new.raw_user_meta_data->>'full_name');
return new;
end;
$$ language plpgsql security definer;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute procedure public.handle_new_user();



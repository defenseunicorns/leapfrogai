-- Create tables
create table if not exists profiles (
                          id uuid references auth.users not null primary key,
                          updated_at timestamp with time zone,
                          username text unique,
                          full_name text,
                          avatar_url text,
                          website text,
                          constraint username_length check (char_length(username) >= 3)
);

-- Set up Storage!
insert into storage.buckets
(id, name, public)
values
    ('assistant_avatars', 'assistant_avatars', true)
ON CONFLICT (id)
DO UPDATE SET
    name = EXCLUDED.name,
    public = EXCLUDED.public;

-- These are user profiles avatars, currently not used by app and will be removed soon
insert into storage.buckets (id, name)
values ('avatars', 'avatars')
ON CONFLICT (id)
DO UPDATE SET
    name = EXCLUDED.name;

-- RLS policies
alter table profiles enable row level security;

DO $$
BEGIN
    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'public'
      AND tablename  = 'profiles'
      AND policyname = 'Public profiles are viewable by everyone.')
        THEN create policy "Public profiles are viewable by everyone." on profiles
          for select using (true);
    END IF;

    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'public'
      AND tablename  = 'profiles'
      AND policyname = 'Users can insert their own profile.')
        THEN create policy "Users can insert their own profile." on profiles
          for insert with check (auth.uid() = id);
    END IF;

    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'public'
      AND tablename  = 'profiles'
      AND policyname = 'Users can insert their own profile.')
        THEN create policy "Users can update own profile." on profiles
          for update using (auth.uid() = id);
    END IF;
END $$;

-- Policies for avatars
DO $$
BEGIN
    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'storage'
      AND tablename  = 'objects'
      AND policyname = 'Avatar images are publicly accessible.')
        THEN create policy "Avatar images are publicly accessible." on storage.objects
          for select using (bucket_id = 'avatars');
    END IF;

    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'storage'
      AND tablename  = 'objects'
      AND policyname = 'Anyone can update their own avatar.')
        THEN create policy "Anyone can update their own avatar." on storage.objects
          for update using (auth.uid() = owner) with check (bucket_id = 'avatars');
    END IF;

    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'storage'
      AND tablename  = 'objects'
      AND policyname = 'Anyone can upload an assistant avatar.')
        THEN create policy "Anyone can upload an assistant avatar." on storage.objects
          for insert with check (bucket_id = 'assistant_avatars');
    END IF;
END $$;

-- Policies for assistant_avatars
DO $$
BEGIN
    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'storage'
      AND tablename  = 'objects'
      AND policyname = 'Assistant Avatar images are publicly accessible.')
        THEN create policy "Assistant Avatar images are publicly accessible." on storage.objects
          for select using (bucket_id = 'assistant_avatars');
    END IF;

    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'storage'
      AND tablename  = 'objects'
      AND policyname = 'Anyone can update their own assistant avatars.')
        THEN create policy "Anyone can update their own assistant avatars." on storage.objects
          for update using (auth.uid() = owner) with check (bucket_id = 'assistant_avatars');
    END IF;

    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'storage'
      AND tablename  = 'objects'
      AND policyname = 'Anyone can upload an assistant avatar.')
        THEN create policy "Anyone can upload an assistant avatar." on storage.objects
          for insert with check (bucket_id = 'assistant_avatars');
    END IF;
END $$;


-- This trigger automatically creates a profile entry when a new user signs up via Supabase Auth.
-- See https://supabase.com/docs/guides/auth/managing-user-data#using-triggers for more details.
DROP TRIGGER IF EXISTS on_auth_user_created on auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user();
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

-- First, rename the existing table to keep a backup
ALTER TABLE profiles RENAME TO profiles_old;

-- Create the new table with the required structure
CREATE TABLE public.profiles (
 id uuid REFERENCES auth.users NOT NULL PRIMARY KEY,
 full_name text,
 thread_ids text[] DEFAULT '{}'
);

-- Insert data from the old table to the new one (only the required columns)
INSERT INTO public.profiles (id, full_name)
SELECT id, full_name
FROM profiles_old;

-- Drop the old table if the data transfer is successful
DROP TABLE profiles_old;

-- Enable row level security and set policies on the profiles
alter table profiles enable row level security;
create policy "Users can view their own profiles" on profiles
    for select using  (auth.uid() = id);
create policy "Users can insert their own profile." on profiles
    for insert with check (auth.uid() = id);
create policy "Users can update own profile." on profiles
    for update using (auth.uid() = id);

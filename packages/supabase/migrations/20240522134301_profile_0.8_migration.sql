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
-- DROP TABLE profiles_old;
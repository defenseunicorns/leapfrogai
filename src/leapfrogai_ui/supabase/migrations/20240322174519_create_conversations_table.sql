create table conversations (
    id uuid primary key DEFAULT uuid_generate_v4(),
    user_id uuid references auth.users not null,
    label text,
    inserted_at timestamp with time zone default timezone('utc'::text, now()) not null
);
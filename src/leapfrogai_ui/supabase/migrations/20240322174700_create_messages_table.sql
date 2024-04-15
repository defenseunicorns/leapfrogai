create table messages (
    id uuid primary key DEFAULT uuid_generate_v4(),
    user_id uuid references auth.users not null,
    conversation_id uuid references conversations on delete cascade not null,
    role text check (role in ('system', 'user')),
    content text,
    inserted_at timestamp with time zone default timezone('utc'::text, now()) not null
);
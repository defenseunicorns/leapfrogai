-- Initialize api_keys table with row level security policies
create table api_keys (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    api_key text not null unique,
    created_at bigint default extract(epoch from now()) not null,
    expires_at bigint
);

alter table api_keys enable row level security;

create policy "Read only if API key matches and is current" ON api_keys for
    select using (
        api_key = current_setting('request.headers')::json->>'x-custom-api-key'
        and (expires_at is null or expires_at > extract(epoch from now()))
    );

create policy "Individuals can view their own api_keys." on api_keys for
    select using (auth.uid() = user_id);
create policy "Individuals can create api_keys." on api_keys for
    insert with check (auth.uid() = user_id);
create policy "Individuals can delete their own api_keys." on api_keys for
    delete using (auth.uid() = user_id);

-- Initialize api_keys table
create table api_keys (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    api_key text not null unique,
    created_at bigint default extract(epoch from now()) not null,
    expires_at bigint
);

--- RLS for api_keys table

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

-- API Key Policies

create policy "Individuals can CRUD their own assistant_objects via API key."
    on assistant_objects for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key = current_setting('request.headers')::json->>'x-custom-api-key'
        )
    );

create policy "Individuals can CRUD their own thread_objects via API key."
    on thread_objects for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key = current_setting('request.headers')::json->>'x-custom-api-key'
        )
    );

create policy "Individuals can CRUD their own message_objects via API key."
    on message_objects for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key = current_setting('request.headers')::json->>'x-custom-api-key'
        )
    );

create policy "Individuals can CRUD their own file_objects via API key."
    on file_objects for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key = current_setting('request.headers')::json->>'x-custom-api-key'
        )
    );

create policy "Individuals can CRUD file_bucket via API key."
    on storage.buckets for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key = current_setting('request.headers')::json->>'x-custom-api-key'
        )
    );

create policy "Individuals can CRUD their own run_objects via API key."
    on run_objects for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key = current_setting('request.headers')::json->>'x-custom-api-key'
        )
    );

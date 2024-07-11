-- Initialize api_keys table
create table api_keys (
    name text,
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    api_key_hash text not null unique,
    created_at bigint default extract(epoch from now()) not null,
    expires_at bigint default null,
    checksum text not null
);

alter table api_keys enable row level security;

-- Hash the api key and store it in the table
create or replace function insert_api_key(
    p_name text,
    p_user_id uuid,
    p_api_key text,
    p_checksum text,
    p_expires_at bigint default null
) returns table (
    name text,
    id uuid,
    created_at bigint,
    expires_at bigint,
    checksum text
) language plpgsql as $$
declare
    v_name text;
    v_id uuid;
    v_created_at bigint;
    v_expires_at bigint;
    v_checksum text;
    v_hash text;
begin
    -- Calculate the one-way hash of the api key
    v_hash := crypt(p_api_key, gen_salt('bf'));

    insert into api_keys (name, user_id, api_key_hash, expires_at, checksum)
    values (p_name, p_user_id, v_hash, p_expires_at, p_checksum)
    returning api_keys.name, api_keys.id, api_keys.created_at, api_keys.expires_at, api_keys.checksum
    into v_name, v_id, v_created_at, v_expires_at, v_checksum;

    return query select v_name, v_id, v_created_at, v_expires_at, v_checksum;
end;
$$;

create policy "Read only if API key matches and is current" ON api_keys for
    select using (
        api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_key_hash)
        and (expires_at is null or expires_at > extract(epoch from now()))
    );

create policy "Individuals can crud their own api_keys." on api_keys for
    all using (auth.uid() = user_id);

-- API Key Policies

create policy "Individuals can CRUD their own assistant_objects via API key."
    on assistant_objects for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = assistant_objects.user_id
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
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = thread_objects.user_id
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
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = message_objects.user_id
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
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = file_objects.user_id
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
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
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
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = run_objects.user_id
        )
    );

create policy "Individuals can CRUD their own vector_store via API key."
    on vector_store for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = vector_store.user_id
        )
    );

create policy "Individuals can CRUD their own vector_store_file via API key."
    on vector_store_file for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = vector_store_file.user_id
        )
    );

create policy "Individuals can CRUD their own vector_content via API key."
    on vector_content for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
            and api_keys.user_id = vector_content.user_id
        )
    );

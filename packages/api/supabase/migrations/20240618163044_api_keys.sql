
create table api_keys (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    api_key text not null,
    created_at bigint default extract(epoch from now()) not null,
    expires_at bigint
);

alter table api_keys enable row level security;

create policy "Individuals can view their own api_keys." on api_keys for
    select using (auth.uid() = user_id);
create policy "Individuals can create api_keys." on api_keys for
    insert with check (auth.uid() = user_id);
create policy "Individuals can delete their own api_keys." on api_keys for
    delete using (auth.uid() = user_id);

create role validator_role noinherit;
grant usage on schema public to validator_role;
grant select on api_keys to validator_role;

-- Only validator role can view api_keys
create policy "Validator can view all api_keys." on api_keys for
    select using (auth.role() = 'validator_role');

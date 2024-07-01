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

create policy "Allow reading api_keys for verification" on api_keys
for select
to authenticated
using (true);

-- Update the insert policy
drop policy "Individuals can view their own assistant_objects. " on assistant_objects;
drop policy "Individuals can create assistant_objects." on assistant_objects;
drop policy "Individuals can update their own assistant_objects." on assistant_objects;
drop policy "Individuals can delete their own assistant_objects." on assistant_objects;

create policy "Individuals can CRUD their own assistant_objects." on assistant_objects for
    all with check (
        auth.uid() = user_id
        or
        exists (
            select 1 from api_keys
            where api_keys.api_key = current_setting('request.headers')::json->>'x-custom-api-key'
        )
    );

create or replace function debug_assistant_objects_insert() returns trigger as $$
begin
  raise log 'Attempting to insert: auth.uid=%, user_id=%, api_key=%',
    auth.uid(),
    NEW.user_id,
    current_setting('request.headers', true)::json->>'x-custom-api-key';
  return NEW;
end;
$$ language plpgsql;

create trigger debug_assistant_objects_insert_trigger
before insert on assistant_objects
for each row execute function debug_assistant_objects_insert();

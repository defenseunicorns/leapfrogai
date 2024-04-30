-- Create a table to store the OpenAI Thread Objects
create table
  thread_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    created_at bigint,
    metadata jsonb
  );

-- Create a table to store the OpenAI Message Objects
create table
  message_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    created_at bigint,
    thread_id uuid references thread_objects(id) on delete cascade,
    role text,
    content jsonb,
    file_ids uuid[],
    assistant_id uuid references assistant_objects(id) on delete set null,
    run_id uuid,
    metadata jsonb
  );

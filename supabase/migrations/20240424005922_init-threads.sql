-- Create a table to store the OpenAI Thread Objects
create table
  thread_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    created_at bigint,
    metadata jsonb,
    object text,
    tools_resources jsonb
  );

-- Create a table to store the OpenAI Message Objects
create table
  message_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    assistant_id uuid references assistant_objects(id) on delete set null,
    attachments jsonb,
    completed_at bigint,
    content jsonb,
    created_at bigint,
    incomplete_at bigint,
    incomplete_details text,
    metadata jsonb,
    object text,
    role text,
    run_id uuid,
    status text,
    thread_id uuid references thread_objects(id) on delete cascade
  );

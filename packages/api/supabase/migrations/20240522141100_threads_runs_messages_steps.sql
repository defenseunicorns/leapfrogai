-- Create a table to store the OpenAI Thread Objects
create table
  thread_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    user_id uuid references auth.users not null,
    object text check (object in ('thread')),
    created_at bigint default extract(epoch FROM NOW()) NOT NULL,
    tool_resources jsonb,
    metadata jsonb
  );

-- Create a table to store the OpenAI Message Objects
create table
  message_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    user_id uuid references auth.users not null,
    object text check (object in ('thread.message')),
    created_at bigint default extract(epoch FROM NOW()) not null,
    thread_id uuid references thread_objects (id) on delete cascade not null,
    status text,
    incomplete_details jsonb,
    completed_at bigint,
    incomplete_at bigint,
    role text,
    content jsonb,
    assistant_id uuid, -- No foreign key constraint, can be null and doesn't have to refer to an assistant that exists
    run_id uuid, -- No foreign key constraint, can be null and doesn't have to refer to a thread that exists
    attachments jsonb,
    metadata jsonb
  );

-- RLS policies
alter table thread_objects enable row level security;
alter table message_objects enable row level security;

-- Policies for thread_objects
create policy "Individuals can view their own thread_objects." on thread_objects for
    select using (auth.uid() = user_id);
create policy "Individuals can create thread_objects." on thread_objects for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own thread_objects." on thread_objects for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own thread_objects." on thread_objects for
    delete using (auth.uid() = user_id);

-- Policies for message_objects
create policy "Individuals can view their own message_objects." on message_objects for
    select using (auth.uid() = user_id);
create policy "Individuals can create message_objects." on message_objects for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own message_objects." on message_objects for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own message_objects." on message_objects for
    delete using (auth.uid() = user_id);

-- Indexes for foreign keys for message_objects
CREATE INDEX message_objects_user_id ON message_objects (user_id);
CREATE INDEX message_objects_thread_id ON message_objects (thread_id);
CREATE INDEX message_objects_created_at ON thread_objects (created_at);

-- Indexes for common filtering and sorting for thread_objects
CREATE INDEX thread_objects_id ON thread_objects (id);
CREATE INDEX thread_objects_user_id ON thread_objects (user_id);
CREATE INDEX thread_objects_created_at ON thread_objects (created_at);

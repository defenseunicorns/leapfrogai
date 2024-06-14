-- Create a table to store OpenAI Assistant Objects
create table
  assistant_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    created_at bigint default extract(epoch from now()) not null,
    description varchar(512),
    instructions text,
    metadata jsonb,
    model varchar(255) not null,
    name varchar(255),
    object text check (object in ('assistant')),
    tools jsonb,
    response_format jsonb,
    temperature float,
    tool_resources jsonb,
    top_p float
  );

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

-- Add user_id column to assistant_objects and file_objects tables
alter table assistant_objects
    add column user_id uuid references auth.users not null;
alter table file_objects
        add column user_id uuid references auth.users not null;
-- Set buckets to private
update storage.buckets
    set public = false
    where id = 'file_bucket';

-- RLS policies
alter table assistant_objects enable row level security;
alter table file_objects enable row level security;

-- Policies for assistant_objects
create policy "Individuals can view their own assistant_objects. " on assistant_objects for
    select using (auth.uid() = user_id);
create policy "Individuals can create assistant_objects." on assistant_objects for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own assistant_objects." on assistant_objects for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own assistant_objects." on assistant_objects for
    delete using (auth.uid() = user_id);

-- Policies for file_objects
create policy "Individuals can view their own file_objects." on file_objects for
    select using (auth.uid() = user_id);
create policy "Individuals can create file_objects." on file_objects for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own file_objects." on file_objects for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own file_objects." on file_objects for
    delete using (auth.uid() = user_id);

-- Policies for file_bucket
create policy "Any authenticated individual can add files to file_bucket."
on storage.objects for
    insert to authenticated with check (bucket_id = 'file_bucket');
create policy "Individuals can view their own files in the file_bucket."
on storage.objects for
    select using (bucket_id = 'file_bucket' AND auth.uid() = owner);
create policy "Individuals can delete their own files."
on storage.objects for
    delete using (bucket_id = 'file_bucket' AND auth.uid() = owner);
create policy "Individuals can update their own files in file_bucket."
on storage.objects for
    update using (auth.uid() = owner) with check (bucket_id = 'file_bucket');

ALTER TABLE file_objects ALTER COLUMN created_at SET DEFAULT extract(epoch from now());
ALTER TABLE file_objects ALTER COLUMN created_at SET NOT NULL;
ALTER TABLE file_objects ADD CHECK (object in ('file'));

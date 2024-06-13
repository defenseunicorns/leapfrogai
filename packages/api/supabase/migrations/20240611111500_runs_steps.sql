-- Create a table to store the OpenAI Run Objects
create table
  run_objects (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    object text check (object in ('thread.run')),
    created_at bigint default extract(epoch FROM NOW()) not null,
    thread_id uuid references thread_objects (id) on delete cascade ,
    assistant_id uuid references assistant_objects (id) on delete set null,
    status text,
    required_action jsonb,
    last_error jsonb,
    expires_at bigint,
    started_at bigint,
    cancelled_at bigint,
    failed_at bigint,
    completed_at bigint,
    model text,
    instructions text,
    tools jsonb,
    metadata jsonb,
    parallel_tool_calls boolean,
    stream boolean,
    file_ids uuid[],
    incomplete_details jsonb,
    usage jsonb,
    temperature float,
    top_p float,
    max_prompt_tokens int,
    max_completion_tokens int,
    truncation_strategy jsonb,
    tool_choice jsonb,
    response_format jsonb
  );

-- Create a table to store the OpenAI Run Step Objects
create table
  run_step_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    user_id uuid references auth.users not null,
    object text check (object in ('thread.run.step')),
    created_at bigint default extract(epoch FROM NOW()) not null,
    assistant_id uuid references assistant_objects (id) on delete set null,
    thread_id uuid references thread_objects (id) on delete cascade not null,
    run_id uuid references run_objects (id) on delete cascade not null,
    step_type text,
    status text,
    step_details jsonb,
    last_error jsonb,
    expired_at bigint,
    cancelled_at bigint,
    failed_at bigint,
    completed_at bigint,
    metadata jsonb,
    usage jsonb
  );

-- RLS policies
alter table run_objects enable row level security;
alter table run_step_objects enable row level security;

-- Policies for run_objects
create policy "Individuals can view their own run_objects." on run_objects for
    select using (auth.uid() = user_id);
create policy "Individuals can create run_objects." on run_objects for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own run_objects." on run_objects for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own run_objects." on run_objects for
    delete using (auth.uid() = user_id);

-- Policies for run_step_objects
create policy "Individuals can view their own run_step_objects." on run_step_objects for
    select using (auth.uid() = user_id);
create policy "Individuals can create run_step_objects." on run_step_objects for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own run_step_objects." on run_step_objects for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own run_step_objects." on run_step_objects for
    delete using (auth.uid() = user_id);

-- Indexes for common filtering and sorting for run_step_objects
CREATE INDEX run_step_id ON run_step_objects (id);
CREATE INDEX run_step_user_id ON run_step_objects (user_id);
CREATE INDEX run_step_created_at ON run_step_objects (created_at);

-- Indexes for common filtering and sorting for run_objects
CREATE INDEX run_objects_id ON run_objects (id);
CREATE INDEX run_objects_user_id ON run_objects (user_id);
CREATE INDEX run_objects_created_at ON run_objects (created_at);
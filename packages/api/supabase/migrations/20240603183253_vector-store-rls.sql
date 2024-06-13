-- RLS policies
alter table vector_store enable row level security;
alter table vector_store_file enable row level security;
alter table vector_content enable row level security;

-- Policies for vector_store
create policy "Individuals can view their own vector_store." on vector_store for
    select using (auth.uid() = user_id);
create policy "Individuals can create vector_store." on vector_store for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own vector_store." on vector_store for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own vector_store." on vector_store for
    delete using (auth.uid() = user_id);

-- Policies for vector_store_file
create policy "Individuals can view their own vector_store_file." on vector_store_file for
    select using (auth.uid() = user_id);
create policy "Individuals can create vector_store_file." on vector_store_file for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own vector_store_file." on vector_store_file for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own vector_store_file." on vector_store_file for
    delete using (auth.uid() = user_id);

-- Policies for vector_content
create policy "Individuals can view their own vector_content." on vector_content for
    select using (auth.uid() = user_id);
create policy "Individuals can create vector_content." on vector_content for
    insert with check (auth.uid() = user_id);
create policy "Individuals can update their own vector_content." on vector_content for
    update using (auth.uid() = user_id);
create policy "Individuals can delete their own vector_content." on vector_content for
    delete using (auth.uid() = user_id);

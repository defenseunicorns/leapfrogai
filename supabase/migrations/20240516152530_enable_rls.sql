-- RLS policies
alter table assistant_objects enable row level security;
alter table file_objects enable row level security;
alter table vector_store enable row level security;
alter table vector_store_file enable row level security;
alter table vector_content enable row level security;

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

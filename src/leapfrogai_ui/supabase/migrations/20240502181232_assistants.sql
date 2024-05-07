CREATE TABLE Assistants (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    object text CHECK (object in ('assistant')),
    name VARCHAR(255),
    description VARCHAR(512),
    model VARCHAR(255) NOT NULL,
    instructions TEXT,
    tools jsonb,
    tool_resources jsonb,
    metadata jsonb,
    temperature FLOAT,
    top_p FLOAT,
    response_format jsonb,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

alter table assistants enable row level security;

-- Policies for assistants
CREATE POLICY "Individuals can view their own assistants." ON assistants
FOR SELECT USING ((metadata ->> 'created_by') = auth.uid()::text);
create policy "Individuals can create assistants." on assistants for
    insert with check ((metadata ->> 'created_by') = auth.uid()::text);
create policy "Individuals can update their own assistants." on assistants for
update using ((metadata ->> 'created_by') = auth.uid()::text);
create policy "Individuals can delete their own assistants." on assistants for
    delete using ((metadata ->> 'created_by') = auth.uid()::text);
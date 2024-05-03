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

-- Create a table to store OpenAI Assistant Objects
create table
  assistant_objects (
    id uuid primary key DEFAULT uuid_generate_v4(),
    created_at bigint,
    description text,
    instructions text,
    metadata jsonb,
    model text,
    name text,
    object text,
    tools jsonb,
    response_format text,
    temperature float,
    tool_resources jsonb,
    top_p float
  );

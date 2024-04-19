-- Create a table to store OpenAI Assistant Objects
create table
  assistant_objects (
    id uuid primary key,
    object text,
    created_at bigint,
    name text,
    description text,
    model text,
    instructions text,
    tools text[],
    tool_resources jsonb,
    metadata jsonb,
    top_p float,
    temperature float,
    response_format text
  );

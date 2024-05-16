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

CREATE TABLE IF NOT EXISTS chat_completion (
    id SERIAL PRIMARY KEY,
    request_timestamp TIMESTAMP NOT NULL,
    username VARCHAR(32) NOT NULL,
    model_name VARCHAR(32) NOT NULL,
    messages BYTEA NOT NULL,
    response BYTEA
);
CREATE TABLE IF NOT EXISTS api_keys (
    api_key_sha512_base64 VARCHAR(88) PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS api_keys (
    api_key_sha512_base64 VARCHAR(88) PRIMARY KEY,
    user_id VARCHAR(20)
);
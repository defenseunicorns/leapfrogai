
-- Migration to delete expired API keys

CREATE OR REPLACE FUNCTION delete_expired_api_keys()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM api_keys WHERE expires_at < EXTRACT(EPOCH FROM NOW());
    RETURN NEW;
END;
$$;

-- Create a trigger to automatically delete expired API keys
CREATE TRIGGER trigger_delete_expired_api_keys
AFTER INSERT OR UPDATE ON api_keys
FOR EACH STATEMENT
EXECUTE FUNCTION delete_expired_api_keys();

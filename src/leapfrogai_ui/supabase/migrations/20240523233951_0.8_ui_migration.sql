-- Drop tables we no longer need (These tables are managed by the API now)
DO $$
BEGIN
    BEGIN
        DROP TABLE IF EXISTS messages;
    END;

    BEGIN
        DROP TABLE IF EXISTS conversations;
    END;

    BEGIN
        DROP TABLE IF EXISTS assistants;
    END;
END $$;

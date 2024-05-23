DO $$
BEGIN
    BEGIN
        DROP TABLE IF EXISTS messages;
    EXCEPTION
        WHEN others THEN
            -- do nothing, fail silently
    END;

    BEGIN
        DROP TABLE IF EXISTS conversations;
    EXCEPTION
        WHEN others THEN
            -- do nothing, fail silently
    END;
END $$;
-- Update existing null metadata entries to '{}'
UPDATE message_objects
SET metadata = '{}'
WHERE metadata IS NULL;

-- Alter the metadata column to set a default value and make it non-null
ALTER TABLE message_objects
ALTER COLUMN metadata SET DEFAULT '{}',
ALTER COLUMN metadata SET NOT NULL;
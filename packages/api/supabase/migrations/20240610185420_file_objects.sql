ALTER TABLE file_objects ALTER COLUMN created_at SET DEFAULT extract(epoch from now());
ALTER TABLE file_objects ALTER COLUMN created_at SET NOT NULL;
ALTER TABLE file_objects ADD CHECK (object in ('file'));

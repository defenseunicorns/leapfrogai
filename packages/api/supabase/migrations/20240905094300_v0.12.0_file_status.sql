-- Update the file_objects table to add an updated_at column
ALTER TABLE file_objects ADD COLUMN updated_at timestamp DEFAULT timezone('utc', now()) NOT NULL;

-- Create a trigger to automatically update the updated_at column
CREATE TRIGGER update_file_objects_modtime
BEFORE UPDATE ON file_objects
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Enable Supabase realtime for the file_objects table
alter publication supabase_realtime
add table file_objects;

-- Update the vector_store_file table to add an updated_at column
ALTER TABLE vector_store_file ADD COLUMN updated_at timestamp DEFAULT timezone('utc', now()) NOT NULL;

-- Add an index on user_id for faster queries
CREATE INDEX idx_vector_store_file_user_id ON vector_store_file(user_id);

-- Create a function to update the updated_at column
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc', now());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the updated_at column
CREATE TRIGGER update_vector_store_file_modtime
BEFORE UPDATE ON vector_store_file
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Enable Supabase realtime for the vector_store_file table
alter publication supabase_realtime
add table vector_store_file;

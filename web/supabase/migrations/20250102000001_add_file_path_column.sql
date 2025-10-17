-- Add file_path column to store original file location in Supabase Storage

ALTER TABLE public.processed_documents 
ADD COLUMN file_path TEXT;

-- Add comment to explain the column
COMMENT ON COLUMN public.processed_documents.file_path IS 'Path to original file in Supabase Storage (documents bucket)';
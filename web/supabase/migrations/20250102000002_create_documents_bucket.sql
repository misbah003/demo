-- Create storage bucket for original documents

-- Insert the bucket (if it doesn't exist)
INSERT INTO storage.buckets (id, name, public)
VALUES ('documents', 'documents', false)
ON CONFLICT (id) DO NOTHING;

-- Enable RLS on storage.objects
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Policy: Users can upload their own documents
CREATE POLICY "Users can upload own documents"
ON storage.objects
FOR INSERT
WITH CHECK (
  bucket_id = 'documents' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy: Users can view their own documents
CREATE POLICY "Users can view own documents"
ON storage.objects
FOR SELECT
USING (
  bucket_id = 'documents' AND
  (auth.uid()::text = (storage.foldername(name))[1] OR auth.role() = 'authenticated')
);

-- Policy: Users can delete their own documents
CREATE POLICY "Users can delete own documents"
ON storage.objects
FOR DELETE
USING (
  bucket_id = 'documents' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy: Allow public access for authenticated users (simplified)
-- This allows any authenticated user to read documents
-- Adjust based on your security requirements
CREATE POLICY "Authenticated users can read documents"
ON storage.objects
FOR SELECT
USING (
  bucket_id = 'documents' AND
  auth.role() = 'authenticated'
);
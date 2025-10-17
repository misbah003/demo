-- Update storage policies to allow avatar uploads in avatars/ folder

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can upload avatars" ON storage.objects;
DROP POLICY IF EXISTS "Users can update avatars" ON storage.objects;
DROP POLICY IF EXISTS "Anyone can view avatars" ON storage.objects;

-- Policy: Users can upload avatars (avatars folder)
CREATE POLICY "Users can upload avatars"
ON storage.objects
FOR INSERT
WITH CHECK (
  bucket_id = 'documents' AND
  (
    -- Allow uploads to user's own folder
    auth.uid()::text = (storage.foldername(name))[1]
    OR
    -- Allow uploads to avatars folder (filename contains user ID)
    (storage.foldername(name))[1] = 'avatars' AND
    name LIKE '%' || auth.uid()::text || '%'
  )
);

-- Policy: Users can update/replace their avatars
CREATE POLICY "Users can update avatars"
ON storage.objects
FOR UPDATE
USING (
  bucket_id = 'documents' AND
  (
    auth.uid()::text = (storage.foldername(name))[1]
    OR
    ((storage.foldername(name))[1] = 'avatars' AND name LIKE '%' || auth.uid()::text || '%')
  )
);

-- Policy: Anyone authenticated can view avatars (for profile pictures)
CREATE POLICY "Anyone can view avatars"
ON storage.objects
FOR SELECT
USING (
  bucket_id = 'documents' AND
  (
    -- Can view own documents
    auth.uid()::text = (storage.foldername(name))[1]
    OR
    -- Can view all avatars (profile pictures should be visible to all users)
    (storage.foldername(name))[1] = 'avatars'
    OR
    -- Authenticated users can view documents
    auth.role() = 'authenticated'
  )
);

-- Make the documents bucket public for avatars
UPDATE storage.buckets
SET public = true
WHERE id = 'documents';
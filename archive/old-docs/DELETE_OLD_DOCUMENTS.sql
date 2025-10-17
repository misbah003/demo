-- ============================================
-- DELETE OLD DOCUMENTS WITHOUT USER_ID
-- ============================================
-- Run this in your Supabase SQL Editor to delete all documents
-- that were uploaded before the user_id functionality was added.
--
-- After running this, re-upload your documents through the application
-- and they will be saved with your user_id.
-- ============================================

-- Delete all documents without user_id
DELETE FROM processed_documents WHERE user_id IS NULL;

-- Verify deletion (should return 0 rows)
SELECT COUNT(*) as documents_without_user_id 
FROM processed_documents 
WHERE user_id IS NULL;

-- Show remaining documents (should show only documents with user_id)
SELECT 
  id,
  user_id,
  filename,
  type,
  classification,
  processed_at
FROM processed_documents
ORDER BY processed_at DESC
LIMIT 10;

-- ============================================
-- OPTIONAL: Update RLS policies to require user_id
-- ============================================
-- Uncomment and run these if you want to enforce user_id requirement
-- This prevents any future documents from being saved without user_id

/*
DROP POLICY IF EXISTS "Users can view their own processed documents" ON public.processed_documents;
DROP POLICY IF EXISTS "Users can insert their own processed documents" ON public.processed_documents;
DROP POLICY IF EXISTS "Users can update their own processed documents" ON public.processed_documents;
DROP POLICY IF EXISTS "Users can delete their own processed documents" ON public.processed_documents;

CREATE POLICY "Users can view their own processed documents" 
ON public.processed_documents
FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own processed documents" 
ON public.processed_documents
FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own processed documents" 
ON public.processed_documents
FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own processed documents" 
ON public.processed_documents
FOR DELETE USING (auth.uid() = user_id);
*/
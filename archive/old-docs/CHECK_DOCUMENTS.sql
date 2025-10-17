-- ============================================
-- DIAGNOSTIC QUERY FOR VAT DOCUMENTS
-- ============================================
-- Run this in Supabase SQL Editor to check your documents

-- 1. Check if processed_documents table exists
SELECT 'processed_documents table exists: ' || 
  CASE WHEN EXISTS (
    SELECT FROM pg_tables 
    WHERE schemaname = 'public' 
    AND tablename = 'processed_documents'
  ) THEN 'YES' ELSE 'NO' END as status;

-- 2. Check total documents count
SELECT 'Total documents: ' || count(*)::text as status
FROM public.processed_documents;

-- 3. Check VAT documents count
SELECT 'VAT documents: ' || count(*)::text as status
FROM public.processed_documents
WHERE type ILIKE '%VAT%';

-- 4. Show all documents with their types
SELECT 
  id,
  user_id,
  type,
  processed_at,
  entities
FROM public.processed_documents
ORDER BY processed_at DESC
LIMIT 10;

-- 5. Check if your user has any documents
SELECT 
  'Your documents: ' || count(*)::text as status
FROM public.processed_documents
WHERE user_id = auth.uid();

-- 6. Check if your user has VAT documents
SELECT 
  'Your VAT documents: ' || count(*)::text as status
FROM public.processed_documents
WHERE user_id = auth.uid()
  AND type ILIKE '%VAT%';

-- 7. Show your VAT documents details
SELECT 
  id,
  type,
  processed_at,
  entities,
  CASE 
    WHEN entities IS NULL THEN 'No entities'
    WHEN jsonb_typeof(entities) = 'array' THEN 'Array with ' || jsonb_array_length(entities)::text || ' items'
    ELSE 'Not an array'
  END as entities_info
FROM public.processed_documents
WHERE user_id = auth.uid()
  AND type ILIKE '%VAT%'
ORDER BY processed_at DESC;
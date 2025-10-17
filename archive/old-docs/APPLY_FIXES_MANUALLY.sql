-- ============================================
-- MANUAL FIX SCRIPT FOR SUPABASE DASHBOARD
-- ============================================
-- Copy and paste this entire script into the Supabase SQL Editor
-- and run it to fix all RLS policy issues

-- ============================================
-- 1. CREATE VAT APPLICATIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS public.vat_applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  business_type TEXT NOT NULL,
  annual_turnover NUMERIC(15, 2) NOT NULL,
  vat_paid NUMERIC(15, 2) NOT NULL,
  input_vat NUMERIC(15, 2) NOT NULL,
  category TEXT NOT NULL,
  region TEXT NOT NULL,
  filing_status TEXT NOT NULL,
  predicted_refund NUMERIC(15, 2) NOT NULL,
  approval_probability NUMERIC(5, 2) NOT NULL,
  processing_days INTEGER NOT NULL,
  risk_level TEXT NOT NULL,
  compliance_flag TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'Submitted',
  submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_vat_applications_user_id ON public.vat_applications(user_id);
CREATE INDEX IF NOT EXISTS idx_vat_applications_status ON public.vat_applications(status);
CREATE INDEX IF NOT EXISTS idx_vat_applications_submitted_at ON public.vat_applications(submitted_at DESC);

-- Enable RLS
ALTER TABLE public.vat_applications ENABLE ROW LEVEL SECURITY;

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view their own applications" ON public.vat_applications;
DROP POLICY IF EXISTS "Users can insert their own applications" ON public.vat_applications;
DROP POLICY IF EXISTS "Users can update their own applications" ON public.vat_applications;

-- Create policies
CREATE POLICY "Users can view their own applications"
  ON public.vat_applications
  FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own applications"
  ON public.vat_applications
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own applications"
  ON public.vat_applications
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- ============================================
-- 2. FIX PROFILES TABLE RLS
-- ============================================

-- Ensure profiles table has all columns
ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS phone TEXT;
ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS department TEXT;
ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS position TEXT;
ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS location TEXT;
ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS join_date DATE;

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view their own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can update their own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can insert their own profile" ON public.profiles;

-- Create policies with WITH CHECK clause
CREATE POLICY "Users can view their own profile" 
  ON public.profiles 
  FOR SELECT 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own profile" 
  ON public.profiles 
  FOR UPDATE 
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can insert their own profile" 
  ON public.profiles 
  FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

-- ============================================
-- 3. FIX STORAGE POLICIES
-- ============================================

-- Ensure documents bucket exists and is public
INSERT INTO storage.buckets (id, name, public)
VALUES ('documents', 'documents', true)
ON CONFLICT (id) DO UPDATE SET public = true;

-- Drop ALL existing storage policies to avoid conflicts
DROP POLICY IF EXISTS "Users can upload their own documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can view their own documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can delete their own documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can upload avatars" ON storage.objects;
DROP POLICY IF EXISTS "Anyone can view avatars" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can upload documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can view documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can delete documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can update their own documents" ON storage.objects;

-- Create comprehensive storage policies
CREATE POLICY "Users can upload their own documents"
  ON storage.objects
  FOR INSERT
  WITH CHECK (
    bucket_id = 'documents' AND
    (
      auth.uid()::text = (storage.foldername(name))[1] OR
      (storage.foldername(name))[1] = 'avatars'
    )
  );

CREATE POLICY "Users can view documents"
  ON storage.objects
  FOR SELECT
  USING (
    bucket_id = 'documents' AND
    (
      auth.uid()::text = (storage.foldername(name))[1] OR
      (storage.foldername(name))[1] = 'avatars'
    )
  );

CREATE POLICY "Users can delete their own documents"
  ON storage.objects
  FOR DELETE
  USING (
    bucket_id = 'documents' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can update their own documents"
  ON storage.objects
  FOR UPDATE
  USING (
    bucket_id = 'documents' AND
    (
      auth.uid()::text = (storage.foldername(name))[1] OR
      (storage.foldername(name))[1] = 'avatars'
    )
  )
  WITH CHECK (
    bucket_id = 'documents' AND
    (
      auth.uid()::text = (storage.foldername(name))[1] OR
      (storage.foldername(name))[1] = 'avatars'
    )
  );

-- ============================================
-- 4. VERIFY SETUP
-- ============================================

-- Check if tables exist
SELECT 'vat_applications table exists' as status 
WHERE EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'vat_applications');

SELECT 'profiles table exists' as status 
WHERE EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'profiles');

-- Check if policies exist
SELECT 'VAT Applications policies: ' || count(*)::text as status
FROM pg_policies 
WHERE schemaname = 'public' AND tablename = 'vat_applications';

SELECT 'Profiles policies: ' || count(*)::text as status
FROM pg_policies 
WHERE schemaname = 'public' AND tablename = 'profiles';

SELECT 'Storage policies: ' || count(*)::text as status
FROM pg_policies 
WHERE schemaname = 'storage' AND tablename = 'objects';

-- Show all policies for verification
SELECT schemaname, tablename, policyname, cmd, qual::text as using_clause, with_check::text as with_check_clause
FROM pg_policies 
WHERE schemaname IN ('public', 'storage') 
  AND tablename IN ('vat_applications', 'profiles', 'objects')
ORDER BY schemaname, tablename, policyname;
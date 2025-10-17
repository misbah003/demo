-- Fix RLS policies for all tables
-- This migration ensures all necessary policies exist

-- ============================================
-- VAT APPLICATIONS TABLE
-- ============================================

-- Create table if it doesn't exist
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

-- Add indexes if they don't exist
CREATE INDEX IF NOT EXISTS idx_vat_applications_user_id ON public.vat_applications(user_id);
CREATE INDEX IF NOT EXISTS idx_vat_applications_status ON public.vat_applications(status);
CREATE INDEX IF NOT EXISTS idx_vat_applications_submitted_at ON public.vat_applications(submitted_at DESC);

-- Enable RLS
ALTER TABLE public.vat_applications ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
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
-- PROFILES TABLE
-- ============================================

-- Ensure profiles table exists
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  phone TEXT,
  department TEXT,
  position TEXT,
  location TEXT,
  join_date DATE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can update their own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can insert their own profile" ON public.profiles;

-- Create policies
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
-- STORAGE POLICIES
-- ============================================

-- Ensure documents bucket exists and is public
INSERT INTO storage.buckets (id, name, public)
VALUES ('documents', 'documents', true)
ON CONFLICT (id) DO UPDATE SET public = true;

-- Drop existing storage policies
DROP POLICY IF EXISTS "Users can upload their own documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can view their own documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can delete their own documents" ON storage.objects;
DROP POLICY IF EXISTS "Users can upload avatars" ON storage.objects;
DROP POLICY IF EXISTS "Anyone can view avatars" ON storage.objects;

-- Create storage policies for documents
CREATE POLICY "Users can upload their own documents"
  ON storage.objects
  FOR INSERT
  WITH CHECK (
    bucket_id = 'documents' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can view their own documents"
  ON storage.objects
  FOR SELECT
  USING (
    bucket_id = 'documents' AND
    (auth.uid()::text = (storage.foldername(name))[1] OR (storage.foldername(name))[1] = 'avatars')
  );

CREATE POLICY "Users can delete their own documents"
  ON storage.objects
  FOR DELETE
  USING (
    bucket_id = 'documents' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

-- Create storage policies for avatars (public access)
CREATE POLICY "Users can upload avatars"
  ON storage.objects
  FOR INSERT
  WITH CHECK (
    bucket_id = 'documents' AND
    (storage.foldername(name))[1] = 'avatars' AND
    auth.role() = 'authenticated'
  );

CREATE POLICY "Anyone can view avatars"
  ON storage.objects
  FOR SELECT
  USING (
    bucket_id = 'documents' AND
    (storage.foldername(name))[1] = 'avatars'
  );

-- Add comments
COMMENT ON TABLE public.vat_applications IS 'Stores VAT refund applications submitted by users';
COMMENT ON TABLE public.profiles IS 'Extended user profile information';
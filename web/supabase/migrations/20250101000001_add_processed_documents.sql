-- Add table for processed documents

CREATE TABLE public.processed_documents (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  type TEXT NOT NULL,
  entities JSONB,
  classification TEXT NOT NULL,
  confidence DECIMAL(3,2) NOT NULL,
  processed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.processed_documents ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view their own processed documents" ON public.processed_documents
  FOR SELECT USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can insert their own processed documents" ON public.processed_documents
  FOR INSERT WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can update their own processed documents" ON public.processed_documents
  FOR UPDATE USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can delete their own processed documents" ON public.processed_documents
  FOR DELETE USING (auth.uid() = user_id OR user_id IS NULL);
-- Extend profiles table with additional fields
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS phone TEXT,
ADD COLUMN IF NOT EXISTS department TEXT,
ADD COLUMN IF NOT EXISTS position TEXT,
ADD COLUMN IF NOT EXISTS location TEXT,
ADD COLUMN IF NOT EXISTS join_date DATE;

-- Add comment for documentation
COMMENT ON COLUMN public.profiles.phone IS 'User phone number';
COMMENT ON COLUMN public.profiles.department IS 'User department';
COMMENT ON COLUMN public.profiles.position IS 'User job position';
COMMENT ON COLUMN public.profiles.location IS 'User country/location';
COMMENT ON COLUMN public.profiles.join_date IS 'User join date';
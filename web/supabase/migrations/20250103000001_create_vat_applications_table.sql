-- Create VAT Applications table to store user applications
CREATE TABLE IF NOT EXISTS vat_applications (
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

-- Add index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_vat_applications_user_id ON vat_applications(user_id);

-- Add index on status for filtering
CREATE INDEX IF NOT EXISTS idx_vat_applications_status ON vat_applications(status);

-- Add index on submitted_at for sorting
CREATE INDEX IF NOT EXISTS idx_vat_applications_submitted_at ON vat_applications(submitted_at DESC);

-- Enable Row Level Security
ALTER TABLE vat_applications ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can only see their own applications
CREATE POLICY "Users can view their own applications"
  ON vat_applications
  FOR SELECT
  USING (auth.uid() = user_id);

-- Create policy: Users can insert their own applications
CREATE POLICY "Users can insert their own applications"
  ON vat_applications
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Create policy: Users can update their own applications
CREATE POLICY "Users can update their own applications"
  ON vat_applications
  FOR UPDATE
  USING (auth.uid() = user_id);

-- Add comments for documentation
COMMENT ON TABLE vat_applications IS 'Stores VAT refund applications submitted by users';
COMMENT ON COLUMN vat_applications.user_id IS 'Reference to the user who submitted the application';
COMMENT ON COLUMN vat_applications.business_type IS 'Type of business (e.g., Retail, Manufacturing)';
COMMENT ON COLUMN vat_applications.annual_turnover IS 'Annual business turnover in rupees';
COMMENT ON COLUMN vat_applications.vat_paid IS 'Total VAT paid in rupees';
COMMENT ON COLUMN vat_applications.input_vat IS 'Input VAT claimed in rupees';
COMMENT ON COLUMN vat_applications.predicted_refund IS 'ML model predicted refund amount';
COMMENT ON COLUMN vat_applications.approval_probability IS 'Probability of approval (0-100)';
COMMENT ON COLUMN vat_applications.processing_days IS 'Estimated processing days';
COMMENT ON COLUMN vat_applications.risk_level IS 'Risk assessment (LOW, MEDIUM, HIGH)';
COMMENT ON COLUMN vat_applications.compliance_flag IS 'Compliance status';
COMMENT ON COLUMN vat_applications.status IS 'Application status (Submitted, Under Review, Approved, Rejected)';
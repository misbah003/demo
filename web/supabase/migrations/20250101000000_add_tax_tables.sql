-- Add tables for tax compliance data

-- Companies table
CREATE TABLE public.companies (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  business_type TEXT,
  turnover DECIMAL(15,2),
  registration_date DATE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Filings table
CREATE TABLE public.filings (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES public.companies(id) ON DELETE CASCADE,
  filing_type TEXT NOT NULL, -- e.g., 'VAT', 'Income Tax'
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,
  due_date DATE NOT NULL,
  submitted_date DATE,
  status TEXT NOT NULL DEFAULT 'pending', -- pending, submitted, late, rejected
  amount DECIMAL(15,2),
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- VAT transactions table
CREATE TABLE public.vat_transactions (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES public.companies(id) ON DELETE CASCADE,
  transaction_date DATE NOT NULL,
  type TEXT NOT NULL, -- 'input' or 'output'
  amount DECIMAL(15,2) NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.filings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vat_transactions ENABLE ROW LEVEL SECURITY;

-- Policies for companies
CREATE POLICY "Users can view their own companies" ON public.companies
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own companies" ON public.companies
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own companies" ON public.companies
  FOR UPDATE USING (auth.uid() = user_id);

-- Policies for filings (via company)
CREATE POLICY "Users can view filings for their companies" ON public.filings
  FOR SELECT USING (company_id IN (SELECT id FROM public.companies WHERE user_id = auth.uid()));
CREATE POLICY "Users can insert filings for their companies" ON public.filings
  FOR INSERT WITH CHECK (company_id IN (SELECT id FROM public.companies WHERE user_id = auth.uid()));
CREATE POLICY "Users can update filings for their companies" ON public.filings
  FOR UPDATE USING (company_id IN (SELECT id FROM public.companies WHERE user_id = auth.uid()));

-- Policies for vat_transactions
CREATE POLICY "Users can view vat transactions for their companies" ON public.vat_transactions
  FOR SELECT USING (company_id IN (SELECT id FROM public.companies WHERE user_id = auth.uid()));
CREATE POLICY "Users can insert vat transactions for their companies" ON public.vat_transactions
  FOR INSERT WITH CHECK (company_id IN (SELECT id FROM public.companies WHERE user_id = auth.uid()));
CREATE POLICY "Users can update vat transactions for their companies" ON public.vat_transactions
  FOR UPDATE USING (company_id IN (SELECT id FROM public.companies WHERE user_id = auth.uid()));

-- Triggers for updated_at
CREATE TRIGGER update_companies_updated_at
  BEFORE UPDATE ON public.companies
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_filings_updated_at
  BEFORE UPDATE ON public.filings
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- Insert some sample data for testing
INSERT INTO public.companies (user_id, name, business_type, turnover, registration_date) VALUES
('00000000-0000-0000-0000-000000000000', 'Sample Company', 'Retail', 1000000.00, '2023-01-01');

INSERT INTO public.filings (company_id, filing_type, period_start, period_end, due_date, submitted_date, status, amount) VALUES
((SELECT id FROM public.companies LIMIT 1), 'VAT', '2023-01-01', '2023-03-31', '2023-04-30', '2023-04-25', 'submitted', 15000.00),
((SELECT id FROM public.companies LIMIT 1), 'VAT', '2023-04-01', '2023-06-30', '2023-07-31', NULL, 'late', 18000.00);

INSERT INTO public.vat_transactions (company_id, transaction_date, type, amount, description) VALUES
((SELECT id FROM public.companies LIMIT 1), '2023-01-15', 'input', 5000.00, 'Purchase supplies'),
((SELECT id FROM public.companies LIMIT 1), '2023-01-20', 'output', 3000.00, 'Sales VAT'),
((SELECT id FROM public.companies LIMIT 1), '2023-02-15', 'input', 4000.00, 'Purchase inventory'),
((SELECT id FROM public.companies LIMIT 1), '2023-02-20', 'output', 2500.00, 'Sales VAT');
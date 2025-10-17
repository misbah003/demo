import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

interface KpiMetrics {
  taxComplianceScore: number
  vatCollectionPredicted: number
  anomalyDetectionCount: number
  processingEfficiency: number
  trends?: {
    compliance: number[]
    collection: number[]
    anomalies: number[]
    efficiency: number[]
  }
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    )

    const { data: { user } } = await supabaseClient.auth.getUser()

    if (!user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Get user's companies
    const { data: companies } = await supabaseClient
      .from('companies')
      .select('id, name, turnover')
      .eq('user_id', user.id)

    if (!companies || companies.length === 0) {
      const emptyMetrics: KpiMetrics = {
        taxComplianceScore: 0,
        vatCollectionPredicted: 0,
        anomalyDetectionCount: 0,
        processingEfficiency: 0
      }
      return new Response(JSON.stringify(emptyMetrics), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    const companyIds = companies.map(c => c.id)

    // Get filings data
    const { data: filings } = await supabaseClient
      .from('filings')
      .select('*')
      .in('company_id', companyIds)

    // Get VAT transactions
    const { data: vatTransactions } = await supabaseClient
      .from('vat_transactions')
      .select('*')
      .in('company_id', companyIds)
      .order('transaction_date', { ascending: false })

    // Calculate metrics
    const totalFilings = filings?.length || 0
    const compliantFilings = filings?.filter(f => f.status === 'submitted' && f.submitted_date <= f.due_date).length || 0
    const taxComplianceScore = totalFilings > 0 ? Math.round((compliantFilings / totalFilings) * 100) : 100

    // VAT Collection Predicted - forecast based on turnover and historical VAT
    const totalTurnover = companies.reduce((sum, c) => sum + (c.turnover || 0), 0)
    const recentVatPaid = vatTransactions?.filter(t => t.type === 'output').slice(0, 10).reduce((sum, t) => sum + t.amount, 0) || 0
    const vatCollectionPredicted = Math.round((recentVatPaid / 10) * 12 * 1.05) // monthly average * 12 * 5% growth

    // Anomaly Detection - simple threshold-based
    const avgTransaction = vatTransactions?.length > 0 ?
      vatTransactions.reduce((sum, t) => sum + t.amount, 0) / vatTransactions.length : 0
    const anomalies = vatTransactions?.filter(t => Math.abs(t.amount - avgTransaction) > avgTransaction * 2).length || 0

    // Processing Efficiency - assume average processing time (placeholder)
    const processingEfficiency = Math.max(0, 100 - (anomalies * 5) - ((totalFilings - compliantFilings) * 2))

    const metrics: KpiMetrics = {
      taxComplianceScore,
      vatCollectionPredicted,
      anomalyDetectionCount: anomalies,
      processingEfficiency: Math.round(processingEfficiency)
    }

    return new Response(JSON.stringify(metrics), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('Error:', error)
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

interface RiskFactor {
  title: string
  score: number
  status: 'low' | 'medium' | 'high'
  reasons: string[]
}

interface ComplianceRiskResponse {
  riskFactors: RiskFactor[]
  overallScore: number
  overallStatus: 'low' | 'medium' | 'high'
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
    const { data: companies, error: companiesError } = await supabaseClient
      .from('companies')
      .select('id, name')
      .eq('user_id', user.id)

    if (companiesError) throw companiesError

    if (!companies || companies.length === 0) {
      return new Response(JSON.stringify({
        riskFactors: [],
        overallScore: 0,
        overallStatus: 'low' as const
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    const companyIds = companies.map(c => c.id)

    // Get filings data
    const { data: filings, error: filingsError } = await supabaseClient
      .from('filings')
      .select('*')
      .in('company_id', companyIds)

    if (filingsError) throw filingsError

    // Calculate risk scores
    const totalFilings = filings?.length || 0
    const lateFilings = filings?.filter(f => f.status === 'late').length || 0
    const lateFilingRisk = totalFilings > 0 ? (lateFilings / totalFilings) * 100 : 0

    // Documentation gap - assume missing docs if submitted_date is null for pending
    const missingDocsFilings = filings?.filter(f => !f.submitted_date && f.status === 'pending').length || 0
    const docGapRisk = totalFilings > 0 ? (missingDocsFilings / totalFilings) * 100 : 0

    // Audit probability - simple model based on turnover and late filings
    // Get company turnover
    const { data: companyData } = await supabaseClient
      .from('companies')
      .select('turnover')
      .in('id', companyIds)
      .single()

    const turnover = companyData?.turnover || 0
    const auditRisk = Math.min(100, (turnover / 1000000) * 20 + lateFilingRisk * 0.5)

    // Penalty risk - based on late filings and amount
    const penaltyRisk = lateFilingRisk + (auditRisk * 0.3)

    const riskFactors: RiskFactor[] = [
      {
        title: 'Late Filing Risk',
        score: Math.round(lateFilingRisk),
        status: lateFilingRisk < 20 ? 'low' : lateFilingRisk < 50 ? 'medium' : 'high',
        reasons: lateFilings > 0 ? [`${lateFilings} late filings out of ${totalFilings}`] : ['No late filings']
      },
      {
        title: 'Documentation Gap',
        score: Math.round(docGapRisk),
        status: docGapRisk < 30 ? 'low' : docGapRisk < 60 ? 'medium' : 'high',
        reasons: missingDocsFilings > 0 ? [`${missingDocsFilings} filings with missing documentation`] : ['All documents submitted']
      },
      {
        title: 'Audit Probability',
        score: Math.round(auditRisk),
        status: auditRisk < 25 ? 'low' : auditRisk < 50 ? 'medium' : 'high',
        reasons: [`Based on turnover of ₹${turnover.toLocaleString()} and filing history`]
      },
      {
        title: 'Penalty Risk',
        score: Math.round(Math.min(100, penaltyRisk)),
        status: penaltyRisk < 40 ? 'low' : penaltyRisk < 70 ? 'medium' : 'high',
        reasons: lateFilings > 0 ? [`${lateFilings} late filings may incur penalties`] : ['No penalty risks identified']
      }
    ]

    const overallScore = Math.round(riskFactors.reduce((sum, r) => sum + r.score, 0) / riskFactors.length)
    const overallStatus = overallScore < 30 ? 'low' : overallScore < 60 ? 'medium' : 'high'

    const response: ComplianceRiskResponse = {
      riskFactors,
      overallScore,
      overallStatus
    }

    return new Response(JSON.stringify(response), {
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
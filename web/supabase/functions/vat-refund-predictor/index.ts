import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

interface VatPredictionRequest {
  businessType: string
  turnover: number
  vatPaid: number
  vatClaimed: number
}

interface VatPredictionResponse {
  predictedRefund: number
  approvalProbability: number
  breakdown: {
    inputVat: number
    outputVat: number
    netRefund: number
    adjustments: string[]
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

    if (req.method === 'POST') {
      const { businessType, turnover, vatPaid, vatClaimed }: VatPredictionRequest = await req.json()

      // Simple rule-based prediction
      // In real ML, this would use trained model
      const inputVat = vatClaimed
      const outputVat = vatPaid
      const basicRefund = Math.max(0, inputVat - outputVat)

      // Approval probability based on business type and amounts
      let baseProbability = 0.8 // 80% base
      if (businessType === 'retail') baseProbability += 0.05
      if (turnover > 500000) baseProbability += 0.05
      if (vatClaimed > vatPaid * 1.5) baseProbability -= 0.1 // suspicious if claiming much more than paid

      const approvalProbability = Math.min(1, Math.max(0, baseProbability))

      // Adjustments based on historical data (simulated)
      const adjustments = []
      if (vatClaimed > vatPaid) {
        adjustments.push('Eligible for refund based on input VAT exceeding output VAT')
      }
      if (turnover < 100000) {
        adjustments.push('Small business - higher approval rate')
        baseProbability += 0.1
      }

      const predictedRefund = basicRefund * approvalProbability

      const response: VatPredictionResponse = {
        predictedRefund: Math.round(predictedRefund),
        approvalProbability: Math.round(approvalProbability * 100),
        breakdown: {
          inputVat: vatClaimed,
          outputVat: vatPaid,
          netRefund: basicRefund,
          adjustments
        }
      }

      return new Response(JSON.stringify(response), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // GET request - return historical data for training (placeholder)
    const { data: { user } } = await supabaseClient.auth.getUser()

    if (!user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    const { data: vatData, error } = await supabaseClient
      .from('vat_transactions')
      .select('*')
      .eq('company_id', (await supabaseClient.from('companies').select('id').eq('user_id', user.id).single()).data?.id)

    if (error) throw error

    return new Response(JSON.stringify({ vatData }), {
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
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import jsPDF from 'https://esm.sh/jspdf@2.5.1'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
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

    // Get risk data by calling the compliance-risk function
    // For simplicity, duplicate the logic here
    const { data: companies } = await supabaseClient
      .from('companies')
      .select('id, name')
      .eq('user_id', user.id)

    const companyIds = companies?.map(c => c.id) || []

    const { data: filings } = await supabaseClient
      .from('filings')
      .select('*')
      .in('company_id', companyIds)

    const totalFilings = filings?.length || 0
    const lateFilings = filings?.filter(f => f.status === 'late').length || 0

    // Generate PDF report
    const doc = new jsPDF()

    doc.setFontSize(20)
    doc.text('Compliance Risk Assessment Report', 20, 30)

    doc.setFontSize(12)
    doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 20, 50)
    doc.text(`User: ${user.email}`, 20, 60)

    doc.text('Risk Summary:', 20, 80)
    doc.text(`Total Filings: ${totalFilings}`, 30, 90)
    doc.text(`Late Filings: ${lateFilings}`, 30, 100)
    doc.text(`Compliance Rate: ${totalFilings > 0 ? Math.round(((totalFilings - lateFilings) / totalFilings) * 100) : 100}%`, 30, 110)

    doc.text('Recommendations:', 20, 130)
    if (lateFilings > 0) {
      doc.text(`- Address ${lateFilings} late filings to improve compliance`, 30, 140)
    }
    doc.text('- Maintain regular filing schedule', 30, 150)
    doc.text('- Keep documentation up to date', 30, 160)

    const pdfBytes = doc.output('arraybuffer')

    return new Response(pdfBytes, {
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename=compliance-report.pdf'
      }
    })

  } catch (error) {
    console.error('Error:', error)
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})
// Test script to verify Supabase connection and data
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  'https://ikqcakganqabiscsibym.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrcWNha2dhbnFhYmlzY3NpYnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjc0NDIsImV4cCI6MjA3Mzk0MzQ0Mn0.hkfGO88f95rQO_7bwsRcxADjZRAjw5LoWFxmq5mNY90'
);

async function testConnection() {
  console.log('🔍 Testing Supabase connection...');
  
  try {
    // Fetch all documents
    const { data, error } = await supabase
      .from('processed_documents')
      .select('*')
      .order('created_at', { ascending: false });
    
    if (error) {
      console.error('❌ Error fetching documents:', error);
      return;
    }
    
    console.log(`✅ Successfully connected to Supabase!`);
    console.log(`📊 Found ${data.length} documents in the database:`);
    
    data.forEach((doc, index) => {
      console.log(`\n${index + 1}. ${doc.filename}`);
      console.log(`   Type: ${doc.type}`);
      console.log(`   Classification: ${doc.classification}`);
      console.log(`   Confidence: ${doc.confidence}`);
      console.log(`   Created: ${doc.created_at}`);
    });
    
  } catch (err) {
    console.error('❌ Unexpected error:', err);
  }
}

testConnection();
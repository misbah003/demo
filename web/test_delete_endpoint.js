// Test script to diagnose delete endpoint issues
const fetch = require('node-fetch');

const API_URL = 'http://localhost:3001';

async function testDeleteEndpoint() {
  console.log('🔍 Testing Delete Endpoint Diagnostics\n');
  
  // Test 1: Check if backend is running
  console.log('1️⃣ Testing backend health...');
  try {
    const healthResponse = await fetch(`${API_URL}/health`);
    if (healthResponse.ok) {
      console.log('✅ Backend is running\n');
    } else {
      console.log('❌ Backend returned error:', healthResponse.status, '\n');
      return;
    }
  } catch (error) {
    console.log('❌ Backend is NOT running!');
    console.log('   Error:', error.message);
    console.log('   Please start the backend server first.\n');
    return;
  }

  // Test 2: List documents to get a valid ID
  console.log('2️⃣ Fetching documents list...');
  try {
    const docsResponse = await fetch(`${API_URL}/api/documents`);
    const docsData = await docsResponse.json();
    
    if (docsData.success && docsData.documents && docsData.documents.length > 0) {
      console.log(`✅ Found ${docsData.documents.length} document(s)`);
      console.log('   First document:', docsData.documents[0].filename);
      console.log('   ID:', docsData.documents[0].id, '\n');
      
      // Test 3: Try to delete (with confirmation)
      const testDocId = docsData.documents[0].id;
      console.log('3️⃣ Testing DELETE endpoint (dry run - not actually deleting)...');
      console.log(`   Would delete: ${docsData.documents[0].filename}`);
      console.log(`   Endpoint: DELETE ${API_URL}/api/documents/${testDocId}\n`);
      
      // Uncomment below to actually test deletion
      /*
      const deleteResponse = await fetch(`${API_URL}/api/documents/${testDocId}`, {
        method: 'DELETE',
      });
      const deleteData = await deleteResponse.json();
      console.log('   Response:', deleteData);
      */
      
    } else {
      console.log('⚠️ No documents found in database');
      console.log('   Upload a document first to test deletion\n');
    }
  } catch (error) {
    console.log('❌ Error fetching documents:', error.message, '\n');
  }

  // Test 4: Check for common issues
  console.log('4️⃣ Common Issues Checklist:');
  console.log('   □ Is backend server running? (node backend-example/server.js)');
  console.log('   □ Is Supabase connection configured?');
  console.log('   □ Are RLS policies allowing deletes?');
  console.log('   □ Is the document ID valid (UUID format)?');
  console.log('   □ Check browser console for CORS errors');
  console.log('   □ Check backend terminal for error logs\n');
}

testDeleteEndpoint().catch(console.error);
// Quick test script to verify email sending
const fetch = require('node-fetch');

async function testEmail() {
  try {
    console.log('🧪 Testing email sending...');
    
    const response = await fetch('http://localhost:3001/api/send-otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        to: 'misbahanwar16@gmail.com', // Send test email to yourself
        otpCode: '123456'
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log('✅ SUCCESS! Email sent successfully!');
      console.log('📧 Check your inbox at misbahanwar16@gmail.com');
    } else {
      console.log('❌ FAILED:', result.error);
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

testEmail();
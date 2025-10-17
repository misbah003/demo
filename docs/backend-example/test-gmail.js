// Test Gmail SMTP connection
const nodemailer = require('nodemailer').default || require('nodemailer');
require('dotenv').config();

async function testGmailConnection() {
  console.log('🔍 Testing Gmail SMTP connection...\n');
  
  console.log('📧 Gmail User:', process.env.GMAIL_USER);
  console.log('🔐 App Password:', process.env.GMAIL_APP_PASSWORD ? '✅ Set' : '❌ Not set');
  console.log('');
  
  try {
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD
      },
      secure: true,
      tls: {
        rejectUnauthorized: false
      }
    });
    
    console.log('🔄 Verifying SMTP connection...');
    await transporter.verify();
    console.log('✅ SMTP connection verified successfully!\n');
    
    console.log('📨 Sending test email...');
    const info = await transporter.sendMail({
      from: `"Tax Intelligence" <${process.env.GMAIL_USER}>`,
      to: process.env.GMAIL_USER,
      subject: 'Test Email - Tax Intelligence',
      html: '<h1>Success!</h1><p>Your email configuration is working correctly!</p>',
      text: 'Success! Your email configuration is working correctly!'
    });
    
    console.log('✅ Email sent successfully!');
    console.log('📬 Message ID:', info.messageId);
    console.log('\n🎉 Everything is working! Check your inbox at', process.env.GMAIL_USER);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error('\n🔍 Troubleshooting:');
    
    if (error.code === 'EAUTH') {
      console.error('   - Your App Password is incorrect');
      console.error('   - Make sure 2-Factor Authentication is enabled');
      console.error('   - Generate a new App Password at: https://myaccount.google.com/apppasswords');
      console.error('   - Remove all spaces from the App Password');
    } else if (error.code === 'ECONNECTION') {
      console.error('   - Check your internet connection');
      console.error('   - Gmail SMTP might be blocked by firewall');
    } else {
      console.error('   - Full error:', error);
    }
  }
}

testGmailConnection();
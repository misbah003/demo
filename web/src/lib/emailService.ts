// Secure Gmail-based OTP email service
// This uses Gmail's SMTP through a backend API for maximum security

export interface GmailConfig {
  gmailUser?: string;
  gmailAppPassword?: string;
  fromName?: string;
}

export class GmailOTPService {
  private config: GmailConfig;

  constructor(config: GmailConfig = {}) {
    this.config = {
      fromName: 'Tax Intelligence',
      ...config
    };
  }

  async sendOTP(email: string, otpCode: string): Promise<{ success: boolean; error?: string }> {
    try {
      // In a production environment, this would call your backend API
      // The backend would use Gmail SMTP with proper authentication
      
      const emailData = {
        to: email,
        subject: 'Your Tax Intelligence Verification Code',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #3b82f6, #1e40af); padding: 20px; text-align: center;">
              <h1 style="color: white; margin: 0;">Tax Intelligence</h1>
            </div>
            <div style="padding: 30px; background: #f8fafc;">
              <h2 style="color: #1e293b; margin-bottom: 20px;">Your Verification Code</h2>
              <p style="color: #475569; font-size: 16px; line-height: 1.5;">
                Hello,<br><br>
                Your verification code for Tax Intelligence is:
              </p>
              <div style="background: white; border: 2px solid #3b82f6; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #3b82f6; letter-spacing: 4px;">${otpCode}</span>
              </div>
              <p style="color: #475569; font-size: 14px;">
                This code will expire in <strong>5 minutes</strong> for security reasons.<br>
                If you didn't request this code, please ignore this email.
              </p>
              <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
              <p style="color: #64748b; font-size: 12px; text-align: center;">
                Best regards,<br>
                Tax Intelligence Team
              </p>
            </div>
          </div>
        `,
        text: `Your Tax Intelligence verification code is: ${otpCode}. This code will expire in 5 minutes.`
      };

      // Call backend API to send email via Gmail SMTP
      const response = await this.callBackendEmailAPI(emailData, otpCode);
      
      if (response.success) {
        console.log(`✅ OTP email sent successfully to ${email}`);
        return { success: true };
      } else {
        console.error('❌ Failed to send OTP email:', response.error);
        return { success: false, error: response.error };
      }
      
    } catch (error) {
      console.error('❌ Email service error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Failed to send email'
      };
    }
  }

  private async callBackendEmailAPI(emailData: any, otpCode: string): Promise<{ success: boolean; error?: string }> {
    try {
      console.log('📧 Sending email via Gmail SMTP backend...');
      console.log('📧 TO:', emailData.to);
      console.log('📧 OTP CODE (passed directly):', otpCode);
      
      // Call the backend API
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';
      const response = await fetch(`${backendUrl}/api/send-otp`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to: emailData.to,
          otpCode: otpCode
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('✅ Email sent successfully:', result);
      return { success: true };
      
    } catch (error) {
      console.error('❌ Backend API error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Backend API error'
      };
    }
  }
}

export const gmailOTPService = new GmailOTPService();

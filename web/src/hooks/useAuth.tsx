import React from 'react';
import { createContext, useContext, useEffect, useState } from 'react';
import { User, Session } from '@supabase/supabase-js';
import { supabase } from '@/integrations/supabase/client';
import { gmailOTPService } from '@/lib/emailService';

interface AuthContextType {
  user: User | null;
  session: Session | null;
  loading: boolean;
  signInWithOtp: (email: string) => Promise<{ error: any }>;
  verifyOtp: (email: string, token: string) => Promise<{ error: any }>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Set up auth state listener FIRST
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (event, session) => {
        setSession(session);
        setUser(session?.user ?? null);
        setLoading(false);
      }
    );

    // THEN check for existing session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signInWithOtp = async (email: string) => {
    try {
      // Generate a 6-digit code
      const otpCode = Math.floor(100000 + Math.random() * 900000).toString();
      
      console.log('🔐 Generated OTP:', otpCode);
      console.log('📧 Email:', email);
      
      // Store the code temporarily with timestamp
      localStorage.setItem(`otp_${email}`, otpCode);
      localStorage.setItem(`otp_${email}_timestamp`, Date.now().toString());
      
      console.log('💾 Stored OTP in localStorage:', localStorage.getItem(`otp_${email}`));
      
      // Send OTP via Gmail
      const emailResult = await gmailOTPService.sendOTP(email, otpCode);
      
      if (!emailResult.success) {
        return { error: { message: emailResult.error || 'Failed to send email' } };
      }
      
      console.log('✅ OTP sent successfully');
      return { error: null };
    } catch (error) {
      console.error('❌ Error in signInWithOtp:', error);
      return { error: { message: 'Failed to generate OTP code' } };
    }
  };

  const verifyOtp = async (email: string, token: string) => {
    console.log('🔍 Verifying OTP...');
    console.log('📧 Email:', email);
    console.log('🔢 Entered token:', token);
    
    // Get stored OTP code
    const storedCode = localStorage.getItem(`otp_${email}`);
    const timestamp = localStorage.getItem(`otp_${email}_timestamp`);
    
    console.log('💾 Stored code:', storedCode);
    console.log('⏰ Timestamp:', timestamp);
    
    // Check if code exists and is not expired (5 minutes)
    if (!storedCode || !timestamp) {
      console.error('❌ No OTP found in localStorage');
      return { error: { message: 'No OTP code found. Please request a new one.' } };
    }
    
    const codeAge = Date.now() - parseInt(timestamp);
    console.log('⏱️ Code age (ms):', codeAge);
    
    if (codeAge > 5 * 60 * 1000) { // 5 minutes
      console.error('❌ OTP expired');
      localStorage.removeItem(`otp_${email}`);
      localStorage.removeItem(`otp_${email}_timestamp`);
      return { error: { message: 'OTP code has expired. Please request a new one.' } };
    }
    
    // Verify the code
    console.log('🔍 Comparing:', { entered: token, stored: storedCode, match: token === storedCode });
    if (token !== storedCode) {
      console.error('❌ OTP mismatch');
      return { error: { message: 'Invalid OTP code. Please try again.' } };
    }
    
    console.log('✅ OTP verified successfully');
    
    // Clean up stored code
    localStorage.removeItem(`otp_${email}`);
    localStorage.removeItem(`otp_${email}_timestamp`);
    
    // Since we're using a custom OTP system (not Supabase's built-in OTP),
    // we need to authenticate the user with password-based auth
    
    // Get or create a consistent password for this email
    let userPassword = localStorage.getItem(`user_password_${email}`);
    console.log('🔑 User password exists in localStorage:', !!userPassword);
    
    if (!userPassword) {
      // Generate a consistent password for new users
      userPassword = 'otp-verified-' + btoa(email).substring(0, 20) + '-secure';
      localStorage.setItem(`user_password_${email}`, userPassword);
      console.log('🆕 Generated new password for user');
    }
    
    // First, try to sign in (user might already exist)
    console.log('🔐 Attempting to sign in existing user...');
    let { error: signInError } = await supabase.auth.signInWithPassword({
      email,
      password: userPassword,
    });
    
    // If sign in fails, check if it's an old unconfirmed user
    if (signInError) {
      console.log('ℹ️ Sign in failed, checking reason...');
      console.log('📝 Sign in error was:', signInError.message);
      
      // Check if this is an "Invalid login credentials" error (likely unconfirmed email)
      if (signInError.message.includes('Invalid login credentials') || 
          signInError.message.includes('Email not confirmed')) {
        console.log('⚠️ This might be an old user with unconfirmed email');
        
        // Try to sign up to see if user already exists
        const { error: testSignUpError } = await supabase.auth.signUp({
          email,
          password: userPassword,
        });
        
        if (testSignUpError && testSignUpError.message.includes('already registered')) {
          console.error('❌ User exists but cannot sign in - likely unconfirmed email');
          return { error: { 
            message: '🔒 This email was registered before but has an unconfirmed status.\n\n' +
                     '📋 To fix this:\n' +
                     '1. Go to Supabase Dashboard > Authentication > Users\n' +
                     '2. Find and DELETE the user: ' + email + '\n' +
                     '3. Come back and try signing in again\n\n' +
                     'OR use a different email address that hasn\'t been used before.'
          } };
        }
      }
      
      console.log('ℹ️ User does not exist, attempting to create new user...');
      
      const { data: signUpData, error: signUpError } = await supabase.auth.signUp({
        email,
        password: userPassword,
        options: {
          emailRedirectTo: window.location.origin,
          data: {
            email_confirmed: true, // Try to auto-confirm
          }
        }
      });
      
      if (signUpError) {
        console.error('❌ Sign up error:', signUpError);
        
        // If user already exists but with unconfirmed email, we have a problem
        if (signUpError.message.includes('already registered')) {
          return { error: { 
            message: 'This email was registered before email confirmation was disabled. Please go to Supabase Dashboard > Authentication > Users, find your email (' + email + '), and delete it. Then try again with a fresh email.' 
          } };
        }
        
        return { error: signUpError };
      }
      
      console.log('✅ User created successfully!');
      console.log('📊 Signup data:', signUpData);
      
      // Check if we got a session from signup (means email confirmation is disabled)
      if (signUpData?.session) {
        console.log('✅ Got session from signup - email confirmation is disabled!');
        return { error: null };
      }
      
      // If no session, email confirmation is required
      console.log('⚠️ No session from signup - email confirmation might be enabled');
      
      // Try to sign in anyway
      console.log('🔐 Attempting to sign in newly created user...');
      const { data: signInData, error: newSignInError } = await supabase.auth.signInWithPassword({
        email,
        password: userPassword,
      });
      
      if (newSignInError) {
        console.error('❌ Sign in error after signup:', newSignInError);
        return { error: { 
          message: '⚠️ IMPORTANT: Email confirmation is still ENABLED in Supabase!\n\n' +
                   'Please follow these steps:\n' +
                   '1. Go to: https://supabase.com/dashboard/project/YOUR_PROJECT/auth/providers\n' +
                   '2. Click on "Email" provider\n' +
                   '3. Toggle OFF "Confirm email"\n' +
                   '4. Click "Save"\n' +
                   '5. Go to Authentication > Users and DELETE the user: ' + email + '\n' +
                   '6. Try signing up again with a NEW email address\n\n' +
                   'Current error: ' + newSignInError.message
        } };
      }
      
      console.log('✅ Sign in successful!', signInData);
    }
    
    console.log('✅ User authenticated successfully!');
    
    return { error: null };
  };





  const signOut = async () => {
    await supabase.auth.signOut();
  };

  return (
    <AuthContext.Provider value={{
      user,
      session,
      loading,
      signInWithOtp,
      verifyOtp,
      signOut,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
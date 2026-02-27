import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, ArrowLeft, Key } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const ResetPasswordPage = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [otpDemo, setOtpDemo] = useState('');

  const sendOtp = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await api.post('/auth/send-otp', { email });
      setOtpDemo(response.data.otp_for_demo);
      toast.success(`OTP sent! (Demo: ${response.data.otp_for_demo})`);
      setStep(2);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to send OTP');
    } finally {
      setLoading(false);
    }
  };

  const resetPassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/auth/reset-password', { email, otp, new_password: newPassword });
      toast.success('Password reset successful!');
      navigate('/login');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fdfbf7] flex items-center justify-center px-4 py-12">
      <div className="grain-overlay"></div>
      
      <div className="w-full max-w-md relative">
        <Link 
          to="/login" 
          className="inline-flex items-center gap-2 text-[#1e1b4b] mb-8 hover:opacity-70 transition-opacity"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Login
        </Link>

        <div className="bg-white rounded-2xl shadow-lg border border-[#1e1b4b]/10 p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold text-[#1e1b4b] mb-2">Reset Password</h1>
            <p className="text-[#64748b]">
              {step === 1 ? 'Enter your email to receive OTP' : 'Enter OTP and new password'}
            </p>
          </div>

          {step === 1 ? (
            <form onSubmit={sendOtp} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[#64748b]" />
                  <input
                    type="email"
                    required
                    data-testid="reset-email-input"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full h-12 pl-11 pr-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    placeholder="your.email@example.com"
                  />
                </div>
              </div>

              <button
                type="submit"
                data-testid="send-otp-btn"
                disabled={loading}
                className="w-full h-12 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors shadow-lg disabled:opacity-50"
              >
                {loading ? 'Sending...' : 'Send OTP'}
              </button>
            </form>
          ) : (
            <form onSubmit={resetPassword} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-[#1e1b4b] mb-2">OTP</label>
                <div className="relative">
                  <Key className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[#64748b]" />
                  <input
                    type="text"
                    required
                    data-testid="reset-otp-input"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    className="w-full h-12 pl-11 pr-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    placeholder="Enter 6-digit OTP"
                  />
                </div>
                {otpDemo && (
                  <p className="text-xs text-[#f59e0b] mt-1">Demo OTP: {otpDemo}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-[#1e1b4b] mb-2">New Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[#64748b]" />
                  <input
                    type="password"
                    required
                    data-testid="reset-new-password-input"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full h-12 pl-11 pr-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    placeholder="Enter new password"
                  />
                </div>
              </div>

              <button
                type="submit"
                data-testid="reset-password-btn"
                disabled={loading}
                className="w-full h-12 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors shadow-lg disabled:opacity-50"
              >
                {loading ? 'Resetting...' : 'Reset Password'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResetPasswordPage;

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, Eye, EyeOff, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const LoginPage = ({ setUser }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await api.post('/auth/login', formData);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      setUser(response.data.user);
      toast.success('Login successful!');
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fdfbf7] flex items-center justify-center px-4 py-12">
      <div className="grain-overlay"></div>
      
      <div className="w-full max-w-md relative">
        <Link 
          to="/" 
          className="inline-flex items-center gap-2 text-[#1e1b4b] mb-8 hover:opacity-70 transition-opacity"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Home
        </Link>

        <div className="bg-white rounded-2xl shadow-lg border border-[#1e1b4b]/10 p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold text-[#1e1b4b] mb-2">Welcome Back</h1>
            <p className="text-[#64748b]">Login to continue your journey</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-[#1e1b4b] mb-2">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[#64748b]" />
                <input
                  type="email"
                  data-testid="login-email-input"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full h-12 pl-11 pr-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb] transition-colors"
                  placeholder="your.email@example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-[#1e1b4b] mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[#64748b]" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  data-testid="login-password-input"
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full h-12 pl-11 pr-11 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb] transition-colors"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#64748b] hover:text-[#1e1b4b]"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <div className="flex justify-end">
              <Link 
                to="/reset-password" 
                className="text-sm text-[#1e1b4b] hover:underline"
                data-testid="forgot-password-link"
              >
                Forgot Password?
              </Link>
            </div>

            <button
              type="submit"
              data-testid="login-submit-btn"
              disabled={loading}
              className="w-full h-12 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <p className="text-center text-[#64748b] mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-[#1e1b4b] font-medium hover:underline" data-testid="register-link">
              Register Now
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

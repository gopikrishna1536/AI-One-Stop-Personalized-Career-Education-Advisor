import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { User, Mail, Lock, Phone, MapPin, Calendar, ArrowLeft, ArrowRight, Eye, EyeOff } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const RegisterPage = ({ setUser }) => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [otp, setOtp] = useState('');
  const [showOtpModal, setShowOtpModal] = useState(false);
  
  const [formData, setFormData] = useState({
    full_name: '',
    gender: '',
    date_of_birth: '',
    mobile_number: '',
    email: '',
    password: '',
    state: '',
    district: '',
    location_type: '',
    category: '',
    current_class: '',
    board: '',
    medium_of_instruction: '',
    marks_percentage: '',
    subjects_studied: [],
    preferred_stream: '',
    preferred_language: 'english'
  });

  const indianStates = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
    'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
    'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi', 'Jammu and Kashmir'
  ];

  const subjects = ['Physics', 'Chemistry', 'Mathematics', 'Biology', 'Computer Science', 'Economics', 
                    'Accountancy', 'Business Studies', 'History', 'Geography', 'Political Science', 'English'];

  const handleSubjectToggle = (subject) => {
    const updated = formData.subjects_studied.includes(subject)
      ? formData.subjects_studied.filter(s => s !== subject)
      : [...formData.subjects_studied, subject];
    setFormData({ ...formData, subjects_studied: updated });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (step < 2) {
      setStep(step + 1);
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/auth/register', formData);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      setUser(response.data.user);
      
      toast.success(`Registration successful! OTP: ${response.data.otp_for_demo}`);
      setShowOtpModal(true);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const verifyOtp = async () => {
    try {
      await api.post('/auth/verify-otp', { email: formData.email, otp });
      toast.success('Email verified successfully!');
      navigate('/dashboard');
    } catch (error) {
      toast.error('Invalid OTP');
    }
  };

  return (
    <div className="min-h-screen bg-[#fdfbf7] py-12 px-4">
      <div className="grain-overlay"></div>
      
      <div className="max-w-3xl mx-auto relative">
        <Link 
          to="/" 
          className="inline-flex items-center gap-2 text-[#1e1b4b] mb-8 hover:opacity-70 transition-opacity"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Home
        </Link>

        <div className="bg-white rounded-2xl shadow-lg border border-[#1e1b4b]/10 p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold text-[#1e1b4b] mb-2">Create Your Account</h1>
            <p className="text-[#64748b]">Step {step} of 2: {step === 1 ? 'Personal Details' : 'Educational Details'}</p>
          </div>

          <div className="flex justify-center mb-8">
            <div className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 1 ? 'bg-[#1e1b4b] text-white' : 'bg-gray-200'}`}>1</div>
              <div className={`w-16 h-1 ${step >= 2 ? 'bg-[#1e1b4b]' : 'bg-gray-200'}`}></div>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 2 ? 'bg-[#1e1b4b] text-white' : 'bg-gray-200'}`}>2</div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {step === 1 && (
              <>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Full Name *</label>
                    <input
                      type="text"
                      required
                      data-testid="register-fullname-input"
                      value={formData.full_name}
                      onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Gender *</label>
                    <select
                      required
                      data-testid="register-gender-select"
                      value={formData.gender}
                      onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    >
                      <option value="">Select Gender</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Date of Birth *</label>
                    <input
                      type="date"
                      required
                      data-testid="register-dob-input"
                      value={formData.date_of_birth}
                      onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Mobile Number *</label>
                    <input
                      type="tel"
                      required
                      data-testid="register-mobile-input"
                      value={formData.mobile_number}
                      onChange={(e) => setFormData({ ...formData, mobile_number: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                      placeholder="10-digit mobile number"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Email Address *</label>
                  <input
                    type="email"
                    required
                    data-testid="register-email-input"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Password *</label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      required
                      data-testid="register-password-input"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      className="w-full h-12 px-4 pr-11 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-[#64748b]"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>

                <div className="grid md:grid-cols-3 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">State *</label>
                    <select
                      required
                      data-testid="register-state-select"
                      value={formData.state}
                      onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    >
                      <option value="">Select State</option>
                      {indianStates.map(state => <option key={state} value={state}>{state}</option>)}
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">District *</label>
                    <input
                      type="text"
                      required
                      data-testid="register-district-input"
                      value={formData.district}
                      onChange={(e) => setFormData({ ...formData, district: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Location Type *</label>
                    <select
                      required
                      data-testid="register-location-select"
                      value={formData.location_type}
                      onChange={(e) => setFormData({ ...formData, location_type: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    >
                      <option value="">Select Type</option>
                      <option value="urban">Urban</option>
                      <option value="rural">Rural</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Preferred Language *</label>
                  <select
                    required
                    data-testid="register-language-select"
                    value={formData.preferred_language}
                    onChange={(e) => setFormData({ ...formData, preferred_language: e.target.value })}
                    className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                  >
                    <option value="english">English</option>
                    <option value="hindi">Hindi</option>
                    <option value="tamil">Tamil</option>
                    <option value="telugu">Telugu</option>
                  </select>
                </div>
              </>
            )}

            {step === 2 && (
              <>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Current Class *</label>
                    <select
                      required
                      data-testid="register-class-select"
                      value={formData.current_class}
                      onChange={(e) => setFormData({ ...formData, current_class: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    >
                      <option value="">Select Class</option>
                      <option value="10th">10th</option>
                      <option value="11th">11th</option>
                      <option value="12th">12th</option>
                      <option value="Completed 12th">Completed 12th</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Board *</label>
                    <select
                      required
                      data-testid="register-board-select"
                      value={formData.board}
                      onChange={(e) => setFormData({ ...formData, board: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    >
                      <option value="">Select Board</option>
                      <option value="CBSE">CBSE</option>
                      <option value="ICSE">ICSE</option>
                      <option value="State Board">State Board</option>
                    </select>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Medium of Instruction *</label>
                    <input
                      type="text"
                      required
                      data-testid="register-medium-input"
                      value={formData.medium_of_instruction}
                      onChange={(e) => setFormData({ ...formData, medium_of_instruction: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                      placeholder="English, Hindi, etc."
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Marks Percentage</label>
                    <input
                      type="number"
                      data-testid="register-marks-input"
                      value={formData.marks_percentage}
                      onChange={(e) => setFormData({ ...formData, marks_percentage: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                      placeholder="85"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Subjects Studied *</label>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {subjects.map(subject => (
                      <button
                        key={subject}
                        type="button"
                        data-testid={`subject-${subject.toLowerCase().replace(/\s+/g, '-')}`}
                        onClick={() => handleSubjectToggle(subject)}
                        className={`px-4 py-2 rounded-lg border-2 transition-all ${
                          formData.subjects_studied.includes(subject)
                            ? 'border-[#1e1b4b] bg-[#1e1b4b] text-white'
                            : 'border-gray-200 hover:border-[#1e1b4b]/50'
                        }`}
                      >
                        {subject}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-[#1e1b4b] mb-2">Preferred Stream</label>
                  <select
                    data-testid="register-stream-select"
                    value={formData.preferred_stream}
                    onChange={(e) => setFormData({ ...formData, preferred_stream: e.target.value })}
                    className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                  >
                    <option value="">Not decided yet</option>
                    <option value="science">Science</option>
                    <option value="commerce">Commerce</option>
                    <option value="arts">Arts & Humanities</option>
                  </select>
                </div>
              </>
            )}

            <div className="flex gap-4">
              {step > 1 && (
                <button
                  type="button"
                  onClick={() => setStep(step - 1)}
                  className="flex-1 h-12 border-2 border-[#1e1b4b]/10 text-[#1e1b4b] font-medium rounded-full hover:bg-[#1e1b4b]/5 transition-colors"
                >
                  Previous
                </button>
              )}
              <button
                type="submit"
                data-testid="register-submit-btn"
                disabled={loading}
                className="flex-1 h-12 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors shadow-lg hover:shadow-xl disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {loading ? 'Processing...' : step === 2 ? 'Register' : 'Next'}
                {!loading && <ArrowRight className="w-5 h-5" />}
              </button>
            </div>
          </form>

          <p className="text-center text-[#64748b] mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-[#1e1b4b] font-medium hover:underline">
              Login
            </Link>
          </p>
        </div>
      </div>

      {showOtpModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-2xl p-8 max-w-md w-full">
            <h2 className="text-2xl font-semibold text-[#1e1b4b] mb-4">Verify Your Email</h2>
            <p className="text-[#64748b] mb-6">Enter the OTP sent to {formData.email}</p>
            <input
              type="text"
              value={otp}
              data-testid="otp-input"
              onChange={(e) => setOtp(e.target.value)}
              className="w-full h-12 px-4 rounded-lg border border-gray-200 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb] mb-4"
              placeholder="Enter 6-digit OTP"
            />
            <div className="flex gap-4">
              <button
                onClick={verifyOtp}
                data-testid="verify-otp-btn"
                className="flex-1 h-12 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors"
              >
                Verify
              </button>
              <button
                onClick={() => navigate('/dashboard')}
                data-testid="skip-verification-btn"
                className="flex-1 h-12 border-2 border-[#1e1b4b]/10 text-[#1e1b4b] font-medium rounded-full hover:bg-[#1e1b4b]/5 transition-colors"
              >
                Skip for Now
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RegisterPage;

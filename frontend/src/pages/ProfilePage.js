import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, User as UserIcon, Mail, Phone, MapPin, BookOpen, Edit2, Save, X } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const ProfilePage = ({ user, setUser }) => {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState(null);
  const [editData, setEditData] = useState({});

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await api.get('/user/profile');
      setProfileData(response.data.user);
      setEditData(response.data.user);
    } catch (error) {
      console.error('Failed to load profile:', error);
      toast.error('Failed to load profile');
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      const updates = {
        full_name: editData.full_name,
        mobile_number: editData.mobile_number,
        state: editData.state,
        district: editData.district,
        current_class: editData.current_class,
        marks_percentage: editData.marks_percentage,
        subjects_studied: editData.subjects_studied,
        preferred_stream: editData.preferred_stream,
        preferred_language: editData.preferred_language
      };
      
      const response = await api.put('/user/profile', updates);
      setProfileData(response.data.user);
      
      // Update local storage
      const updatedUser = { ...user, ...updates };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      setUser(updatedUser);
      
      toast.success('Profile updated successfully');
      setIsEditing(false);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setEditData(profileData);
    setIsEditing(false);
  };

  if (!profileData) {
    return (
      <div className="min-h-screen bg-[#fdfbf7] flex items-center justify-center">
        <div className="text-[#1e1b4b]">Loading profile...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#fdfbf7]">
      <div className="grain-overlay"></div>
      
      {/* Header */}
      <header className="bg-white border-b border-[#1e1b4b]/10 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <button 
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-[#1e1b4b] hover:opacity-70 transition-opacity"
            data-testid="back-to-dashboard-btn"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="font-medium">Dashboard</span>
          </button>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Profile Header */}
        <div className="bg-gradient-to-br from-[#1e1b4b] to-[#312e81] text-white rounded-2xl p-8 mb-8">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 bg-[#f59e0b] rounded-full flex items-center justify-center text-4xl font-bold">
              {profileData.full_name?.charAt(0).toUpperCase()}
            </div>
            <div>
              <h1 className="text-3xl font-semibold mb-2">{profileData.full_name}</h1>
              <p className="text-lg opacity-90">{profileData.email}</p>
              <div className="flex items-center gap-2 mt-2">
                {profileData.email_verified ? (
                  <span className="px-3 py-1 bg-[#14b8a6] text-white text-xs font-medium rounded-full">
                    Email Verified
                  </span>
                ) : (
                  <span className="px-3 py-1 bg-yellow-500 text-white text-xs font-medium rounded-full">
                    Email Not Verified
                  </span>
                )}
                <span className="px-3 py-1 bg-white/20 text-white text-xs font-medium rounded-full capitalize">
                  {profileData.role}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Profile Content */}
        <div className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-[#1e1b4b]">Profile Information</h2>
            {!isEditing ? (
              <button
                onClick={() => setIsEditing(true)}
                data-testid="edit-profile-btn"
                className="flex items-center gap-2 px-6 py-2.5 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors"
              >
                <Edit2 className="w-4 h-4" />
                Edit Profile
              </button>
            ) : (
              <div className="flex gap-3">
                <button
                  onClick={handleCancel}
                  data-testid="cancel-edit-btn"
                  className="flex items-center gap-2 px-6 py-2.5 border-2 border-[#1e1b4b]/10 text-[#1e1b4b] font-medium rounded-full hover:bg-[#1e1b4b]/5 transition-colors"
                >
                  <X className="w-4 h-4" />
                  Cancel
                </button>
                <button
                  onClick={handleSave}
                  data-testid="save-profile-btn"
                  disabled={loading}
                  className="flex items-center gap-2 px-6 py-2.5 bg-[#14b8a6] text-white font-medium rounded-full hover:bg-[#0d9488] transition-colors disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            )}
          </div>

          <div className="space-y-6">
            {/* Personal Information */}
            <div>
              <h3 className="text-lg font-semibold text-[#1e1b4b] mb-4 flex items-center gap-2">
                <UserIcon className="w-5 h-5 text-[#f59e0b]" />
                Personal Information
              </h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Full Name</label>
                  {isEditing ? (
                    <input
                      type="text"
                      data-testid="edit-fullname"
                      value={editData.full_name || ''}
                      onChange={(e) => setEditData({ ...editData, full_name: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                  ) : (
                    <p className="text-[#1e1b4b] font-medium">{profileData.full_name}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Gender</label>
                  <p className="text-[#1e1b4b] font-medium capitalize">{profileData.gender}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Date of Birth</label>
                  <p className="text-[#1e1b4b] font-medium">{profileData.date_of_birth}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Mobile Number</label>
                  {isEditing ? (
                    <input
                      type="tel"
                      data-testid="edit-mobile"
                      value={editData.mobile_number || ''}
                      onChange={(e) => setEditData({ ...editData, mobile_number: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                  ) : (
                    <p className="text-[#1e1b4b] font-medium">{profileData.mobile_number}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Location */}
            <div className="pt-6 border-t border-[#1e1b4b]/10">
              <h3 className="text-lg font-semibold text-[#1e1b4b] mb-4 flex items-center gap-2">
                <MapPin className="w-5 h-5 text-[#f59e0b]" />
                Location
              </h3>
              <div className="grid md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">State</label>
                  {isEditing ? (
                    <input
                      type="text"
                      data-testid="edit-state"
                      value={editData.state || ''}
                      onChange={(e) => setEditData({ ...editData, state: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                  ) : (
                    <p className="text-[#1e1b4b] font-medium">{profileData.state}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">District</label>
                  {isEditing ? (
                    <input
                      type="text"
                      data-testid="edit-district"
                      value={editData.district || ''}
                      onChange={(e) => setEditData({ ...editData, district: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                  ) : (
                    <p className="text-[#1e1b4b] font-medium">{profileData.district}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Location Type</label>
                  <p className="text-[#1e1b4b] font-medium capitalize">{profileData.location_type}</p>
                </div>
              </div>
            </div>

            {/* Education */}
            <div className="pt-6 border-t border-[#1e1b4b]/10">
              <h3 className="text-lg font-semibold text-[#1e1b4b] mb-4 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-[#f59e0b]" />
                Education
              </h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Current Class</label>
                  {isEditing ? (
                    <select
                      data-testid="edit-class"
                      value={editData.current_class || ''}
                      onChange={(e) => setEditData({ ...editData, current_class: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    >
                      <option value="10th">10th</option>
                      <option value="11th">11th</option>
                      <option value="12th">12th</option>
                      <option value="Completed 12th">Completed 12th</option>
                    </select>
                  ) : (
                    <p className="text-[#1e1b4b] font-medium">{profileData.current_class}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Board</label>
                  <p className="text-[#1e1b4b] font-medium">{profileData.board}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Marks Percentage</label>
                  {isEditing ? (
                    <input
                      type="number"
                      data-testid="edit-marks"
                      value={editData.marks_percentage || ''}
                      onChange={(e) => setEditData({ ...editData, marks_percentage: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    />
                  ) : (
                    <p className="text-[#1e1b4b] font-medium">{profileData.marks_percentage}%</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#64748b] mb-2">Preferred Stream</label>
                  {isEditing ? (
                    <select
                      data-testid="edit-stream"
                      value={editData.preferred_stream || ''}
                      onChange={(e) => setEditData({ ...editData, preferred_stream: e.target.value })}
                      className="w-full h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                    >
                      <option value="">Not decided</option>
                      <option value="science">Science</option>
                      <option value="commerce">Commerce</option>
                      <option value="arts">Arts</option>
                    </select>
                  ) : (
                    <p className="text-[#1e1b4b] font-medium capitalize">{profileData.preferred_stream || 'Not decided'}</p>
                  )}
                </div>
              </div>
              
              <div className="mt-6">
                <label className="block text-sm font-medium text-[#64748b] mb-2">Subjects Studied</label>
                <div className="flex flex-wrap gap-2">
                  {profileData.subjects_studied?.map((subject, i) => (
                    <span key={i} className="px-3 py-1.5 bg-[#1e1b4b]/5 text-[#1e1b4b] text-sm font-medium rounded-full">
                      {subject}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Language Preference */}
            <div className="pt-6 border-t border-[#1e1b4b]/10">
              <h3 className="text-lg font-semibold text-[#1e1b4b] mb-4">Language Preference</h3>
              <div>
                <label className="block text-sm font-medium text-[#64748b] mb-2">Preferred Language</label>
                {isEditing ? (
                  <select
                    data-testid="edit-language"
                    value={editData.preferred_language || 'english'}
                    onChange={(e) => setEditData({ ...editData, preferred_language: e.target.value })}
                    className="w-full md:w-64 h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb]"
                  >
                    <option value="english">English</option>
                    <option value="hindi">Hindi</option>
                    <option value="tamil">Tamil</option>
                    <option value="telugu">Telugu</option>
                  </select>
                ) : (
                  <p className="text-[#1e1b4b] font-medium capitalize">{profileData.preferred_language}</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;

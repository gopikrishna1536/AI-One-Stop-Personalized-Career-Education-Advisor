import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Users, Building2, MessageSquare, TrendingUp } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const AdminDashboard = ({ user }) => {
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user?.role !== 'admin') {
      toast.error('Admin access required');
      navigate('/dashboard');
      return;
    }
    loadAnalytics();
  }, [user, navigate]);

  const loadAnalytics = async () => {
    try {
      const response = await api.get('/admin/analytics');
      setAnalytics(response.data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
      toast.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading || !analytics) {
    return (
      <div className="min-h-screen bg-[#fdfbf7] flex items-center justify-center">
        <div className="text-[#1e1b4b]">Loading analytics...</div>
      </div>
    );
  }

  const stats = [
    { icon: <Users className="w-8 h-8" />, label: 'Total Users', value: analytics.total_users, color: 'bg-[#1e1b4b]' },
    { icon: <Building2 className="w-8 h-8" />, label: 'Total Colleges', value: analytics.total_colleges, color: 'bg-[#f59e0b]' },
    { icon: <MessageSquare className="w-8 h-8" />, label: 'Total Chats', value: analytics.total_chats, color: 'bg-[#14b8a6]' },
  ];

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

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-[#1e1b4b] via-[#312e81] to-[#1e1b4b] text-white py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-4 mb-4">
            <TrendingUp className="w-12 h-12" />
            <h1 className="text-4xl md:text-5xl font-semibold tracking-tight">
              Admin Dashboard
            </h1>
          </div>
          <p className="text-lg md:text-xl opacity-90">
            Monitor platform analytics and manage content
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Stats Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          {stats.map((stat, index) => (
            <div
              key={index}
              data-testid={`stat-card-${index}`}
              className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm"
            >
              <div className={`w-14 h-14 ${stat.color} rounded-xl flex items-center justify-center text-white mb-4`}>
                {stat.icon}
              </div>
              <h3 className="text-3xl font-bold text-[#1e1b4b] mb-2">{stat.value.toLocaleString()}</h3>
              <p className="text-[#64748b] font-medium">{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Stream Distribution */}
        <div className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm">
          <h2 className="text-2xl font-semibold text-[#1e1b4b] mb-6">Stream Distribution</h2>
          {Object.keys(analytics.stream_distribution).length > 0 ? (
            <div className="space-y-4">
              {Object.entries(analytics.stream_distribution).map(([stream, count]) => {
                const total = Object.values(analytics.stream_distribution).reduce((a, b) => a + b, 0);
                const percentage = total > 0 ? ((count / total) * 100).toFixed(1) : 0;
                
                return (
                  <div key={stream} data-testid={`stream-${stream}`}>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-[#1e1b4b] font-medium capitalize">{stream || 'Undecided'}</span>
                      <span className="text-[#64748b] font-medium">{count} students ({percentage}%)</span>
                    </div>
                    <div className="w-full h-3 bg-[#1e1b4b]/10 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-[#1e1b4b] rounded-full transition-all duration-500"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-[#64748b]">No stream data available yet</p>
          )}
        </div>

        {/* Quick Actions */}
        <div className="mt-12 grid md:grid-cols-2 gap-6">
          <div className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm">
            <h3 className="text-xl font-semibold text-[#1e1b4b] mb-4">College Management</h3>
            <p className="text-[#64748b] mb-6">Add, edit, or remove colleges from the directory</p>
            <button 
              className="px-6 py-3 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors"
              data-testid="manage-colleges-btn"
            >
              Manage Colleges
            </button>
          </div>

          <div className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm">
            <h3 className="text-xl font-semibold text-[#1e1b4b] mb-4">Timeline Management</h3>
            <p className="text-[#64748b] mb-6">Update admission dates and exam schedules</p>
            <button 
              className="px-6 py-3 bg-[#f59e0b] text-white font-medium rounded-full hover:bg-[#d97706] transition-colors"
              data-testid="manage-timeline-btn"
            >
              Manage Timeline
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;

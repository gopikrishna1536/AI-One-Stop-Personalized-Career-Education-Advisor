import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { LogOut, MessageCircle, BookOpen, Calendar, User, MapPin, TrendingUp, GraduationCap, Menu, X, Target } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const Dashboard = ({ user }) => {
  const navigate = useNavigate();
  const [colleges, setColleges] = useState([]);
  const [events, setEvents] = useState([]);
  const [streams, setStreams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [collegesRes, eventsRes, streamsRes] = await Promise.all([
        api.get('/colleges', { params: { state: user.state } }),
        api.get('/timeline/events'),
        api.get('/streams')
      ]);
      setColleges(collegesRes.data.colleges.slice(0, 3));
      setEvents(eventsRes.data.events.slice(0, 3));
      setStreams(streamsRes.data.streams);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    toast.success('Logged out successfully');
    navigate('/');
  };

  const NavItem = ({ to, icon, label, testId }) => (
    <Link
      to={to}
      data-testid={testId}
      className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-[#1e1b4b]/5 transition-colors text-[#1e1b4b]"
      onClick={() => setMenuOpen(false)}
    >
      {icon}
      <span className="font-medium">{label}</span>
    </Link>
  );

  return (
    <div className="min-h-screen bg-[#fdfbf7]">
      <div className="grain-overlay"></div>
      
      {/* Header */}
      <header className="bg-white border-b border-[#1e1b4b]/10 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <BookOpen className="w-8 h-8 text-[#1e1b4b]" />
            <span className="text-2xl font-semibold text-[#1e1b4b]">EduPath India</span>
          </div>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Link to="/dashboard" className="text-[#1e1b4b] font-medium hover:opacity-70 transition-opacity" data-testid="nav-dashboard">
              Dashboard
            </Link>
            <Link to="/chatbot" className="text-[#1e1b4b] font-medium hover:opacity-70 transition-opacity" data-testid="nav-chatbot">
              AI Chatbot
            </Link>
            <Link to="/colleges" className="text-[#1e1b4b] font-medium hover:opacity-70 transition-opacity" data-testid="nav-colleges">
              Colleges
            </Link>
            <Link to="/timeline" className="text-[#1e1b4b] font-medium hover:opacity-70 transition-opacity" data-testid="nav-timeline">
              Timeline
            </Link>
            <Link to="/profile" className="text-[#1e1b4b] font-medium hover:opacity-70 transition-opacity" data-testid="nav-profile">
              Profile
            </Link>
            <button 
              onClick={handleLogout}
              data-testid="logout-btn"
              className="px-6 py-2.5 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors"
            >
              Logout
            </button>
          </nav>

          {/* Mobile Menu Button */}
          <button 
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden p-2 hover:bg-[#1e1b4b]/5 rounded-lg"
            data-testid="mobile-menu-btn"
          >
            {menuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {menuOpen && (
          <div className="md:hidden border-t border-[#1e1b4b]/10 bg-white p-4 space-y-2">
            <NavItem to="/dashboard" icon={<TrendingUp className="w-5 h-5" />} label="Dashboard" testId="mobile-nav-dashboard" />
            <NavItem to="/chatbot" icon={<MessageCircle className="w-5 h-5" />} label="AI Chatbot" testId="mobile-nav-chatbot" />
            <NavItem to="/colleges" icon={<MapPin className="w-5 h-5" />} label="Colleges" testId="mobile-nav-colleges" />
            <NavItem to="/timeline" icon={<Calendar className="w-5 h-5" />} label="Timeline" testId="mobile-nav-timeline" />
            <NavItem to="/profile" icon={<User className="w-5 h-5" />} label="Profile" testId="mobile-nav-profile" />
            <button 
              onClick={handleLogout}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-[#1e1b4b] text-white hover:bg-[#312e81] transition-colors"
              data-testid="mobile-logout-btn"
            >
              <LogOut className="w-5 h-5" />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Section */}
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-semibold tracking-tight text-[#1e1b4b] mb-4">
            Welcome back, {user?.full_name}! 
          </h1>
          <p className="text-lg text-[#64748b]">
            Let's continue your journey to the perfect career path
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">Loading...</div>
        ) : (
          <>
            {/* Quick Actions */}
            <div className="grid md:grid-cols-3 gap-6 mb-12">
              <button
                onClick={() => navigate('/aptitude-test')}
                data-testid="quick-action-aptitude"
                className="bg-gradient-to-br from-[#14b8a6] to-[#0d9488] text-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group"
              >
                <Target className="w-12 h-12 mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="text-2xl font-semibold mb-2">Career Aptitude Test</h3>
                <p className="opacity-90">Take our 12-question test and get personalized roadmap</p>
              </button>

              <button
                onClick={() => navigate('/chatbot')}
                data-testid="quick-action-chatbot"
                className="bg-gradient-to-br from-[#1e1b4b] to-[#312e81] text-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group"
              >
                <MessageCircle className="w-12 h-12 mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="text-2xl font-semibold mb-2">AI Career Guidance</h3>
                <p className="opacity-90">Get personalized career recommendations</p>
              </button>

              <button
                onClick={() => navigate('/colleges')}
                data-testid="quick-action-colleges"
                className="bg-white border-2 border-[#1e1b4b]/10 p-8 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 group"
              >
                <MapPin className="w-12 h-12 mb-4 text-[#f59e0b] group-hover:scale-110 transition-transform" />
                <h3 className="text-2xl font-semibold text-[#1e1b4b] mb-2">Explore Colleges</h3>
                <p className="text-[#64748b]">Find government colleges near you</p>
              </button>
            </div>

            {/* Bento Grid Layout */}
            <div className="grid md:grid-cols-3 gap-6">
              {/* Recommended Streams */}
              <div className="md:col-span-2 bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm" data-testid="recommended-streams">
                <h2 className="text-2xl font-semibold text-[#1e1b4b] mb-6 flex items-center gap-2">
                  <GraduationCap className="w-7 h-7 text-[#f59e0b]" />
                  Recommended Streams
                </h2>
                <div className="grid sm:grid-cols-3 gap-4">
                  {streams.map((stream, index) => (
                    <div
                      key={stream.id}
                      data-testid={`stream-card-${stream.id}`}
                      className="p-6 border-2 border-[#1e1b4b]/10 rounded-xl hover:border-[#1e1b4b]/30 hover:shadow-md transition-all cursor-pointer"
                      onClick={() => navigate('/chatbot')}
                    >
                      <div className="text-3xl mb-3">{index === 0 ? '🔬' : index === 1 ? '💼' : '🎨'}</div>
                      <h3 className="font-semibold text-[#1e1b4b] mb-1">{stream.name}</h3>
                      <p className="text-sm text-[#64748b]">Explore options</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Next Deadline */}
              <div className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm" data-testid="next-deadline">
                <h2 className="text-xl font-semibold text-[#1e1b4b] mb-6 flex items-center gap-2">
                  <Calendar className="w-6 h-6 text-[#14b8a6]" />
                  Next Deadline
                </h2>
                {events.length > 0 ? (
                  <div className="space-y-4">
                    <div className="p-4 bg-[#14b8a6]/10 rounded-lg">
                      <h3 className="font-semibold text-[#1e1b4b] mb-1">{events[0].title}</h3>
                      <p className="text-sm text-[#64748b] mb-2">{events[0].description}</p>
                      <p className="text-xs font-medium text-[#14b8a6]">{new Date(events[0].event_date).toLocaleDateString()}</p>
                    </div>
                    <Link 
                      to="/timeline" 
                      className="text-sm text-[#1e1b4b] hover:underline inline-block"
                      data-testid="view-all-events-link"
                    >
                      View all events →
                    </Link>
                  </div>
                ) : (
                  <p className="text-[#64748b]">No upcoming events</p>
                )}
              </div>

              {/* Nearby Colleges */}
              <div className="md:col-span-3 bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm" data-testid="nearby-colleges">
                <h2 className="text-2xl font-semibold text-[#1e1b4b] mb-6 flex items-center gap-2">
                  <MapPin className="w-7 h-7 text-[#f59e0b]" />
                  Colleges in {user?.state}
                </h2>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {colleges.map(college => (
                    <div 
                      key={college.id}
                      data-testid={`college-card-${college.id}`}
                      className="p-6 border border-[#1e1b4b]/10 rounded-xl hover:shadow-md transition-all cursor-pointer"
                      onClick={() => navigate('/colleges')}
                    >
                      <h3 className="font-semibold text-[#1e1b4b] mb-2">{college.name}</h3>
                      <p className="text-sm text-[#64748b] mb-3">{college.district}, {college.state}</p>
                      <div className="flex flex-wrap gap-2">
                        {college.streams.slice(0, 2).map((stream, i) => (
                          <span key={i} className="px-3 py-1 bg-[#f59e0b]/10 text-[#f59e0b] text-xs font-medium rounded-full">
                            {stream}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
                <Link 
                  to="/colleges" 
                  className="mt-6 text-[#1e1b4b] hover:underline inline-block"
                  data-testid="view-all-colleges-link"
                >
                  View all colleges →
                </Link>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
};

export default Dashboard;

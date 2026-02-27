import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Search, MapPin, GraduationCap, Home as HomeIcon, Phone, Globe } from 'lucide-react';
import api from '@/utils/api';

const CollegesPage = ({ user }) => {
  const navigate = useNavigate();
  const [colleges, setColleges] = useState([]);
  const [filteredColleges, setFilteredColleges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    state: '',
    district: '',
    stream: '',
    course: ''
  });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadColleges();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [colleges, filters, searchTerm]);

  const loadColleges = async () => {
    try {
      const response = await api.get('/colleges');
      setColleges(response.data.colleges || []);
    } catch (error) {
      console.error('Failed to load colleges:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = colleges;

    if (filters.state) {
      filtered = filtered.filter(c => c.state === filters.state);
    }
    if (filters.district) {
      filtered = filtered.filter(c => c.district.toLowerCase().includes(filters.district.toLowerCase()));
    }
    if (filters.stream) {
      filtered = filtered.filter(c => c.streams.includes(filters.stream));
    }
    if (searchTerm) {
      filtered = filtered.filter(c => 
        c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.state.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.district.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredColleges(filtered);
  };

  const uniqueStates = [...new Set(colleges.map(c => c.state))].sort();

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
          <h1 className="text-4xl md:text-5xl font-semibold tracking-tight mb-4">
            Government College Directory
          </h1>
          <p className="text-lg md:text-xl opacity-90 max-w-3xl">
            Explore {colleges.length}+ Indian Government Colleges across the country
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Search and Filters */}
        <div className="mb-8 space-y-4">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#64748b]" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              data-testid="college-search-input"
              placeholder="Search colleges by name, state, or district..."
              className="w-full h-14 pl-12 pr-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-white"
            />
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <select
              value={filters.state}
              onChange={(e) => setFilters({ ...filters, state: e.target.value })}
              data-testid="filter-state"
              className="h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-white"
            >
              <option value="">All States</option>
              {uniqueStates.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>

            <input
              type="text"
              value={filters.district}
              onChange={(e) => setFilters({ ...filters, district: e.target.value })}
              data-testid="filter-district"
              placeholder="District"
              className="h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-white"
            />

            <select
              value={filters.stream}
              onChange={(e) => setFilters({ ...filters, stream: e.target.value })}
              data-testid="filter-stream"
              className="h-12 px-4 rounded-lg border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-white"
            >
              <option value="">All Streams</option>
              <option value="science">Science</option>
              <option value="commerce">Commerce</option>
              <option value="arts">Arts & Humanities</option>
            </select>

            <button
              onClick={() => setFilters({ state: '', district: '', stream: '', course: '' })}
              data-testid="clear-filters-btn"
              className="h-12 px-6 bg-[#1e1b4b]/5 text-[#1e1b4b] font-medium rounded-lg hover:bg-[#1e1b4b]/10 transition-colors"
            >
              Clear Filters
            </button>
          </div>
        </div>

        {/* Results */}
        {loading ? (
          <div className="text-center py-12">Loading colleges...</div>
        ) : filteredColleges.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-lg text-[#64748b]">No colleges found matching your criteria</p>
          </div>
        ) : (
          <>
            <p className="text-[#64748b] mb-6">
              Showing {filteredColleges.length} college{filteredColleges.length !== 1 ? 's' : ''}
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredColleges.map(college => (
                <div
                  key={college.id}
                  data-testid={`college-card-${college.id}`}
                  className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 bg-[#f59e0b]/10 rounded-lg flex items-center justify-center">
                      <GraduationCap className="w-6 h-6 text-[#f59e0b]" />
                    </div>
                    {college.hostel_facility && (
                      <span className="px-3 py-1 bg-[#14b8a6]/10 text-[#14b8a6] text-xs font-medium rounded-full">
                        Hostel Available
                      </span>
                    )}
                  </div>

                  <h3 className="text-xl font-semibold text-[#1e1b4b] mb-2">{college.name}</h3>
                  
                  <div className="space-y-2 mb-4">
                    <div className="flex items-center gap-2 text-sm text-[#64748b]">
                      <MapPin className="w-4 h-4" />
                      <span>{college.district}, {college.state}</span>
                    </div>
                    {college.website && (
                      <div className="flex items-center gap-2 text-sm text-[#64748b]">
                        <Globe className="w-4 h-4" />
                        <a href={college.website} target="_blank" rel="noopener noreferrer" className="hover:underline">
                          Visit Website
                        </a>
                      </div>
                    )}
                    {college.contact && (
                      <div className="flex items-center gap-2 text-sm text-[#64748b]">
                        <Phone className="w-4 h-4" />
                        <span>{college.contact}</span>
                      </div>
                    )}
                  </div>

                  <div className="mb-4">
                    <p className="text-xs font-medium text-[#64748b] mb-2">Streams Offered:</p>
                    <div className="flex flex-wrap gap-2">
                      {college.streams.map((stream, i) => (
                        <span key={i} className="px-3 py-1 bg-[#1e1b4b]/5 text-[#1e1b4b] text-xs font-medium rounded-full capitalize">
                          {stream}
                        </span>
                      ))}
                    </div>
                  </div>

                  {college.entrance_exam && (
                    <div className="pt-4 border-t border-[#1e1b4b]/10">
                      <p className="text-xs font-medium text-[#64748b]">Entrance Exam:</p>
                      <p className="text-sm text-[#1e1b4b] font-semibold">{college.entrance_exam}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default CollegesPage;

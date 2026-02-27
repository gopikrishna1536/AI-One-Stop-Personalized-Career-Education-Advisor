import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Download, Target, TrendingUp, Building2, Code, Calendar, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const AptitudeResultPage = ({ user }) => {
  const navigate = useNavigate();
  const { resultId } = useParams();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResult();
  }, [resultId]);

  const loadResult = async () => {
    try {
      const response = await api.get(`/aptitude-test/result/${resultId}`);
      setResult(response.data.result);
    } catch (error) {
      console.error('Failed to load result:', error);
      toast.error('Failed to load test results');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const downloadRoadmap = () => {
    toast.success('Roadmap download feature coming soon!');
  };

  if (loading || !result) {
    return (
      <div className="min-h-screen bg-[#fdfbf7] flex items-center justify-center">
        <div className="text-[#1e1b4b]">Loading results...</div>
      </div>
    );
  }

  const getDomainLabel = (domain) => {
    const labels = {
      'Government_Jobs': 'Government Jobs',
      'Technology': 'Technology',
      'Science': 'Science',
      'Medical': 'Medical',
      'Commerce': 'Commerce',
      'Arts': 'Arts & Humanities',
      'Entrepreneurship': 'Entrepreneurship'
    };
    return labels[domain] || domain;
  };

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
          
          <button
            onClick={downloadRoadmap}
            data-testid="download-roadmap-btn"
            className="flex items-center gap-2 px-6 py-2.5 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors"
          >
            <Download className="w-5 h-5" />
            Download Roadmap
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-[#1e1b4b] via-[#312e81] to-[#1e1b4b] text-white py-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <div className="w-20 h-20 bg-[#14b8a6] rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="w-10 h-10" />
          </div>
          <h1 className="text-4xl md:text-5xl font-semibold tracking-tight mb-4">
            Your Career Aptitude Results
          </h1>
          <p className="text-lg md:text-xl opacity-90 max-w-3xl mx-auto">
            Based on your responses, here's your personalized career roadmap
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Top Domains */}
        <div className="mb-12">
          <h2 className="text-3xl font-semibold text-[#1e1b4b] mb-6">Your Top Career Domains</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {result.top_domains.map((domain, index) => {
              const maxScore = Math.max(...result.top_domains.map(d => d.score));
              const percentage = (domain.score / maxScore) * 100;
              
              return (
                <div
                  key={domain.domain}
                  data-testid={`domain-${index}`}
                  className="bg-white border-2 border-[#1e1b4b]/10 rounded-2xl p-6 shadow-sm"
                >
                  <div className="flex items-center justify-between mb-4">
                    <span className={`px-4 py-1.5 rounded-full text-sm font-medium ${
                      index === 0 ? 'bg-[#14b8a6] text-white' :
                      index === 1 ? 'bg-[#f59e0b] text-white' :
                      'bg-[#1e1b4b]/10 text-[#1e1b4b]'
                    }`}>
                      {index === 0 ? '🥇 Best Match' : index === 1 ? '🥈 Second' : '🥉 Third'}
                    </span>
                  </div>
                  <h3 className="text-2xl font-semibold text-[#1e1b4b] mb-3">
                    {getDomainLabel(domain.domain)}
                  </h3>
                  <div className="mb-3">
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-[#64748b]">Match Score</span>
                      <span className="font-semibold text-[#1e1b4b]">{domain.score} points</span>
                    </div>
                    <div className="w-full h-3 bg-[#1e1b4b]/10 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-1000 ${
                          index === 0 ? 'bg-[#14b8a6]' :
                          index === 1 ? 'bg-[#f59e0b]' :
                          'bg-[#1e1b4b]'
                        }`}
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Career Suggestions */}
        {result.career_suggestions.length > 0 && (
          <div className="mb-12">
            <div className="flex items-center gap-3 mb-6">
              <Target className="w-8 h-8 text-[#f59e0b]" />
              <h2 className="text-3xl font-semibold text-[#1e1b4b]">Recommended Career Paths</h2>
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              {result.career_suggestions.map((career, index) => (
                <div
                  key={index}
                  data-testid={`career-${index}`}
                  className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all"
                >
                  <h3 className="text-xl font-semibold text-[#1e1b4b] mb-2">{career.title}</h3>
                  <p className="text-[#64748b] mb-4">{career.description}</p>
                  <div className="flex items-center gap-2">
                    <span className="px-4 py-2 bg-[#14b8a6]/10 text-[#14b8a6] font-semibold rounded-lg">
                      {career.salary}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* College Recommendations */}
        {result.college_recommendations.length > 0 && (
          <div className="mb-12">
            <div className="flex items-center gap-3 mb-6">
              <Building2 className="w-8 h-8 text-[#f59e0b]" />
              <h2 className="text-3xl font-semibold text-[#1e1b4b]">Recommended Colleges</h2>
            </div>
            <div className="space-y-6">
              {result.college_recommendations.map((college, index) => (
                <div
                  key={index}
                  data-testid={`college-${index}`}
                  className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm hover:shadow-md transition-all"
                >
                  <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-4">
                    <div>
                      <h3 className="text-2xl font-semibold text-[#1e1b4b] mb-2">{college.name}</h3>
                      <p className="text-[#64748b] mb-3">{college.location}</p>
                      {college.ranking && (
                        <span className="px-3 py-1 bg-[#f59e0b]/10 text-[#f59e0b] text-sm font-medium rounded-full">
                          {college.ranking}
                        </span>
                      )}
                    </div>
                    {college.website && (
                      <a
                        href={college.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-6 py-2.5 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors"
                      >
                        Visit Website
                      </a>
                    )}
                  </div>

                  <div className="grid md:grid-cols-2 gap-6 mb-4">
                    <div>
                      <p className="text-sm font-medium text-[#64748b] mb-2">Courses Offered</p>
                      <div className="flex flex-wrap gap-2">
                        {college.courses.map((course, i) => (
                          <span key={i} className="px-3 py-1 bg-[#1e1b4b]/5 text-[#1e1b4b] text-sm rounded-full">
                            {course}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-[#64748b] mb-2">Admission Process</p>
                      <p className="text-[#1e1b4b] font-medium">{college.admission}</p>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-3 gap-4 pt-4 border-t border-[#1e1b4b]/10">
                    <div>
                      <p className="text-sm font-medium text-[#64748b] mb-1">Fees</p>
                      <p className="text-[#1e1b4b] font-semibold">{college.fees}</p>
                    </div>
                    <div className="md:col-span-2">
                      <p className="text-sm font-medium text-[#64748b] mb-1">Placements</p>
                      <p className="text-[#1e1b4b] font-semibold">{college.placements}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Coding Practice Timeline */}
        {result.coding_timeline && result.coding_timeline.length > 0 && (
          <div className="mb-12">
            <div className="flex items-center gap-3 mb-6">
              <Code className="w-8 h-8 text-[#f59e0b]" />
              <h2 className="text-3xl font-semibold text-[#1e1b4b]">Weekly Coding Practice Timeline</h2>
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              {result.coding_timeline.map((week, index) => (
                <div
                  key={index}
                  data-testid={`coding-week-${index}`}
                  className="bg-white border-l-4 border-[#14b8a6] rounded-lg p-6 shadow-sm"
                >
                  <h3 className="text-xl font-semibold text-[#1e1b4b] mb-2">{week.week}</h3>
                  <p className="text-lg font-medium text-[#14b8a6] mb-4">{week.focus}</p>
                  <div className="space-y-3 mb-4">
                    <div>
                      <p className="text-sm font-medium text-[#64748b] mb-1">Topics</p>
                      <p className="text-[#1e1b4b]">{week.topics.join(', ')}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-[#64748b] mb-1">Platforms</p>
                      <div className="flex flex-wrap gap-2">
                        {week.platforms.map((platform, i) => (
                          <span key={i} className="px-3 py-1 bg-[#1e1b4b]/5 text-[#1e1b4b] text-sm font-medium rounded-full">
                            {platform}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-[#64748b] mb-1">Practice Schedule</p>
                      <p className="text-[#1e1b4b]">{week.practice}</p>
                    </div>
                  </div>
                  <div className="pt-3 border-t border-[#1e1b4b]/10">
                    <p className="text-sm font-medium text-[#f59e0b]">Goal: {week.goal}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 6-Month Roadmap */}
        {result.roadmap && result.roadmap.length > 0 && (
          <div className="mb-12">
            <div className="flex items-center gap-3 mb-6">
              <Calendar className="w-8 h-8 text-[#f59e0b]" />
              <h2 className="text-3xl font-semibold text-[#1e1b4b]">Your 6-Month Personalized Roadmap</h2>
            </div>
            <div className="relative">
              {/* Timeline Line */}
              <div className="absolute left-8 top-0 bottom-0 w-1 bg-[#1e1b4b]/10 hidden md:block"></div>
              
              <div className="space-y-8">
                {result.roadmap.map((month, index) => (
                  <div
                    key={index}
                    data-testid={`roadmap-month-${index}`}
                    className="relative"
                  >
                    {/* Timeline Dot */}
                    <div className="absolute left-6 w-5 h-5 bg-[#14b8a6] rounded-full border-4 border-white hidden md:block"></div>
                    
                    <div className="md:ml-20 bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm hover:shadow-md transition-all">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <span className="px-4 py-1.5 bg-[#14b8a6]/10 text-[#14b8a6] text-sm font-medium rounded-full">
                            {month.month}
                          </span>
                          <h3 className="text-2xl font-semibold text-[#1e1b4b] mt-3 mb-2">{month.title}</h3>
                        </div>
                        <TrendingUp className="w-8 h-8 text-[#f59e0b]" />
                      </div>
                      
                      <div className="space-y-3 mb-6">
                        {month.tasks.map((task, taskIndex) => (
                          <div key={taskIndex} className="flex items-start gap-3">
                            <CheckCircle className="w-5 h-5 text-[#14b8a6] flex-shrink-0 mt-0.5" />
                            <p className="text-[#64748b]">{task}</p>
                          </div>
                        ))}
                      </div>
                      
                      <div className="pt-4 border-t border-[#1e1b4b]/10">
                        <p className="text-sm font-medium text-[#64748b] mb-1">Milestone</p>
                        <p className="text-[#1e1b4b] font-semibold">{month.milestone}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="text-center">
          <button
            onClick={() => navigate('/aptitude-test')}
            className="px-8 py-4 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors shadow-lg hover:shadow-xl"
          >
            Take Test Again
          </button>
        </div>
      </div>
    </div>
  );
};

export default AptitudeResultPage;

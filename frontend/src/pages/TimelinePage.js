import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Calendar as CalendarIcon, Clock, BookOpen, AlertCircle } from 'lucide-react';
import { format, parseISO, isFuture, isPast } from 'date-fns';
import api from '@/utils/api';

const TimelinePage = ({ user }) => {
  const navigate = useNavigate();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      const response = await api.get('/timeline/events');
      setEvents(response.data.events || []);
    } catch (error) {
      console.error('Failed to load events:', error);
    } finally {
      setLoading(false);
    }
  };

  const upcomingEvents = events.filter(e => isFuture(parseISO(e.event_date)));
  const pastEvents = events.filter(e => isPast(parseISO(e.event_date)));

  const displayEvents = filter === 'upcoming' ? upcomingEvents : filter === 'past' ? pastEvents : events;

  const getEventTypeColor = (type) => {
    const colors = {
      exam_registration: 'bg-[#f59e0b]/10 text-[#f59e0b] border-[#f59e0b]/20',
      application_deadline: 'bg-red-500/10 text-red-600 border-red-500/20',
      counseling: 'bg-[#14b8a6]/10 text-[#14b8a6] border-[#14b8a6]/20',
      scholarship: 'bg-purple-500/10 text-purple-600 border-purple-500/20',
      default: 'bg-[#1e1b4b]/10 text-[#1e1b4b] border-[#1e1b4b]/20'
    };
    return colors[type] || colors.default;
  };

  const getEventTypeLabel = (type) => {
    const labels = {
      exam_registration: 'Exam Registration',
      application_deadline: 'Application Deadline',
      counseling: 'Counseling',
      scholarship: 'Scholarship',
    };
    return labels[type] || type.replace('_', ' ').toUpperCase();
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
        </div>
      </header>

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-[#1e1b4b] via-[#312e81] to-[#1e1b4b] text-white py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-4 mb-4">
            <CalendarIcon className="w-12 h-12" />
            <h1 className="text-4xl md:text-5xl font-semibold tracking-tight">
              Important Timeline
            </h1>
          </div>
          <p className="text-lg md:text-xl opacity-90 max-w-3xl">
            Track admission dates, exam registrations, and scholarship deadlines
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Filter Tabs */}
        <div className="flex gap-4 mb-8 border-b border-[#1e1b4b]/10 overflow-x-auto">
          <button
            onClick={() => setFilter('all')}
            data-testid="filter-all"
            className={`px-6 py-3 font-medium border-b-2 transition-colors ${
              filter === 'all'
                ? 'border-[#1e1b4b] text-[#1e1b4b]'
                : 'border-transparent text-[#64748b] hover:text-[#1e1b4b]'
            }`}
          >
            All Events ({events.length})
          </button>
          <button
            onClick={() => setFilter('upcoming')}
            data-testid="filter-upcoming"
            className={`px-6 py-3 font-medium border-b-2 transition-colors ${
              filter === 'upcoming'
                ? 'border-[#1e1b4b] text-[#1e1b4b]'
                : 'border-transparent text-[#64748b] hover:text-[#1e1b4b]'
            }`}
          >
            Upcoming ({upcomingEvents.length})
          </button>
          <button
            onClick={() => setFilter('past')}
            data-testid="filter-past"
            className={`px-6 py-3 font-medium border-b-2 transition-colors ${
              filter === 'past'
                ? 'border-[#1e1b4b] text-[#1e1b4b]'
                : 'border-transparent text-[#64748b] hover:text-[#1e1b4b]'
            }`}
          >
            Past ({pastEvents.length})
          </button>
        </div>

        {loading ? (
          <div className="text-center py-12">Loading events...</div>
        ) : displayEvents.length === 0 ? (
          <div className="text-center py-12">
            <AlertCircle className="w-16 h-16 text-[#64748b] mx-auto mb-4" />
            <p className="text-lg text-[#64748b]">No events found</p>
          </div>
        ) : (
          <div className="space-y-6">
            {displayEvents.map((event, index) => {
              const eventDate = parseISO(event.event_date);
              const isUpcoming = isFuture(eventDate);
              
              return (
                <div
                  key={event.id}
                  data-testid={`event-card-${index}`}
                  className={`bg-white border-2 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 ${
                    isUpcoming ? 'border-[#14b8a6]/20' : 'border-[#1e1b4b]/10 opacity-75'
                  }`}
                >
                  <div className="flex flex-col md:flex-row md:items-start gap-6">
                    {/* Date Badge */}
                    <div className="flex-shrink-0">
                      <div className={`w-20 h-20 rounded-xl flex flex-col items-center justify-center ${
                        isUpcoming ? 'bg-[#14b8a6]/10 text-[#14b8a6]' : 'bg-[#64748b]/10 text-[#64748b]'
                      }`}>
                        <span className="text-2xl font-bold">{format(eventDate, 'd')}</span>
                        <span className="text-xs font-medium uppercase">{format(eventDate, 'MMM')}</span>
                      </div>
                    </div>

                    {/* Event Details */}
                    <div className="flex-1">
                      <div className="flex flex-wrap items-start justify-between gap-4 mb-3">
                        <div>
                          <h3 className="text-xl font-semibold text-[#1e1b4b] mb-2">{event.title}</h3>
                          <div className="flex flex-wrap items-center gap-3">
                            <span className={`px-3 py-1 border text-xs font-medium rounded-full ${getEventTypeColor(event.event_type)}`}>
                              {getEventTypeLabel(event.event_type)}
                            </span>
                            {event.stream && (
                              <span className="px-3 py-1 bg-[#1e1b4b]/5 text-[#1e1b4b] text-xs font-medium rounded-full capitalize">
                                {event.stream}
                              </span>
                            )}
                            {event.target_class && (
                              <span className="px-3 py-1 bg-[#f59e0b]/10 text-[#f59e0b] text-xs font-medium rounded-full">
                                Class {event.target_class}
                              </span>
                            )}
                          </div>
                        </div>
                        
                        {isUpcoming && (
                          <div className="flex items-center gap-2 px-4 py-2 bg-[#14b8a6]/10 text-[#14b8a6] rounded-full">
                            <Clock className="w-4 h-4" />
                            <span className="text-sm font-medium">Upcoming</span>
                          </div>
                        )}
                      </div>

                      <p className="text-[#64748b] leading-relaxed mb-3">
                        {event.description}
                      </p>

                      <div className="flex items-center gap-2 text-sm text-[#64748b]">
                        <CalendarIcon className="w-4 h-4" />
                        <span>{format(eventDate, 'MMMM d, yyyy')}</span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Reminder Notice */}
        {upcomingEvents.length > 0 && filter !== 'past' && (
          <div className="mt-12 p-6 bg-[#14b8a6]/10 border border-[#14b8a6]/20 rounded-2xl">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-[#14b8a6] rounded-full flex items-center justify-center flex-shrink-0">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-[#1e1b4b] mb-2">
                  Don't miss important dates!
                </h3>
                <p className="text-[#64748b]">
                  You have {upcomingEvents.length} upcoming event{upcomingEvents.length !== 1 ? 's' : ''}. 
                  Make sure to mark your calendar and prepare in advance.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TimelinePage;

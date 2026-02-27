import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, BookOpen, Brain, MapPin, Calendar, TrendingUp, Users } from 'lucide-react';
import { motion } from 'framer-motion';

const LandingPage = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI Career Guidance",
      description: "Personalized recommendations based on your interests, strengths, and academic performance"
    },
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: "Stream Selection",
      description: "Choose the right path - Science, Commerce, or Arts - tailored to your goals"
    },
    {
      icon: <MapPin className="w-8 h-8" />,
      title: "College Directory",
      description: "Comprehensive database of Indian Government Colleges with detailed information"
    },
    {
      icon: <Calendar className="w-8 h-8" />,
      title: "Timeline Tracker",
      description: "Never miss admission dates, exam registrations, and scholarship deadlines"
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: "Career Roadmap",
      description: "Visualize your path from degree to dream career with step-by-step guidance"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Multi-language Support",
      description: "Access guidance in English, Hindi, Tamil, and Telugu"
    }
  ];

  return (
    <div className="min-h-screen bg-[#fdfbf7]">
      <div className="grain-overlay"></div>
      
      <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-white/70 border-b border-[#1e1b4b]/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2">
            <BookOpen className="w-8 h-8 text-[#1e1b4b]" />
            <span className="text-2xl font-semibold text-[#1e1b4b]">EduPath India</span>
          </Link>
          <div className="flex gap-4">
            <button 
              onClick={() => navigate('/login')}
              data-testid="nav-login-btn"
              className="px-6 py-2.5 text-[#1e1b4b] font-medium hover:bg-[#1e1b4b]/5 rounded-full transition-colors"
            >
              Login
            </button>
            <button 
              onClick={() => navigate('/register')}
              data-testid="nav-register-btn"
              className="px-6 py-2.5 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all duration-300"
            >
              Get Started
            </button>
          </div>
        </div>
      </nav>

      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-16">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div 
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-8"
            >
              <h1 className="text-4xl md:text-6xl font-semibold tracking-tight leading-tight text-[#1e1b4b]">
                Your Path to Success Starts Here
              </h1>
              <p className="text-lg md:text-xl leading-relaxed text-[#64748b]">
                AI-powered career guidance for Indian students. Find the perfect stream, degree, and government college for your bright future.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <button 
                  onClick={() => navigate('/register')}
                  data-testid="hero-register-btn"
                  className="px-8 py-6 bg-[#1e1b4b] text-white text-lg font-medium rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 flex items-center justify-center gap-2"
                >
                  Start Your Journey <ArrowRight className="w-5 h-5" />
                </button>
                <button 
                  onClick={() => navigate('/login')}
                  data-testid="hero-login-btn"
                  className="px-8 py-4 border-2 border-[#1e1b4b]/10 text-[#1e1b4b] text-lg font-medium rounded-full hover:bg-[#1e1b4b]/5 transition-all duration-300"
                >
                  Login
                </button>
              </div>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="relative rounded-3xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1719245309441-c577e0d1959d?crop=entropy&cs=srgb&fm=jpg&q=85" 
                  alt="Indian student with laptop" 
                  className="w-full h-auto object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#1e1b4b]/50 to-transparent"></div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      <section className="py-20 px-4 sm:px-6 lg:px-16 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-medium tracking-tight text-[#1e1b4b] mb-4">
              Why Choose EduPath India?
            </h2>
            <p className="text-lg text-[#64748b] max-w-2xl mx-auto">
              Comprehensive tools and guidance to help you make informed decisions about your education and career
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white border border-[#1e1b4b]/10 rounded-xl p-8 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1"
                data-testid={`feature-card-${index}`}
              >
                <div className="w-14 h-14 bg-[#f59e0b]/10 rounded-lg flex items-center justify-center text-[#f59e0b] mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-medium text-[#1e1b4b] mb-3">
                  {feature.title}
                </h3>
                <p className="text-base leading-relaxed text-[#64748b]">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-4 sm:px-6 lg:px-16 bg-gradient-to-br from-[#1e1b4b] via-[#312e81] to-[#1e1b4b] text-white">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="text-3xl md:text-5xl font-medium tracking-tight">
            Ready to Plan Your Future?
          </h2>
          <p className="text-lg md:text-xl opacity-90">
            Join thousands of students who have found their perfect career path with EduPath India
          </p>
          <button 
            onClick={() => navigate('/register')}
            data-testid="cta-register-btn"
            className="px-8 py-6 bg-[#f59e0b] text-[#1e1b4b] text-lg font-medium rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 inline-flex items-center gap-2"
          >
            Start Free Today <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </section>

      <footer className="py-12 px-4 sm:px-6 lg:px-16 bg-white border-t border-[#1e1b4b]/10">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <BookOpen className="w-6 h-6 text-[#1e1b4b]" />
            <span className="text-xl font-semibold text-[#1e1b4b]">EduPath India</span>
          </div>
          <p className="text-[#64748b]">
            Empowering Indian students to make informed career decisions
          </p>
          <p className="text-sm text-[#64748b] mt-4">
            &copy; 2026 EduPath India. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;

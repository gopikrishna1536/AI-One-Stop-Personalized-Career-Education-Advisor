import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, CheckCircle, Brain } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const AptitudeTestPage = ({ user }) => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const response = await api.get('/aptitude-test/questions');
      setQuestions(response.data.questions || []);
    } catch (error) {
      console.error('Failed to load questions:', error);
      toast.error('Failed to load test questions');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, optionIndex) => {
    setAnswers({ ...answers, [questionId]: optionIndex });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    const unansweredCount = questions.length - Object.keys(answers).length;
    
    if (unansweredCount > 0) {
      const confirmSubmit = window.confirm(
        `You have ${unansweredCount} unanswered question(s). Do you want to submit anyway?`
      );
      if (!confirmSubmit) return;
    }

    setSubmitting(true);
    try {
      const submission = {
        answers: Object.entries(answers).map(([question_id, selected_option]) => ({
          question_id,
          selected_option
        }))
      };

      const response = await api.post('/aptitude-test/submit', submission);
      toast.success('Test submitted successfully!');
      navigate(`/aptitude-result/${response.data.id}`);
    } catch (error) {
      console.error('Failed to submit test:', error);
      toast.error('Failed to submit test');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fdfbf7] flex items-center justify-center">
        <div className="text-[#1e1b4b]">Loading test questions...</div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen bg-[#fdfbf7] flex items-center justify-center">
        <div className="text-center">
          <p className="text-[#64748b] mb-4">No questions available</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-3 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const currentQ = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;
  const answeredCount = Object.keys(answers).length;

  return (
    <div className="min-h-screen bg-[#fdfbf7]">
      <div className="grain-overlay"></div>
      
      {/* Header */}
      <header className="bg-white border-b border-[#1e1b4b]/10 sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-4 flex justify-between items-center">
          <button 
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-[#1e1b4b] hover:opacity-70 transition-opacity"
            data-testid="back-to-dashboard-btn"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="font-medium">Dashboard</span>
          </button>
          
          <div className="flex items-center gap-4">
            <span className="text-sm text-[#64748b]">
              {answeredCount}/{questions.length} Answered
            </span>
          </div>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="bg-white border-b border-[#1e1b4b]/10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-[#1e1b4b]">
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <span className="text-sm font-medium text-[#14b8a6]">
              {Math.round(progress)}% Complete
            </span>
          </div>
          <div className="w-full h-2 bg-[#1e1b4b]/10 rounded-full overflow-hidden">
            <div 
              className="h-full bg-[#14b8a6] transition-all duration-300 rounded-full"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Question Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
        <div className="bg-white border border-[#1e1b4b]/10 rounded-2xl p-8 shadow-sm mb-8">
          <div className="flex items-start gap-4 mb-8">
            <div className="w-12 h-12 bg-[#1e1b4b] rounded-full flex items-center justify-center flex-shrink-0">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-semibold text-[#1e1b4b] mb-2">
                {currentQ.question}
              </h2>
              <p className="text-sm text-[#64748b]">Select the option that best describes you</p>
            </div>
          </div>

          <div className="space-y-3">
            {currentQ.options.map((option, index) => {
              const isSelected = answers[currentQ.id] === index;
              
              return (
                <button
                  key={index}
                  data-testid={`option-${index}`}
                  onClick={() => handleAnswer(currentQ.id, index)}
                  className={`w-full p-5 rounded-xl border-2 text-left transition-all duration-200 ${
                    isSelected
                      ? 'border-[#1e1b4b] bg-[#1e1b4b]/5 shadow-md'
                      : 'border-[#1e1b4b]/10 hover:border-[#1e1b4b]/30 hover:bg-[#1e1b4b]/5'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 mt-0.5 ${
                      isSelected
                        ? 'border-[#1e1b4b] bg-[#1e1b4b]'
                        : 'border-[#1e1b4b]/30'
                    }`}>
                      {isSelected && <CheckCircle className="w-4 h-4 text-white" />}
                    </div>
                    <span className="text-[#1e1b4b] font-medium">{option.text}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between items-center">
          <button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            data-testid="prev-btn"
            className="px-6 py-3 border-2 border-[#1e1b4b]/10 text-[#1e1b4b] font-medium rounded-full hover:bg-[#1e1b4b]/5 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <ArrowLeft className="w-5 h-5" />
            Previous
          </button>

          {currentQuestion === questions.length - 1 ? (
            <button
              onClick={handleSubmit}
              disabled={submitting}
              data-testid="submit-btn"
              className="px-8 py-3 bg-[#14b8a6] text-white font-medium rounded-full hover:bg-[#0d9488] transition-colors shadow-lg hover:shadow-xl disabled:opacity-50 flex items-center gap-2"
            >
              {submitting ? 'Submitting...' : 'Submit Test'}
              <CheckCircle className="w-5 h-5" />
            </button>
          ) : (
            <button
              onClick={handleNext}
              data-testid="next-btn"
              className="px-6 py-3 bg-[#1e1b4b] text-white font-medium rounded-full hover:bg-[#312e81] transition-colors shadow-lg flex items-center gap-2"
            >
              Next
              <ArrowRight className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Question Navigator */}
        <div className="mt-12 p-6 bg-white border border-[#1e1b4b]/10 rounded-2xl">
          <h3 className="text-lg font-semibold text-[#1e1b4b] mb-4">Quick Navigation</h3>
          <div className="grid grid-cols-6 sm:grid-cols-12 gap-2">
            {questions.map((q, index) => {
              const isAnswered = answers[q.id] !== undefined;
              const isCurrent = index === currentQuestion;
              
              return (
                <button
                  key={q.id}
                  onClick={() => setCurrentQuestion(index)}
                  data-testid={`nav-q-${index}`}
                  className={`w-10 h-10 rounded-lg font-medium transition-all ${
                    isCurrent
                      ? 'bg-[#1e1b4b] text-white shadow-md'
                      : isAnswered
                      ? 'bg-[#14b8a6] text-white'
                      : 'bg-[#1e1b4b]/5 text-[#64748b] hover:bg-[#1e1b4b]/10'
                  }`}
                >
                  {index + 1}
                </button>
              );
            })}
          </div>
          <div className="flex items-center gap-6 mt-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-[#14b8a6] rounded"></div>
              <span className="text-[#64748b]">Answered</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-[#1e1b4b] rounded"></div>
              <span className="text-[#64748b]">Current</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-[#1e1b4b]/5 rounded"></div>
              <span className="text-[#64748b]">Not Answered</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AptitudeTestPage;

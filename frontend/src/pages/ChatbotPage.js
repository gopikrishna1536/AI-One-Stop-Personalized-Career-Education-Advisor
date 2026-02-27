import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Bot, User as UserIcon, ArrowLeft, Globe } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/utils/api';

const ChatbotPage = ({ user }) => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [language, setLanguage] = useState(user?.preferred_language || 'english');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChatHistory = async () => {
    try {
      const response = await api.get('/chatbot/history');
      const history = response.data.history || [];
      const formattedMessages = history.flatMap(h => [
        { role: 'user', content: h.user_message, timestamp: h.timestamp },
        { role: 'bot', content: h.bot_response, timestamp: h.timestamp }
      ]);
      setMessages(formattedMessages);
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await api.post('/chatbot/message', {
        message: inputMessage,
        language: language
      });
      
      const botMessage = { 
        role: 'bot', 
        content: response.data.response,
        timestamp: response.data.timestamp 
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      toast.error('Failed to get response');
      const errorMessage = { 
        role: 'bot', 
        content: 'Sorry, I encountered an error. Please try again.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const languageLabels = {
    english: 'English',
    hindi: 'हिंदी',
    tamil: 'தமிழ்',
    telugu: 'తెలుగు'
  };

  return (
    <div className="min-h-screen bg-[#fdfbf7] flex flex-col">
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
          
          <div className="flex items-center gap-2">
            <Globe className="w-5 h-5 text-[#64748b]" />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              data-testid="language-select"
              className="px-3 py-1.5 bg-[#f9fafb] border border-[#1e1b4b]/10 rounded-lg text-sm font-medium text-[#1e1b4b] focus:outline-none focus:ring-2 focus:ring-[#1e1b4b]/20"
            >
              {Object.entries(languageLabels).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
          {messages.length === 0 ? (
            <div className="text-center py-12" data-testid="welcome-message">
              <div className="w-20 h-20 bg-gradient-to-br from-[#1e1b4b] to-[#312e81] rounded-full flex items-center justify-center mx-auto mb-6">
                <Bot className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-3xl font-semibold text-[#1e1b4b] mb-4">
                Hi {user?.full_name}! I'm your AI Career Guide
              </h2>
              <p className="text-lg text-[#64748b] mb-8 max-w-2xl mx-auto">
                I'm here to help you discover the perfect career path. Ask me about:
              </p>
              <div className="grid sm:grid-cols-2 gap-4 max-w-2xl mx-auto">
                {[
                  'Which stream should I choose?',
                  'What degrees are available in Science?',
                  'Best colleges in my state',
                  'Career options after B.Tech'
                ].map((suggestion, i) => (
                  <button
                    key={i}
                    data-testid={`suggestion-${i}`}
                    onClick={() => setInputMessage(suggestion)}
                    className="p-4 bg-white border border-[#1e1b4b]/10 rounded-xl hover:border-[#1e1b4b]/30 hover:shadow-md transition-all text-left"
                  >
                    <p className="text-[#1e1b4b] font-medium">{suggestion}</p>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  data-testid={`message-${msg.role}-${index}`}
                  className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  {msg.role === 'bot' && (
                    <div className="w-10 h-10 bg-gradient-to-br from-[#1e1b4b] to-[#312e81] rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                  )}
                  
                  <div className={`max-w-[80%] ${msg.role === 'user' ? 'order-first' : ''}`}>
                    <div
                      className={`p-4 rounded-2xl ${
                        msg.role === 'user'
                          ? 'bg-[#1e1b4b] text-white'
                          : 'bg-white border border-[#1e1b4b]/10 text-[#1e1b4b]'
                      }`}
                    >
                      <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                    </div>
                  </div>
                  
                  {msg.role === 'user' && (
                    <div className="w-10 h-10 bg-[#f59e0b] rounded-full flex items-center justify-center flex-shrink-0">
                      <UserIcon className="w-5 h-5 text-white" />
                    </div>
                  )}
                </div>
              ))}
              
              {loading && (
                <div className="flex gap-4 justify-start" data-testid="typing-indicator">
                  <div className="w-10 h-10 bg-gradient-to-br from-[#1e1b4b] to-[#312e81] rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                  <div className="bg-white border border-[#1e1b4b]/10 p-4 rounded-2xl">
                    <div className="flex gap-1.5">
                      <div className="w-2 h-2 bg-[#1e1b4b] rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-[#1e1b4b] rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-[#1e1b4b] rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-[#1e1b4b]/10 bg-white sticky bottom-0">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-4">
          <form onSubmit={sendMessage} className="flex gap-3">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              data-testid="chat-input"
              placeholder="Ask me anything about your career..."
              className="flex-1 h-14 px-6 rounded-full border border-[#1e1b4b]/10 focus:border-[#1e1b4b] focus:ring-2 focus:ring-[#1e1b4b]/20 bg-[#f9fafb] transition-colors"
              disabled={loading}
            />
            <button
              type="submit"
              data-testid="send-message-btn"
              disabled={loading || !inputMessage.trim()}
              className="w-14 h-14 bg-[#1e1b4b] text-white rounded-full hover:bg-[#312e81] transition-colors flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;

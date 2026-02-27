import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import '@/App.css';
import LandingPage from '@/pages/LandingPage';
import RegisterPage from '@/pages/RegisterPage';
import LoginPage from '@/pages/LoginPage';
import ResetPasswordPage from '@/pages/ResetPasswordPage';
import Dashboard from '@/pages/Dashboard';
import ChatbotPage from '@/pages/ChatbotPage';
import CollegesPage from '@/pages/CollegesPage';
import TimelinePage from '@/pages/TimelinePage';
import ProfilePage from '@/pages/ProfilePage';
import AdminDashboard from '@/pages/AdminDashboard';
import AptitudeTestPage from '@/pages/AptitudeTestPage';
import AptitudeResultPage from '@/pages/AptitudeResultPage';
import { Toaster } from '@/components/ui/sonner';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  const ProtectedRoute = ({ children }) => {
    if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
    return user ? children : <Navigate to="/login" />;
  };

  const PublicRoute = ({ children }) => {
    if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
    return !user ? children : <Navigate to="/dashboard" />;
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<PublicRoute><LandingPage /></PublicRoute>} />
          <Route path="/register" element={<PublicRoute><RegisterPage setUser={setUser} /></PublicRoute>} />
          <Route path="/login" element={<PublicRoute><LoginPage setUser={setUser} /></PublicRoute>} />
          <Route path="/reset-password" element={<PublicRoute><ResetPasswordPage /></PublicRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard user={user} /></ProtectedRoute>} />
          <Route path="/chatbot" element={<ProtectedRoute><ChatbotPage user={user} /></ProtectedRoute>} />
          <Route path="/colleges" element={<ProtectedRoute><CollegesPage user={user} /></ProtectedRoute>} />
          <Route path="/timeline" element={<ProtectedRoute><TimelinePage user={user} /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage user={user} setUser={setUser} /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute><AdminDashboard user={user} /></ProtectedRoute>} />
          <Route path="/aptitude-test" element={<ProtectedRoute><AptitudeTestPage user={user} /></ProtectedRoute>} />
          <Route path="/aptitude-result/:resultId" element={<ProtectedRoute><AptitudeResultPage user={user} /></ProtectedRoute>} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" expand={false} richColors />
    </div>
  );
}

export default App;

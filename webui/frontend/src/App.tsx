import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { motion } from 'framer-motion';

// Components
import Navbar from './components/Layout/Navbar';
import Sidebar from './components/Layout/Sidebar';
import Dashboard from './components/Dashboard/Dashboard';
import { ChatInterface } from './components/Chat/ChatInterface';
import { MemoryViewer } from './components/Memory/MemoryViewer';
import { ReasoningAnalyzer } from './components/Reasoning/ReasoningAnalyzer';
import { LearningCenter } from './components/Learning/LearningCenter';
import { EvolutionMonitor } from './components/Evolution/EvolutionMonitor';
import { SystemMonitor } from './components/System/SystemMonitor';
import { AdminPanel } from './components/Admin/AdminPanel';
import AuthPage from './pages/AuthPage';
import ProtectedRoute from './components/Auth/ProtectedRoute';

// Hooks and Context
import { useAGIStore } from './store/agiStore';
import { AGIProvider } from './context/AGIContext';
import { AuthProvider } from './context/AuthContext';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Create dark theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00e5ff',
      light: '#62efff',
      dark: '#00b2cc',
    },
    secondary: {
      main: '#ff4081',
      light: '#ff79b0',
      dark: '#c60055',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1a1a1a',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b0b0b0',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      background: 'linear-gradient(45deg, #00e5ff, #ff4081)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
      },
    },
  },
});

const App: React.FC = () => {
  const { sidebarOpen } = useAGIStore();

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <AGIProvider>
          <ThemeProvider theme={darkTheme}>
            <CssBaseline />
            <Router>
            <Box sx={{ display: 'flex', minHeight: '100vh' }}>
              {/* Animated background */}
              <Box
                sx={{
                  position: 'fixed',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  background: `
                    radial-gradient(circle at 20% 80%, rgba(0, 229, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 64, 129, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(0, 229, 255, 0.05) 0%, transparent 50%)
                  `,
                  zIndex: -1,
                }}
              />

              {/* Sidebar */}
              <Sidebar />

              {/* Main content */}
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  display: 'flex',
                  flexDirection: 'column',
                  marginLeft: sidebarOpen ? '280px' : '80px',
                  transition: 'margin-left 0.3s ease',
                }}
              >
                {/* Navbar */}
                <Navbar />

                {/* Page content */}
                <Box
                  sx={{
                    flexGrow: 1,
                    p: 3,
                    overflow: 'auto',
                  }}
                >
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    <Routes>
                  {/* Public route for authentication */}
                  <Route path="/auth" element={<AuthPage />} />
                  
                  {/* Main chat page - default route for all users */}
                  <Route path="/" element={
                    <ProtectedRoute>
                      <ChatInterface />
                    </ProtectedRoute>
                  } />
                  
                  {/* Dashboard for admin/developers */}
                  <Route path="/dashboard" element={
                    <ProtectedRoute requiredRole="developer">
                      <Dashboard />
                    </ProtectedRoute>
                  } />
                  
                  {/* Developer/Admin routes */}
                  <Route path="/memory" element={
                    <ProtectedRoute requiredRole="developer">
                      <MemoryViewer />
                    </ProtectedRoute>
                  } />
                  <Route path="/reasoning" element={
                    <ProtectedRoute requiredRole="developer">
                      <ReasoningAnalyzer />
                    </ProtectedRoute>
                  } />
                  <Route path="/learning" element={
                    <ProtectedRoute requiredRole="developer">
                      <LearningCenter />
                    </ProtectedRoute>
                  } />
                  <Route path="/evolution" element={
                    <ProtectedRoute requiredRole="developer">
                      <EvolutionMonitor />
                    </ProtectedRoute>
                  } />
                  <Route path="/system" element={
                    <ProtectedRoute requiredRole="developer">
                      <SystemMonitor />
                    </ProtectedRoute>
                  } />
                  <Route path="/admin" element={
                    <ProtectedRoute requiredRole="admin">
                      <AdminPanel />
                    </ProtectedRoute>
                  } />
                </Routes>
                  </motion.div>
                </Box>
              </Box>
            </Box>

            {/* Toast notifications */}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#1a1a1a',
                  color: '#ffffff',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                },
                success: {
                  iconTheme: {
                    primary: '#00e5ff',
                    secondary: '#1a1a1a',
                  },
                },
                error: {
                  iconTheme: {
                    primary: '#ff4081',
                    secondary: '#1a1a1a',
                  },
                },
              }}
            />
            </Router>
          </ThemeProvider>
        </AGIProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;
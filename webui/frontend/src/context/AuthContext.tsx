import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, AuthResponse, LoginRequest, RegisterRequest } from '../services/api';
import { agiApi } from '../services/api';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  hasRole: (role: string) => boolean;
  hasPermission: (permission: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user;

  // Initialize auth state
  useEffect(() => {
    const initAuth = async () => {
      const token = agiApi.getToken();
      if (token) {
        try {
          const userData = await agiApi.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error('Failed to get current user:', error);
          agiApi.clearToken();
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginRequest) => {
    try {
      setIsLoading(true);
      const response: AuthResponse = await agiApi.login(credentials);
      setUser(response.user);
      toast.success(`Welcome back, ${response.user.username}!`);
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Login failed';
      toast.error(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData: RegisterRequest) => {
    try {
      setIsLoading(true);
      const response: AuthResponse = await agiApi.register(userData);
      setUser(response.user);
      toast.success(`Welcome to Atulya Tantra AGI, ${response.user.username}!`);
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Registration failed';
      toast.error(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      await agiApi.logout();
      setUser(null);
      toast.success('Logged out successfully');
    } catch (error) {
      console.error('Logout error:', error);
      // Clear local state even if API call fails
      setUser(null);
      agiApi.clearToken();
    }
  };

  const refreshUser = async () => {
    try {
      const userData = await agiApi.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to refresh user:', error);
      setUser(null);
      agiApi.clearToken();
    }
  };

  const hasRole = (role: string): boolean => {
    return user?.role === role;
  };

  const hasPermission = (permission: string): boolean => {
    return user?.permissions?.includes(permission) || false;
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
    hasRole,
    hasPermission,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
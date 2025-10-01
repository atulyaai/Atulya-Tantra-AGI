import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

// Types
export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  sender: 'user' | 'assistant';
  timestamp: Date;
  metadata?: {
    reasoning?: string;
    confidence?: number;
    sources?: string[];
    tokens?: number;
  };
}

export interface SystemStatus {
  status: 'healthy' | 'warning' | 'error' | 'offline';
  uptime: number;
  cpu_usage: number;
  memory_usage: number;
  active_connections: number;
  last_updated: string;
}

export interface MemoryStats {
  total_memories: number;
  recent_memories: number;
  memory_types: Record<string, number>;
  storage_size: number;
}

export interface LearningStats {
  total_experiences: number;
  learning_rate: number;
  adaptation_score: number;
  knowledge_growth: number;
}

export interface EvolutionStatus {
  generation: number;
  fitness_score: number;
  mutations: number;
  improvements: string[];
  last_evolution: string;
}

export interface ErrorLog {
  id: string;
  timestamp: Date;
  type: 'connection' | 'message' | 'system' | 'ui';
  message: string;
  details?: any;
  resolved: boolean;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  created_at: Date;
  updated_at: Date;
}

// Store interface
interface AGIStore {
  // UI State
  sidebarOpen: boolean;
  currentPage: string;
  loading: boolean;
  error: string | null;

  // Chat State
  messages: Message[];
  isTyping: boolean;
  connectionStatus: 'connected' | 'disconnected' | 'connecting';
  chatSessions: ChatSession[];
  currentSessionId: string | null;

  // Error Logging
  errorLogs: ErrorLog[];
  lastError: ErrorLog | null;

  // System State
  systemStatus: SystemStatus | null;
  memoryStats: MemoryStats | null;
  learningStats: LearningStats | null;
  evolutionStatus: EvolutionStatus | null;

  // Actions
  setSidebarOpen: (open: boolean) => void;
  setCurrentPage: (page: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;

  // Chat Actions
  addMessage: (message: Message) => void;
  clearMessages: () => void;
  setIsTyping: (typing: boolean) => void;
  setConnectionStatus: (status: 'connected' | 'disconnected' | 'connecting') => void;
  
  // Chat Session Actions
  createNewSession: () => void;
  loadSession: (sessionId: string) => void;
  saveCurrentSession: () => void;
  deleteSession: (sessionId: string) => void;
  
  // Error Logging Actions
  logError: (type: ErrorLog['type'], message: string, details?: any) => void;
  clearErrors: () => void;
  markErrorResolved: (errorId: string) => void;

  // System Actions
  setSystemStatus: (status: SystemStatus) => void;
  setMemoryStats: (stats: MemoryStats) => void;
  setLearningStats: (stats: LearningStats) => void;
  setEvolutionStatus: (status: EvolutionStatus) => void;

  // Utility Actions
  reset: () => void;
}

// Initial state
const initialState = {
  sidebarOpen: true,
  currentPage: 'dashboard',
  loading: false,
  error: null,
  messages: [],
  isTyping: false,
  connectionStatus: 'disconnected' as const,
  chatSessions: [],
  currentSessionId: null,
  errorLogs: [],
  lastError: null,
  systemStatus: null,
  memoryStats: null,
  learningStats: null,
  evolutionStatus: null,
};

// Create store
export const useAGIStore = create<AGIStore>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        // UI Actions
        setSidebarOpen: (open) => set({ sidebarOpen: open }),
        setCurrentPage: (page) => set({ currentPage: page }),
        setLoading: (loading) => set({ loading }),
        setError: (error) => set({ error }),

        // Chat Actions
        addMessage: (message) =>
          set((state) => ({
            messages: [...state.messages, message],
          })),
        clearMessages: () => set({ messages: [] }),
        setIsTyping: (typing) => set({ isTyping: typing }),
        setConnectionStatus: (status) => set({ connectionStatus: status }),

        // Chat Session Actions
        createNewSession: () => {
          const newSession: ChatSession = {
            id: Date.now().toString(),
            title: `Chat ${new Date().toLocaleDateString()}`,
            messages: [],
            created_at: new Date(),
            updated_at: new Date(),
          };
          set((state) => ({
            chatSessions: [...state.chatSessions, newSession],
            currentSessionId: newSession.id,
            messages: [],
          }));
        },
        
        loadSession: (sessionId) => {
          const session = get().chatSessions.find(s => s.id === sessionId);
          if (session) {
            set({
              currentSessionId: sessionId,
              messages: session.messages,
            });
          }
        },
        
        saveCurrentSession: () => {
          const state = get();
          if (state.currentSessionId) {
            set((prevState) => ({
              chatSessions: prevState.chatSessions.map(session =>
                session.id === state.currentSessionId
                  ? { ...session, messages: state.messages, updated_at: new Date() }
                  : session
              ),
            }));
          }
        },
        
        deleteSession: (sessionId) => {
          set((state) => ({
            chatSessions: state.chatSessions.filter(s => s.id !== sessionId),
            currentSessionId: state.currentSessionId === sessionId ? null : state.currentSessionId,
            messages: state.currentSessionId === sessionId ? [] : state.messages,
          }));
        },

        // Error Logging Actions
        logError: (type, message, details) => {
          const errorLog: ErrorLog = {
            id: Date.now().toString(),
            timestamp: new Date(),
            type,
            message,
            details,
            resolved: false,
          };
          set((state) => ({
            errorLogs: [...state.errorLogs, errorLog],
            lastError: errorLog,
          }));
        },
        
        clearErrors: () => set({ errorLogs: [], lastError: null }),
        
        markErrorResolved: (errorId) => {
          set((state) => ({
            errorLogs: state.errorLogs.map(error =>
              error.id === errorId ? { ...error, resolved: true } : error
            ),
          }));
        },

        // System Actions
        setSystemStatus: (status) => set({ systemStatus: status }),
        setMemoryStats: (stats) => set({ memoryStats: stats }),
        setLearningStats: (stats) => set({ learningStats: stats }),
        setEvolutionStatus: (status) => set({ evolutionStatus: status }),

        // Utility Actions
        reset: () => set(initialState),
      }),
       {
         name: 'agi-store',
       }
     ),
     {
       name: 'agi-store-devtools',
     }
   )
 )

// Selectors
export const useMessages = () => useAGIStore((state) => state.messages);
export const useSystemStatus = () => useAGIStore((state) => state.systemStatus);
export const useMemoryStats = () => useAGIStore((state) => state.memoryStats);
export const useLearningStats = () => useAGIStore((state) => state.learningStats);
export const useEvolutionStatus = () => useAGIStore((state) => state.evolutionStatus);
export const useConnectionStatus = () => useAGIStore((state) => state.connectionStatus);
export const useIsTyping = () => useAGIStore((state) => state.isTyping);
export const useLoading = () => useAGIStore((state) => state.loading);
export const useError = () => useAGIStore((state) => state.error);
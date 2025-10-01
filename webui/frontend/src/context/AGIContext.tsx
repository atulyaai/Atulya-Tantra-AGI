import React, { createContext, useContext, useEffect, useRef, useState, ReactNode } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAGIStore } from '../store/agiStore';
import { agiApi } from '../services/api';
import toast from 'react-hot-toast';

// Types
interface AGIContextType {
  socket: Socket | null;
  isConnected: boolean;
  sendMessage: (message: string) => Promise<void>;
  reconnect: () => void;
  disconnect: () => void;
}

// Create context
const AGIContext = createContext<AGIContextType | undefined>(undefined);

// Provider props
interface AGIProviderProps {
  children: ReactNode;
}

// Provider component
export const AGIProvider: React.FC<AGIProviderProps> = ({ children }) => {
  const socketRef = useRef<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const {
    setConnectionStatus,
    addMessage,
    setIsTyping,
    setSystemStatus,
    setMemoryStats,
    setLearningStats,
    setEvolutionStatus,
    setError,
    logError,
    saveCurrentSession,
  } = useAGIStore();

  // Initialize socket connection
  const initializeSocket = () => {
    if (socketRef.current) {
      socketRef.current.disconnect();
    }

    setConnectionStatus('connecting');

    socketRef.current = io('ws://localhost:8000', {
      transports: ['websocket'],
      autoConnect: true,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    const socket = socketRef.current;

    // Connection events
    socket.on('connect', () => {
      console.log('Connected to AGI WebSocket');
      setConnectionStatus('connected');
      setIsConnected(true);
      setError(null);
      toast.success('Connected to AGI System');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from AGI WebSocket');
      setConnectionStatus('disconnected');
      setIsConnected(false);
      toast.error('Disconnected from AGI System');
    });

    socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
      setConnectionStatus('disconnected');
      setIsConnected(false);
      setError('Failed to connect to AGI System');
      logError('connection', 'Failed to connect to AGI System', { error: error.message });
      toast.error('Connection failed');
    });

    // Message events
    socket.on('message', (data) => {
      addMessage({
        id: Date.now().toString(),
        content: data.content,
        role: 'assistant',
        sender: 'assistant',
        timestamp: new Date(),
        metadata: data.metadata,
      });
      setIsTyping(false);
    });

    socket.on('typing', (data) => {
      setIsTyping(data.typing);
    });

    socket.on('error', (data) => {
      setError(data.message);
      logError('system', data.message, data);
      setIsTyping(false);
      toast.error(data.message);
    });

    // System status events
    socket.on('system_status', (data) => {
      setSystemStatus(data);
    });

    socket.on('memory_stats', (data) => {
      setMemoryStats(data);
    });

    socket.on('learning_stats', (data) => {
      setLearningStats(data);
    });

    socket.on('evolution_status', (data) => {
      setEvolutionStatus(data);
    });

    // Reasoning events
    socket.on('reasoning_update', (data) => {
      console.log('Reasoning update:', data);
      // Handle reasoning updates
    });

    // Learning events
    socket.on('learning_update', (data) => {
      console.log('Learning update:', data);
      // Handle learning updates
    });

    // Evolution events
    socket.on('evolution_update', (data) => {
      console.log('Evolution update:', data);
      toast.success(`Evolution: ${data.message}`);
    });
  };

  // Send message function
  const sendMessage = async (message: string): Promise<void> => {
    try {
      // Add user message to store
      addMessage({
        id: Date.now().toString(),
        content: message,
        role: 'user',
        sender: 'user',
        timestamp: new Date(),
      });

      // Send via WebSocket if connected
      if (socketRef.current?.connected) {
        socketRef.current.emit('message', { content: message });
        setIsTyping(true);
      } else {
        // Fallback to HTTP API
        const response = await agiApi.sendMessage(message);
        addMessage({
          id: Date.now().toString(),
          content: response.response,
          role: 'assistant',
          sender: 'assistant',
          timestamp: new Date(),
          metadata: response.metadata,
        });
      }
      
      // Save current session after successful message
      saveCurrentSession();
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = error instanceof Error ? error.message : 'Failed to send message';
      setError(errorMessage);
      logError('message', errorMessage, { originalMessage: message, error });
      toast.error('Failed to send message');
    }
  };

  // Reconnect function
  const reconnect = () => {
    initializeSocket();
  };

  // Disconnect function
  const disconnect = () => {
    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
    }
    setConnectionStatus('disconnected');
  };

  // Initialize on mount
  useEffect(() => {
    initializeSocket();

    // Cleanup on unmount
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  // Fetch initial system status
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [systemStatus, memoryStats, learningStats, evolutionStatus] = await Promise.all([
          agiApi.getSystemStatus(),
          agiApi.getMemoryStats(),
          agiApi.getLearningStats(),
          agiApi.getEvolutionStatus(),
        ]);

        setSystemStatus(systemStatus);
        setMemoryStats(memoryStats);
        setLearningStats(learningStats);
        setEvolutionStatus(evolutionStatus);
      } catch (error) {
        console.error('Error fetching initial data:', error);
        setError('Failed to load system data');
      }
    };

    fetchInitialData();
  }, []);

  const contextValue: AGIContextType = {
    socket: socketRef.current,
    isConnected,
    sendMessage,
    reconnect,
    disconnect,
  };

  return (
    <AGIContext.Provider value={contextValue}>
      {children}
    </AGIContext.Provider>
  );
};

// Hook to use AGI context
export const useAGI = (): AGIContextType => {
  const context = useContext(AGIContext);
  if (context === undefined) {
    throw new Error('useAGI must be used within an AGIProvider');
  }
  return context;
};
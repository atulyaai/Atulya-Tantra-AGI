import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface User {
  id: string;
  username: string;
  email: string;
  full_name?: string;
  role: string;
  permissions: string[];
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  context?: any;
}

export interface ChatResponse {
  response: string;
  session_id: string;
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

export interface MemoryRequest {
  content: string;
  type: 'episodic' | 'semantic' | 'procedural';
  importance: number;
  tags?: string[];
}

export interface MemoryResponse {
  id: string;
  content: string;
  type: string;
  importance: number;
  tags: string[];
  created_at: string;
  accessed_count: number;
}

export interface MemoryStats {
  total_memories: number;
  recent_memories: number;
  memory_types: Record<string, number>;
  storage_size: number;
}

export interface ReasoningRequest {
  query: string;
  context?: any;
  reasoning_type?: 'deductive' | 'inductive' | 'abductive';
}

export interface ReasoningResponse {
  conclusion: string;
  reasoning_chain: string[];
  confidence: number;
  evidence: string[];
}

export interface LearningRequest {
  experience: string;
  outcome: string;
  feedback?: string;
  importance?: number;
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

export interface SystemMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_io: {
    bytes_sent: number;
    bytes_received: number;
  };
  process_count: number;
  uptime: number;
}

// API Client Class
export class AGIApiClient {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor(baseURL: string = 'http://localhost:8000') {
    this.api = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('Request error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error('Response error:', error.response?.data || error.message);
        if (error.response?.status === 401) {
          this.clearToken();
          window.location.href = '/auth';
        }
        return Promise.reject(error);
      }
    );

    // Load token from localStorage
    this.token = localStorage.getItem('agi_token');
  }

  // Token management
  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('agi_token', token);
  }

  clearToken(): void {
    this.token = null;
    localStorage.removeItem('agi_token');
  }

  getToken(): string | null {
    return this.token;
  }

  // Authentication endpoints
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/login', credentials);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/register', userData);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async logout(): Promise<void> {
    await this.api.post('/auth/logout');
    this.clearToken();
  }

  async getCurrentUser(): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get('/auth/me');
    return response.data;
  }

  async refreshToken(): Promise<AuthResponse> {
    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/refresh');
    this.setToken(response.data.access_token);
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response: AxiosResponse<{ status: string }> = await this.api.get('/health');
    return response.data;
  }

  // Chat endpoints
  async sendMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response: AxiosResponse<ChatResponse> = await this.api.post('/chat/message', {
      message,
      session_id: sessionId,
    });
    return response.data;
  }

  async getChatHistory(sessionId?: string): Promise<any[]> {
    const params = sessionId ? { session_id: sessionId } : {};
    const response: AxiosResponse<any[]> = await this.api.get('/chat/history', { params });
    return response.data;
  }

  async getChatSessions(): Promise<any[]> {
    const response: AxiosResponse<any[]> = await this.api.get('/chat/sessions');
    return response.data;
  }

  async clearChatHistory(sessionId?: string): Promise<void> {
    const data = sessionId ? { session_id: sessionId } : {};
    await this.api.delete('/chat/history', { data });
  }

  // Memory endpoints
  async storeMemory(memory: MemoryRequest): Promise<MemoryResponse> {
    const response: AxiosResponse<MemoryResponse> = await this.api.post('/memory/store', memory);
    return response.data;
  }

  async retrieveMemories(query: string, limit?: number): Promise<MemoryResponse[]> {
    const response: AxiosResponse<MemoryResponse[]> = await this.api.get('/memory/retrieve', {
      params: { query, limit },
    });
    return response.data;
  }

  async getMemoryStats(): Promise<MemoryStats> {
    const response: AxiosResponse<MemoryStats> = await this.api.get('/memory/stats');
    return response.data;
  }

  // Reasoning endpoints
  async analyzeReasoning(request: ReasoningRequest): Promise<ReasoningResponse> {
    const response: AxiosResponse<ReasoningResponse> = await this.api.post('/reasoning/analyze', request);
    return response.data;
  }

  // Learning endpoints
  async addLearningExperience(experience: LearningRequest): Promise<void> {
    await this.api.post('/learning/experience', experience);
  }

  async getLearningStats(): Promise<LearningStats> {
    const response: AxiosResponse<LearningStats> = await this.api.get('/learning/stats');
    return response.data;
  }

  // Evolution endpoints
  async getEvolutionStatus(): Promise<EvolutionStatus> {
    const response: AxiosResponse<EvolutionStatus> = await this.api.get('/evolution/status');
    return response.data;
  }

  async triggerEvolution(): Promise<void> {
    await this.api.post('/evolution/trigger');
  }

  // System endpoints
  async getSystemStatus(): Promise<SystemStatus> {
    const response: AxiosResponse<SystemStatus> = await this.api.get('/system/status');
    return response.data;
  }

  async getSystemMetrics(): Promise<SystemMetrics> {
    const response: AxiosResponse<SystemMetrics> = await this.api.get('/system/metrics');
    return response.data;
  }

  // Admin endpoints
  async getAdminDashboard(): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/admin/dashboard');
    return response.data;
  }

  async getSystemHealth(): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/admin/system/health');
    return response.data;
  }

  async getSystemLogs(level?: string, limit?: number): Promise<any[]> {
    const response: AxiosResponse<any[]> = await this.api.get('/admin/system/logs', {
      params: { level, limit },
    });
    return response.data;
  }

  async getSystemConfig(): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/admin/system/config');
    return response.data;
  }

  async updateSystemConfig(config: any): Promise<void> {
    await this.api.put('/admin/system/config', config);
  }

  async restartSystem(): Promise<void> {
    await this.api.post('/admin/system/restart');
  }

  async getUserActivity(): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/admin/users/activity');
    return response.data;
  }

  async getPerformanceMetrics(): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/admin/performance/metrics');
    return response.data;
  }

  // Developer endpoints
  async getDeveloperDashboard(): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/developer/dashboard');
    return response.data;
  }

  async getMetrics(component?: string, category?: string): Promise<any[]> {
    const response: AxiosResponse<any[]> = await this.api.get('/developer/metrics', {
      params: { component, category },
    });
    return response.data;
  }

  async getDebugInfo(component: string): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get(`/developer/debug/${component}`);
    return response.data;
  }

  async getSystemTraces(): Promise<any[]> {
    const response: AxiosResponse<any[]> = await this.api.get('/developer/traces');
    return response.data;
  }

  async triggerDebugOperation(component: string, operation: string): Promise<any> {
    const response: AxiosResponse<any> = await this.api.post(`/developer/debug/${component}/${operation}`);
    return response.data;
  }
}

// Export singleton instance
export const agiApi = new AGIApiClient();
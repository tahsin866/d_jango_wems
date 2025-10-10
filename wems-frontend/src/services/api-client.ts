/**
 * Simple API Client for WEMS System
 */

interface User {
  id: number;
  email: string;
  phone?: string;
  user_type: string;
  full_name: string;
  permissions: string[];
}

interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status_code: number;
}

class ApiClient {
  private baseURL: string;
  private timeout: number;
  private accessToken: string | null = null;

  constructor() {
    this.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
    this.timeout = 30000;
    this.accessToken = localStorage.getItem('access_token');
  }

  private async makeRequest(url: string, options: RequestInit = {}): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': this.accessToken ? `Bearer ${this.accessToken}` : '',
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  private async apiRequest<T = any>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseURL}${endpoint}`;
      const response = await this.makeRequest(url, options);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }

      const data = await response.json();
      return {
        data,
        status_code: response.status,
      };
    } catch (error) {
      if (error instanceof Error) {
        return {
          error: error.message,
          status_code: 500,
        };
      }
      return {
        error: 'Unknown error occurred',
        status_code: 500,
      };
    }
  }

  // Get departments from API
  async getDepartments() {
    return this.apiRequest('/api/admin/departments/', {
      method: 'GET',
    });
  }

  // Get user types from API
  async getUserTypes() {
    return this.apiRequest('/api/admin/departments/user-types/', {
      method: 'GET',
    });
  }

  // Get modules from API
  async getModules() {
    return this.apiRequest('/api/admin/departments/modules/', {
      method: 'GET',
    });
  }

  // Get modules by department
  async getModulesByDepartment(departmentId: number) {
    return this.apiRequest(`/api/admin/departments/modules/${departmentId}/`, {
      method: 'GET',
    });
  }

  // Get menus from API
  async getMenus() {
    return this.apiRequest('/api/admin/departments/menus/', {
      method: 'GET',
    });
  }

  // Get menus by module
  async getMenusByModule(moduleId: number) {
    return this.apiRequest(`/api/admin/departments/menus/${moduleId}/`, {
      method: 'GET',
    });
  }

  // Get permissions from API
  async getPermissions() {
    return this.apiRequest('/api/admin/departments/permissions/', {
      method: 'GET',
    });
  }

  // Get user permissions
  async getUserPermissions(userId: number) {
    return this.apiRequest(`/api/admin/departments/user-permissions/${userId}/`, {
      method: 'GET',
    });
  }

  // Save user permissions
  async saveUserPermissions(userId: number, permissions: any[]) {
    return this.apiRequest(`/api/admin/departments/user-permissions/${userId}/save/`, {
      method: 'POST',
      body: JSON.stringify({ permissions }),
    });
  }
}

const apiClient = new ApiClient();
export default apiClient;
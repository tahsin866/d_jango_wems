/**
 * Simple API Client for WEMS System
 */

class ApiClient {
  constructor() {
    this.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    this.timeout = 30000
    this.accessToken = localStorage.getItem('access_token')
  }

  async makeRequest(url, options = {}) {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), this.timeout)

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': this.accessToken ? `Bearer ${this.accessToken}` : '',
          ...(options.headers || {})
        }
      })
      clearTimeout(timeoutId)
      return response
    } catch (error) {
      clearTimeout(timeoutId)
      throw error
    }
  }

  async apiRequest(endpoint, options = {}) {
    try {
      const url = `${this.baseURL}${endpoint}`
      const response = await this.makeRequest(url, options)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `HTTP ${response.status}`)
      }

      const data = await response.json()
      return {
        data,
        status_code: response.status
      }
    } catch (error) {
      return {
        error: error && error.message ? error.message : 'Unknown error occurred',
        status_code: 500
      }
    }
  }

  async getDepartments() {
    return this.apiRequest('/api/admin/departments/', { method: 'GET' })
  }

  async getUserTypes() {
    return this.apiRequest('/api/admin/departments/user-types/', { method: 'GET' })
  }

  async getModules() {
    return this.apiRequest('/api/admin/departments/modules/', { method: 'GET' })
  }

  async getModulesByDepartment(departmentId) {
    return this.apiRequest(`/api/admin/departments/modules/${departmentId}/`, { method: 'GET' })
  }

  async getMenus() {
    return this.apiRequest('/api/admin/departments/menus/', { method: 'GET' })
  }

  async getMenusByModule(moduleId) {
    return this.apiRequest(`/api/admin/departments/menus/${moduleId}/`, { method: 'GET' })
  }

  async getPermissions() {
    return this.apiRequest('/api/admin/departments/permissions/', { method: 'GET' })
  }

  async getUserPermissions(userId) {
    return this.apiRequest(`/api/admin/departments/user-permissions/${userId}/`, { method: 'GET' })
  }

  async saveUserPermissions(userId, permissions) {
    return this.apiRequest(`/api/admin/departments/user-permissions/${userId}/save/`, {
      method: 'POST',
      body: JSON.stringify({ permissions })
    })
  }
}

const apiClient = new ApiClient()
export default apiClient

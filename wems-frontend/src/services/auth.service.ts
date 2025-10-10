import { ref, computed } from 'vue'
import apiClient from './api-client'
import axios from 'axios'

// User interface
export interface User {
  id: number
  email: string
  phone?: string
  name: string
  user_type: string
  user_type_id: number
  admin_category?: string
  admin_category_id?: number
  status: string
  department_id?: number
  permissions?: string[]
  profile_image?: string
}

// Auth state interface
export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

// Central authentication service
class AuthService {
  // Reactive state
  private state = ref<AuthState>({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
    isLoading: true, // Start with loading state during initialization
    error: null
  })

  // Computed properties
  user = computed(() => this.state.value.user)
  token = computed(() => this.state.value.token)
  isAuthenticated = computed(() => this.state.value.isAuthenticated)
  isLoading = computed(() => this.state.value.isLoading)
  error = computed(() => this.state.value.error)

  // Check if user is admin type
  get isAdmin(): boolean {
    const adminTypes = ['Master Admin', 'Super Admin', 'Board Admin', 'Admin', 'Accounts Head', 'Department Head', 'Manager']
    return adminTypes.includes(this.user.value?.user_type || '')
  }

  // Get user department info
  get userDepartment(): { id: number; name: string } | null {
    if (!this.user.value?.department_id) return null
    return {
      id: this.user.value.department_id,
      name: this.getDepartmentName(this.user.value.department_id)
    }
  }

  // Initialize auth service
  async initialize(): Promise<void> {
    const token = this.state.value.token
    if (token) {
      this.state.value.isLoading = true
      try {
        await this.validateToken(token)
        console.log('✅ Auth service initialized successfully')
      } catch (error) {
        console.error('Token validation failed:', error)
        await this.logout()
      } finally {
        this.state.value.isLoading = false
      }
    } else {
      console.log('🔓 No token found, user not authenticated')
      this.state.value.isAuthenticated = false
      this.state.value.isLoading = false
    }
  }

  // Login with email/phone and password
  async login(identifier: string, password: string): Promise<{ success: boolean; error?: string }> {
    this.state.value.isLoading = true
    this.state.value.error = null

    try {
      const response = await axios.post('http://localhost:8000/api/auth/login/', {
        identifier,
        password
      })

      const { user, token } = response.data

      // Update state
      this.state.value.user = user
      this.state.value.token = token
      this.state.value.isAuthenticated = true

      // Store in localStorage for sidebar and routing
      localStorage.setItem('token', token)
      localStorage.setItem('user_id', user.id.toString())
      localStorage.setItem('user_type', user.user_type)
      localStorage.setItem('department_id', user.department_id?.toString() || '')
      localStorage.setItem('is_master_admin', (user as any).is_master_admin?.toString() || 'false')
      localStorage.setItem('department_name', user.department_name || '')

      return { success: true }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Login failed'
      this.state.value.error = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      this.state.value.isLoading = false
    }
  }

  // Register new user
  async register(userData: any): Promise<{ success: boolean; error?: string }> {
    this.state.value.isLoading = true
    this.state.value.error = null

    try {
      const response = await axios.post('http://localhost:8000/api/auth/register/', userData)
      const { user, token } = response.data

      // Update state
      this.state.value.user = user
      this.state.value.token = token
      this.state.value.isAuthenticated = true

      // Store in localStorage
      localStorage.setItem('token', token)
      localStorage.setItem('user_id', user.id.toString())
      localStorage.setItem('user_type', user.user_type)

      return { success: true }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Registration failed'
      this.state.value.error = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      this.state.value.isLoading = false
    }
  }

  // Logout user
  async logout(): Promise<void> {
    try {
      // Call logout endpoint if available
      if (this.state.value.token) {
        await axios.post('http://localhost:8000/api/auth/logout/', {}, {
          headers: { 'Authorization': `Bearer ${this.state.value.token}` }
        })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear state
      this.state.value.user = null
      this.state.value.token = null
      this.state.value.isAuthenticated = false
      this.state.value.error = null

      // Clear localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('user_type')
      localStorage.removeItem('department_id')
      localStorage.removeItem('permissions')
    }
  }

  // Validate token with backend
  async validateToken(token: string): Promise<User | null> {
    try {
      const response = await axios.get('http://localhost:8000/api/auth/validate/', {
        headers: { 'Authorization': `Bearer ${token}` }
      })

      const user = response.data.user
      this.state.value.user = user
      this.state.value.isAuthenticated = true
      this.state.value.error = null

      // Update localStorage with fresh data
      localStorage.setItem('user_id', user.id.toString())
      localStorage.setItem('user_type', user.user_type)
      localStorage.setItem('department_id', user.department_id?.toString() || '')

      console.log(`✅ Token validated successfully for user: ${user.user_type}`)
      return user
    } catch (error) {
      console.error('❌ Token validation failed:', error)
      this.state.value.isAuthenticated = false
      this.state.value.user = null
      throw new Error('Invalid token')
    }
  }

  // Refresh user data
  async refreshUserData(): Promise<void> {
    if (!this.state.value.token) return

    try {
      await this.validateToken(this.state.value.token)
    } catch (error) {
      await this.logout()
    }
  }

  // Check if user has permission
  hasPermission(permission: string): boolean {
    if (!this.user.value) return false

    // Admin users have all permissions
    if (this.isAdmin) return true

    const permissions = this.user.value.permissions || []
    return permissions.some(p => p.includes(permission))
  }

  // Get dashboard route based on user type and department
  getDashboardRoute(): string {
    const user = this.user.value
    if (!user) return '/signin'

    // Master Admin routing - check if user is Master Admin
    if (user.user_type === 'Master Admin' || (user as any).is_master_admin) {
      return '/admin/dashboard'
    }

    // Other admin types also go to admin dashboard
    if (this.isAdmin) {
      return '/admin/dashboard'
    }

    // Department-based routing for other users (madrasha, etc.)
    if (user.department_id) {
      return `/admin/department/${user.department_id}/dashboard`
    }

    // Default user dashboard
    return '/user/dashboard'
  }

  // Get department name from ID
  private getDepartmentName(departmentId: number): string {
    const departmentMap: Record<number, string> = {
      1: 'একাউন্টস',
      2: 'প্রকাশনা',
      3: 'তালিম তারবিয়াত',
      4: 'পরীক্ষাবিভাগ',
      5: 'সনদ শাখা',
      6: 'রেজিস্ট্রেশন',
      7: 'প্রশাসন',
      8: 'প্রশিক্ষণ'
    }
    return departmentMap[departmentId] || 'অজানা বিভাগ'
  }

  // Clear error
  clearError(): void {
    this.state.value.error = null
  }
}

// Create singleton instance
export const authService = new AuthService()

// Export composable for Vue components
export function useAuth() {
  return {
    user: authService.user,
    token: authService.token,
    isAuthenticated: authService.isAuthenticated,
    isLoading: authService.isLoading,
    error: authService.error,
    isAdmin: authService.isAdmin,
    userDepartment: authService.userDepartment,
    login: authService.login.bind(authService),
    logout: authService.logout.bind(authService),
    register: authService.register.bind(authService),
    refreshUserData: authService.refreshUserData.bind(authService),
    hasPermission: authService.hasPermission.bind(authService),
    getDashboardRoute: authService.getDashboardRoute.bind(authService),
    clearError: authService.clearError.bind(authService)
  }
}
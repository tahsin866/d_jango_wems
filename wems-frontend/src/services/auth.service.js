import { ref, computed } from 'vue'
import axios from 'axios'

class AuthService {
  state = ref({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
    isLoading: true,
    error: null
  })

  user = computed(() => this.state.value.user)
  token = computed(() => this.state.value.token)
  isAuthenticated = computed(() => this.state.value.isAuthenticated)
  isLoading = computed(() => this.state.value.isLoading)
  error = computed(() => this.state.value.error)

  get isAdmin() {
    const adminTypes = [
      'Master Admin', 'Super Admin', 'Board Admin', 'Admin',
      'Accounts Head', 'Department Head', 'Manager'
    ]
    return adminTypes.includes(this.user.value?.user_type || '')
  }

  get userDepartment() {
    if (!this.user.value?.department_id) return null
    return {
      id: this.user.value.department_id,
      name: this.getDepartmentName(this.user.value.department_id)
    }
  }

  async initialize() {
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

  async login(identifier, password) {
    this.state.value.isLoading = true
    this.state.value.error = null
    try {
      const response = await axios.post('http://localhost:8000/api/auth/login/', {
        identifier,
        password
      })
      const { user, token } = response.data
      this.state.value.user = user
      this.state.value.token = token
      this.state.value.isAuthenticated = true
      localStorage.setItem('token', token)
      localStorage.setItem('user_id', user.id.toString())
      localStorage.setItem('user_type', user.user_type)
      localStorage.setItem('department_id', user.department_id?.toString() || '')
      localStorage.setItem('is_master_admin', user.is_master_admin?.toString() || 'false')
      localStorage.setItem('department_name', user.department_name || '')
      return { success: true }
    } catch (error) {
      const errorMessage = error?.response?.data?.error || 'Login failed'
      this.state.value.error = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      this.state.value.isLoading = false
    }
  }

  async register(userData) {
    this.state.value.isLoading = true
    this.state.value.error = null
    try {
      const response = await axios.post('http://localhost:8000/api/auth/register/', userData)
      const { user, token } = response.data
      this.state.value.user = user
      this.state.value.token = token
      this.state.value.isAuthenticated = true
      localStorage.setItem('token', token)
      localStorage.setItem('user_id', user.id.toString())
      localStorage.setItem('user_type', user.user_type)
      return { success: true }
    } catch (error) {
      const errorMessage = error?.response?.data?.error || 'Registration failed'
      this.state.value.error = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      this.state.value.isLoading = false
    }
  }

  async logout() {
    try {
      if (this.state.value.token) {
        await axios.post('http://localhost:8000/api/auth/logout/', {}, {
          headers: { 'Authorization': `Bearer ${this.state.value.token}` }
        })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      this.state.value.user = null
      this.state.value.token = null
      this.state.value.isAuthenticated = false
      this.state.value.error = null
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('user_type')
      localStorage.removeItem('department_id')
      localStorage.removeItem('permissions')
    }
  }

  async validateToken(token) {
    try {
      const response = await axios.get('http://localhost:8000/api/auth/validate/', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const user = response.data.user
      this.state.value.user = user
      this.state.value.isAuthenticated = true
      this.state.value.error = null
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

  async refreshUserData() {
    if (!this.state.value.token) return
    try {
      await this.validateToken(this.state.value.token)
    } catch  {
      await this.logout()
    }
  }

  hasPermission(permission) {
    if (!this.user.value) return false
    if (this.isAdmin) return true
    const permissions = this.user.value.permissions || []
    return permissions.some(p => p.includes(permission))
  }

  getDashboardRoute() {
    const user = this.user.value
    if (!user) return '/signin'
    if (user.user_type === 'Master Admin' || user.is_master_admin) {
      return '/admin/dashboard'
    }
    if (this.isAdmin) {
      return '/admin/dashboard'
    }
    if (user.department_id) {
      return `/admin/department/${user.department_id}/dashboard`
    }
    return '/user/dashboard'
  }

  getDepartmentName(departmentId) {
    const departmentMap = {
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

  clearError() {
    this.state.value.error = null
  }
}

// Create singleton instance
export const authService = new AuthService()

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

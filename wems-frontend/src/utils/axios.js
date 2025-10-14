import axios from 'axios'

// Configure axios defaults
axios.defaults.baseURL = 'http://127.0.0.1:8000'  // Django Docker container port
axios.defaults.withCredentials = true
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Function to get CSRF token from cookie
function getCsrfToken() {
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Add request interceptor for JWT token and CSRF
axios.interceptors.request.use(
  (config) => {
    // Add JWT token to requests
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
      console.log('🔑 Token added to request:', token.substring(0, 20) + '...')
    } else {
      console.warn('⚠️ No token found in localStorage')
    }

    config.withCredentials = true // যদি session cookie লাগে

    // Add CSRF token for POST, PUT, DELETE requests
    if (['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase() || '')) {
      const csrfToken = getCsrfToken()
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
      }
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Enhanced response interceptor with route validation handling
axios.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle layout access violations from backend
    if (error.response?.status === 403 && error.response?.data?.redirect_to) {
      const redirectTo = error.response.data.redirect_to

      // Redirect using router if available
      if (typeof window !== 'undefined') {
        window.location.href = redirectTo
      }
    }

    // Handle authentication errors more carefully
    if (error.response?.status === 401) {
      // Only auto-logout for certain endpoints, not for form submissions
      const isAuthEndpoint = error.config?.url?.includes('/auth/') ||
                            error.config?.url?.includes('/users/')

      if (isAuthEndpoint) {
        console.log('Authentication failed for auth endpoint, logging out')
        localStorage.removeItem('token')
        localStorage.removeItem('user_type')
        localStorage.removeItem('user_id')

        if (typeof window !== 'undefined' && !window.location.pathname.includes('/signin')) {
          window.location.href = '/signin'
        }
      } else {
        // For other endpoints, just log the error without auto-logout
        console.warn('401 error on non-auth endpoint:', error.config?.url)
      }
    }

    return Promise.reject(error)
  }
)

export default axios

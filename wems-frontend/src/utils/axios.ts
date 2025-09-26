import axios from 'axios'

// Configure axios defaults
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Function to get CSRF token from cookie
function getCsrfToken() {
  const name = 'csrftoken'
  let cookieValue = null
  // Debug: log cookies for CSRF troubleshooting
  console.log('[Axios Debug] document.cookie:', document.cookie)
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
    // Debug: log token value before request
    console.log('[Axios Debug] token from localStorage:', token)
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
      // Debug: log Authorization header value
      console.log('[Axios Debug] Authorization header:', config.headers['Authorization'])
    }

    config.withCredentials = true // যদি session cookie লাগে

    // Add CSRF token for POST, PUT, DELETE requests
    if (['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase() || '')) {
      const csrfToken = getCsrfToken()
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
      }
    }

    console.log('Axios request:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Enhanced response interceptor with route validation handling
axios.interceptors.response.use(
  (response) => {
    console.log('Axios response:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('Axios error:', error.response?.status, error.config?.url, error.response?.data)

    // Handle layout access violations from backend
    if (error.response?.status === 403 && error.response?.data?.redirect_to) {
      const redirectTo = error.response.data.redirect_to
      console.log(`🚫 Backend layout violation detected, redirecting to: ${redirectTo}`)

      // Redirect using router if available
      if (typeof window !== 'undefined') {
        window.location.href = redirectTo
      }
    }

    // Handle authentication errors
    if (error.response?.status === 401) {
      console.log('🔒 Authentication required, clearing token and redirecting to signin')
      localStorage.removeItem('token')
      localStorage.removeItem('user_type')
      localStorage.removeItem('user_id')

      if (typeof window !== 'undefined' && !window.location.pathname.includes('/signin')) {
        window.location.href = '/signin'
      }
    }

    return Promise.reject(error)
  }
)

export default axios

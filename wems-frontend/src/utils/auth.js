import axios from './axios'
import { setCurrentUserId } from '@/stores/userProfile'

// Admin types for easier checking
const ADMIN_TYPES = [
  'Master Admin',
  'Director',
  'System Admin',
  'Accounts Head',
  'Publication Head',
  'Talim & Tarbiyat Head',
  'Certificate Section Head',
  'Chief Director',
  'Training Section Head'
]

// Define route access control
export const ROUTE_ACCESS = {
  ADMIN_ONLY: [
    'AdminDashboard',
    'UserSetup',
    'MarhalaSetup',
    'SubjectSetup'
  ],
  USER_ONLY: [
    'Dashboard',
    'MarkazList',
    'MarkazApply',
    'MarkazChange',
    'MarkazChangeForm',
    'MarkazSetup',
    'Confirmation',
    'MarhalaChange',
    'StudentRegistrationOverview',
    'RegistrationList',
    'OldStudentList',
    'VerifyOldStudents',
    'OldStudentReg',
    'RegistrationCard',
    'RegistrationTable',
    'Restore',
    'Payment',
    'SubjectList'
  ],
  PUBLIC: [
    'Welcome',
    'Signin',
    'Signup',
    '404 Error',
    'Unauthorized',
    'NotFound',
    'MadrashaCheck'
  ]
}

// Enhanced JWT token parser
export function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(function (c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        })
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch {
    return null
  }
}

// Enhanced token expiry check
export function isTokenExpired(token) {
  if (!token || token.split('.').length !== 3) return false
  if (!token || token.split('.').length !== 3) return false
  const decoded = parseJwt(token)
  if (!decoded) return true
  const currentTime = Date.now() / 1000
  return decoded.exp < currentTime
}

// Get user type from token
export function getUserTypeFromToken(token) {
  const decoded = parseJwt(token)
  return decoded?.user_type || null
}

// Get user permissions from token
export function getUserPermissions(token) {
  const decoded = parseJwt(token)
  return decoded?.permissions || []
}

// Check if route requires authentication
export function requiresAuth(routeName) {
  const name = String(routeName || '')
  return !ROUTE_ACCESS.PUBLIC.includes(name)
}

// Check if user is admin type
export function isAdminType(userType) {
  return ADMIN_TYPES.includes(userType)
}

// Enhanced route access validation - Check if admin accessing user routes
export function isAdminAccessingUserRoute(routeName, userType) {
  const name = String(routeName || '')
  const isUserRoute = ROUTE_ACCESS.USER_ONLY.some(route =>
    name === route || name.includes(route.toLowerCase())
  )
  return isUserRoute && isAdminType(userType)
}

// Enhanced admin route protection
export function isNonAdminAccessingAdminRoute(routeName, userType) {
  const name = String(routeName || '')
  const requiresAdmin = ROUTE_ACCESS.ADMIN_ONLY.some(route =>
    name === route || name.includes(route.toLowerCase()) || name.startsWith(route)
  )
  return requiresAdmin && !isAdminType(userType)
}

// Validate route access with backend
export async function validateRouteAccess(route, token) {
  try {
    const authToken = token || localStorage.getItem('token')
    if (!authToken) return false

    const response = await axios.post('/auth/validate-access/', {
      route,
      token: authToken
    })

    return response.data.valid
  } catch (error) {
    console.error('Route validation error:', error)
    return false
  }
}

// Enhanced logout function
export async function secureLogout() {
  try {
    await axios.post('/auth/logout/')
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    localStorage.removeItem('token')
    localStorage.removeItem('user_type')
    localStorage.removeItem('user_id')
    localStorage.removeItem('permissions')
  }
}

// Call this after successful login
export function handleLoginSuccess(token) {
  localStorage.setItem('token', token)

  const userData = parseJwt(token)
  if (userData?.user_id) {
    localStorage.setItem('user_id', userData.user_id.toString())
    setCurrentUserId(userData.user_id)
  }
}

// Get current user data from token
export function getCurrentUser(token) {
  const authToken = token || localStorage.getItem('token')
  if (!authToken || isTokenExpired(authToken)) return null

  return parseJwt(authToken)
}

// Check if user has specific permission
export function hasPermission(permission, token) {
  const user = getCurrentUser(token)
  if (!user) return false

  if (isAdminType(user.user_type)) return true

  const permissions = getUserPermissions(token || localStorage.getItem('token') || '')
  return permissions.some(p => p.includes(permission))
}

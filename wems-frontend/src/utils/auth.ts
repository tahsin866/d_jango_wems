import axios from './axios'
import { setCurrentUserId } from '@/stores/userProfile'

// Authentication utility functions
export interface UserRole {
  MASTER_ADMIN: 'Master Admin';
  SUPER_ADMIN: 'Super Admin';
  BOARD_ADMIN: 'Board Admin';
  ADMIN: 'Admin';
  MADRASA: 'Madrasah';
  MARKAZ: 'Markaz';
  NEGARAN: 'Negaran';
  MUMTAHIN: 'Mumtahin';
  ZONAL: 'Zonal';
  STUDENT: 'Student';
}

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
];

// Define route access control
export const ROUTE_ACCESS = {
  // Admin-only routes (admin layout)
  ADMIN_ONLY: [
    'AdminDashboard',
    'UserSetup',
    'MarhalaSetup',
    'SubjectSetup'
  ],

  // User-only routes (user layout)
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

  // Public routes (no authentication required)
  PUBLIC: [
    'Welcome',
    'Signin',
    'Signup',
    '404 Error',
    'Unauthorized',
    'NotFound',
    'MadrashaCheck'
  ]
};

// Enhanced JWT token parser
export function parseJwt(token: string) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(function (c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

// Enhanced token expiry check
export function isTokenExpired(token: string): boolean {
  // If token is not JWT, always return false (never expired)
  if (!token || token.split('.').length !== 3) return false;
  // If token is not JWT, treat as never expired
  if (!token || token.split('.').length !== 3) return false;
  const decoded = parseJwt(token);
  if (!decoded) return true;
  const currentTime = Date.now() / 1000;
  return decoded.exp < currentTime;
}

// Get user type from token
export function getUserTypeFromToken(token: string): string | null {
  const decoded = parseJwt(token);
  return decoded?.user_type || null;
}

// Get user permissions from token
export function getUserPermissions(token: string): string[] {
  const decoded = parseJwt(token);
  return decoded?.permissions || [];
}

// Check if route requires authentication
export function requiresAuth(routeName: string | symbol | null | undefined): boolean {
  const name = String(routeName || '');
  return !ROUTE_ACCESS.PUBLIC.includes(name);
}

// Check if user is admin type
export function isAdminType(userType: string): boolean {
  return ADMIN_TYPES.includes(userType);
}

// Enhanced route access validation - Check if admin accessing user routes
export function isAdminAccessingUserRoute(routeName: string | symbol | null | undefined, userType: string): boolean {
  const name = String(routeName || '');
  const isUserRoute = ROUTE_ACCESS.USER_ONLY.some((route: string) =>
    name === route || name.includes(route.toLowerCase())
  );
  return isUserRoute && isAdminType(userType);
}

// Enhanced admin route protection
export function isNonAdminAccessingAdminRoute(routeName: string | symbol | null | undefined, userType: string): boolean {
  const name = String(routeName || '');
  const requiresAdmin = ROUTE_ACCESS.ADMIN_ONLY.some((route: string) =>
    name === route || name.includes(route.toLowerCase()) || name.startsWith(route)
  );
  return requiresAdmin && !isAdminType(userType);
}

// Validate route access with backend
export async function validateRouteAccess(route: string, token?: string): Promise<boolean> {
  try {
    const authToken = token || localStorage.getItem('token');
    if (!authToken) return false;

    const response = await axios.post('/auth/validate-access/', {
      route,
      token: authToken
    });

    return response.data.valid;
  } catch (error) {
    console.error('Route validation error:', error);
    return false;
  }
}

// Enhanced logout function
export async function secureLogout(): Promise<void> {
  try {
    await axios.post('/auth/logout/');
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    // Clear all auth data
    localStorage.removeItem('token');
    localStorage.removeItem('user_type');
    localStorage.removeItem('user_id');
    localStorage.removeItem('permissions');
  }
}

// Call this after successful login
export function handleLoginSuccess(token: string): void {
  localStorage.setItem('token', token);

  const userData = parseJwt(token);
  if (userData?.user_id) {
    localStorage.setItem('user_id', userData.user_id.toString());
    setCurrentUserId(userData.user_id);
  }
}

// Get current user data from token
export function getCurrentUser(token?: string) {
  const authToken = token || localStorage.getItem('token');
  if (!authToken || isTokenExpired(authToken)) return null;

  return parseJwt(authToken);
}

// Check if user has specific permission
export function hasPermission(permission: string, token?: string): boolean {
  const user = getCurrentUser(token);
  if (!user) return false;

  // Admin users have all permissions
  if (isAdminType(user.user_type)) return true;

  const permissions = getUserPermissions(token || localStorage.getItem('token') || '');
  return permissions.some((p: string) => p.includes(permission));
}

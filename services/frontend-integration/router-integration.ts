/**
 * Router Integration for WEMS Microservices
 * Handles service-based routing for Vue.js frontend
 */

import { RouteRecordRaw } from 'vue-router';

// Service-based route configuration
export interface ServiceRouteConfig {
  service: string;
  endpoint?: string;
  component: () => Promise<any>;
  meta?: Record<string, any>;
}

// Service route mappings
const serviceRoutes: Record<string, ServiceRouteConfig[]> = {
  admin: [
    {
      service: 'auth',
      endpoint: '/admin/dashboard',
      component: () => import('@/views/Pages/Admin/dashboard/AdminDashboard.vue'),
      meta: {
        title: 'অ্যাডমিন ড্যাশবোর্ড',
        requiresAuth: true,
        role: 'admin',
        permissions: ['admin', 'dashboard_access']
      }
    },
    {
      service: 'accounts',
      endpoint: '/api/accounts/vouchers/',
      component: () => import('@/views/Pages/Admin/accounts/VoucherList.vue'),
      meta: {
        title: 'ভাউচার ব্যবস্থাপনা',
        requiresAuth: true,
        role: 'admin',
        permissions: ['admin', 'voucher_manage']
      }
    },
    {
      service: 'accounts',
      endpoint: '/api/accounts/payments/',
      component: () => import('@/views/Pages/Admin/accounts/PaymentList.vue'),
      meta: {
        title: 'পেমেন্ট ব্যবস্থাপনা',
        requiresAuth: true,
        role: 'admin',
        permissions: ['admin', 'payment_manage']
      }
    },
    {
      service: 'administration',
      endpoint: '/api/administration/users/',
      component: () => import('@/views/Pages/Admin/users/UserManagement.vue'),
      meta: {
        title: 'ব্যবহারকারী ব্যবস্থাপনা',
        requiresAuth: true,
        role: 'admin',
        permissions: ['admin', 'user_manage']
      }
    },
    {
      service: 'registration',
      endpoint: '/api/registration/overview',
      component: () => import('@/views/Pages/Admin/registration/RegistrationOverview.vue'),
      meta: {
        title: 'নিবন্ধন ওভারভিউ',
        requiresAuth: true,
        role: 'admin',
        permissions: ['admin', 'registration_view']
      }
    },
    {
      service: 'taleem',
      endpoint: '/api/taleem/subjects/',
      component: () => import('@/views/Pages/Admin/taleem/SubjectManagement.vue'),
      meta: {
        title: 'বিষয় ব্যবস্থাপনা',
        requiresAuth: true,
        role: 'admin',
        permissions: ['admin', 'subject_manage']
      }
    },
  ],
  user: [
    {
      service: 'auth',
      endpoint: '/user/dashboard',
      component: () => import('@/views/Ecommerce.vue'),
      meta: {
        title: 'ইউজার ড্যাশবোর্ড',
        requiresAuth: true,
        role: 'user',
        permissions: ['user', 'dashboard_access']
      }
    },
    {
      service: 'registration',
      endpoint: '/api/registration/overview',
      component: () => import('@/views/Pages/registraion/registrationOverview.vue'),
      meta: {
        title: 'ছাত্র নিবন্ধন ওভারভিউ',
        requiresAuth: true,
        role: 'user',
        permissions: ['user', 'registration_view']
      }
    },
    {
      service: 'registration',
      endpoint: '/api/registration/students/',
      component: () => import('@/views/Pages/registraion/registrationList.vue'),
      meta: {
        title: 'নিবন্ধন তালিকা',
        requiresAuth: true,
        role: 'user',
        permissions: ['user', 'registration_manage']
      }
    },
    {
      service: 'registration',
      endpoint: '/api/registration/old-students/',
      component: () => import('@/views/Pages/registraion/oldStudentList.vue'),
      meta: {
        title: 'বিগত ছাত্র তালিকা',
        requiresAuth: true,
        role: 'user',
        permissions: ['user', 'old_student_manage']
      }
    },
    {
      service: 'taleem',
      endpoint: '/api/taleem/subjects/',
      component: () => import('@/views/Pages/taleem/SubjectList.vue'),
      meta: {
        title: 'বিষয় তালিকা',
        requiresAuth: true,
        role: 'user',
        permissions: ['user', 'subject_view']
      }
    },
  ],
};

// Convert service routes to Vue Router format
export function generateServiceRoutes(layout: 'admin' | 'user'): RouteRecordRaw[] {
  const routes = serviceRoutes[layout] || [];

  return routes.map((routeConfig, index) => ({
    path: routeConfig.endpoint || `/service/${index}`,
    name: `${layout}-${routeConfig.service}-${index}`,
    component: routeConfig.component,
    meta: {
      ...routeConfig.meta,
      service: routeConfig.service,
      serviceEndpoint: routeConfig.endpoint,
    },
  }));
}

// Service-based navigation guard
export function createServiceNavigationGuard(apiClient: any) {
  return async (to: any, from: any, next: any) => {
    const userPermissions = await getUserPermissions(apiClient);

    // Check if user is authenticated
    if (to.meta.requiresAuth && !apiClient.accessToken) {
      next('/signin');
      return;
    }

    // Check role-based access
    if (to.meta.role) {
      const userType = localStorage.getItem('user_type');
      if (to.meta.role === 'admin' && !isAdminType(userType)) {
        next('/user/dashboard');
        return;
      }
      if (to.meta.role === 'user' && isAdminType(userType)) {
        next('/admin/dashboard');
        return;
      }
    }

    // Check permission-based access
    if (to.meta.permissions) {
      const hasPermission = to.meta.permissions.some((permission: string) =>
        userPermissions.includes(permission) || userPermissions.includes('admin')
      );

      if (!hasPermission) {
        next('/unauthorized');
        return;
      }
    }

    // Check service availability
    if (to.meta.service) {
      try {
        const serviceURL = apiClient.getServiceURL(to.meta.service);
        const response = await fetch(`${serviceURL}/health`);
        if (!response.ok) {
          console.warn(`Service ${to.meta.service} is not available`);
          // You might want to show a service unavailable page
        }
      } catch (error) {
        console.error(`Service ${to.meta.service} health check failed:`, error);
        // Handle service unavailable scenario
      }
    }

    next();
  };
}

// Helper functions
async function getUserPermissions(apiClient: any): Promise<string[]> {
  try {
    const user = await apiClient.getCurrentUser();
    return user.permissions || [];
  } catch (error) {
    console.error('Failed to get user permissions:', error);
    return [];
  }
}

function isAdminType(userType: string | null): boolean {
  const adminTypes = ['Master Admin', 'Super Admin', 'Board Admin', 'Admin'];
  return adminTypes.includes(userType || '');
}

// Service status monitoring
export class ServiceMonitor {
  private apiClient: any;
  private serviceStatus: Record<string, boolean> = {};

  constructor(apiClient: any) {
    this.apiClient = apiClient;
    this.startMonitoring();
  }

  private async startMonitoring() {
    // Check service health every 30 seconds
    setInterval(async () => {
      await this.checkAllServices();
    }, 30000);

    // Initial check
    await this.checkAllServices();
  }

  private async checkAllServices() {
    const services = ['auth', 'accounts', 'registration', 'taleem', 'administration'];

    for (const service of services) {
      try {
        const serviceURL = this.apiClient.getServiceURL(service);
        const response = await fetch(`${serviceURL}/health`, {
          method: 'GET',
          timeout: 5000,
        });
        this.serviceStatus[service] = response.ok;
      } catch (error) {
        this.serviceStatus[service] = false;
        console.warn(`Service ${service} is unavailable:`, error);
      }
    }
  }

  getServiceStatus(service: string): boolean {
    return this.serviceStatus[service] || false;
  }

  getAllServiceStatus(): Record<string, boolean> {
    return { ...this.serviceStatus };
  }
}

// Service-based component loader
export function createServiceComponentLoader(service: string) {
  return async () => {
    try {
      // Try to load component from the specific service
      const module = await import(`@/views/Services/${service}/index.vue`);
      return module.default;
    } catch (error) {
      console.warn(`Failed to load service component for ${service}, using fallback`);
      // Load a generic service component fallback
      const fallback = await import('@/views/Services/GenericService.vue');
      return fallback.default;
    }
  };
}

// Export utilities for route management
export const routeUtils = {
  generateServiceRoutes,
  createServiceNavigationGuard,
  createServiceComponentLoader,
  ServiceMonitor,
  isAdminType,
  getUserPermissions,
};

export default routeUtils;
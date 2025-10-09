/**
 * Unified API Client for WEMS Microservices
 * Handles authentication and routing to different backend services
 */

interface ServiceConfig {
  baseURL: string;
  timeout: number;
}

interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

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
  message?: string;
  status_code: number;
}

class ApiClient {
  private baseURL: string;
  private authBaseURL: string;
  private timeout: number;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private refreshPromise: Promise<void> | null = null;

  constructor() {
    this.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:80';
    this.authBaseURL = process.env.VUE_APP_AUTH_BASE_URL || 'http://localhost:8000';
    this.timeout = 30000; // 30 seconds

    // Initialize tokens from localStorage
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token') || this.getCookie('refresh_token');

    // Set up automatic token refresh
    this.setupTokenRefresh();
  }

  private getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop()?.split(';').shift() || null;
    }
    return null;
  }

  private setCookie(name: string, value: string, expiresIn: number): void {
    const date = new Date();
    date.setTime(date.getTime() + (expiresIn * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value};${expires};path=/;SameSite=Lax`;
  }

  private deleteCookie(name: string): void {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;SameSite=Lax`;
  }

  private async setupTokenRefresh(): Promise<void> {
    // Set up periodic token refresh
    setInterval(async () => {
      if (this.accessToken) {
        try {
          await this.refreshAccessToken();
        } catch (error) {
          console.error('Auto token refresh failed:', error);
          this.logout();
        }
      }
    }, 15 * 60 * 1000); // Refresh every 15 minutes
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
          ...this.getAuthHeaders(),
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

  private getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {};
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }
    return headers;
  }

  private async refreshAccessToken(): Promise<void> {
    // Prevent multiple refresh attempts
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    this.refreshPromise = this.doRefreshAccessToken();
    return this.refreshPromise;
  }

  private async doRefreshAccessToken(): Promise<void> {
    try {
      const response = await this.makeRequest(`${this.authBaseURL}/auth/refresh/`, {
        method: 'POST',
        body: JSON.stringify({
          refresh_token: this.refreshToken,
        }),
      });

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      const data = await response.json();
      this.accessToken = data.access_token;
      localStorage.setItem('access_token', this.accessToken);

      if (data.refresh_token) {
        this.refreshToken = data.refresh_token;
        localStorage.setItem('refresh_token', this.refreshToken);
        this.setCookie('refresh_token', this.refreshToken, data.expires_in || 7 * 24 * 60 * 60);
      }
    } finally {
      this.refreshPromise = null;
    }
  }

  private async handleRequestError(response: Response): Promise<never> {
    if (response.status === 401) {
      // Try to refresh token
      try {
        await this.refreshAccessToken();
        throw new Error('Token refreshed, please retry the request');
      } catch {
        // Refresh failed, logout user
        this.logout();
        throw new Error('Session expired, please login again');
      }
    }

    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || errorData.message || `HTTP ${response.status}`);
  }

  // Authentication methods
  async login(emailOrPhone: string, password: string, rememberMe: boolean = false): Promise<{ user: User; tokens: AuthTokens }> {
    const response = await this.makeRequest(`${this.authBaseURL}/auth/login/`, {
      method: 'POST',
      body: JSON.stringify({
        email_or_phone: emailOrPhone,
        password,
        remember_me: rememberMe,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Login failed');
    }

    const data = await response.json();

    // Store tokens
    this.accessToken = data.access_token;
    this.refreshToken = data.refresh_token;
    localStorage.setItem('access_token', this.accessToken);
    localStorage.setItem('refresh_token', this.refreshToken);
    localStorage.setItem('user_data', JSON.stringify(data.user));

    if (rememberMe) {
      this.setCookie('refresh_token', this.refreshToken, data.expires_in);
    }

    return {
      user: data.user,
      tokens: {
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
        expiresIn: data.expires_in,
      },
    };
  }

  async logout(): Promise<void> {
    try {
      if (this.accessToken) {
        await this.makeRequest(`${this.authBaseURL}/auth/logout/`, {
          method: 'POST',
        });
      }
    } catch (error) {
      console.error('Logout request failed:', error);
    } finally {
      // Clear local storage and cookies
      this.accessToken = null;
      this.refreshToken = null;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_data');
      localStorage.removeItem('user_type');
      localStorage.removeItem('user_id');
      this.deleteCookie('refresh_token');

      // Redirect to login page
      window.location.href = '/signin';
    }
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.makeRequest(`${this.authBaseURL}/auth/profile/`);

    if (!response.ok) {
      throw new Error('Failed to get user profile');
    }

    const data = await response.json();
    return data.user;
  }

  // Generic API request method
  private async apiRequest<T = any>(
    service: string,
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const serviceURL = this.getServiceURL(service);
      const url = `${serviceURL}${endpoint}`;

      let response = await this.makeRequest(url, options);

      // Handle 401 unauthorized with token refresh
      if (response.status === 401 && this.refreshToken) {
        try {
          await this.refreshAccessToken();
          // Retry the request with new token
          response = await this.makeRequest(url, {
            ...options,
            headers: {
              ...options.headers,
              ...this.getAuthHeaders(),
            },
          });
        } catch (refreshError) {
          // Refresh failed, logout user
          this.logout();
          throw new Error('Session expired, please login again');
        }
      }

      if (!response.ok) {
        await this.handleRequestError(response);
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

  private getServiceURL(service: string): string {
    const servicePorts: Record<string, number> = {
      auth: 8000,
      accounts: 8001,
      taleem: 8002,
      sanad: 8003,
      registration: 8004,
      administration: 8005,
      training: 8006,
      publication: 8007,
      exam: 8008,
    };

    const port = servicePorts[service];
    if (!port) {
      throw new Error(`Unknown service: ${service}`);
    }

    return service === 'auth' ? this.authBaseURL : `${this.baseURL.replace(':80', `:${port}`)}`;
  }

  // Service-specific API methods
  accounts = {
    // Vouchers
    getVouchers: (params: any = {}) =>
      this.apiRequest('accounts', '/api/accounts/vouchers/', {
        method: 'GET',
      }),

    createVoucher: (voucherData: any) =>
      this.apiRequest('accounts', '/api/accounts/vouchers/', {
        method: 'POST',
        body: JSON.stringify(voucherData),
      }),

    updateVoucher: (id: number, voucherData: any) =>
      this.apiRequest('accounts', `/api/accounts/vouchers/${id}`, {
        method: 'PUT',
        body: JSON.stringify(voucherData),
      }),

    deleteVoucher: (id: number) =>
      this.apiRequest('accounts', `/api/accounts/vouchers/${id}`, {
        method: 'DELETE',
      }),

    // Payments
    getPayments: (params: any = {}) =>
      this.apiRequest('accounts', '/api/accounts/payments/', {
        method: 'GET',
      }),

    createPayment: (paymentData: any) =>
      this.apiRequest('accounts', '/api/accounts/payments/', {
        method: 'POST',
        body: JSON.stringify(paymentData),
      }),

    // Reports
    getFinancialSummary: (filters: any = {}) =>
      this.apiRequest('accounts', '/api/accounts/reports/summary', {
        method: 'GET',
      }),

    getVoucherReport: (filters: any = {}) =>
      this.apiRequest('accounts', '/api/accounts/reports/vouchers', {
        method: 'GET',
      }),
  };

  registration = {
    // Students
    getStudents: (params: any = {}) =>
      this.apiRequest('registration', '/api/registration/students/', {
        method: 'GET',
      }),

    createStudent: (studentData: any) =>
      this.apiRequest('registration', '/api/registration/students/', {
        method: 'POST',
        body: JSON.stringify(studentData),
      }),

    updateStudent: (id: number, studentData: any) =>
      this.apiRequest('registration', `/api/registration/students/${id}`, {
        method: 'PUT',
        body: JSON.stringify(studentData),
      }),

    getStudent: (id: number) =>
      this.apiRequest('registration', `/api/registration/students/${id}`, {
        method: 'GET',
      }),

    // Old Students
    getOldStudents: (params: any = {}) =>
      this.apiRequest('registration', '/api/registration/old-students/', {
        method: 'GET',
      }),

    createOldStudent: (oldStudentData: any) =>
      this.apiRequest('registration', '/api/registration/old-students/', {
        method: 'POST',
        body: JSON.stringify(oldStudentData),
      }),

    verifyOldStudent: (id: number, verificationData: any) =>
      this.apiRequest('registration', `/api/registration/old-students/${id}/verify`, {
        method: 'POST',
        body: JSON.stringify(verificationData),
      }),

    // Overview and Reports
    getOverview: () =>
      this.apiRequest('registration', '/api/registration/overview', {
        method: 'GET',
      }),

    getStudentListReport: (filters: any = {}) =>
      this.apiRequest('registration', '/api/registration/reports/student-list', {
        method: 'GET',
      }),

    getRegistrationStatistics: (filters: any = {}) =>
      this.apiRequest('registration', '/api/registration/reports/registration-statistics', {
        method: 'GET',
      }),
  };

  // Taleem Tarbiyat Service Methods
  taleem = {
    // Subjects
    getSubjects: (params: any = {}) =>
      this.apiRequest('taleem', '/subjects/', {
        method: 'GET',
      }),

    createSubject: (subjectData: any) =>
      this.apiRequest('taleem', '/subjects/', {
        method: 'POST',
        body: JSON.stringify(subjectData),
      }),

    updateSubject: (id: number, subjectData: any) =>
      this.apiRequest('taleem', `/subjects/${id}`, {
        method: 'PUT',
        body: JSON.stringify(subjectData),
      }),

    // Class Schedules
    getClassSchedules: (params: any = {}) =>
      this.apiRequest('taleem', '/class-schedules/', {
        method: 'GET',
      }),

    createClassSchedule: (scheduleData: any) =>
      this.apiRequest('taleem', '/class-schedules/', {
        method: 'POST',
        body: JSON.stringify(scheduleData),
      }),

    // Student Progress
    getStudentProgress: (studentId: number) =>
      this.apiRequest('taleem', `/student-progress/${studentId}`, {
        method: 'GET',
      }),

    updateStudentProgress: (studentId: number, progressData: any) =>
      this.apiRequest('taleem', `/student-progress/${studentId}`, {
        method: 'PUT',
        body: JSON.stringify(progressData),
      }),

    // Teacher Assignments
    getTeacherAssignments: (teacherId: number) =>
      this.apiRequest('taleem', `/teacher-assignments/${teacherId}`, {
        method: 'GET',
      }),

    assignTeacher: (assignmentData: any) =>
      this.apiRequest('taleem', '/teacher-assignments/', {
        method: 'POST',
        body: JSON.stringify(assignmentData),
      }),

    // Statistics
    getStatistics: (madrashaId?: number) =>
      this.apiRequest('taleem', '/statistics', {
        method: 'GET',
      }),
  };

  // Sanad (Certificate) Service Methods
  sanad = {
    // Certificates
    getCertificates: (params: any = {}) =>
      this.apiRequest('sanad', '/certificates/', {
        method: 'GET',
      }),

    createCertificate: (certificateData: any) =>
      this.apiRequest('sanad', '/certificates/', {
        method: 'POST',
        body: JSON.stringify(certificateData),
      }),

    verifyCertificate: (certificateNumber: string) =>
      this.apiRequest('sanad', `/certificates/verify/${certificateNumber}`, {
        method: 'GET',
      }),

    generateCertificate: (studentId: number, templateData: any) =>
      this.apiRequest('sanad', '/certificates/generate', {
        method: 'POST',
        body: JSON.stringify({ student_id: studentId, ...templateData }),
      }),

    // Certificate Templates
    getTemplates: () =>
      this.apiRequest('sanad', '/templates/', {
        method: 'GET',
      }),

    createTemplate: (templateData: any) =>
      this.apiRequest('sanad', '/templates/', {
        method: 'POST',
        body: JSON.stringify(templateData),
      }),

    // Batch Operations
    batchGenerate: (batchData: any) =>
      this.apiRequest('sanad', '/certificates/batch-generate', {
        method: 'POST',
        body: JSON.stringify(batchData),
      }),
  };

  // Administration Service Methods
  administration = {
    // System Settings
    getSettings: (category?: string) =>
      this.apiRequest('admin', '/settings', {
        method: 'GET',
      }),

    updateSetting: (settingId: number, settingData: any) =>
      this.apiRequest('admin', `/settings/${settingId}`, {
        method: 'PUT',
        body: JSON.stringify(settingData),
      }),

    createSetting: (settingData: any) =>
      this.apiRequest('admin', '/settings', {
        method: 'POST',
        body: JSON.stringify(settingData),
      }),

    // Activity Logs
    getActivityLogs: (params: any = {}) =>
      this.apiRequest('admin', '/activity', {
        method: 'GET',
      }),

    // System Announcements
    getAnnouncements: (params: any = {}) =>
      this.apiRequest('admin', '/announcements', {
        method: 'GET',
      }),

    createAnnouncement: (announcementData: any) =>
      this.apiRequest('admin', '/announcements', {
        method: 'POST',
        body: JSON.stringify(announcementData),
      }),

    updateAnnouncement: (announcementId: number, announcementData: any) =>
      this.apiRequest('admin', `/announcements/${announcementId}`, {
        method: 'PUT',
        body: JSON.stringify(announcementData),
      }),

    // User Permissions
    grantPermission: (permissionData: any) =>
      this.apiRequest('admin', '/permissions', {
        method: 'POST',
        body: JSON.stringify(permissionData),
      }),

    getUserPermissions: (userId?: number) =>
      this.apiRequest('admin', '/permissions', {
        method: 'GET',
      }),

    revokePermission: (permissionId: number) =>
      this.apiRequest('admin', `/permissions/${permissionId}`, {
        method: 'DELETE',
      }),

    // Statistics
    getStatistics: () =>
      this.apiRequest('admin', '/statistics', {
        method: 'GET',
      }),
  };

  // Training Service Methods
  training = {
    // Training Programs
    getPrograms: (params: any = {}) =>
      this.apiRequest('training', '/programs', {
        method: 'GET',
      }),

    createProgram: (programData: any) =>
      this.apiRequest('training', '/programs', {
        method: 'POST',
        body: JSON.stringify(programData),
      }),

    updateProgram: (programId: number, programData: any) =>
      this.apiRequest('training', `/programs/${programId}`, {
        method: 'PUT',
        body: JSON.stringify(programData),
      }),

    // Enrollments
    enrollInProgram: (enrollmentData: any) =>
      this.apiRequest('training', '/enrollments', {
        method: 'POST',
        body: JSON.stringify(enrollmentData),
      }),

    getEnrollments: (params: any = {}) =>
      this.apiRequest('training', '/enrollments', {
        method: 'GET',
      }),

    // Training Materials
    getMaterials: (programId?: number) =>
      this.apiRequest('training', '/materials', {
        method: 'GET',
      }),

    uploadMaterial: (materialId: number, file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      return this.apiRequest('training', `/materials/${materialId}/upload`, {
        method: 'POST',
        body: formData,
        headers: {}, // Let browser set Content-Type for FormData
      });
    },

    // Training Schedules
    getSchedules: (programId?: number) =>
      this.apiRequest('training', '/schedules', {
        method: 'GET',
      }),

    createSchedule: (scheduleData: any) =>
      this.apiRequest('training', '/schedules', {
        method: 'POST',
        body: JSON.stringify(scheduleData),
      }),

    // Certificates
    generateCertificate: (enrollmentId: number) =>
      this.apiRequest('training', `/certificates/generate/${enrollmentId}`, {
        method: 'POST',
      }),

    verifyCertificate: (verificationCode: string) =>
      this.apiRequest('training', `/certificates/verify/${verificationCode}`, {
        method: 'GET',
      }),

    // Statistics
    getStatistics: (madrashaId?: number) =>
      this.apiRequest('training', '/statistics', {
        method: 'GET',
      }),
  };

  // Publication Service Methods
  publication = {
    // Books
    getBooks: (params: any = {}) =>
      this.apiRequest('publication', '/books', {
        method: 'GET',
      }),

    createBook: (bookData: any) =>
      this.apiRequest('publication', '/books', {
        method: 'POST',
        body: JSON.stringify(bookData),
      }),

    uploadBookFile: (bookId: number, file: File, coverImage?: File) => {
      const formData = new FormData();
      formData.append('file', file);
      if (coverImage) {
        formData.append('cover_image', coverImage);
      }
      return this.apiRequest('publication', `/books/${bookId}/upload`, {
        method: 'POST',
        body: formData,
        headers: {},
      });
    },

    // Libraries
    getLibraries: (madrashaId?: number) =>
      this.apiRequest('publication', '/libraries', {
        method: 'GET',
      }),

    createLibrary: (libraryData: any) =>
      this.apiRequest('publication', '/libraries', {
        method: 'POST',
        body: JSON.stringify(libraryData),
      }),

    // Book Issues
    issueBook: (issueData: any) =>
      this.apiRequest('publication', '/issues', {
        method: 'POST',
        body: JSON.stringify(issueData),
      }),

    returnBook: (issueId: number) =>
      this.apiRequest('publication', `/issues/${issueId}/return`, {
        method: 'POST',
      }),

    getBookIssues: (params: any = {}) =>
      this.apiRequest('publication', '/issues', {
        method: 'GET',
      }),

    // Journals
    getJournals: (params: any = {}) =>
      this.apiRequest('publication', '/journals', {
        method: 'GET',
      }),

    createJournal: (journalData: any) =>
      this.apiRequest('publication', '/journals', {
        method: 'POST',
        body: JSON.stringify(journalData),
      }),

    // Research Papers
    getResearchPapers: (params: any = {}) =>
      this.apiRequest('publication', '/research-papers', {
        method: 'GET',
      }),

    createResearchPaper: (paperData: any) =>
      this.apiRequest('publication', '/research-papers', {
        method: 'POST',
        body: JSON.stringify(paperData),
      }),

    // Statistics
    getStatistics: (madrashaId?: number) =>
      this.apiRequest('publication', '/statistics', {
        method: 'GET',
      }),
  };

  // Department Service Methods (Django backend)
  departments = {
    // Get all departments
    getDepartments: (params: any = {}) =>
      this.apiRequest('auth', '/api/admin/departments/', {
        method: 'GET',
      }),

    // Get single department
    getDepartment: (departmentId: number) =>
      this.apiRequest('auth', `/api/admin/departments/${departmentId}`, {
        method: 'GET',
      }),

    // Create new department
    createDepartment: (departmentData: any) =>
      this.apiRequest('auth', '/api/admin/departments/', {
        method: 'POST',
        body: JSON.stringify(departmentData),
      }),

    // Update department
    updateDepartment: (departmentId: number, departmentData: any) =>
      this.apiRequest('auth', `/api/admin/departments/${departmentId}`, {
        method: 'PUT',
        body: JSON.stringify(departmentData),
      }),

    // Delete department (soft delete)
    deleteDepartment: (departmentId: number) =>
      this.apiRequest('auth', `/api/admin/departments/${departmentId}`, {
        method: 'DELETE',
      }),

    // Get department statistics
    getDepartmentStatistics: () =>
      this.apiRequest('auth', '/api/admin/departments/statistics/', {
        method: 'GET',
      }),

    // Get users in a department
    getDepartmentUsers: (departmentId: number) =>
      this.apiRequest('auth', `/api/admin/departments/${departmentId}/users/`, {
        method: 'GET',
      }),

    // Assign user to department
    assignUserToDepartment: (assignmentData: any) =>
      this.apiRequest('auth', '/api/admin/departments/assign-user/', {
        method: 'POST',
        body: JSON.stringify(assignmentData),
      }),

    // Remove user from department
    removeUserFromDepartment: (departmentId: number, userId: number) =>
      this.apiRequest('auth', `/api/admin/departments/${departmentId}/users/${userId}/remove/`, {
        method: 'POST',
      }),

    // Update department head
    updateDepartmentHead: (departmentId: number, headUserId: number) =>
      this.apiRequest('auth', `/api/admin/departments/${departmentId}/update-head/`, {
        method: 'PUT',
        body: JSON.stringify({ head_user_id: headUserId }),
      }),

    // Get department head candidates
    getDepartmentHeadCandidates: (departmentId: number) =>
      this.apiRequest('auth', `/api/admin/departments/${departmentId}/head-candidates/`, {
        method: 'GET',
      }),
  };
}

// Create singleton instance
const apiClient = new ApiClient();

export default apiClient;
export type { User, AuthTokens, ApiResponse };
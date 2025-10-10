/**
 * Student Service - API calls for student data
 */
import axios from 'axios';

// Types for student data
export interface Student {
  id: number;
  reg_no: string;
  student_image?: string;
  name_bn: string;
  father_name_bn: string;
  current_madrasha: string;
  exam_name_Bn: string;
  current_class: string;
  Date_of_birth: string;
  student_type: string;
  payment_status: string;
  is_paid: boolean;
  status: string;
  activities?: StudentActivity[];
}

export interface StudentActivity {
  id: number;
  date: string;
  activity: string;
  status: string;
  action: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

export interface ApiError {
  response?: {
    data?: {
      error?: string;
    };
    status?: number;
  };
  message?: string;
}

export interface StatisticsData {
  total: number;
  submitted: number;
  approved: number;
  pending: number;
  paid: number;
  unpaid: number;
}

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const STUDENTS_API_URL = `${API_BASE_URL}/api/admin/registration/students/`;

// Configure axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth token if needed
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export class StudentService {
  /**
   * Get all students with optional filters and user-based madrasha_id filtering
   */
  static async getStudents(params?: {
    page?: number;
    limit?: number;
    search?: string;
    status?: string;
    student_type?: string;
    is_paid?: boolean;
    user_id?: number;
  }): Promise<Student[]> {
    try {
      const response = await apiClient.get<ApiResponse<Student[]>>(STUDENTS_API_URL, {
        params
      });

      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Failed to fetch students');
      }
    } catch (error: unknown) {
      const apiError = error as ApiError;
      console.error('Error fetching students:', error);
      throw new Error(apiError.response?.data?.error || apiError.message || 'Failed to fetch students');
    }
  }

  /**
   * Get single student by ID
   */
  static async getStudent(id: number): Promise<Student> {
    try {
      const response = await apiClient.get<ApiResponse<Student>>(`${STUDENTS_API_URL}${id}/`);

      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Failed to fetch student');
      }
    } catch (error: unknown) {
      const apiError = error as ApiError;
      console.error('Error fetching student:', error);
      throw new Error(apiError.response?.data?.error || apiError.message || 'Failed to fetch student');
    }
  }

  /**
   * Search students
   */
  static async searchStudents(params: {
    q?: string;
    madrasha?: string;
    class?: string;
    exam?: string;
  }): Promise<Student[]> {
    try {
      const response = await apiClient.get<ApiResponse<Student[]>>(`${STUDENTS_API_URL}search/`, {
        params
      });

      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Failed to search students');
      }
    } catch (error: unknown) {
      const apiError = error as ApiError;
      console.error('Error searching students:', error);
      throw new Error(apiError.response?.data?.error || apiError.message || 'Failed to search students');
    }
  }

  /**
   * Get student statistics
   */
  static async getStatistics(): Promise<StatisticsData> {
    try {
      const response = await apiClient.get<ApiResponse<StatisticsData>>(`${STUDENTS_API_URL}statistics/`);

      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Failed to fetch statistics');
      }
    } catch (error: unknown) {
      const apiError = error as ApiError;
      console.error('Error fetching statistics:', error);
      throw new Error(apiError.response?.data?.error || apiError.message || 'Failed to fetch statistics');
    }
  }

  /**
   * Update student data
   */
  static async updateStudent(id: number, data: Partial<Student>): Promise<Student> {
    try {
      const response = await apiClient.put<ApiResponse<Student>>(`${STUDENTS_API_URL}${id}/`, data);

      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Failed to update student');
      }
    } catch (error: unknown) {
      const apiError = error as ApiError;
      console.error('Error updating student:', error);
      throw new Error(apiError.response?.data?.error || apiError.message || 'Failed to update student');
    }
  }

  /**
   * Delete student
   */
  static async deleteStudent(id: number): Promise<void> {
    try {
      const response = await apiClient.delete<ApiResponse<void>>(`${STUDENTS_API_URL}${id}/`);

      if (!response.data.success) {
        throw new Error(response.data.error || 'Failed to delete student');
      }
    } catch (error: unknown) {
      const apiError = error as ApiError;
      console.error('Error deleting student:', error);
      throw new Error(apiError.response?.data?.error || apiError.message || 'Failed to delete student');
    }
  }
}

export default StudentService;

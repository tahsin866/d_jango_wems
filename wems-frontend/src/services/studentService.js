/**
 * Student Service - API calls for student data
 */
import axios from 'axios'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const STUDENTS_API_URL = `${API_BASE_URL}/api/registration/students/`

// Configure axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth token if needed
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export class StudentService {
  // Get all students with optional filters and user-based madrasha_id filtering
  static async getStudents(params) {
    try {
      const response = await apiClient.get(STUDENTS_API_URL, { params })
      if (response.data.success) {
        return response.data.data
      } else {
        throw new Error(response.data.error || 'Failed to fetch students')
      }
    } catch (error) {
      console.error('Error fetching students:', error)
      throw new Error(error?.response?.data?.error || error.message || 'Failed to fetch students')
    }
  }

  // Get single student by ID (for detail view)
  static async getStudent(id, params = {}) {
    try {
      const response = await apiClient.get(`${API_BASE_URL}/api/registration/${id}/`, { params })
      if (response.data.success) {
        return response.data.data
      } else {
        throw new Error(response.data.error || 'Failed to fetch student')
      }
    } catch (error) {
      console.error('Error fetching student:', error)
      throw new Error(error?.response?.data?.error || error.message || 'Failed to fetch student')
    }
  }

  // Update single student field
  static async updateStudentField(id, fieldData, params = {}) {
    try {
      const response = await apiClient.patch(`${API_BASE_URL}/api/registration/${id}/update/`, fieldData, { params })
      if (response.data.success) {
        return response.data
      } else {
        throw new Error(response.data.error || 'Failed to update student field')
      }
    } catch (error) {
      console.error('Error updating student field:', error)
      throw new Error(error?.response?.data?.error || error.message || 'Failed to update student field')
    }
  }

  // Update student address field
  static async updateStudentAddressField(id, fieldData, params = {}) {
    try {
      const response = await apiClient.patch(`${API_BASE_URL}/api/registration/${id}/update-address/`, fieldData, { params })
      if (response.data.success) {
        return response.data
      } else {
        throw new Error(response.data.error || 'Failed to update address field')
      }
    } catch (error) {
      console.error('Error updating address field:', error)
      throw new Error(error?.response?.data?.error || error.message || 'Failed to update address field')
    }
  }

  // Search students
  static async searchStudents(params) {
    try {
      const response = await apiClient.get(`${STUDENTS_API_URL}search/`, { params })
      if (response.data.success) {
        return response.data.data
      } else {
        throw new Error(response.data.error || 'Failed to search students')
      }
    } catch (error) {
      console.error('Error searching students:', error)
      throw new Error(error?.response?.data?.error || error.message || 'Failed to search students')
    }
  }

  // Get student statistics
  static async getStatistics() {
    try {
      const response = await apiClient.get(`${STUDENTS_API_URL}statistics/`)
      if (response.data.success) {
        return response.data.data
      } else {
        throw new Error(response.data.error || 'Failed to fetch statistics')
      }
    } catch (error) {
      console.error('Error fetching statistics:', error)
      throw new Error(error?.response?.data?.error || error.message || 'Failed to fetch statistics')
    }
  }

  // Update student data
  static async updateStudent(id, data) {
    try {
      const response = await apiClient.put(`${STUDENTS_API_URL}${id}/`, data)
      if (response.data.success) {
        return response.data.data
      } else {
        throw new Error(response.data.error || 'Failed to update student')
      }
    } catch (error) {
      console.error('Error updating student:', error)
      throw new Error(error?.response?.data?.error || error.message || 'Failed to update student')
    }
  }

  // Delete student
  static async deleteStudent(id) {
    try {
      const response = await apiClient.delete(`${STUDENTS_API_URL}${id}/`)
      if (!response.data.success) {
        throw new Error(response.data.error || 'Failed to delete student')
      }
    } catch (error) {
      console.error('Error deleting student:', error)
      throw new Error(error?.response?.data?.error || error.message || 'Failed to delete student')
    }
  }
}

export default StudentService

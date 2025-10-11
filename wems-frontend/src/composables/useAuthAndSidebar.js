import { ref, computed } from 'vue'
import axios from 'axios'

const currentUser = ref(null)
const isLoading = ref(false)

export function useAuthAndSidebar() {
  // Load user data from various storage sources
  function loadStoredUserData() {
    try {
      // Check localStorage first
      const localUser = localStorage.getItem('currentUser')
      if (localUser) {
        return JSON.parse(localUser)
      }

      // Check sessionStorage
      const sessionUser = sessionStorage.getItem('currentUser')
      if (sessionUser) {
        return JSON.parse(sessionUser)
      }

      // Check cookies
      const cookies = document.cookie.split(';')
      for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=')
        if (name === 'currentUser' || name === 'userData') {
          return JSON.parse(decodeURIComponent(value))
        }
      }

      return null
    } catch (error) {
      console.error('Error loading stored user data:', error)
      return null
    }
  }

  // Store user data
  function storeUserData(userData) {
    try {
      localStorage.setItem('currentUser', JSON.stringify(userData))
      sessionStorage.setItem('currentUser', JSON.stringify(userData))
      currentUser.value = userData
    } catch (error) {
      console.error('Error storing user data:', error)
    }
  }

  // Clear user data
  function clearUserData() {
    localStorage.removeItem('currentUser')
    sessionStorage.removeItem('currentUser')
    currentUser.value = null

    // Clear user-specific cookies
    const cookies = document.cookie.split(';')
    for (const cookie of cookies) {
      const [name] = cookie.trim().split('=')
      if (name === 'currentUser' || name === 'userData') {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`
      }
    }
  }

  // Fetch user department info from API
  async function fetchUserDepartmentInfo(userId) {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/user-department-info/?user_id=${userId}`)

      if (response.data.user_id) {
        const userData = {
          id: response.data.user_id,
          name: response.data.user_name,
          email: response.data.user_email,
          department_id: response.data.department_id,
          department_name: response.data.department_name
        }
        storeUserData(userData)
        return userData
      }
    } catch (error) {
      console.error('Failed to fetch user department info:', error)
    }
    return null
  }

  // Get or load current user
  async function getCurrentUser() {
    if (currentUser.value) {
      return currentUser.value
    }

    const storedUser = loadStoredUserData()
    if (storedUser) {
      currentUser.value = storedUser

      // Refresh department info if missing
      if (!storedUser.department_name && storedUser.id) {
        await fetchUserDepartmentInfo(storedUser.id)
      }

      return currentUser.value
    }

    return null
  }

  // Computed properties
  const userDepartment = computed(() => currentUser.value?.department_name || 'Unknown Department')
  const userDepartmentId = computed(() => currentUser.value?.department_id || null)
  const hasDepartment = computed(() => !!currentUser.value?.department_id)

  // Initialize
  async function initialize() {
    isLoading.value = true
    try {
      await getCurrentUser()
    } finally {
      isLoading.value = false
    }
  }

  return {
    // State
    currentUser: computed(() => currentUser.value),
    isLoading: computed(() => isLoading.value),

    // Computed
    userDepartment,
    userDepartmentId,
    hasDepartment,

    // Methods
    loadStoredUserData,
    storeUserData,
    clearUserData,
    fetchUserDepartmentInfo,
    getCurrentUser,
    initialize
  }
}

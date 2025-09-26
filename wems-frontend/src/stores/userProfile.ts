import { ref, computed } from 'vue'
import axios from '@/utils/axios'

export interface UserProfile {
  id: number
  name: string
  email: string
  user_type_id: number
  user_type_name: string
  photo: string | null
  is_admin: boolean
  avatar_url: string | null
  madrasha_id: number | null
  madrasha_name: string | null
}

// Global state
const user = ref<UserProfile | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const currentUserId = ref<number | null>(null)

// Set user ID (call this after login)
export function setCurrentUserId(userId: number) {
  currentUserId.value = userId
  localStorage.setItem('current_user_id', userId.toString())
}

// Get user ID from storage
export function getCurrentUserId(): number | null {
  if (currentUserId.value) {
    return currentUserId.value
  }

  const stored = localStorage.getItem('current_user_id')
  if (stored) {
    currentUserId.value = parseInt(stored)
    return currentUserId.value
  }

  return null
}

// Getters
export const isAdmin = computed(() => user.value?.is_admin || false)
export const userName = computed(() => user.value?.name || 'অজানা ব্যবহারকারী')
export const userEmail = computed(() => user.value?.email || '')
export const userType = computed(() => user.value?.user_type_name || '')
export const madrashaName = computed(() => user.value?.madrasha_name || 'মাদ্রাসার তথ্য নেই')
export const avatarUrl = computed(() => {
  if (user.value?.avatar_url) {
    return `${axios.defaults.baseURL}${user.value.avatar_url}`
  }
  return null
})

// Default avatar based on user type
export const defaultAvatar = computed(() => {
  if (isAdmin.value) {
    return '/images/default-admin-avatar.svg'
  }
  return '/images/default-user-avatar.svg'
})

export const displayAvatar = computed(() => avatarUrl.value || defaultAvatar.value)

// Actions
export async function fetchUserProfile() {
  try {
    loading.value = true
    error.value = null

    // Always use session-based profile endpoint
    try {
      const response = await axios.get('/auth/profile/')
      if (response.data.success) {
        user.value = response.data.user
        return
      } else {
        throw new Error('Session token auth failed')
      }
    } catch {
      // Fallback: use currentUserId if available
      const fallbackUserId = getCurrentUserId();
      if (fallbackUserId) {
        console.log(`Session token auth failed, using fallback for user ${fallbackUserId}...`);
        const fallbackResponse = await axios.get(`/auth/profile/fallback/?user_id=${fallbackUserId}`);
        if (fallbackResponse.data.success) {
          user.value = fallbackResponse.data.user;
        } else {
          throw new Error('All authentication methods failed');
        }
      } else {
        throw new Error('No user_id available for fallback profile fetch');
      }
    }
  } catch (err: unknown) {
    const errorMessage = err instanceof Error ? err.message : 'Profile fetch failed'
    error.value = errorMessage
    console.error('Profile fetch error:', err)
  } finally {
    loading.value = false
  }
}export async function updateProfile(profileData: Partial<UserProfile>) {
  try {
    loading.value = true
    error.value = null

    const response = await axios.post('/auth/profile/update/', profileData)

    if (response.data.success) {
      // Refresh profile data
      await fetchUserProfile()
      return true
    } else {
      throw new Error(response.data.error || 'Failed to update profile')
    }
  } catch (err: unknown) {
    const errorMessage = err instanceof Error ? err.message : 'Profile update failed'
    error.value = errorMessage
    console.error('Profile update error:', err)
    return false
  } finally {
    loading.value = false
  }
}

export async function uploadProfilePhoto(photoFile: File) {
  try {
    loading.value = true
    error.value = null

    const formData = new FormData()
    formData.append('photo', photoFile)

    const response = await axios.post('/auth/profile/upload-photo/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    if (response.data.success) {
      // Refresh profile data to get new photo URL
      await fetchUserProfile()
      return response.data.photo_url
    } else {
      throw new Error(response.data.error || 'Failed to upload photo')
    }
  } catch (err: unknown) {
    const errorMessage = err instanceof Error ? err.message : 'Photo upload failed'
    error.value = errorMessage
    console.error('Photo upload error:', err)
    return null
  } finally {
    loading.value = false
  }
}

export function clearProfile() {
  user.value = null
  error.value = null
  currentUserId.value = null
  localStorage.removeItem('current_user_id')
}

// Reactive state exports
export const userProfile = user
export const profileLoading = loading
export const profileError = error

// Initialize profile on module load
const token = localStorage.getItem('token')
if (token && !user.value) {
  fetchUserProfile()
}

import { ref } from 'vue'
import axios from 'axios'

// Global sidebar data store
const sidebarData = ref(null)
const isLoading = ref(false)
const isLoaded = ref(false)

export const useSidebarPreloader = () => {
  const preloadSidebarData = async () => {
    if (isLoaded.value || isLoading.value) return

    isLoading.value = true

    try {
      console.log('🚀 Preloading sidebar data...')
      const response = await axios.get('http://localhost:8000/api/sidebar/')

      if (response.data.sidebar_data) {
        sidebarData.value = response.data.sidebar_data
        isLoaded.value = true
        console.log('✅ Sidebar data preloaded successfully')

        // Cache the data
        localStorage.setItem('preloaded_sidebar_data', JSON.stringify({
          data: response.data.sidebar_data,
          timestamp: new Date().getTime()
        }))
      }
    } catch (error) {
      console.warn('⚠️ Failed to preload sidebar data:', error)
    } finally {
      isLoading.value = false
    }
  }

  const getPreloadedData = () => {
    // First try memory
    if (sidebarData.value) {
      return sidebarData.value
    }

    // Then try localStorage
    try {
      const cached = localStorage.getItem('preloaded_sidebar_data')
      if (cached) {
        const parsed = JSON.parse(cached)
        const currentTime = new Date().getTime()
        // Use cached data if less than 1 hour old
        if (currentTime - parsed.timestamp < 60 * 60 * 1000) {
          sidebarData.value = parsed.data
          isLoaded.value = true
          return parsed.data
        }
      }
    } catch (error) {
      console.warn('Failed to load cached preloaded data:', error)
    }

    return null
  }

  return {
    sidebarData,
    isLoading,
    isLoaded,
    preloadSidebarData,
    getPreloadedData
  }
}

<template>
  <aside
    style="font-family: 'SolaimanLipi', sans-serif;"
    :class="[
      'fixed top-0 left-0 h-screen transition-all duration-300 z-50 flex flex-col bg-gray-800 text-gray-300 shadow-sm border-r border-gray-700',
      isMobileOpen ? 'translate-x-0 w-[300px]' : '-translate-x-full',
      isExpanded || isMobileOpen || isHovered ? 'lg:w-[290px]' : 'lg:w-[60px]',
      'lg:translate-x-0'
    ]"
    @mouseenter="!isExpanded && setIsHovered(true)"
    @mouseleave="setIsHovered(false)"
  >
    <!-- Sidebar Header / Logo -->
    <div class="flex items-center justify-center h-16 border-b border-gray-700 bg-gray-900">
      <div class="flex items-center gap-2">
        <!-- <div class="bg-gray-700 px-2 py-1 rounded-sm text-gray-200 shadow font-bold text-lg">EM</div> -->
        <h1 class="text-xl font-bold text-gray-200 tracking-wide font-sans" style="letter-spacing: 1px;">
          <span class="ml-1">{{ departmentDisplayName }}</span>
        </h1>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto py-4 classic-scrollbar">
      <ul class="space-y-1 px-2">
        <li v-for="(item, index) in menuItems" :key="item.label">
          <!-- If has submenu -->
          <template v-if="item.items && item.items.length > 0">
            <button
              @click="toggleSubmenu(index)"
              class="w-full flex items-center px-3 py-2 rounded-sm font-semibold text-base transition-all duration-150 classic-menu-btn"
              :class="isSubmenuOpen(index)
                ? 'bg-gray-700 text-gray-100 border-l-4 border-gray-500 shadow-sm'
                : 'hover:bg-gray-700 hover:text-gray-100'"
              style="letter-spacing: 0.5px;"
            >
              <span class="w-5 h-5 mr-3 flex items-center justify-center">
                <component :is="item.icon" class="w-full h-full" />
              </span>
              <span class="flex-1 text-left font-sans">{{ item.label }}</span>
              <ChevronDownIcon class="ml-2 w-4 h-4 text-gray-400 transition-transform duration-200" :class="{ 'rotate-180': isSubmenuOpen(index) }" />
            </button>
            <transition name="slide-fade">
              <ul v-show="isSubmenuOpen(index)" class="pl-7 mt-1 space-y-1 classic-submenu" style="border-left:2px solid #6b7280;">
                <li v-for="subItem in item.items" :key="subItem.label">
                  <button
                    @click="router.push(subItem.href)"
                    class="w-full flex items-center px-3 py-2 rounded-sm text-base font-medium transition-all duration-150 classic-submenu-btn"
                    :class="isActive(subItem.href)
                      ? 'bg-gray-600 text-gray-100 font-bold shadow-sm'
                      : 'hover:bg-gray-700 hover:text-gray-100'"
                  >
                    <span class="w-4 h-4 mr-3 flex items-center justify-center">
                      <component :is="subItem.icon" class="w-full h-full" />
                    </span>
                    <span class="flex-1 text-left font-sans">{{ subItem.label }}</span>
                  </button>
                </li>
              </ul>
            </transition>
          </template>
          <!-- Direct link -->
          <button
            v-else-if="item.href"
            @click="router.push(item.href)"
            class="w-full flex items-center px-3 py-2 rounded-sm font-semibold text-base transition-all duration-150 classic-menu-btn"
            :class="isActive(item.href)
              ? 'bg-gray-600 text-gray-100 font-bold shadow-sm'
              : 'hover:bg-gray-700 hover:text-gray-100'"
            style="letter-spacing: 0.5px;"
          >
            <span class="w-5 h-5 mr-3 flex items-center justify-center">
              <component :is="item.icon" class="w-full h-full" />
            </span>
            <span class="font-sans">{{ item.label }}</span>
          </button>
        </li>
      </ul>
    </nav>
    <!-- Classic footer divider -->
    <div class="h-2 w-full bg-gradient-to-r from-gray-700/30 via-gray-600/60 to-gray-700/30"></div>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, markRaw} from 'vue'
import { useRouter } from 'vue-router'
import { useSidebar } from '@/composables/useSidebar'
import { useAuthAndSidebar } from '@/composables/useAuthAndSidebar'
import axios from 'axios'
import {
  HomeIcon, SettingsIcon, BarChartIcon, BoxCubeIcon, UserGroupIcon, CalenderIcon,
  UserCircleIcon, DocsIcon, ChevronDownIcon, ListIcon, TaskIcon, RefreshIcon, SendIcon,
  DraftIcon, TrashIcon, FolderIcon, SupportIcon, SchoolIcon
} from '@/icons'

const router = useRouter()
const { isExpanded, isMobileOpen, isHovered, setIsHovered } = useSidebar()
const { getCurrentUser } = useAuthAndSidebar()

// Define a proper type for icon components
type IconComponent = Component

interface MenuItem {
  label: string
  href?: string
  icon: IconComponent
  iconName?: string
  items?: SubMenuItem[]
}

interface SubMenuItem {
  label: string
  href: string
  icon: IconComponent
  iconName?: string
}

// Define API response types
interface ApiMenuItem {
  label: string
  href?: string
  icon?: string
  iconName?: string
  items?: ApiSubMenuItem[]
}

interface ApiSubMenuItem {
  label: string
  href: string
  icon?: string
  iconName?: string
}

const iconMap: Record<string, IconComponent> = {
  HomeIcon: markRaw(HomeIcon),
  SettingsIcon: markRaw(SettingsIcon),
  BarChartIcon: markRaw(BarChartIcon),
  BoxCubeIcon: markRaw(BoxCubeIcon),
  UserGroupIcon: markRaw(UserGroupIcon),
  CalenderIcon: markRaw(CalenderIcon),
  UserCircleIcon: markRaw(UserCircleIcon),
  DocsIcon: markRaw(DocsIcon),
  ChevronDownIcon: markRaw(ChevronDownIcon),
  ListIcon: markRaw(ListIcon),
  TaskIcon: markRaw(TaskIcon),
  RefreshIcon: markRaw(RefreshIcon),
  SendIcon: markRaw(SendIcon),
  DraftIcon: markRaw(DraftIcon),
  TrashIcon: markRaw(TrashIcon),
  FolderIcon: markRaw(FolderIcon),
  SupportIcon: markRaw(SupportIcon),
  SchoolIcon: markRaw(SchoolIcon)
}

function getIconComponent(iconName: string): IconComponent {
  return iconMap[iconName] || iconMap.HomeIcon
}

const openSubmenu = ref<string | null>(null)
const departmentDisplayName = ref('এক্সাম মেনেজমেন্ট')  // Default fallback
const defaultMenuItems: MenuItem[] = [
  {
    label: 'ই এম ড্যাশবোর্ড',
    href: '/admin/dashboard',
    icon: getIconComponent('HomeIcon'),
    items: undefined // Ensure 'items' property exists
  }
]
const menuItems = ref<MenuItem[]>(defaultMenuItems)
const CACHE_KEY = 'sidebar_menu_cache'
const CACHE_VERSION_KEY = 'sidebar_cache_version'
const CACHE_EXPIRY_HOURS = 24

function getCachedData(): MenuItem[] | null {
  try {
    const cachedData = localStorage.getItem(CACHE_KEY)
    const cacheVersion = localStorage.getItem(CACHE_VERSION_KEY)
    const currentTime = new Date().getTime()

    if (cachedData && cacheVersion) {
      const cached = JSON.parse(cachedData) as ApiMenuItem[]
      const version = JSON.parse(cacheVersion)
      if (currentTime - version.timestamp < CACHE_EXPIRY_HOURS * 60 * 60 * 1000) {
        return cached.map((item: ApiMenuItem) => ({
          ...item,
          icon: getIconComponent(item.iconName || 'HomeIcon'),
          items: item.items?.map((subItem: ApiSubMenuItem) => ({
            ...subItem,
            icon: getIconComponent(subItem.iconName || 'DocsIcon')
          }))
        }))
      }
    }
  } catch (error) {
    console.error('Error getting cached data:', error)
  }
  return null
}

function setCachedData(data: MenuItem[]): void {
  try {
    const cacheData = data.map(item => ({
      ...item,
      iconName: getIconNameFromComponent(item.icon),
      icon: undefined,
      items: item.items?.map((subItem: SubMenuItem) => ({
        ...subItem,
        iconName: getIconNameFromComponent(subItem.icon),
        icon: undefined
      }))
    }))
    localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData))
    localStorage.setItem(CACHE_VERSION_KEY, JSON.stringify({
      timestamp: new Date().getTime(),
      version: '1.0'
    }))
  } catch (error) {
    console.error('Error setting cached data:', error)
  }
}

function getIconNameFromComponent(component: IconComponent): string {
  for (const [name, comp] of Object.entries(iconMap)) {
    if (comp === component) return name
  }
  return 'HomeIcon'
}

onMounted(async () => {
  await loadSidebarData()
  await loadDepartmentName()
})

async function loadSidebarData(): Promise<void> {
  const cachedData = getCachedData()
  if (cachedData && cachedData.length > 1) {
    menuItems.value = [
      defaultMenuItems[0],
      ...cachedData.slice(1)
    ]
  }

  try {
    // Get current user info using the composable
    const userData = await getCurrentUser()
    const userId = userData?.id
    const departmentId = userData?.department_id

    // Build API URL with user_id and department_id parameters
    let apiUrl = 'http://127.0.0.1:8080/api/sidebar/'
    const params = []
    if (userId) {
      params.push(`user_id=${userId}`)
    }
    if (departmentId) {
      params.push(`department_id=${departmentId}`)
    }
    if (params.length > 0) {
      apiUrl += `?${params.join('&')}`
    }

    console.log(`Loading sidebar from: ${apiUrl}`)
    const response = await axios.get(apiUrl)

    if (response.data.sidebar_data && Array.isArray(response.data.sidebar_data)) {
      const freshData: MenuItem[] = [
        defaultMenuItems[0],
        ...response.data.sidebar_data.map((item: ApiMenuItem) => ({
          label: item.label,
          key: item.label.toLowerCase().replace(/\s+/g, '_'),
          icon: getIconComponent(
            item.iconName || item.icon || 'HomeIcon'
          ),
          items: item.items?.map((subItem: ApiSubMenuItem) => ({
            label: subItem.label,
            href: subItem.href,
            icon: getIconComponent(
              subItem.iconName || subItem.icon || 'DocsIcon'
            )
          }))
        }))
      ]
      menuItems.value = freshData
      setCachedData(freshData)

      // Log department info for debugging
      if (response.data.department_name) {
        console.log(`✅ Sidebar loaded for department: ${response.data.department_name} (ID: ${response.data.department_id})`)
        console.log(`📊 Total modules loaded: ${response.data.total_modules || (freshData.length - 1)}`)
      }
    }
  } catch (error) {
    console.error('❌ Failed to load sidebar data:', error)
    if (!cachedData) {
      // If no cached data and API fails, try fallback without user_id
      try {
        const fallbackResponse = await axios.get('http://127.0.0.1:8080/api/sidebar/')
        if (fallbackResponse.data.sidebar_data && Array.isArray(fallbackResponse.data.sidebar_data)) {
          const freshData: MenuItem[] = [
            defaultMenuItems[0],
            ...fallbackResponse.data.sidebar_data.map((item: ApiMenuItem) => ({
              label: item.label,
              key: item.label.toLowerCase().replace(/\s+/g, '_'),
              icon: getIconComponent(
                item.iconName || item.icon || 'HomeIcon'
              ),
              items: item.items?.map((subItem: ApiSubMenuItem) => ({
                label: subItem.label,
                href: subItem.href,
                icon: getIconComponent(
                  subItem.iconName || subItem.icon || 'DocsIcon'
                )
              }))
            }))
          ]
          menuItems.value = freshData
          setCachedData(freshData)
          console.log('⚠️ Using fallback sidebar (all modules)')
        }
      } catch (fallbackError) {
        console.error('❌ Fallback sidebar loading also failed:', fallbackError)
      }
    }
  }
}

async function loadDepartmentName(): Promise<void> {
  try {
    // Get current user info
    const userData = await getCurrentUser()
    const departmentId = userData?.department_id

    if (departmentId) {
      console.log(`🏢 Loading department name for ID: ${departmentId}`)

      const response = await axios.get(`http://127.0.0.1:8080/api/admin/departments/name/${departmentId}/`)

      if (response.data.success && response.data.department_name) {
        departmentDisplayName.value = response.data.department_name
        console.log(`✅ Department name loaded: ${response.data.department_name}`)
      } else {
        console.warn('⚠️ Department name not found, using fallback')
        departmentDisplayName.value = 'এক্সাম মেনেজমেন্ট'
      }
    } else {
      console.warn('⚠️ No department ID found for user, using fallback')
      departmentDisplayName.value = 'এক্সাম মেনেজমেন্ট'
    }
  } catch (error) {
    console.error('❌ Failed to load department name:', error)
    departmentDisplayName.value = 'এক্সাম মেনেজমেন্ট'
  }
}

const isActive = (href: string): boolean => window.location.pathname === href
const toggleSubmenu = (groupIndex: string | number): void => {
  const currentKey = `${groupIndex}`
  openSubmenu.value = openSubmenu.value === currentKey ? null : currentKey
}
const isSubmenuOpen = (groupIndex: string | number): boolean => {
  const key = `${groupIndex}`
  const index = typeof groupIndex === 'number' ? groupIndex : Number(groupIndex)
  return (
    openSubmenu.value === key ||
    (
      Array.isArray(menuItems.value[index]?.items) &&
      menuItems.value[index].items!.some((subItem: SubMenuItem) => isActive(subItem.href))
    )
  )
}
const clearSidebarCache = async (userId?: number): Promise<void> => {
  // Clear local cache
  localStorage.removeItem(CACHE_KEY)
  localStorage.removeItem(CACHE_VERSION_KEY)

  try {
    // Get current user if no userId provided
    if (!userId) {
      const userData = await getCurrentUser()
      userId = userData?.id
    }

    // Clear server-side cache
    if (userId) {
      await axios.post('http://127.0.0.1:8080/api/clear-department-cache/', {
        user_id: userId
      })
      console.log(`Cleared sidebar cache for user ${userId}`)
    } else {
      await axios.post('http://127.0.0.1:8080/api/clear-department-cache/')
      console.log('Cleared all sidebar cache')
    }
  } catch (error) {
    console.error('Failed to clear server cache:', error)
  }

  // Reload sidebar data
  await loadSidebarData()
}

declare global {
  interface Window {
    clearSidebarCache: (userId?: number) => Promise<void>
    refreshSidebar: () => Promise<void>
  }
}
window.clearSidebarCache = clearSidebarCache
window.refreshSidebar = loadSidebarData
</script>

<style scoped>
.classic-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #6b7280 #1f2937;
  max-height: 100%;
}
.classic-scrollbar::-webkit-scrollbar {
  width: 7px;
}
.classic-scrollbar::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 4px;
}
.classic-scrollbar::-webkit-scrollbar-track {
  background: #1f2937;
  border-radius: 4px;
}
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(.25,.8,.25,1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-4px);
  opacity: 0;
}
.classic-menu-btn {
  border-left: 3px solid transparent;
  box-shadow: none;
}
.classic-menu-btn:active, .classic-menu-btn:focus {
  outline: none;
  border-left: 3px solid #6b7280;
}
.classic-menu-btn.bg-gray-600 {
  border-left: 3px solid #4b5563;
  background: linear-gradient(90deg,#6b7280, #4b5563 80%);
}
.classic-submenu {
  background: #1f2937;
  border-radius: 0 0 0.125rem 0.125rem;
  box-shadow: 0 4px 12px -3px rgba(31, 41, 55, 0.8);
}
.classic-submenu-btn {
  border-left: 2px solid transparent;
}
.classic-submenu-btn.bg-gray-600 {
  border-left: 2px solid #4b5563;
}

/* Professional styling enhancements */
.transition-all {
  transition: all 0.2s ease;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.rounded-sm {
  border-radius: 0.125rem;
}

/* Custom focus styles for accessibility */
button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.3);
}

/* Hover effect for buttons */
button:hover {
  transition: background-color 0.2s ease, color 0.2s ease;
}
</style>

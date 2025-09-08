<template>
  <aside style="font-family: 'SolaimanLipi', sans-serif;" :class="[
    'fixed mt-16 flex flex-col lg:mt-0 top-0 px-0 left-0 bg-[#18222e] text-[#e0e6ed] h-screen transition-all duration-300 ease-in-out z-99999 border-none shadow-none',
    {
      'lg:w-[280px]': isExpanded || isMobileOpen || isHovered,
      'lg:w-[70px]': !isExpanded && !isHovered,
      'translate-x-0 w-[280px]': isMobileOpen,
      '-translate-x-full': !isMobileOpen,
      'lg:translate-x-0': true,
    },
  ]" @mouseenter="!isExpanded && setIsHovered(true)" @mouseleave="setIsHovered(false)">
    <!-- Header -->
    <div :class="[
      'py-5 px-4 bg-gradient-to-r from-emerald-600/80 to-emerald-800/80 border-b border-emerald-900/30',
      !isExpanded && !isHovered ? 'lg:px-3' : 'px-4',
    ]">
      <div v-if="isExpanded || isHovered || isMobileOpen" class="flex items-center">
        <h1 class="text-base font-semibold text-emerald-50 text-xl text-center tracking-wide">
          এক্সাম মেনেজমেন্ট সিস্টেম
        </h1>
      </div>
      <div v-else class="flex justify-center">
        <div class="w-8 h-8 bg-emerald-600 rounded-lg flex items-center justify-center">
          <span class="text-white text-sm font-semibold">E</span>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="flex-1 overflow-y-auto bg-[#18222e] custom-scrollbar">
      <nav class="px-0 py-2">
        <div class="space-y-1">
          <div v-for="(item, index) in menuItems" :key="item.label">
            <!-- Submenu Items -->
            <div v-if="item.items && item.items.length > 0">
              <button @click="toggleSubmenu(index)" :class="[
                'w-full flex items-center text-left px-5 py-2 text-xl font-medium rounded transition-all duration-150',
                {
                  'bg-emerald-50/10 text-emerald-400 border-l-4 border-emerald-400': isSubmenuOpen(index),
                  'text-[#e0e6ed] hover:bg-[#223049] hover:text-emerald-400 border-l-4 border-transparent': !isSubmenuOpen(index),
                },
                !isExpanded && !isHovered ? 'justify-center' : '',
              ]">
                <span class="flex-shrink-0 w-5 h-5">
                  <component :is="item.icon" class="w-full h-full" />
                </span>
                <span v-if="isExpanded || isHovered || isMobileOpen" class="ml-3 flex-1">
                  {{ item.label }}
                </span>
                <ChevronDownIcon v-if="isExpanded || isHovered || isMobileOpen" :class="[
                  'ml-2 w-4 h-4 transition-transform duration-200',
                  { 'rotate-180': isSubmenuOpen(index) },
                ]" />
              </button>

              <!-- Submenu -->
              <transition @enter="startTransition" @after-enter="endTransition" @before-leave="startTransition"
                @after-leave="endTransition">
                <div v-show="isSubmenuOpen(index) && (isExpanded || isHovered || isMobileOpen)" class="bg-[#1d2737] rounded-md ml-3 my-1 py-1">
                  <button v-for="subItem in item.items" :key="subItem.label" @click="router.push(subItem.href)" :class="[
                    'flex items-center w-full px-5 py-2 text-xl rounded transition-all duration-150',
                    {
                      'bg-emerald-50/10 text-emerald-400': isActive(subItem.href),
                      'text-[#e0e6ed] hover:bg-[#223049] hover:text-emerald-400': !isActive(subItem.href),
                    },
                  ]">
                    <span class="flex-shrink-0 w-4 h-4 mr-3">
                      <component :is="subItem.icon" class="w-full h-full" />
                    </span>
                    <span class="flex-1 text-left">{{ subItem.label }}</span>
                  </button>
                </div>
              </transition>
            </div>

            <!-- Direct Link Items -->
            <button v-else-if="item.href" @click="router.push(item.href)" :class="[
              'w-full flex items-center px-5 py-2 text-xl font-medium rounded transition-all duration-150',
              {
                'bg-emerald-50/10 text-emerald-400 border-l-4 border-emerald-400': isActive(item.href),
                'text-[#e0e6ed] hover:bg-[#223049] hover:text-emerald-400 border-l-4 border-transparent': !isActive(item.href),
              },
              !isExpanded && !isHovered ? 'justify-center' : '',
            ]">
              <span class="flex-shrink-0 w-5 h-5">
                <component :is="item.icon" class="w-full h-full" />
              </span>
              <span v-if="isExpanded || isHovered || isMobileOpen" class="ml-3">
                {{ item.label }}
              </span>
            </button>
          </div>
        </div>
      </nav>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import { useSidebar } from '@/composables/useSidebar'
import axios from 'axios'

// Import all icons you need individually
import {
  HomeIcon,          // Dashboard
  SettingsIcon,      // Setup & Settings
  BarChartIcon,      // Stats, Payment, Performance
  BoxCubeIcon,       // Bill, Madrasa, Markaz
  UserGroupIcon,     // Teams, Groups, Inclusion
  CalenderIcon,      // Routine, Attendance
  UserCircleIcon,    // Admin, Supervisor, Profile
  DocsIcon,          // Documents, Registration, Khata
  ChevronDownIcon,   // Dropdown arrow
  ListIcon,          // List
  TaskIcon,          // Task/Training
  RefreshIcon,       // Refresh/Change
  SendIcon,          // Apply/Send
  DraftIcon,         // Draft
  TrashIcon,         // Delete/Cancel
  FolderIcon,        // Folder/Subject
  SupportIcon,       // Support/Help
  SchoolIcon         // School/Help
} from '@/icons'

const router = useRouter()
const { isExpanded, isMobileOpen, isHovered, setIsHovered } = useSidebar()

// Define types for menu items
interface MenuItem {
  label: string
  href?: string
  icon: unknown
  iconName?: string
  items?: SubMenuItem[]
}

interface SubMenuItem {
  label: string
  href: string
  icon: unknown
  iconName?: string
}

// Icon mapping function with markRaw
const iconMap: Record<string, unknown> = {
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

function getIconComponent(iconName: string) {
  return iconMap[iconName] || iconMap.HomeIcon
}

const openSubmenu = ref<string | null>(null)

// Default fallback menu items for instant loading with markRaw - Only Dashboard
const defaultMenuItems = [
  {
    label: 'ই এম ড্যাশবোর্ড',
    href: '/admin/dashboard',
    icon: getIconComponent('HomeIcon'),
  }
]

// Dynamic menu items from database
const menuItems = ref(defaultMenuItems)

// Cache management
const CACHE_KEY = 'sidebar_menu_cache'
const CACHE_VERSION_KEY = 'sidebar_cache_version'
const CACHE_EXPIRY_HOURS = 24 // Cache for 24 hours

function getCachedData() {
  try {
    const cachedData = localStorage.getItem(CACHE_KEY)
    const cacheVersion = localStorage.getItem(CACHE_VERSION_KEY)
    const currentTime = new Date().getTime()

    if (cachedData && cacheVersion) {
      const cached = JSON.parse(cachedData)
      const version = JSON.parse(cacheVersion)

      // Check if cache is still valid (within expiry time)
      if (currentTime - version.timestamp < CACHE_EXPIRY_HOURS * 60 * 60 * 1000) {
        return cached.map((item: MenuItem) => ({
          ...item,
          icon: getIconComponent(item.iconName || 'HomeIcon'),
          items: item.items?.map((subItem: SubMenuItem) => ({
            ...subItem,
            icon: getIconComponent(subItem.iconName || 'DocsIcon')
          }))
        }))
      }
    }
  } catch (error) {
    console.warn('Failed to load cached sidebar data:', error)
  }
  return null
}

function setCachedData(data: MenuItem[]) {
  try {
    // Store data with icon names (not components) for serialization
    const cacheData = data.map(item => ({
      ...item,
      iconName: typeof item.icon === 'string' ? item.icon : getIconNameFromComponent(item.icon),
      icon: undefined, // Remove component reference
      items: item.items?.map((subItem: SubMenuItem) => ({
        ...subItem,
        iconName: typeof subItem.icon === 'string' ? subItem.icon : getIconNameFromComponent(subItem.icon),
        icon: undefined // Remove component reference
      }))
    }))

    localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData))
    localStorage.setItem(CACHE_VERSION_KEY, JSON.stringify({
      timestamp: new Date().getTime(),
      version: '1.0'
    }))
  } catch (error) {
    console.warn('Failed to cache sidebar data:', error)
  }
}

function getIconNameFromComponent(component: unknown): string {
  // Try to find icon name by comparing with iconMap
  for (const [name, comp] of Object.entries(iconMap)) {
    if (comp === component) return name
  }
  return 'HomeIcon'
}

// Load menu items with smart caching
onMounted(async () => {
  // Step 1: Try to load from cache immediately
  const cachedData = getCachedData()
  if (cachedData && cachedData.length > 1) { // More than just dashboard
    console.log('Loading sidebar from cache for instant display')
    menuItems.value = [
      defaultMenuItems[0], // Dashboard
      ...cachedData.slice(1) // Other cached items
    ]
  }

  // Step 2: Load fresh data from API in background
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/sidebar/')

    if (response.data.sidebar_data && Array.isArray(response.data.sidebar_data)) {
      const freshData = [
        defaultMenuItems[0], // Dashboard
        ...response.data.sidebar_data.map((item: MenuItem) => ({
          label: item.label,
          key: item.label.toLowerCase().replace(/\s+/g, '_'),
          icon: getIconComponent(
            ((item as MenuItem).iconName ?? (item as { icon?: string }).icon ?? 'HomeIcon') as string
          ),
          items: item.items?.map((subItem: SubMenuItem) => ({
            label: subItem.label,
            href: subItem.href,
            icon: getIconComponent(
              typeof (subItem as SubMenuItem).iconName === 'string'
                ? ((subItem as SubMenuItem).iconName || 'DocsIcon')
                : String((subItem as SubMenuItem).icon || 'DocsIcon')
            )
          }))
        }))
      ]

      // Update UI with fresh data
      menuItems.value = freshData

      // Cache the fresh data for next time
      setCachedData(freshData)

      console.log('Sidebar updated with fresh data from API')
    }
  } catch (error) {
    console.warn('Failed to load fresh sidebar data, using cached/default data:', error)

    // If API fails and no cache, keep default items
    if (!cachedData) {
      console.log('Using default sidebar items')
    }
  }
})

// Helper functions for menu interaction
const isActive = (href: string) => window.location.pathname === href

const toggleSubmenu = (groupIndex: string | number) => {
  const currentKey = `${groupIndex}`
  openSubmenu.value = openSubmenu.value === currentKey ? null : currentKey
}

const isSubmenuOpen = (groupIndex: string | number) => {
  const key = `${groupIndex}`
  const index = typeof groupIndex === 'number' ? groupIndex : Number(groupIndex)
  return (
    openSubmenu.value === key ||
    (
      Array.isArray(menuItems.value[index]?.items) &&
      menuItems.value[index].items.some((subItem: SubMenuItem) => isActive(subItem.href))
    )
  )
}

const endTransition = (el: Element) => {
  (el as HTMLElement).style.height = ""
}

const startTransition = (el: Element) => {
  (el as HTMLElement).style.height = "auto"
}

// Clear cache function (for development/debugging)
const clearSidebarCache = () => {
  localStorage.removeItem(CACHE_KEY)
  localStorage.removeItem(CACHE_VERSION_KEY)
  console.log('Sidebar cache cleared')
}

// Make it available globally for debugging
// Extend the Window interface to include clearSidebarCache
declare global {
  interface Window {
    clearSidebarCache: () => void
  }
}
window.clearSidebarCache = clearSidebarCache
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #3ba97b #18222e;
  max-height: 100%;
}
.custom-scrollbar::-webkit-scrollbar {
  width: 7px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #3ba97b;
  border-radius: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #18222e;
  border-radius: 8px;
}
</style>

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
  ]" @mouseenter="!isExpanded && setHovered(true)" @mouseleave="setHovered(false)">
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
import { ref, onMounted } from 'vue'
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
const { isExpanded, isMobileOpen, isHovered, setHovered } = useSidebar()

// Icon mapping function
const iconMap: { [key: string]: any } = {
  HomeIcon,
  SettingsIcon,
  BarChartIcon,
  BoxCubeIcon,
  UserGroupIcon,
  CalenderIcon,
  UserCircleIcon,
  DocsIcon,
  ChevronDownIcon,
  ListIcon,
  TaskIcon,
  RefreshIcon,
  SendIcon,
  DraftIcon,
  TrashIcon,
  FolderIcon,
  SupportIcon,
  SchoolIcon
}

function getIconComponent(iconName: string) {
  console.log('Getting icon for:', iconName, 'Result:', iconMap[iconName] ? iconName : 'HomeIcon (fallback)')
  return iconMap[iconName] || HomeIcon
}

const openSubmenu = ref<string | null>(null)

// Dynamic menu items from database
const menuItems = ref<any[]>([])

// Load menu items from database
onMounted(async () => {
  try {
    console.log('Loading sidebar data from database...')
    const response = await axios.get('http://localhost:8000/api/sidebar/')
    console.log('Sidebar API response:', response.data)
    
    if (response.data.sidebar_data && Array.isArray(response.data.sidebar_data)) {
      // Add default dashboard item at the beginning
      menuItems.value = [
        {
          label: 'ই এম ড্যাশবোর্ড',
          href: '/AdminDashboard',
          icon: getIconComponent('HomeIcon'),
        },
        ...response.data.sidebar_data.map((item: any) => {
          console.log('Processing module:', item.label, 'with icon:', item.icon)
          return {
            label: item.label,
            key: item.label.toLowerCase().replace(/\s+/g, '_'),
            icon: getIconComponent(item.icon),
            items: item.items?.map((subItem: any) => {
              console.log('Processing menu:', subItem.label, 'with icon:', subItem.icon)
              return {
                label: subItem.label,
                href: subItem.href,
                icon: getIconComponent(subItem.icon)
              }
            })
          }
        })
      ]
      console.log('Menu items loaded:', menuItems.value)
    }
  } catch (error) {
    console.error('Error loading sidebar data:', error)
    // Fallback to default dashboard only
    menuItems.value = [
      {
        label: 'ই এম ড্যাশবোর্ড',
        href: '/AdminDashboard',
        icon: getIconComponent('HomeIcon'),
      }
    ]
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
      menuItems.value[index].items.some((subItem: any) => isActive(subItem.href))
    )
  )
}

const endTransition = (el: Element) => {
  (el as HTMLElement).style.height = ""
}

const startTransition = (el: Element) => {
  (el as HTMLElement).style.height = "auto"
}
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

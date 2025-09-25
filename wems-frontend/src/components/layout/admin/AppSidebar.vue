<template>
  <aside
    style="font-family: 'SolaimanLipi', sans-serif;"
    :class="[
      'fixed top-0 left-0 h-screen transition-all duration-300 z-50 flex flex-col bg-[#222d32] text-[#b8c7ce] shadow-xl border-r border-[#1a2226]',
      isMobileOpen ? 'translate-x-0 w-[300px]' : '-translate-x-full',
      isExpanded || isMobileOpen || isHovered ? 'lg:w-[290px]' : 'lg:w-[60px]',
      'lg:translate-x-0'
    ]"
    @mouseenter="!isExpanded && setIsHovered(true)"
    @mouseleave="setIsHovered(false)"
  >
    <!-- Sidebar Header / Logo (Classic) -->
    <div class="flex items-center justify-center h-16 border-b border-[#1a2226] bg-gradient-to-r from-[#222d32] to-[#3c8dbc]">
      <div class="flex items-center gap-2">
        <div class="bg-[#367fa9] px-2 py-1 rounded text-white shadow font-bold text-lg">EM</div>
        <h1 class="text-xl font-bold text-[#b8c7ce] tracking-wide font-sans" style="letter-spacing: 1px;">
          <span class="ml-1">এক্সাম মেনেজমেন্ট</span>
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
              class="w-full flex items-center px-3 py-2 rounded font-semibold text-base transition-all duration-150 classic-menu-btn"
              :class="isSubmenuOpen(index)
                ? 'bg-[#1a2226] text-white border-l-4 border-[#3c8dbc] shadow'
                : 'hover:bg-[#293846] hover:text-white'"
              style="letter-spacing: 0.5px;"
            >
              <span class="w-5 h-5 mr-3 flex items-center justify-center">
                <component :is="item.icon" class="w-full h-full" />
              </span>
              <span class="flex-1 text-left font-sans">{{ item.label }}</span>
              <ChevronDownIcon class="ml-2 w-4 h-4 text-[#b8c7ce] transition-transform duration-200" :class="{ 'rotate-180': isSubmenuOpen(index) }" />
            </button>
            <transition name="slide-fade">
              <ul v-show="isSubmenuOpen(index)" class="pl-7 mt-1 space-y-1 classic-submenu" style="border-left:2px solid #3c8dbc;">
                <li v-for="subItem in item.items" :key="subItem.label">
                  <button
                    @click="router.push(subItem.href)"
                    class="w-full flex items-center px-3 py-2 rounded text-base font-medium transition-all duration-150 classic-submenu-btn"
                    :class="isActive(subItem.href)
                      ? 'bg-[#3c8dbc] text-white font-bold shadow'
                      : 'hover:bg-[#1a2226] hover:text-white'"
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
            class="w-full flex items-center px-3 py-2 rounded font-semibold text-base transition-all duration-150 classic-menu-btn"
            :class="isActive(item.href)
              ? 'bg-[#3c8dbc] text-white font-bold shadow'
              : 'hover:bg-[#293846] hover:text-white'"
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
    <div class="h-2 w-full bg-gradient-to-r from-[#3c8dbc]/30 via-[#d2d6de]/60 to-[#605ca8]/30"></div>
  </aside>
</template>

<script setup lang="ts">
// তোমার পুরা স্ক্রিপ্ট অপরিবর্তিত (ফাংশন, ডাটা, এপিআই, ক্যাশ, ইত্যাদি)
// শুধু template ও style বদলানো হয়েছে—সব function যেমন ছিল তেমনই থাকবে!
import { ref, onMounted, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import { useSidebar } from '@/composables/useSidebar'
import axios from 'axios'
import {
  HomeIcon, SettingsIcon, BarChartIcon, BoxCubeIcon, UserGroupIcon, CalenderIcon,
  UserCircleIcon, DocsIcon, ChevronDownIcon, ListIcon, TaskIcon, RefreshIcon, SendIcon,
  DraftIcon, TrashIcon, FolderIcon, SupportIcon, SchoolIcon
} from '@/icons'

const router = useRouter()
const { isExpanded, isMobileOpen, isHovered, setIsHovered } = useSidebar()

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
const defaultMenuItems = [
  {
    label: 'ই এম ড্যাশবোর্ড',
    href: '/admin/dashboard',
    icon: getIconComponent('HomeIcon'),
  }
]
const menuItems = ref(defaultMenuItems)
const CACHE_KEY = 'sidebar_menu_cache'
const CACHE_VERSION_KEY = 'sidebar_cache_version'
const CACHE_EXPIRY_HOURS = 24

function getCachedData() {
  try {
    const cachedData = localStorage.getItem(CACHE_KEY)
    const cacheVersion = localStorage.getItem(CACHE_VERSION_KEY)
    const currentTime = new Date().getTime()

    if (cachedData && cacheVersion) {
      const cached = JSON.parse(cachedData)
      const version = JSON.parse(cacheVersion)
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
  } catch (error) { }
  return null
}
function setCachedData(data: MenuItem[]) {
  try {
    const cacheData = data.map(item => ({
      ...item,
      iconName: typeof item.icon === 'string' ? item.icon : getIconNameFromComponent(item.icon),
      icon: undefined,
      items: item.items?.map((subItem: SubMenuItem) => ({
        ...subItem,
        iconName: typeof subItem.icon === 'string' ? subItem.icon : getIconNameFromComponent(subItem.icon),
        icon: undefined
      }))
    }))
    localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData))
    localStorage.setItem(CACHE_VERSION_KEY, JSON.stringify({
      timestamp: new Date().getTime(),
      version: '1.0'
    }))
  } catch (error) { }
}
function getIconNameFromComponent(component: unknown): string {
  for (const [name, comp] of Object.entries(iconMap)) {
    if (comp === component) return name
  }
  return 'HomeIcon'
}
onMounted(async () => {
  const cachedData = getCachedData()
  if (cachedData && cachedData.length > 1) {
    menuItems.value = [
      defaultMenuItems[0],
      ...cachedData.slice(1)
    ]
  }
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/sidebar/')
    if (response.data.sidebar_data && Array.isArray(response.data.sidebar_data)) {
      const freshData = [
        defaultMenuItems[0],
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
      menuItems.value = freshData
      setCachedData(freshData)
    }
  } catch (error) {
    if (!cachedData) { }
  }
})
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
const endTransition = (el: Element) => { (el as HTMLElement).style.height = "" }
const startTransition = (el: Element) => { (el as HTMLElement).style.height = "auto" }
const clearSidebarCache = () => {
  localStorage.removeItem(CACHE_KEY)
  localStorage.removeItem(CACHE_VERSION_KEY)
}
declare global {
  interface Window { clearSidebarCache: () => void }
}
window.clearSidebarCache = clearSidebarCache
</script>

<style scoped>
.classic-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #888 #222d32;
  max-height: 100%;
}
.classic-scrollbar::-webkit-scrollbar {
  width: 7px;
}
.classic-scrollbar::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 8px;
}
.classic-scrollbar::-webkit-scrollbar-track {
  background: #222d32;
  border-radius: 8px;
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
  border-left: 3px solid #3c8dbc;
}
.classic-menu-btn.bg-[#3c8dbc] {
  border-left: 3px solid #367fa9;
  background: linear-gradient(90deg,#3c8dbc, #367fa9 80%);
}
.classic-submenu {
  background: #222d32;
  border-radius: 0 0 7px 7px;
  box-shadow: 0 4px 12px -3px #222d32a0;
}
.classic-submenu-btn {
  border-left: 2px solid transparent;
}
.classic-submenu-btn.bg-[#3c8dbc] {
  border-left: 2px solid #367fa9;
}
</style>

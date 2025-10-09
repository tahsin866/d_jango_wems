<template>
  <header
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="sticky top-0 left-0 w-full z-50 bg-white shadow border-b border-gray-300"
  >
    <div class="flex items-center justify-between px-4 py-3 md:px-6 min-h-[56px]">
      <!-- Sidebar Toggle & Logo -->
      <div class="flex items-center gap-3 flex-1">
        <button
          @click="handleToggle"
          aria-label="Toggle Sidebar"
          class="inline-flex items-center justify-center w-10 h-10 rounded bg-gray-100 border border-gray-300 text-gray-700 hover:bg-gray-200"
          :class="{ 'ring-2 ring-gray-400': isMobileOpen }"
        >
          <svg v-if="isMobileOpen" class="w-6 h-6" viewBox="0 0 24 24" fill="none">
            <path d="M6.22 7.28c-.29-.29-.29-.76 0-1.06.29-.29.76-.29 1.05 0l5.73 5.73 5.73-5.73c.29-.29.76-.29 1.06 0 .29.29.29.77 0 1.06l-6.2 6.2 6.2 6.21c.29.29.29.76 0 1.06-.29.29-.76.29-1.06 0l-5.73-5.73-5.73 5.73c-.29.29-.76.29-1.05 0-.29-.3-.29-.77 0-1.06l6.2-6.21-6.2-6.2z" fill="currentColor" />
          </svg>
          <svg v-else class="w-6 h-6" viewBox="0 0 20 20" fill="none">
            <path d="M2 5h16M2 10h16M2 15h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
        <div class="hidden md:block ml-2">
          <HeaderLogo />
        </div>
      </div>

      <!-- Center Section: Madrasha/App Name -->
      <div class="flex-1 flex items-center justify-center">
        <div
          class="px-5 py-2 bg-gray-100 rounded border border-gray-300 text-gray-800 font-semibold text-lg"
        >
          {{ madrashaName }}
        </div>
      </div>

      <!-- Right Section: User Actions -->
      <div class="flex-1 flex items-center justify-end gap-3">
        <!-- <div class="hidden md:flex">
          <ThemeToggler />
        </div> -->
        <div class="relative hidden md:flex">
          <NotificationMenu />
        </div>
        <div class="relative hidden md:flex">
          <UserMenu />
        </div>
        <!-- Mobile Actions -->
        <button
          @click="toggleApplicationMenu"
          aria-label="Open Menu"
          class="md:hidden inline-flex items-center justify-center w-10 h-10 rounded bg-gray-100 border border-gray-300 text-gray-700 hover:bg-gray-200"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none">
            <circle cx="5" cy="12" r="1.5" fill="currentColor"/>
            <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
            <circle cx="19" cy="12" r="1.5" fill="currentColor"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu Dropdown -->
    <transition name="slide-fade">
      <div
        v-if="isApplicationMenuOpen"
        class="md:hidden absolute top-full left-0 w-full bg-white border-t border-gray-300 shadow z-50"
      >
        <div class="flex flex-col gap-4 p-4">
          <div class="flex items-center gap-2 px-3 py-3 bg-gray-100 rounded-lg border border-gray-300">
            <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3z" />
            </svg>
            <span class="text-base font-semibold text-gray-800">{{ madrashaName }}</span>
          </div>
          <div class="flex items-center gap-4">
            <ThemeToggler />
            <NotificationMenu />
            <UserMenu />
          </div>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSidebar } from '@/composables/useSidebar'
import ThemeToggler from '@/components/common/ThemeToggler.vue'
import HeaderLogo from '@/components/layout/header/HeaderLogo.vue'
import NotificationMenu from '@/components/layout/header/NotificationMenu.vue'
import UserMenu from '@/components/layout/header/UserMenu.vue'
import { madrashaName, fetchUserProfile } from '@/stores/userProfile'

const { toggleSidebar, toggleMobileSidebar, isMobileOpen } = useSidebar()

const isApplicationMenuOpen = ref(false)

const toggleApplicationMenu = () => {
  isApplicationMenuOpen.value = !isApplicationMenuOpen.value
}

const handleToggle = () => {
  if (window.innerWidth >= 768) {
    toggleSidebar()
  } else {
    toggleMobileSidebar()
  }
}

onMounted(() => {
  fetchUserProfile()
})
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
/* Make header flush with sidebar, remove gap */
header {
  margin-left: 0 !important;
}
</style>

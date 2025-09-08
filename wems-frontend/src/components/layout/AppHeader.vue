<template>
  <header
    class="sticky top-0 flex w-full bg-white dark:bg-gray-900   z-99999 "
  >
    <div class="flex items-center justify-between w-full px-4 py-3 lg:px-6">
      <!-- Left Section -->
      <div class="flex items-center gap-4 flex-1">
        <!-- Toggle Button -->
        <button
          @click="handleToggle"
          class="flex items-center justify-center w-9 h-9 text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-gray-100 transition-colors duration-150"
          :class="[
            isMobileOpen
              ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
              : 'bg-white dark:bg-gray-800',
          ]"
        >
          <svg
            v-if="isMobileOpen"
            class="w-4 h-4"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M6.21967 7.28131C5.92678 6.98841 5.92678 6.51354 6.21967 6.22065C6.51256 5.92775 6.98744 5.92775 7.28033 6.22065L11.999 10.9393L16.7176 6.22078C17.0105 5.92789 17.4854 5.92788 17.7782 6.22078C18.0711 6.51367 18.0711 6.98855 17.7782 7.28144L13.0597 12L17.7782 16.7186C18.0711 17.0115 18.0711 17.4863 17.7782 17.7792C17.4854 18.0721 17.0105 18.0721 16.7176 17.7792L11.999 13.0607L7.28033 17.7794C6.98744 18.0722 6.51256 18.0722 6.21967 17.7794C5.92678 17.4865 5.92678 17.0116 6.21967 16.7187L10.9384 12L6.21967 7.28131Z"
              fill="currentColor"
            />
          </svg>
          <svg
            v-else
            class="w-4 h-4"
            viewBox="0 0 16 12"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M0.583252 1C0.583252 0.585788 0.919038 0.25 1.33325 0.25H14.6666C15.0808 0.25 15.4166 0.585786 15.4166 1C15.4166 1.41421 15.0808 1.75 14.6666 1.75L1.33325 1.75C0.919038 1.75 0.583252 1.41422 0.583252 1ZM0.583252 11C0.583252 10.5858 0.919038 10.25 1.33325 10.25L14.6666 10.25C15.0808 10.25 15.4166 10.5858 15.4166 11C15.4166 11.4142 15.0808 11.75 14.6666 11.75L1.33325 11.75C0.919038 11.75 0.583252 11.4142 0.583252 11ZM1.33325 5.25C0.919038 5.25 0.583252 5.58579 0.583252 6C0.583252 6.41421 0.919038 6.75 1.33325 6.75L7.99992 6.75C8.41413 6.75 8.74992 6.41421 8.74992 6C8.74992 5.58579 8.41413 5.25 7.99992 5.25L1.33325 5.25Z"
              fill="currentColor"
            />
          </svg>
        </button>

        <!-- Header Logo -->
        <div class="lg:block hidden">
          <HeaderLogo />
        </div>

        <!-- Mobile Header Logo -->
        <div class="lg:hidden block">
          <HeaderLogo />
        </div>
      </div>

      <!-- Center Section - Madrasha Name (Desktop) -->
      <div
        style="font-family: 'SolaimanLipi', sans-serif;"

      class="hidden lg:flex items-center justify-center flex-1">
        <div class="flex items-center gap-2 px-4 py-2  ">

          <span class="text-xl font-medium text-green-700 dark:text-green-300 text-center">
            {{ madrashaName }}
          </span>
        </div>
      </div>

      <!-- Right Section - Desktop Actions -->
      <div class="hidden lg:flex items-center gap-3 flex-1 justify-end">
        <!-- Theme Toggler -->
        <div class="flex items-center justify-center w-9 h-9 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <ThemeToggler />
        </div>

        <!-- Notification Menu -->
        <div class="relative">
          <NotificationMenu />
        </div>

        <!-- User Menu -->
        <div class="relative">
          <UserMenu />
        </div>
      </div>

      <!-- Right Section - Mobile Toggle -->
      <div class="lg:hidden">
        <button
          @click="toggleApplicationMenu"
          class="flex items-center justify-center w-9 h-9 text-gray-600 dark:text-gray-400 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-gray-100 transition-colors duration-150"
        >
          <svg
            class="w-5 h-5"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M5.99902 10.4951C6.82745 10.4951 7.49902 11.1667 7.49902 11.9951V12.0051C7.49902 12.8335 6.82745 13.5051 5.99902 13.5051C5.1706 13.5051 4.49902 12.8335 4.49902 12.0051V11.9951C4.49902 11.1667 5.1706 10.4951 5.99902 10.4951ZM17.999 10.4951C18.8275 10.4951 19.499 11.1667 19.499 11.9951V12.0051C19.499 12.8335 18.8275 13.5051 17.999 13.5051C17.1706 13.5051 16.499 12.8335 16.499 12.0051V11.9951C16.499 11.1667 17.1706 10.4951 17.999 10.4951ZM13.499 11.9951C13.499 11.1667 12.8275 10.4951 11.999 10.4951C11.1706 10.4951 10.499 11.1667 10.499 11.9951V12.0051C10.499 12.8335 11.1706 13.5051 11.999 13.5051C12.8275 13.5051 13.499 12.8335 13.499 12.0051V11.9951Z"
              fill="currentColor"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu Dropdown -->
    <div
      v-if="isApplicationMenuOpen"
      class="lg:hidden absolute top-full left-0 w-full bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 shadow-lg z-50"
    >
      <div class="flex flex-col gap-4 p-4">
        <!-- Mobile Madrasha Name -->
        <div class="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg border border-green-200 dark:border-green-700">
          <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z"/>
          </svg>
          <span class="text-sm font-medium text-green-700 dark:text-green-300">
            {{ madrashaName }}
          </span>
        </div>

        <!-- Mobile Actions Row -->
        <div class="flex items-center justify-between gap-3">
          <!-- Quick Access -->
          <div class="flex items-center gap-2 px-3 py-2 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 flex-1">
            <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
              দ্রুত অ্যাক্সেস
            </span>
            <div class="w-1.5 h-1.5 bg-blue-500 rounded-full ml-auto"></div>
          </div>

          <!-- Theme Toggler -->
          <div class="flex items-center justify-center w-10 h-10 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <ThemeToggler />
          </div>
        </div>

        <!-- Mobile Status & Notifications Row -->
        <div class="flex items-center justify-between gap-3">
          <!-- User Status -->
          <div class="flex items-center gap-2 px-3 py-2 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700 flex-1">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <span class="text-xs font-medium text-green-700 dark:text-green-300">
              অনলাইন
            </span>
          </div>

          <!-- Notification Menu -->
          <div class="relative">
            <NotificationMenu />
          </div>
        </div>

        <!-- Mobile User Menu -->
        <div class="pt-2 border-t border-gray-200 dark:border-gray-700">
          <UserMenu />
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useSidebar } from '@/composables/useSidebar'
import ThemeToggler from '@/components/common/ThemeToggler.vue'
import HeaderLogo from '@/components/layout/header/HeaderLogo.vue'
import NotificationMenu from '@/components/layout/header/NotificationMenu.vue'
import UserMenu from '@/components/layout/header/UserMenu.vue'
import { madrashaName } from '@/stores/userProfile'

const { toggleSidebar, toggleMobileSidebar, isMobileOpen } = useSidebar()

const isApplicationMenuOpen = ref(false)

const toggleApplicationMenu = () => {
  isApplicationMenuOpen.value = !isApplicationMenuOpen.value
}

const handleToggle = () => {
  if (window.innerWidth >= 1024) {
    toggleSidebar()
  } else {
    toggleMobileSidebar()
  }
}
</script>

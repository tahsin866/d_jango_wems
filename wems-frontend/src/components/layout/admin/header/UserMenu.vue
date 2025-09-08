<template>
  <div

  style="font-family: 'SolaimanLipi', sans-serif;"

  class="relative" ref="dropdownRef">
    <button
      class="flex items-center text-gray-700 dark:text-gray-400"
      @click.prevent="toggleDropdown"
    >
      <span class="mr-3 overflow-hidden rounded-full h-11 w-11">
        <img :src="displayAvatar" :alt="userName" class="w-full h-full object-cover" />
      </span>

      <span class="block mr-1 font-medium text-theme-sm">{{ userName }}</span>

      <ChevronDownIcon :class="{ 'rotate-180': dropdownOpen }" />
    </button>

    <!-- Dropdown Start -->
    <div



      v-if="dropdownOpen"
      class="absolute right-0 mt-[17px] flex w-[260px] flex-col rounded-2xl border border-gray-200 bg-white p-3 shadow-theme-lg dark:border-gray-800 dark:bg-gray-dark"
    >
      <div>
        <span class="block font-medium text-gray-700 text-theme-sm dark:text-gray-400">
          {{ userName }}
        </span>
        <span class="mt-0.5 block text-theme-xs text-gray-500 dark:text-gray-400">
          {{ userEmail }}
        </span>
        <span v-if="isAdmin" class="mt-1 inline-flex items-center px-2 py-1 text-xs font-medium bg-purple-100 text-purple-800 rounded-full dark:bg-purple-900 dark:text-purple-300">
          অ্যাডমিন
        </span>
      </div>

      <ul class="flex flex-col gap-1 pt-4 pb-3 border-b border-gray-200 dark:border-gray-800">
        <li v-for="item in menuItems" :key="item.href">
          <router-link
            :to="item.href"
            class="flex items-center gap-3 px-3 py-2 font-medium text-gray-700 rounded-lg group text-theme-sm hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
          >
            <!-- SVG icon would go here -->
            <component
              :is="item.icon"
              class="text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-300"
            />
            {{ item.text }}
          </router-link>
        </li>
      </ul>
      <router-link
        to="/signin"
        @click="signOut"
        class="flex items-center gap-3 px-3 py-2 mt-3 font-medium text-gray-700 rounded-lg group text-theme-sm hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
      >
        <LogoutIcon
          class="text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-300"
        />
        সাইন আউট
      </router-link>
    </div>
    <!-- Dropdown End -->
  </div>
</template>

<script setup lang="ts">
import { UserCircleIcon, ChevronDownIcon, LogoutIcon, SettingsIcon, InfoCircleIcon } from '@/icons'
import { RouterLink, useRouter } from 'vue-router'
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'
import {
  userName,
  userEmail,
  displayAvatar,
  isAdmin,
  clearProfile
} from '@/stores/userProfile'

const dropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const menuItems = computed(() => {
  const baseItems = [
    { href: '/admin/profile', icon: UserCircleIcon, text: 'প্রোফাইল সম্পাদনা' },
    { href: '/admin/settings', icon: SettingsIcon, text: 'অ্যাকাউন্ট সেটিংস' },
  ]

  if (isAdmin.value) {
    return [
      ...baseItems,
      { href: '/admin/dashboard', icon: InfoCircleIcon, text: 'অ্যাডমিন ড্যাশবোর্ড' },
      { href: '/admin/users', icon: UserCircleIcon, text: 'ব্যবহারকারী ব্যবস্থাপনা' },
      { href: '/admin/support', icon: InfoCircleIcon, text: 'সাপোর্ট' },
    ]
  }

  return [
    ...baseItems,
    { href: '/admin/support', icon: InfoCircleIcon, text: 'সাপোর্ট' },
  ]
})

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const router = useRouter()
const signOut = async () => {
  try {
    await axios.post('http://localhost:8000/auth/logout')
  } catch {}
  localStorage.removeItem('token')
  clearProfile() // Clear user profile from store
  closeDropdown()
  router.push('/')
}

const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div
    style="font-family: 'SolaimanLipi', Arial, sans-serif;"
    class="relative"
    ref="dropdownRef"
  >
    <button
      class="flex items-center px-2 py-2 rounded border border-gray-300 bg-white shadow-sm hover:shadow-md transition"
      @click.prevent="toggleDropdown"
    >
      <span class="mr-2 overflow-hidden rounded-full border border-gray-400 bg-gray-100" style="height:44px;width:44px;">
        <img :src="displayAvatar" :alt="userName" class="w-full h-full object-cover" />
      </span>
      <span class="block mr-2 font-semibold text-gray-900 text-base">{{ userName }}</span>
      <ChevronDownIcon :class="{ 'rotate-180': dropdownOpen }" class="ml-1 text-gray-500" />
    </button>

    <!-- Dropdown Start -->
    <div
      v-if="dropdownOpen"
      class="absolute right-0 mt-2 w-64 rounded border border-gray-200 bg-white shadow-lg"
      style="min-width:256px;z-index:99;"
    >
      <div class="px-4 py-3 border-b border-gray-200">
        <span class="block font-semibold text-gray-900 text-base truncate">{{ userName }}</span>
        <span class="block text-gray-600 text-sm truncate">{{ userEmail }}</span>
        <span
          v-if="isAdmin"
          class="mt-1 inline-flex items-center px-2 py-1 text-xs font-bold bg-gray-200 text-gray-700 rounded"
        >
          অ্যাডমিন
        </span>
        <span
          v-else
          class="mt-1 inline-flex items-center px-2 py-1 text-xs font-bold bg-gray-100 text-gray-700 rounded"
        >
          ব্যবহারকারী
        </span>
      </div>
      <ul class="flex flex-col gap-1 py-2 px-2 border-b border-gray-200">
        <li v-for="item in menuItems" :key="item.href">
          <router-link
            :to="item.href"
            class="flex items-center gap-2 px-2 py-2 rounded text-gray-900 hover:bg-gray-100 font-normal text-sm transition"
          >
            <component
              :is="item.icon"
              class="text-gray-500 mr-1"
            />
            {{ item.text }}
          </router-link>
        </li>
      </ul>
      <router-link
        to="/signin"
        @click="signOut"
        class="flex items-center gap-2 px-2 py-2 mt-2 font-normal text-gray-900 rounded hover:bg-gray-100 text-sm transition"
      >
        <LogoutIcon class="text-gray-500 mr-1" />
        <span>সাইন আউট</span>
      </router-link>
    </div>
    <!-- Dropdown End -->
  </div>
</template>

<script setup>
import { UserCircleIcon, ChevronDownIcon, LogoutIcon, SettingsIcon, InfoCircleIcon } from '@/icons'
import { RouterLink, useRouter } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import {
  userName,
  userEmail,
  displayAvatar,
  isAdmin,
  clearProfile,
  fetchUserProfile
} from '@/stores/userProfile'

const dropdownOpen = ref(false)
const dropdownRef = ref(null)

const menuItems = [
  { href: '/profile', icon: UserCircleIcon, text: 'প্রোফাইল সম্পাদনা' },
  { href: '/settings', icon: SettingsIcon, text: 'অ্যাকাউন্ট সেটিংস' },
  { href: '/support', icon: InfoCircleIcon, text: 'সাপোর্ট' },
]

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const router = useRouter()
const signOut = async () => {
  try {
    await axios.post('http://localhost:8000/auth/logout/')
  } catch {}
  localStorage.removeItem('token')
  clearProfile()
  closeDropdown()
  router.push('/')
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  fetchUserProfile()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

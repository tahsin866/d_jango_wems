<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="relative"
    ref="dropdownRef"
  >
    <button
      class="flex items-center px-2 py-1 text-[#b8c7ce] hover:text-white focus:outline-none"
      @click.prevent="toggleDropdown"
    >
      <span class="mr-2 overflow-hidden rounded-circle border border-[#3c8dbc] h-10 w-10 bg-[#2c3b41] flex items-center justify-center">
        <img :src="displayAvatar" :alt="userName" class="w-full h-full object-cover" />
      </span>
      <span class="block mr-1 font-semibold text-base hidden md:inline">{{ userName }}</span>
      <ChevronDownIcon :class="['ml-1 w-4 h-4 transition-transform', { 'rotate-180': dropdownOpen }]" />
    </button>
    <transition name="slide-fade">
      <div
        v-if="dropdownOpen"
        class="absolute right-0 mt-2 w-64 rounded border border-[#1a2226] bg-[#222d32] shadow-lg text-[#b8c7ce] z-50"
      >
        <div class="px-4 py-3 border-b border-[#1a2226] flex items-center">
          <span class="overflow-hidden rounded-circle border border-[#3c8dbc] h-10 w-10 bg-[#2c3b41] flex items-center justify-center mr-3">
            <img :src="displayAvatar" :alt="userName" class="w-full h-full object-cover" />
          </span>
          <div>
            <span class="block font-semibold text-base">{{ userName }}</span>
            <span class="block text-xs text-[#999]">{{ userEmail }}</span>
            <span
              v-if="isAdmin"
              class="mt-1 inline-block px-2 py-1 text-xs font-semibold bg-[#605ca8] text-white rounded"
            >
              অ্যাডমিন
            </span>
          </div>
        </div>
        <ul class="py-2">
          <li v-for="item in menuItems" :key="item.href">
            <router-link
              :to="item.href"
              class="flex items-center gap-3 px-4 py-2 text-base font-medium hover:bg-[#1a2226] hover:text-white transition rounded-none"
            >
              <component
                :is="item.icon"
                class="text-[#999] group-hover:text-white"
              />
              <span>{{ item.text }}</span>
            </router-link>
          </li>
        </ul>
        <div class="p-2 border-t border-[#1a2226]">
          <router-link
            to="/signin"
            @click="signOut"
            class="flex items-center gap-3 px-4 py-2 font-medium hover:bg-[#1a2226] hover:text-white text-base transition rounded-none"
          >
            <LogoutIcon class="text-[#999]" />
            <span>সাইন আউট</span>
          </router-link>
        </div>
      </div>
    </transition>
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
  clearProfile()
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

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(.25,.8,.25,1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-4px);
  opacity: 0;
}
.rounded-circle {
  border-radius: 50%;
}
</style>

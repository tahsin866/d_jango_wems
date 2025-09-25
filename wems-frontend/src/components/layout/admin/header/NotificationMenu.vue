<template>
  <div class="relative" ref="dropdownRef">
    <!-- Notification Button -->
    <button
      class="relative flex items-center justify-center text-[#b8c7ce] bg-[#222d32] border border-[#1a2226] rounded-full h-11 w-11 hover:bg-[#293846] hover:text-white transition-all duration-150 shadow"
      @click="toggleDropdown"
      aria-label="Notifications"
    >
      <span v-if="notifying" class="absolute right-1 top-1 z-1 h-2.5 w-2.5 rounded-full bg-[#f39c12]">
        <span class="absolute inline-flex w-full h-full bg-[#f39c12] rounded-full opacity-75 animate-ping"></span>
      </span>
      <svg class="fill-current" width="22" height="22" viewBox="0 0 22 22" fill="none">
        <path
          d="M17.5 16.5V9.75C17.5 6.5 14.75 4.25 11 4.25C7.25 4.25 4.5 6.5 4.5 9.75V16.5H3.5C3.09 16.5 2.75 16.84 2.75 17.25C2.75 17.66 3.09 18 3.5 18H18.5C18.91 18 19.25 17.66 19.25 17.25C19.25 16.84 18.91 16.5 18.5 16.5H17.5ZM5.5 9.75C5.5 7.4 8.04 5.25 11 5.25C13.96 5.25 16.5 7.4 16.5 9.75V16.5H5.5V9.75ZM10 19.25C10 19.66 10.34 20 10.75 20H13.25C13.66 20 14 19.66 14 19.25C14 18.84 13.66 18.5 13.25 18.5H10.75C10.34 18.5 10 18.84 10 19.25Z"
          fill="currentColor"
        />
      </svg>
    </button>

    <!-- Dropdown Start -->
    <transition name="slide-fade">
      <div
        v-if="dropdownOpen"
        class="absolute right-0 mt-3 w-80 rounded border border-[#1a2226] bg-[#222d32] shadow-2xl text-[#b8c7ce] z-50 classic-scrollbar"
        style="max-height:480px;overflow-y:auto;"
      >
        <div class="flex items-center justify-between px-5 py-3 border-b border-[#1a2226] bg-gradient-to-r from-[#293846] to-[#222d32]">
          <h5 class="text-lg font-bold text-white">বিজ্ঞপ্তি</h5>
          <button @click="closeDropdown" class="text-[#b8c7ce] hover:text-white transition">
            <svg class="fill-current" width="20" height="20" viewBox="0 0 20 20">
              <path d="M6.22 7.28c-.29-.29-.29-.76 0-1.06.29-.29.76-.29 1.05 0l3.73 3.73 3.73-3.73c.29-.29.76-.29 1.06 0 .29.29.29.77 0 1.06l-4.2 4.2 4.2 4.21c.29.29.29.76 0 1.06-.29.29-.76.29-1.06 0l-3.73-3.73-3.73 3.73c-.29.29-.76.29-1.05 0-.29-.3-.29-.77 0-1.06l4.2-4.21-4.2-4.2z" fill="currentColor"/>
            </svg>
          </button>
        </div>

        <ul class="flex flex-col py-1">
          <li v-for="notification in notifications" :key="notification.id" @click="handleItemClick">
            <a
              class="flex gap-3 rounded border-b border-[#1a2226] px-5 py-3 hover:bg-[#293846] hover:text-white transition"
              href="#"
            >
              <span class="relative block w-10 h-10 rounded-full overflow-hidden border-2 border-[#3c8dbc]">
                <img :src="notification.userImage" alt="User" class="w-full h-full object-cover" />
                <span
                  :class="notification.status === 'online' ? 'bg-[#00a65a]' : 'bg-[#dd4b39]'"
                  class="absolute bottom-1 right-1 h-2.5 w-2.5 rounded-full border-2 border-white"
                ></span>
              </span>
              <span class="block flex-1">
                <span class="mb-1 block text-sm">
                  <span class="font-bold text-[#3c8dbc]">{{ notification.userName }}</span>
                  <span class="ml-1">{{ notification.action }}</span>
                  <span class="font-bold text-[#00a65a] ml-1">{{ notification.project }}</span>
                </span>
                <span class="flex items-center gap-2 text-xs text-[#b5bbc7]">
                  <span>{{ notification.type }}</span>
                  <span class="w-1 h-1 bg-[#b5bbc7] rounded-full"></span>
                  <span>{{ notification.time }}</span>
                </span>
              </span>
            </a>
          </li>
        </ul>
        <div class="px-5 py-3 border-t border-[#1a2226] text-center bg-[#1a2226]">
          <router-link
            to="#"
            class="inline-block rounded bg-[#3c8dbc] px-4 py-2 text-white font-semibold shadow hover:bg-[#367fa9] transition"
            @click="handleViewAllClick"
          >
            সব বিজ্ঞপ্তি দেখুন
          </router-link>
        </div>
      </div>
    </transition>
  </div>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'

const dropdownOpen = ref(false)
const notifying = ref(true)
const dropdownRef = ref(null)

const notifications = ref([
  {
    id: 1,
    userName: 'Terry Franci',
    userImage: '/images/user/user-02.jpg',
    action: 'অনুমতি চায়',
    project: 'Project - Nganter App',
    type: 'Project',
    time: '৫ মিনিট আগে',
    status: 'online',
  },
  {
    id: 2,
    userName: 'Rahim Uddin',
    userImage: '/images/user/user-03.jpg',
    action: 'নতুন রিকোয়েস্ট',
    project: 'Project - WEMS',
    type: 'Project',
    time: '১০ মিনিট আগে',
    status: 'offline',
  },
  // আরও বিজ্ঞপ্তি যোগ করুন...
])

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
  notifying.value = false
}
const closeDropdown = () => {
  dropdownOpen.value = false
}
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}
const handleItemClick = (event) => {
  event.preventDefault()
  closeDropdown()
}
const handleViewAllClick = (event) => {
  event.preventDefault()
  closeDropdown()
}
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
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
</style>

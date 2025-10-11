<template>
  <nav
    class="bg-gray-900 fixed top-0 left-0 w-full z-50 shadow-lg border-b border-gray-800 classic-navbar"
    style="font-family: 'SolaimanLipi', sans-serif;"
  >
    <!-- Top accent line -->
    <div class="h-1 bg-gradient-to-r from-gray-700 via-gray-600 to-gray-800"></div>

    <div class="max-w-screen-xl mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo/Brand -->
        <div class="flex items-center group gap-3">
          <div class="h-12 w-12 rounded-sm bg-gray-800 flex items-center justify-center shadow-inner border-2 border-gray-700">
            <svg class="h-8 w-8 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <div>
            <span class="text-gray-400 text-xs tracking-wide font-semibold">বাংলাদেশ কওমি মাদরাসা শিক্ষাবোর্ড</span>
            <span class="block text-white text-xl font-bold tracking-wide">WEMS</span>
          </div>
        </div>

        <!-- Navigation Links -->
        <div class="hidden lg:flex items-center space-x-1">
          <a href="#" class="classic-nav-btn">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0L2 9.586V17a1 1 0 001 1h5v-5h2v5h5a1 1 0 001-1V9.586l-7.293-7.293z" /></svg>
            <span>বেফাক ইয়ারপি</span>
          </a>
          <a href="#" class="classic-nav-btn">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24"><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm4 0h2v-2H7v2zm0-4h2v-2H7v2zm4 0h2v-2h-2v2zm0 4h2v-2h-2v2zm4 0h2v-2h-2v2zm0-4h2v-2h-2v2z"/></svg>
            <span>মাদরাসা পেনেল</span>
          </a>
          <a href="#" class="classic-nav-btn">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 3-1.34 3-3S9.66 5 8 5s-3 1.34-3 3 1.34 3 3 3zm8 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zM8 13c-2.67 0-8 1.34-8 4v2h6v-2c0-1.1.9-2 2-2s2 .9 2 2v2h6v-2c0-2.66-5.33-4-8-4z"/></svg>
            <span>শিক্ষক পেনেল</span>
          </a>
          <a href="#" class="classic-nav-btn">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="7" r="4" /><path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2" /></svg>
            <span>ছাত্র-ছাত্রী পেনেল</span>
          </a>
          <a href="#" class="classic-nav-btn">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2v20"/></svg>
            <span>ওয়েব সাইট</span>
          </a>
          <a href="/Signin" class="classic-login-btn ml-2">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M10 17v-4h4v4m-7-8v6h6V9m-6 10v-2H7v2m6-2v2h1v-2z"/></svg>
            <span>Login</span>
          </a>
        </div>

        <!-- Mobile Menu Button -->
        <div class="lg:hidden">
          <button
            @click="toggleMobileMenu"
            class="text-white hover:text-gray-300 focus:outline-none transition bg-gray-800 hover:bg-gray-700 p-3 rounded-sm border border-gray-700"
          >
            <svg class="h-6 w-6 transition-transform duration-300" :class="{ 'rotate-90': mobileMenuOpen }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                v-if="!mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div
      v-show="mobileMenuOpen"
      class="lg:hidden bg-gray-900 border-t border-gray-800 transition-all duration-500 ease-out"
      :class="mobileMenuOpen ? 'animate-fadeIn' : ''"
    >
      <div class="px-6 py-6 space-y-2">
        <a href="#" class="classic-mobile-btn">
          <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.707 2.293a1 1 0 00-1.414 0L2 9.586V17a1 1 0 001 1h5v-5h2v5h5a1 1 0 001-1V9.586l-7.293-7.293z" />
          </svg>
          <span>বেফাক ইয়ারপি</span>
        </a>
        <a href="#" class="classic-mobile-btn">
          <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm4 0h2v-2H7v2zm0-4h2v-2H7v2zm4 0h2v-2h-2v2zm0 4h2v-2h-2v2zm4 0h2v-2h-2v2zm0-4h2v-2h-2v2z"/>
          </svg>
          <span>মাদরাসা পেনেল</span>
        </a>
        <a href="#" class="classic-mobile-btn">
          <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 3-1.34 3-3S9.66 5 8 5s-3 1.34-3 3 1.34 3 3 3zm8 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zM8 13c-2.67 0-8 1.34-8 4v2h6v-2c0-1.1.9-2 2-2s2 .9 2 2v2h6v-2c0-2.66-5.33-4-8-4z"/>
          </svg>
          <span>শিক্ষক পেনেল</span>
        </a>
        <a href="#" class="classic-mobile-btn">
          <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="7" r="4" />
            <path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2" />
          </svg>
          <span>ছাত্র-ছাত্রী পেনেল</span>
        </a>
        <a href="#" class="classic-mobile-btn">
          <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/>
            <path d="M2 12h20M12 2v20"/>
          </svg>
          <span>ওয়েব সাইট</span>
        </a>
        <div class="pt-4 mt-4 border-t border-gray-800">
          <a href="/dashboard" class="classic-login-btn w-full flex justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M10 17v-4h4v4m-7-8v6h6V9m-6 10v-2H7v2m6-2v2h1v-2z"/>
            </svg>
            <span>Login</span>
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
const mobileMenuOpen = ref(false)
function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}
</script>

<style scoped>
.classic-navbar {
  margin-left: 0 !important;
}
.classic-nav-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #d1d5db;
  background: transparent;
  font-weight: 500;
  font-size: 0.98rem;
  border-radius: 0;
  padding: 0.5rem 1rem;
  border: none;
  border-bottom: 2px solid transparent;
  transition: all 0.18s;
  cursor: pointer;
}
.classic-nav-btn:hover {
  background: transparent;
  color: #ffffff;
  border-bottom-color: #9ca3af;
}
.classic-login-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #374151;
  color: #ffffff;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 0;
  padding: 0.5rem 1rem;
  border: 1px solid #4b5563;
  transition: all 0.2s;
}
.classic-login-btn:hover {
  background: #4b5563;
  color: #ffffff;
  border-color: #6b7280;
}
.classic-mobile-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #d1d5db;
  background: transparent;
  font-weight: 500;
  font-size: 1rem;
  border-radius: 0;
  padding: 0.75rem 1.2rem;
  border: none;
  border-bottom: 1px solid #374151;
  transition: all 0.18s;
  cursor: pointer;
}
.classic-mobile-btn:hover {
  background: transparent;
  color: #ffffff;
  border-bottom-color: #9ca3af;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
</style>

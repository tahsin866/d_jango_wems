<template>
  <nav
    class="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 fixed top-0 w-full z-50 shadow-2xl backdrop-blur-md border-b border-slate-700/20"
    style="font-family: 'Inter', 'SolaimanLipi', sans-serif;"
  >
    <!-- Top accent line -->
    <div class="h-1 "></div>

    <div class="container mx-auto px-6">
      <div class="flex items-center justify-between h-18">

        <!-- Logo and Brand -->
        <div class="flex items-center group">
          <div class="relative">
            <div
              class="h-14 w-14 rounded-2xl bg-gradient-to-br from-emerald-500 via-teal-500 to-emerald-600 flex items-center justify-center mr-4 shadow-xl border border-emerald-400/30 transform transition-all duration-500 hover:scale-105 hover:rotate-3 group-hover:shadow-emerald-500/30"
            >
              <svg class="h-8 w-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <!-- Animated ring -->
            <div class="absolute inset-0 rounded-2xl border-2 border-emerald-400/0 group-hover:border-emerald-400/50 transition-all duration-700 animate-pulse"></div>
          </div>

          <div class="flex flex-col">
            <span class="text-slate-300 text-sm font-medium tracking-wide opacity-90 transition-all duration-300 group-hover:text-emerald-300">
              বাংলাদেশ কওমি মাদরাসা শিক্ষাবোর্ড
            </span>
            <span class="text-white text-3xl font-bold tracking-wider bg-gradient-to-r from-emerald-300 to-teal-300 bg-clip-text text-transparent">
              WEMS
            </span>
          </div>
        </div>

        <!-- Navigation Links -->
        <div class="hidden lg:flex items-center space-x-2">
          <a
            href="#"
            class="group text-slate-200 text-sm font-semibold hover:bg-slate-700/70 hover:text-white px-5 py-3.5 rounded-md transition-all duration-300 flex items-center gap-2.5 relative overflow-hidden backdrop-blur-sm"
          >
            <!-- Animated background -->
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/0 to-teal-500/0 group-hover:from-emerald-500/20 group-hover:to-teal-500/20 transition-all duration-500"></div>

            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-emerald-400 to-teal-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>

            <svg class="w-5 h-5 text-emerald-400 transition-transform duration-300 group-hover:scale-110" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.707 2.293a1 1 0 00-1.414 0L2 9.586V17a1 1 0 001 1h5v-5h2v5h5a1 1 0 001-1V9.586l-7.293-7.293z" />
            </svg>
            <span class="relative z-10">বেফাক ইয়ারপি</span>
          </a>

          <a
            href="#"
            class="group text-slate-200 text-sm font-semibold hover:bg-slate-700/70 hover:text-white px-5 py-3.5 rounded-md transition-all duration-300 flex items-center gap-2.5 relative overflow-hidden backdrop-blur-sm"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/0 to-teal-500/0 group-hover:from-emerald-500/20 group-hover:to-teal-500/20 transition-all duration-500"></div>
            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-emerald-400 to-teal-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>

            <svg class="w-5 h-5 text-emerald-400 transition-transform duration-300 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
              <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm4 0h2v-2H7v2zm0-4h2v-2H7v2zm4 0h2v-2h-2v2zm0 4h2v-2h-2v2zm4 0h2v-2h-2v2zm0-4h2v-2h-2v2z"/>
            </svg>
            <span class="relative z-10">মাদরাসা পেনেল</span>
          </a>

          <a
            href="#"
            class="group text-slate-200 text-sm font-semibold hover:bg-slate-700/70 hover:text-white px-5 py-3.5 rounded-md transition-all duration-300 flex items-center gap-2.5 relative overflow-hidden backdrop-blur-sm"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/0 to-teal-500/0 group-hover:from-emerald-500/20 group-hover:to-teal-500/20 transition-all duration-500"></div>
            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-emerald-400 to-teal-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>

            <svg class="w-5 h-5 text-emerald-400 transition-transform duration-300 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
              <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 3-1.34 3-3S9.66 5 8 5s-3 1.34-3 3 1.34 3 3 3zm8 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zM8 13c-2.67 0-8 1.34-8 4v2h6v-2c0-1.1.9-2 2-2s2 .9 2 2v2h6v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
            <span class="relative z-10">শিক্ষক পেনেল</span>
          </a>

          <a
            href="#"
            class="group text-slate-200 text-sm font-semibold hover:bg-slate-700/70 hover:text-white px-5 py-3.5 rounded-md transition-all duration-300 flex items-center gap-2.5 relative overflow-hidden backdrop-blur-sm"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/0 to-teal-500/0 group-hover:from-emerald-500/20 group-hover:to-teal-500/20 transition-all duration-500"></div>
            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-emerald-400 to-teal-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>

            <svg class="w-5 h-5 text-emerald-400 transition-transform duration-300 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="7" r="4" />
              <path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2" />
            </svg>
            <span class="relative z-10">ছাত্র-ছাত্রী পেনেল</span>
          </a>

          <a
            href="#"
            class="group text-slate-200 text-sm font-semibold hover:bg-slate-700/70 hover:text-white px-5 py-3.5 rounded-md transition-all duration-300 flex items-center gap-2.5 relative overflow-hidden backdrop-blur-sm"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/0 to-teal-500/0 group-hover:from-emerald-500/20 group-hover:to-teal-500/20 transition-all duration-500"></div>
            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-emerald-400 to-teal-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>

            <svg class="w-5 h-5 text-emerald-400 transition-transform duration-300 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10"/>
              <path d="M2 12h20M12 2v20"/>
            </svg>
            <span class="relative z-10">ওয়েব সাইট</span>
          </a>

          <!-- Auth Button -->
          <div class="ml-8 flex items-center">
            <a
              href="/Signin"
              class="group relative bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-600 text-white hover:from-emerald-500 hover:via-teal-500 hover:to-emerald-500 px-8 py-3 rounded-md  transition-all duration-300 font-semibold shadow-xl hover:shadow-emerald-500/50 flex items-center gap-3 backdrop-blur-sm border border-emerald-500/30 hover:border-emerald-400/50 transform hover:scale-105"
            >
              <!-- Animated shine effect -->
              <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>

              <svg class="w-5 h-5 transition-transform duration-300 group-hover:rotate-12" fill="currentColor" viewBox="0 0 24 24">
                <path d="M10 17v-4h4v4m-7-8v6h6V9m-6 10v-2H7v2m6-2v2h1v-2z"/>
              </svg>
              <span class="relative z-10">Login</span>
            </a>
          </div>
        </div>

        <!-- Mobile Menu Button -->
        <div class="lg:hidden">
          <button
            @click="toggleMobileMenu"
            class="text-white hover:text-emerald-300 focus:outline-none transition-all duration-300 bg-slate-700/70 hover:bg-slate-600/70 p-3 rounded-md backdrop-blur-sm border border-slate-600/50 hover:border-emerald-500/50 transform hover:scale-105"
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
      class="lg:hidden bg-slate-900/98 border-t border-slate-700/50 backdrop-blur-xl transition-all duration-500 ease-out"
      :class="mobileMenuOpen ? 'animate-fadeIn' : ''"
    >
      <div class="px-6 py-6 space-y-2">
        <a href="#" class="group text-white flex items-center gap-4 px-5 py-4 rounded-md hover:bg-slate-700/70 transition-all duration-300 font-medium backdrop-blur-sm border border-transparent hover:border-slate-600/50">
          <div class="p-2 bg-emerald-500/20 rounded-lg group-hover:bg-emerald-500/30 transition-all duration-300">
            <svg class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.707 2.293a1 1 0 00-1.414 0L2 9.586V17a1 1 0 001 1h5v-5h2v5h5a1 1 0 001-1V9.586l-7.293-7.293z" />
            </svg>
          </div>
          <span>বেফাক ইয়ারপি</span>
        </a>

        <a href="#" class="group text-white flex items-center gap-4 px-5 py-4 rounded-md hover:bg-slate-700/70 transition-all duration-300 font-medium backdrop-blur-sm border border-transparent hover:border-slate-600/50">
          <div class="p-2 bg-emerald-500/20 rounded-lg group-hover:bg-emerald-500/30 transition-all duration-300">
            <svg class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm4 0h2v-2H7v2zm0-4h2v-2H7v2zm4 0h2v-2h-2v2zm0 4h2v-2h-2v2zm4 0h2v-2h-2v2zm0-4h2v-2h-2v2z"/>
            </svg>
          </div>
          <span>মাদরাসা পেনেল</span>
        </a>

        <a href="#" class="group text-white flex items-center gap-4 px-5 py-4 rounded-md hover:bg-slate-700/70 transition-all duration-300 font-medium backdrop-blur-sm border border-transparent hover:border-slate-600/50">
          <div class="p-2 bg-emerald-500/20 rounded-lg group-hover:bg-emerald-500/30 transition-all duration-300">
            <svg class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 3-1.34 3-3S9.66 5 8 5s-3 1.34-3 3 1.34 3 3 3zm8 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zM8 13c-2.67 0-8 1.34-8 4v2h6v-2c0-1.1.9-2 2-2s2 .9 2 2v2h6v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <span>শিক্ষক পেনেল</span>
        </a>

        <a href="#" class="group text-white flex items-center gap-4 px-5 py-4 rounded-md hover:bg-slate-700/70 transition-all duration-300 font-medium backdrop-blur-sm border border-transparent hover:border-slate-600/50">
          <div class="p-2 bg-emerald-500/20 rounded-lg group-hover:bg-emerald-500/30 transition-all duration-300">
            <svg class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="7" r="4" />
              <path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2" />
            </svg>
          </div>
          <span>ছাত্র-ছাত্রী পেনেল</span>
        </a>

        <a href="#" class="group text-white flex items-center gap-4 px-5 py-4 rounded-md hover:bg-slate-700/70 transition-all duration-300 font-medium backdrop-blur-sm border border-transparent hover:border-slate-600/50">
          <div class="p-2 bg-emerald-500/20 rounded-lg group-hover:bg-emerald-500/30 transition-all duration-300">
            <svg class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10"/>
              <path d="M2 12h20M12 2v20"/>
            </svg>
          </div>
          <span>ওয়েব সাইট</span>
        </a>

        <!-- Mobile Login Button -->
        <div class="pt-4 mt-4 border-t border-slate-700/50">
          <a
            href="/dashboard"
            class="group w-full bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-600 text-white hover:from-emerald-500 hover:via-teal-500 hover:to-emerald-500 px-6 py-4 rounded-md transition-all duration-300 font-semibold shadow-xl hover:shadow-emerald-500/30 flex items-center justify-center gap-3 backdrop-blur-sm border border-emerald-500/30 transform hover:scale-[1.02]"
          >
            <svg class="w-5 h-5 transition-transform duration-300 group-hover:rotate-12" fill="currentColor" viewBox="0 0 24 24">
              <path d="M10 17v-4h4v4m-7-8v6h6V9m-6 10v-2H7v2m6-2v2h1v-2z"/>
            </svg>
            <span>Login</span>
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineOptions({
  name: 'AppNavbar'
})

const mobileMenuOpen = ref(false)

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}
</script>

<style scoped>
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

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
</style>

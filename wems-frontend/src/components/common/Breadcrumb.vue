<template>
  <nav style="font-family: 'SolaimanLipi', sans-serif;" class="flex mb-6" aria-label="Breadcrumb">
    <ol class="inline-flex items-center space-x-1 md:space-x-3">
      <!-- Home Icon -->
      <li class="inline-flex items-center">
        <router-link to="/user/dashboard"
          class="inline-flex items-center text-xl font-medium text-gray-700 hover:text-blue-600 dark:text-gray-400 dark:hover:text-white transition-colors duration-200">
          <svg class="w-3 h-3 me-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
            viewBox="0 0 20 20">
            <path
              d="m19.707 9.293-2-2-7-7a1 1 0 0 0-1.414 0l-7 7-2 2a1 1 0 0 0 1.414 1.414L9 3.414V19a1 1 0 0 0 2 0V3.414l8.293 8.293a1 1 0 0 0 1.414-1.414Z" />
          </svg>
          হোম
        </router-link>
      </li>

      <!-- Breadcrumb Items -->
      <li v-for="(item, index) in breadcrumbItems" :key="index">
        <div class="flex items-center">
          <svg class="rtl:rotate-180 w-3 h-3 text-gray-400 mx-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
            fill="none" viewBox="0 0 6 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m1 9 4-4-4-4" />
          </svg>

          <!-- Clickable breadcrumb -->
          <router-link v-if="!item.isLast && item.path" :to="item.path"
            class="ml-1 text-xl font-medium text-gray-700 hover:text-blue-600 dark:text-gray-400 dark:hover:text-white transition-colors duration-200">
            {{ item.name }}
          </router-link>

          <!-- Current page (non-clickable) -->
          <span v-else class="ml-1 text-xl font-medium text-blue-600 dark:text-blue-400" aria-current="page">
            {{ item.name }}
          </span>
        </div>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
defineOptions({ name: 'CommonBreadcrumb' })
import { computed } from 'vue'
import { useRoute } from 'vue-router'

interface BreadcrumbItem {
  name: string
  path?: string
  isLast?: boolean
}

const route = useRoute()

// Breadcrumb mapping based on route patterns
const breadcrumbMap: Record<string, BreadcrumbItem[]> = {
  // Admin Routes
  '/admin/dashboard': [
    // { name: 'অ্যাডমিন প্যানেল', path: '/admin' },
    { name: 'ড্যাশবোর্ড', path: '/admin/dashboard' }
  ],
  '/admin/user/setup': [
    // { name: 'অ্যাডমিন প্যানেল', path: '/admin' },
    { name: 'সেটাপ সংক্রান্ত', path: '#' },
    { name: 'ব্যবহারকারী সেটাপ', path: '/admin/user/setup' }
  ],
  '/admin/marhala/setup': [
    // { name: 'অ্যাডমিন প্যানেল', path: '/admin' },
    { name: 'সেটাপ সংক্রান্ত', path: '#' },
    { name: 'মারহালা লিস্ট', path: '/admin/marhala/setup' },
    // { name: 'মারহালা সংশোধান', path: '/admin/marhala/edit' },
    // { name: 'মারহালা তৈরি', path: '/admin/marhala/setup/create' },
  ],
  '/admin/subject/setup': [
    { name: 'অ্যাডমিন প্যানেল', path: '/admin' },
    { name: 'সেটাপ সংক্রান্ত', path: '#' },
     { name: 'মারহালা তৈরি', path: '/admin/marhala/setup/create' },
  ],

  // User Routes
  '/user/dashboard': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'ড্যাশবোর্ড', path: '/user/dashboard' }
  ],

  // Markaz Routes
  '/user/markaz/list': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'মারকায সংক্রান্ত', path: '#' },
    { name: 'মারকায তালিকা', path: '/user/markaz/list' }
  ],
  '/user/markaz/apply': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'মারকায সংক্রান্ত', path: '#' },
    { name: 'মারকায আবেদন', path: '/user/markaz/apply' }
  ],
  '/user/markaz/change': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'মারকায সংক্রান্ত', path: '#' },
    { name: 'মারকায পরিবর্তন', path: '/user/markaz/change' }
  ],
  '/user/markaz/change/form': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'মারকায সংক্রান্ত', path: '#' },
    { name: 'মারকায পরিবর্তন', path: '/user/markaz/change' },
    { name: 'পরিবর্তন ফর্ম', path: '/user/markaz/change/form' }
  ],
  '/user/markaz/setup': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'মারকায সংক্রান্ত', path: '#' },
    { name: 'মারকায সেটাপ', path: '/user/markaz/setup' }
  ],
  '/user/confirmation': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'মারকায সংক্রান্ত', path: '#' },
    { name: 'মন্জুরিপত্র আবেদন', path: '/user/confirmation' }
  ],
  '/user/marhala/change': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'মারহালা পরিবর্তন', path: '/user/marhala/change' }
  ],

  // Registration Routes
  '/user/registration/overview': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'পরীক্ষার্থী নিবন্ধন', path: '/user/registration/overview' }
  ],
  '/user/registration/list': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'নিবন্ধন তালিকা', path: '/user/registration/list' }
  ],
  '/user/student/old/list': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'বিগত পরীক্ষার্থী তালিকা', path: '/user/student/old/list' }
  ],
  '/user/student/old/verify': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'বিগত পরীক্ষার্থী যাচাই', path: '/user/student/old/verify' }
  ],
  '/user/student/old/registration/form': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'বিগত পরীক্ষার্থী', path: '/user/student/old/list' },
    { name: 'নিবন্ধন ফর্ম', path: '/user/student/old/registration/form' }
  ],
  '/user/registration/card': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'নিবন্ধন পত্র', path: '/user/registration/card' }
  ],
  '/user/registration/table': [
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'নিবন্ধন টেবিল', path: '/user/registration/table' }
  ],
  '/user/restore': [
    { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'পুনরুদ্ধার', path: '/user/restore' }
  ],
  '/user/payment': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'নিবন্ধন সংক্রান্ত', path: '#' },
    { name: 'পেমেন্ট', path: '/user/payment' }
  ],

  // Other Routes
  '/user/subject/list': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'অন্যান্য', path: '#' },
    { name: 'বিষয় তালিকা', path: '/user/subject/list' }
  ],
  '/user/student/inclution': [
    // { name: 'ইউজার প্যানেল', path: '/user' },
    { name: 'অন্যান্য', path: '#' },
    { name: 'ছাত্র অন্তর্ভুক্তি', path: '/user/student/inclution' }
  ]
}

const breadcrumbItems = computed(() => {
  const currentPath = route.path
  let items = breadcrumbMap[currentPath] || []

  // If no exact match, try to generate from route meta or path segments
  if (items.length === 0) {
    items = generateBreadcrumbFromPath(currentPath)
  }

  // Mark the last item as current page
  if (items.length > 0) {
    items[items.length - 1].isLast = true
  }

  return items
})

// Fallback function to generate breadcrumb from path
function generateBreadcrumbFromPath(path: string): BreadcrumbItem[] {
  const segments = path.split('/').filter(segment => segment !== '')
  const items: BreadcrumbItem[] = []

  // Add base panel
  if (path.startsWith('/admin')) {
    items.push({ name: 'অ্যাডমিন প্যানেল', path: '/admin' })
  } else if (path.startsWith('/user')) {
    items.push({ name: 'ইউজার প্যানেল', path: '/user' })
  }

  // Add current page title from route meta or segment
  const pageTitle = String(route.meta?.title || segments[segments.length - 1] || 'পেজ')
  if (pageTitle !== 'Admin' && pageTitle !== 'User') {
    items.push({ name: pageTitle, path: path })
  }

  return items
}
</script>

<style scoped>
/* Custom styles for better appearance */
nav {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  padding: 0.75rem 1rem;
}

@media (prefers-color-scheme: dark) {
  nav {
    background: #1f2937;
    border-color: #374151;
  }
}

a:hover {
  text-decoration: underline;
  text-decoration-thickness: 2px;
  text-underline-offset: 2px;
}
</style>

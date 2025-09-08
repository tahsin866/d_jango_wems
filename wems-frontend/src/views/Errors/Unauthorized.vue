<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <div class="mx-auto h-12 w-12 text-red-600">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          অনুমতি নেই
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          আপনার এই পেজে প্রবেশের অনুমতি নেই
        </p>
      </div>

      <div class="mt-8 space-y-6">
        <div class="text-center">
          <p class="text-gray-500 mb-4">
            আপনি যে পেজটি অ্যাক্সেস করার চেষ্টা করছেন সেটি আপনার user role এর জন্য অনুমোদিত নয়।
          </p>

          <div class="space-y-3">
            <button
              @click="goBack"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              পূর্ববর্তী পেজে ফিরে যান
            </button>

            <button
              @click="goToDashboard"
              class="group relative w-full flex justify-center py-2 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              ড্যাশবোর্ডে যান
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { isAdminType, getUserTypeFromToken } from '@/utils/auth'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}

const goToDashboard = () => {
  const token = localStorage.getItem('token')
  const userType = getUserTypeFromToken(token || '')

  if (isAdminType(userType || '')) {
    router.push({ name: 'AdminDashboard' })
  } else {
    router.push({ name: 'Dashboard' })
  }
}
</script>

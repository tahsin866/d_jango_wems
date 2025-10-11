<script setup>
import { ref } from 'vue'

// Types removed, now pure JS
const examCenters = ref([
  {
    id: 1,
    name: 'দারুল উলুম মাদরাসা কেন্দ্র',
    location: 'ঢাকা',
    capacity: '৫০০',
    assignedStudents: '৪৮৫',
    status: 'active'
  },
  {
    id: 2,
    name: 'জামিয়া ইসলামিয়া কেন্দ্র',
    location: 'চট্টগ্রাম',
    capacity: '৪৫০',
    assignedStudents: '৪২০',
    status: 'active'
  },
  {
    id: 3,
    name: 'মাদরাসা আল-আরাবিয়া কেন্দ্র',
    location: 'সিলেট',
    capacity: '৩৫০',
    assignedStudents: '৩৪০',
    status: 'active'
  },
  {
    id: 4,
    name: 'নূরানী মাদরাসা কেন্দ্র',
    location: 'রাজশাহী',
    capacity: '৪০০',
    assignedStudents: '৩৮০',
    status: 'active'
  },
  {
    id: 5,
    name: 'হাফেজিয়া মাদরাসা কেন্দ্র',
    location: 'খুলনা',
    capacity: '৩০০',
    assignedStudents: '২৮৫',
    status: 'active'
  }
])

const centerSummary = ref({
  totalCenters: '৩৪৫',
  totalCapacity: '১,৫০,০০০',
  assignedStudents: '১,৪৫,৬৭৮',
  remainingCapacity: '৪,৩২২'
})

const selectedCenter = ref(null)
const showModal = ref(false)

// Current date/time and user information
const currentDateTime = '2025-08-07 07:01:22'
const currentUser = 'tahsin866'

function showCenterDetails(center) {
  selectedCenter.value = center
  showModal.value = true
}

function closeCenterDetails() {
  showModal.value = false
  setTimeout(() => {
    selectedCenter.value = null
  }, 200)
}

function calculatePercentage(assigned, capacity) {
  const cleanAssigned = parseInt(assigned.replace(/,/g, ''))
  const cleanCapacity = parseInt(capacity.replace(/,/g, ''))
  return (cleanAssigned / cleanCapacity) * 100
}

function getCapacityColorClass(percentage) {
  if (percentage >= 90) return 'bg-red-600'
  if (percentage >= 75) return 'bg-amber-500'
  return 'bg-green-600'
}
</script>

<template>
  <div class="bg-white shadow-sm border border-gray-200 rounded-lg overflow-hidden">
    <!-- Header with metadata -->
    <div class="bg-gray-50 border-b border-gray-200 px-6 py-4">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center">
        <div class="flex items-center">
          <div class="flex-shrink-0 h-10 w-10 rounded-md bg-indigo-100 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <div class="ml-4">
            <h3 class="text-base font-medium text-gray-900">পরীক্ষা কেন্দ্র ব্যবস্থাপনা</h3>
            <p class="text-sm text-gray-500">সর্বমোট {{ centerSummary.totalCenters }} টি কেন্দ্র</p>
          </div>
        </div>
        <div class="mt-3 sm:mt-0 text-sm text-gray-500 flex items-center space-x-3">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ currentDateTime }}
          </div>
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            {{ currentUser }}
          </div>
        </div>
      </div>
    </div>

    <div class="p-6">
      <!-- Key Metrics Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <!-- Total Centers -->
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm px-4 py-5">
          <div class="flex items-center">
            <div class="flex-shrink-0 rounded-md w-12 h-12 bg-indigo-100 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div class="ml-4">
              <div class="text-sm font-medium text-gray-500">মোট কেন্দ্র</div>
              <div class="text-sm font-semibold text-gray-900">{{ centerSummary.totalCenters }}</div>
            </div>
          </div>
        </div>

        <!-- Total Capacity -->
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm px-4 py-5">
          <div class="flex items-center">
            <div class="flex-shrink-0 rounded-md w-12 h-12 bg-blue-100 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <div class="ml-4">
              <div class="text-sm font-medium text-gray-500">মোট ধারণক্ষমতা</div>
              <div class="text-sm font-semibold text-gray-900">{{ centerSummary.totalCapacity }}</div>
            </div>
          </div>
        </div>

        <!-- Assigned Students -->
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm px-4 py-5">
          <div class="flex items-center">
            <div class="flex-shrink-0 rounded-md w-12 h-12 bg-green-100 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <div class="text-sm font-medium text-gray-500">বরাদ্দকৃত পরীক্ষার্থী</div>
              <div class="text-sm font-semibold text-gray-900">{{ centerSummary.assignedStudents }}</div>
            </div>
          </div>
        </div>

        <!-- Remaining Capacity -->
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm px-4 py-5">
          <div class="flex items-center">
            <div class="flex-shrink-0 rounded-md w-12 h-12 bg-amber-100 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <div class="text-sm font-medium text-gray-500">অবশিষ্ট ধারণক্ষমতা</div>
              <div class="text-sm font-semibold text-gray-900">{{ centerSummary.remainingCapacity }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Table Section -->
      <div class="mt-5 overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
        <table class="min-w-full divide-y divide-gray-300">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500 sm:pl-6">
                কেন্দ্রের নাম
              </th>
              <th scope="col" class="px-3 py-3.5 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                অবস্থান
              </th>
              <th scope="col" class="px-3 py-3.5 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                ধারণক্ষমতা
              </th>
              <th scope="col" class="px-3 py-3.5 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                বরাদ্দকৃত পরীক্ষার্থী
              </th>
              <th scope="col" class="px-3 py-3.5 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                অবস্থা
              </th>
              <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6 text-right">
                <span class="text-xs font-medium text-gray-500 uppercase tracking-wide">অ্যাকশন</span>
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 bg-white">
            <tr v-for="center in examCenters" :key="center.id" class="hover:bg-gray-50 transition-colors duration-150">
              <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                {{ center.name }}
              </td>
              <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                {{ center.location }}
              </td>
              <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                {{ center.capacity }}
              </td>
              <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-900">
                <div class="flex items-center">
                  <span class="font-medium mr-2">{{ center.assignedStudents }}</span>
                  <span class="text-gray-400 text-xs">({{ Math.round(calculatePercentage(center.assignedStudents, center.capacity)) }}%)</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-1.5 mt-1.5">
                  <div class="h-1.5 rounded-full"
                      :class="getCapacityColorClass(calculatePercentage(center.assignedStudents, center.capacity))"
                      :style="`width: ${calculatePercentage(center.assignedStudents, center.capacity)}%`">
                  </div>
                </div>
              </td>
              <td class="whitespace-nowrap px-3 py-4 text-sm">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  সক্রিয়
                </span>
              </td>
              <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                <button
                  @click="showCenterDetails(center)"
                  class="text-indigo-600 hover:text-indigo-900 font-medium focus:outline-none focus:underline">
                  বিস্তারিত
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination/Action Section -->
      <div class="flex items-center justify-between border-t border-gray-200 bg-gray-50 px-4 py-3 sm:px-6 mt-6">
        <div class="flex flex-1 justify-between sm:hidden">
          <button class="relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-md text-gray-700 bg-white border border-gray-300 hover:bg-gray-50">
            পূর্ববর্তী
          </button>
          <button class="relative ml-3 inline-flex items-center px-4 py-2 text-sm font-medium rounded-md text-gray-700 bg-white border border-gray-300 hover:bg-gray-50">
            পরবর্তী
          </button>
        </div>
        <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              মোট <span class="font-medium">{{ examCenters.length }}</span> টি কেন্দ্র প্রদর্শিত (কুল {{ centerSummary.totalCenters }} টির মধ্যে)
            </p>
          </div>
          <div>
            <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
              <button class="relative inline-flex items-center rounded-l-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500">
                <span class="sr-only">পূর্ববর্তী</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
              <button class="relative hidden items-center border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500 md:inline-flex">১</button>
              <span class="relative inline-flex items-center border border-gray-300 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-600 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500">২</span>
              <button class="relative hidden items-center border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500 md:inline-flex">৩</button>
              <button class="relative inline-flex items-center rounded-r-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500">
                <span class="sr-only">পরবর্তী</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Center Details Modal using only Tailwind -->
    <div
      v-if="selectedCenter && showModal"
      class="fixed inset-0 flex items-center justify-center z-50"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeCenterDetails"></div>

      <!-- Modal panel -->
      <div
        class="bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full"
        :class="{'opacity-100 translate-y-0 sm:scale-100': showModal, 'opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95': !showModal}"
      >
        <!-- Header -->
        <div class="bg-gray-50 px-4 py-4 border-b border-gray-200 sm:px-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-10 w-10 rounded-md bg-indigo-100 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
              </div>
              <div class="ml-3">
                <h3 class="text-base font-medium text-gray-900" id="modal-title">
                  {{ selectedCenter.name }}
                </h3>
                <p class="text-sm text-gray-500">{{ selectedCenter.location }}</p>
              </div>
            </div>
            <button @click="closeCenterDetails" class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              <span class="sr-only">Close</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Content -->
        <div class="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Basic Info Section -->
            <div class="border-b border-gray-200 md:border-b-0 md:border-r pb-4 md:pb-0 md:pr-4">
              <h4 class="text-sm font-medium text-gray-900 mb-4">মৌলিক তথ্য</h4>
              <div class="space-y-4">
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">ধারণক্ষমতা</label>
                  <p class="text-sm font-medium text-gray-900">{{ selectedCenter.capacity }} জন</p>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">বরাদ্দকৃত পরীক্ষার্থী</label>
                  <p class="text-sm font-medium text-gray-900">{{ selectedCenter.assignedStudents }} জন</p>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">অবস্থা</label>
                  <div class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 mt-1">
                    সক্রিয়
                  </div>
                </div>
              </div>
            </div>

            <!-- Capacity Usage -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-4">ধারণক্ষমতা ব্যবহার</h4>
              <div>
                <div class="mb-2 flex justify-between text-xs text-gray-600">
                  <span>{{ selectedCenter.assignedStudents }} বরাদ্দকৃত</span>
                  <span>{{ selectedCenter.capacity }} মোট</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="rounded-full h-2"
                      :class="getCapacityColorClass(calculatePercentage(selectedCenter.assignedStudents, selectedCenter.capacity))"
                      :style="`width: ${calculatePercentage(selectedCenter.assignedStudents, selectedCenter.capacity)}%`">
                  </div>
                </div>
                <div class="mt-2 text-sm font-medium text-center">
                  {{ Math.round(calculatePercentage(selectedCenter.assignedStudents, selectedCenter.capacity)) }}% ব্যবহৃত
                </div>
              </div>

              <!-- Supervisor Info -->
              <div class="mt-6 pt-6 border-t border-gray-200">
                <h4 class="text-sm font-medium text-gray-900 mb-4">কেন্দ্র সুপারভাইজার</h4>
                <div class="flex items-center">
                  <span class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </span>
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">মাওলানা আব্দুল করিম</div>
                    <div class="text-xs text-gray-500">০১৭১২-৩৪৫৬৭৮</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            class="inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            সম্পাদনা করুন
          </button>
          <button
            type="button"
            class="mt-3 sm:mt-0 inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            @click="closeCenterDetails"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            বন্ধ করুন
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

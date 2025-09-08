<script setup lang="ts">
import { ref, computed } from 'vue'
import AdminLayout from '@/components/layout/admin/AdminLayout.vue'
// ------------------- Dummy Data -------------------
type Exam = {
  id: number
  exam_setup_id: number
  name: string
  serial: number
  year: string
  hijri: string
  bangla: string
}

const exams = ref<Exam[]>([
  {
    id: 1,
    exam_setup_id: 1,
    name: "৪৬ তম কেন্দ্রীয় পরীক্ষা ১৪৪৬ হিজরি/১৪৩০ বঙ্গাব্দ/২০২৫ ইসাব্দ",
    serial: 8,
    year: "২০২৫",
    hijri: "১৪৪৬",
    bangla: "১৪৩০"
  },
  {
    id: 2,
    exam_setup_id: 2,
    name: "৪৫ তম কেন্দ্রীয় পরীক্ষা ১৪৪৫ হিজরি/১৪২৯ বঙ্গাব্দ/২০২৪ ইসাব্দ",
    serial: 7,
    year: "২০২৪",
    hijri: "১৪৪৫",
    bangla: "১৪২৯"
  },
  {
    id: 3,
    exam_setup_id: 3,
    name: "৪৪ তম কেন্দ্রীয় পরীক্ষা ১৪৪৪ হিজরি/১৪২৮ বঙ্গাব্দ/২০২৩ ইসাব্দ",
    serial: 6,
    year: "২০২৩",
    hijri: "১৪৪৪",
    bangla: "১৪২৮"
  },
  {
    id: 4,
    exam_setup_id: 4,
    name: "৪৩ তম কেন্দ্রীয় পরীক্ষা ১৪৪৩ হিজরি/১৪২৭ বঙ্গাব্দ/২০২২ ইসাব্দ",
    serial: 4,
    year: "২০২২",
    hijri: "১৪৪৩",
    bangla: "১৪২৭"
  },
  {
    id: 5,
    exam_setup_id: 5,
    name: "৪২ তম কেন্দ্রীয় পরীক্ষা ১৪৪২ হিজরি/১৪২৬ বঙ্গাব্দ/২০২১ ইসাব্দ",
    serial: 1,
    year: "২০২১",
    hijri: "১৪৪২",
    bangla: "১৪২৬"
  }
])

const currentPage = ref(1)
const perPage = ref(5)

const filters = ref({
  global: { value: '', matchMode: 'contains' },
  name: { value: '', matchMode: 'equals' },
  year: { value: '', matchMode: 'equals' },
  hijri: { value: '', matchMode: 'equals' },
})

// ------------------- Computed -------------------
const hasActiveFilters = computed(() =>
  filters.value.global.value ||
  filters.value.name.value ||
  filters.value.year.value ||
  filters.value.hijri.value
)

function getUniqueValues(field: keyof Exam) {
  const values = exams.value.map(exam => exam[field]).filter(Boolean)
  const uniqueValues = [...new Set(values)]
  return [
    { label: `${field === 'name' ? 'সকল পরীক্ষা' : field === 'year' ? 'সকল ইয়ার' : 'সকল হিজরি'}`, value: '' },
    ...uniqueValues.map(value => ({ label: value, value }))
  ]
}
function getUniqueYears() {
  return [...new Set(exams.value.map(e => e.year))]
}
function getUniqueHijriYears() {
  return [...new Set(exams.value.map(e => e.hijri))]
}
function getMostRecentHijri() {
  const hijriYears = getUniqueHijriYears()
  return hijriYears.length > 0 ? Math.max(...hijriYears.map(year => parseInt(year))) : 'N/A'
}
function getCurrentYear() {
  return new Date().getFullYear().toString()
}
function getCurrentDateTime() {
  return '2025-07-17 23:37:58'
}
function getCurrentUser() {
  return 'tahsin866'
}

// ------------------- Filtering & Pagination -------------------
const filteredExams = computed(() =>
  exams.value.filter(exam => {
    if (filters.value.global.value && !exam.name.includes(filters.value.global.value)) return false
    if (filters.value.name.value && exam.name !== filters.value.name.value) return false
    if (filters.value.year.value && exam.year !== filters.value.year.value) return false
    if (filters.value.hijri.value && exam.hijri !== filters.value.hijri.value) return false
    return true
  })
)
const paginatedExams = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return filteredExams.value.slice(start, end)
})
const totalPages = computed(() => Math.ceil(filteredExams.value.length / perPage.value))
const paginationRange = computed(() => {
  const maxPages = 5
  const range: number[] = []
  if (totalPages.value <= maxPages) {
    for (let i = 1; i <= totalPages.value; i++) range.push(i)
  } else {
    let start = Math.max(1, currentPage.value - 2)
    let end = Math.min(totalPages.value, start + maxPages - 1)
    if (end - start < maxPages - 1) start = Math.max(1, end - maxPages + 1)
    for (let i = start; i <= end; i++) range.push(i)
  }
  return range
})

// ------------------- Actions -------------------
function resetFilters() {
  filters.value = {
    global: { value: '', matchMode: 'contains' },
    name: { value: '', matchMode: 'equals' },
    year: { value: '', matchMode: 'equals' },
    hijri: { value: '', matchMode: 'equals' }
  }
  currentPage.value = 1
}
function navigateToExamEdit(id: number) {
  alert(`নিবন্ধন সংশোধনী: ${id}`)
}
function navigateToNibondon(id: number) {
  alert(`নিবন্ধন সেটআপ: ${id}`)
}
function navigateToOthersSetup() {
  alert('অন্যান্য সেটআপ')
}
function navigateToOthersSetupEdit(id: number) {
  alert(`অন্যান্য সংশোধনী: ${id}`)
}
</script>

<template>
<AdminLayout>
    <div class="py-8 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
    <div class="mx-auto max-w-7xl">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-5 mb-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 relative">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">মোট কেন্দ্রীয় পরীক্ষা</p>
              <h3 class="text-2xl font-bold text-gray-900">{{ filteredExams.length }}</h3>
              <p class="text-xs text-emerald-600 mt-2 font-medium flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                সর্বশেষ আপডেট {{ getCurrentDateTime() }}
              </p>
            </div>
            <div class="p-3 bg-blue-500/10 rounded-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 relative">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">অ্যাকাডেমিক বছর</p>
              <h3 class="text-2xl font-bold text-gray-900">{{ getUniqueYears().length }}</h3>
              <p class="text-xs text-emerald-600 mt-2 font-medium flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ getCurrentYear() }} চলমান বছর
              </p>
            </div>
            <div class="p-3 bg-purple-500/10 rounded-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 relative">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">হিজরি বছর</p>
              <h3 class="text-2xl font-bold text-gray-900">{{ getUniqueHijriYears().length }}</h3>
              <p class="text-xs text-emerald-600 mt-2 font-medium flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                সর্বশেষ {{ getMostRecentHijri() }} হিজরি
              </p>
            </div>
            <div class="p-3 bg-amber-500/10 rounded-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl shadow-md border border-blue-500 p-5 text-white">
          <div class="flex flex-col items-start justify-between h-full">
            <div>
              <p class="text-sm text-blue-100 mb-1">নতুন পরীক্ষা সেটাপ</p>
              <h3 class="text-xl font-bold text-white">কেন্দ্রীয় পরীক্ষা সেটাপ</h3>
            </div>
            <button class="mt-3 inline-flex items-center px-4 py-2 bg-white text-blue-600 font-medium rounded-lg shadow-sm hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all duration-200">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              নতুন কেন্দ্রীয় পরীক্ষা
            </button>
          </div>
        </div>
      </div>

      <!-- Filters Section -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-6 overflow-hidden">
        <div class="bg-blue-600 px-5 py-4 border-b border-blue-700/50">
          <h3 class="text-lg font-medium text-white flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            অনুসন্ধান ফিল্টার
          </h3>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-5">
            <!-- Global Search -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                অনুসন্ধান
              </label>
              <div class="relative rounded-md shadow-sm">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  v-model="filters.global.value"
                  type="text"
                  placeholder="পরীক্ষার নাম দিয়ে অনুসন্ধান করুন..."
                  class="block w-full pl-10 pr-12 py-2.5 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 shadow-sm"
                />
                <div v-if="filters.global.value" class="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <button @click="filters.global.value = ''" class="text-gray-400 hover:text-gray-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Exam Name Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                কেন্দ্রীয় পরীক্ষা
              </label>
              <div class="relative">
                <select
                  v-model="filters.name.value"
                  class="block w-full pl-3 pr-10 py-2.5 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 shadow-sm appearance-none"
                >
                  <option value="">সকল পরীক্ষা</option>
                  <option v-for="(option, index) in getUniqueValues('name')" :key="index" :value="option.value">{{ option.label }}</option>
                </select>
                <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
            </div>

            <!-- Year Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                ইয়ার
              </label>
              <div class="relative">
                <select
                  v-model="filters.year.value"
                  class="block w-full pl-3 pr-10 py-2.5 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 shadow-sm appearance-none"
                >
                  <option value="">সকল ইয়ার</option>
                  <option v-for="(option, index) in getUniqueValues('year')" :key="index" :value="option.value">{{ option.label }}</option>
                </select>
                <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
            </div>

            <!-- Hijri Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                হিজরি
              </label>
              <div class="relative">
                <select
                  v-model="filters.hijri.value"
                  class="block w-full pl-3 pr-10 py-2.5 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 shadow-sm appearance-none"
                >
                  <option value="">সকল হিজরি</option>
                  <option v-for="(option, index) in getUniqueValues('hijri')" :key="index" :value="option.value">{{ option.label }}</option>
                </select>
                <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Active Filters -->
          <div v-if="hasActiveFilters" class="mt-4 flex flex-wrap gap-2">
            <span class="text-sm text-gray-600 py-1">সক্রিয় ফিল্টার:</span>
            <div v-if="filters.global.value" class="inline-flex items-center bg-blue-50 text-blue-700 rounded-full px-3 py-1 text-sm">
              <span>অনুসন্ধান: "{{ filters.global.value }}"</span>
              <button @click="filters.global.value = ''" class="ml-1 text-blue-500 hover:text-blue-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div v-if="filters.name.value" class="inline-flex items-center bg-purple-50 text-purple-700 rounded-full px-3 py-1 text-sm">
              <span>পরীক্ষা: "{{ filters.name.value }}"</span>
              <button @click="filters.name.value = ''" class="ml-1 text-purple-500 hover:text-purple-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div v-if="filters.year.value" class="inline-flex items-center bg-green-50 text-green-700 rounded-full px-3 py-1 text-sm">
              <span>ইয়ার: {{ filters.year.value }}</span>
              <button @click="filters.year.value = ''" class="ml-1 text-green-500 hover:text-green-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div v-if="filters.hijri.value" class="inline-flex items-center bg-amber-50 text-amber-700 rounded-full px-3 py-1 text-sm">
              <span>হিজরি: {{ filters.hijri.value }}</span>
              <button @click="filters.hijri.value = ''" class="ml-1 text-amber-500 hover:text-amber-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Reset Button -->
          <div class="mt-4 flex justify-end">
            <button
              @click="resetFilters"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              ফিল্টার রিসেট করুন
            </button>
          </div>
        </div>
      </div>

      <!-- Exam Table -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-5 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-700 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            পরীক্ষার তালিকা ({{ filteredExams.length }} টি রেকর্ড)
          </h3>
          <span class="text-sm text-gray-500">
            {{ getCurrentUser() }} | {{ getCurrentDateTime() }}
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead>
              <tr class="bg-gradient-to-r from-gray-50 to-gray-100">
                <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                  কেন্দ্রীয় পরীক্ষার নাম
                </th>
                <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                  ক্রম
                </th>
                <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                  ইয়ার
                </th>
                <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                  হিজরি
                </th>
                <th scope="col" class="px-6 py-3 text-center text-sm font-semibold text-gray-700 uppercase tracking-wider">
                  করনীয়
                </th>
                <th scope="col" class="px-6 py-3 text-center text-sm font-semibold text-gray-700 uppercase tracking-wider">
                  নিবন্ধন সেটাপ
                </th>
                <th scope="col" class="px-6 py-3 text-center text-sm font-semibold text-gray-700 uppercase tracking-wider">
                  অন্তর্ভুক্তি সেটাপ
                </th>
                <th scope="col" class="px-6 py-3 text-center text-sm font-semibold text-gray-700 uppercase tracking-wider">
                  অন্যান্য সেটাপ
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(exam, index) in paginatedExams" :key="exam.id"
                  class="hover:bg-blue-50 transition-colors duration-200"
                  :class="index % 2 === 0 ? '' : 'bg-gray-50/50'">
                <td class="px-6 py-4">
                  <div class="text-sm font-medium text-gray-900">{{ exam.name }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="inline-flex items-center justify-center h-6 w-6 rounded-full bg-blue-100 text-blue-800 text-xs font-medium">
                    {{ exam.serial }}
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ exam.year }}
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                    {{ exam.hijri }} হিজরি
                  </div>
                </td>
                <td class="px-6 py-4 text-center">
                  <button
                    class="inline-flex items-center px-3 py-1.5 bg-amber-500 border border-transparent rounded-md text-sm text-white font-medium hover:bg-amber-600 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2 transition-all duration-200 shadow-sm"
                    @click="navigateToExamEdit(exam.id)"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    সংশোধনী
                  </button>
                </td>
                <td class="px-6 py-4 text-center">
                  <div class="relative inline-block text-left">
                    <div>
                      <button type="button" @click="navigateToNibondon(exam.id)"
                              class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-blue-600 px-3 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        নিবন্ধন সেটআপ
                        <svg class="-mr-1 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-center">
                  <div class="relative inline-block text-left">
                    <div>
                      <button type="button" @click="navigateToNibondon(exam.id)"
                              class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-purple-600 px-3 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                        অন্তর্ভুক্তি সেটআপ
                        <svg class="-mr-1 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-center">
                  <div class="relative inline-block text-left">
                    <div>
                      <button type="button" @click="navigateToOthersSetup"
                              class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-green-600 px-3 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                        </svg>
                        অন্যান্য সেটআপ
                        <svg class="-mr-1 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredExams.length === 0">
                <td colspan="8" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    <h3 class="mt-2 text-sm font-medium text-gray-900">কোন পরীক্ষা পাওয়া যায়নি</h3>
                    <p class="mt-1 text-sm text-gray-500">নতুন পরীক্ষা সেটাপ করতে বাটনে ক্লিক করুন।</p>
                    <div class="mt-6">
                      <button class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                        নতুন কেন্দ্রীয় পরীক্ষা
                      </button>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="filteredExams.length > 0" class="bg-white px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex-1 flex justify-between sm:hidden">
              <button @click="currentPage > 1 ? currentPage-- : null" :disabled="currentPage === 1"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                পূর্ববর্তী
              </button>
              <button @click="currentPage < totalPages ? currentPage++ : null" :disabled="currentPage === totalPages"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                পরবর্তী
              </button>
            </div>
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  মোট <span class="font-medium">{{ filteredExams.length }}</span> টি এন্ট্রি থেকে
                  <span class="font-medium">{{ (currentPage - 1) * perPage + 1 }}</span> -
                  <span class="font-medium">{{ Math.min(currentPage * perPage, filteredExams.length) }}</span> দেখানো হচ্ছে
                </p>
              </div>
              <div>
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button @click="currentPage > 1 ? currentPage-- : null" :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                    <span class="sr-only">পূর্ববর্তী</span>
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                      aria-hidden="true">
                      <path fill-rule="evenodd"
                        d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>
                  <button v-for="page in paginationRange" :key="page" @click="currentPage = page"
                    :class="[
                      'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                      currentPage === page
                        ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                        : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                    ]">
                    {{ page }}
                  </button>
                  <button @click="currentPage < totalPages ? currentPage++ : null" :disabled="currentPage === totalPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                    <span class="sr-only">পরবর্তী</span>
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                      aria-hidden="true">
                      <path fill-rule="evenodd"
                        d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</AdminLayout>
</template>

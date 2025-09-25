<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="bg-[#f4f6f9] text-[#222d32]"
  >
    <div class="mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="mb-8 bg-white rounded shadow-lg border border-[#d2d6de]">
        <div class="flex flex-col md:flex-row items-center justify-between p-6 border-b border-[#d2d6de]">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-[#e9ecef] rounded">
              <svg class="w-8 h-8 text-[#3c8dbc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-[#222d32]">পরীক্ষার ফি সেটআপ</h2>
              <p class="text-gray-500 text-base">{{ examName }}</p>
            </div>
          </div>
          <div class="flex gap-4 mt-4 md:mt-0">
            <div class="flex items-center gap-1 px-3 py-1.5 bg-[#f4f6f9] rounded text-base border border-[#d2d6de]">
              <svg class="w-4 h-4 text-[#3c8dbc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ getCurrentDate() }}
            </div>
            <div class="flex items-center gap-1 px-3 py-1.5 bg-[#f4f6f9] rounded text-base border border-[#d2d6de]">
              <svg class="w-4 h-4 text-[#3c8dbc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ getCurrentTime() }}
            </div>
            <div class="flex items-center gap-1 px-3 py-1.5 bg-[#f4f6f9] rounded text-base border border-[#d2d6de]">
              <svg class="w-4 h-4 text-[#3c8dbc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              tahsin866
            </div>
          </div>
        </div>
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-6 bg-[#f4f6f9]">
          <div class="flex flex-col items-center justify-center bg-white rounded shadow border border-[#d2d6de] p-4">
            <div class="text-base text-gray-500 mb-1">মোট মারহালা</div>
            <div class="text-xl font-semibold text-[#222d32]">{{ totalRecords }}</div>
          </div>
          <div class="flex flex-col items-center justify-center bg-white rounded shadow border border-[#d2d6de] p-4">
            <div class="text-base text-gray-500 mb-1">মোট ছাত্র</div>
            <div class="text-xl font-semibold text-[#222d32]">
              {{ totalRecords }}
            </div>
          </div>
          <div class="flex flex-col items-center justify-center bg-white rounded shadow border border-[#d2d6de] p-4">
            <div class="text-base text-gray-500 mb-1">গড় ফি (নিয়মিত)</div>
            <div class="text-xl font-semibold text-[#222d32]">
              NA
            </div>
          </div>
        </div>
      </div>

      <!-- Table Controls -->
      <div class="mb-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <input
          v-model="globalFilterValue"
          type="search"
          class="block w-full md:w-96 p-2.5 border border-[#d2d6de] rounded bg-[#f4f6f9] focus:ring-[#3c8dbc] focus:border-[#3c8dbc] text-base"
          placeholder="অনুসন্ধান করুন..."
        >
        <div class="flex gap-2">
          <button @click="exportToExcel"
            class="flex items-center px-4 py-2 border border-[#3c8dbc] rounded bg-[#e9ecef] hover:bg-[#f4f6f9] text-[#3c8dbc] font-semibold">
            <svg class="w-5 h-5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            এক্সপোর্ট
          </button>
          <button @click="fetchOverview"
            class="flex items-center px-4 py-2 border border-[#605ca8] rounded bg-[#e9ecef] hover:bg-[#f4f6f9] text-[#605ca8] font-semibold">
            <svg class="w-5 h-5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            রিফ্রেশ
          </button>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white rounded shadow-lg border border-[#d2d6de]">
        <div v-if="isLoading" class="flex items-center justify-center p-16">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#3c8dbc]"></div>
        </div>
        <div v-else>
          <div class="overflow-x-auto max-w-full">
            <table class="min-w-max w-full border-collapse">
              <thead class="bg-[#e9ecef] text-[#222d32] text-md uppercase tracking-wider">
                <tr>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">পরীক্ষা</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">ID</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">নিয়মিত (শুরু)</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">নিয়মিত (শেষ)</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">নিয়মিত ফি</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">বিলম্ব (শুরু)</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">বিলম্ব (শেষ)</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">বিলম্ব ফি</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">অনিয়মিত ফি</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">অনিয়মিত বিলম্ব ফি</th>
                  <th class="py-3 px-4 text-left font-bold whitespace-nowrap">একশন</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-[#d2d6de]">
                <tr
                  v-for="row in displayedRows"
                  :key="row.id"
                  class="hover:bg-[#f4f6f9] transition"
                >
                  <td class="px-4 py-3 font-medium text-[#222d32] whitespace-nowrap">
                    <span class="text-base text-gray-500">{{ row.marhala_name_bn }}</span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">{{ row.id }}</td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    {{ getFeeField(row, 'reg_date_from') }}
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    {{ getFeeField(row, 'reg_date_to') }}
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap font-bold">
                    {{ getFeeField(row, 'reg_regular_fee', true) }}
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    {{ getFeeField(row, 'late_date_from') }}
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    {{ getFeeField(row, 'late_date_to') }}
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap font-bold">
                    {{ getFeeField(row, 'late_regular_fee', true) }}
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap font-bold">
                    {{ getFeeField(row, 'reg_irregular_jemni', true) }}
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap font-bold">
                    {{ getFeeField(row, 'late_irregular_jemni', true) }}
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <div class="flex gap-2">
                      <RouterLink
                        :to="getOldRegistrationPath(row)"
                        class="inline-flex items-center px-3 py-1.5 bg-[#3c8dbc] rounded text-base text-white hover:bg-[#367fa9] transition shadow-sm"
                      >
                        নিবন্ধন
                      </RouterLink>
                      <RouterLink
                        :to="getRegistrationTablePath(row)"
                        class="inline-flex items-center px-3 py-1.5 bg-[#605ca8] rounded text-base text-white hover:bg-[#483d8b] transition shadow-sm"
                      >
                        তালিকা
                      </RouterLink>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- Empty State -->
          <div v-if="displayedRows.length === 0" class="py-16 flex flex-col items-center justify-center">
            <svg class="w-16 h-16 text-[#d2d6de]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 class="mt-2 text-base font-semibold text-[#222d32]">কোন রেকর্ড পাওয়া যায়নি</h3>
            <p class="mt-1 text-base text-gray-500">আপনার অনুসন্ধানের সাথে মিলে এমন কোন তথ্য নেই।</p>
          </div>
          <!-- Pagination -->
          <div class="border-t border-[#d2d6de]">
            <div class="px-4 py-4 flex items-center justify-between">
              <div class="flex items-center">
                <span class="text-base text-[#222d32] mr-2">প্রতি পৃষ্ঠায়:</span>
                <select v-model="rowsPerPage" class="border border-[#d2d6de] rounded-md text-base p-1 focus:ring-[#3c8dbc] focus:border-[#3c8dbc]">
                  <option v-for="option in [5, 10, 20, 50]" :key="option" :value="option">{{ option }}</option>
                </select>
                <span class="ml-4 text-base text-[#222d32]">
                  {{ (currentPage - 1) * rowsPerPage + 1 }} - {{ Math.min(currentPage * rowsPerPage, totalRecords) }} / {{ totalRecords }}
                </span>
              </div>
              <div class="flex items-center space-x-2">
                <button @click="currentPage = 1" :disabled="currentPage === 1"
                  class="p-2 border rounded-md"
                  :class="currentPage === 1 ? 'bg-[#e9ecef] text-[#b5bbc7] cursor-not-allowed' : 'bg-white text-[#222d32] hover:bg-[#f4f6f9]'">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                </button>
                <button @click="currentPage = Math.max(1, currentPage - 1)" :disabled="currentPage === 1"
                  class="p-2 border rounded-md"
                  :class="currentPage === 1 ? 'bg-[#e9ecef] text-[#b5bbc7] cursor-not-allowed' : 'bg-white text-[#222d32] hover:bg-[#f4f6f9]'">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <div class="hidden md:flex">
                  <template v-for="page in getPageNumbers()" :key="page">
                    <button v-if="page !== '...'" @click="typeof page === 'number' && (currentPage = page)"
                      class="px-3 py-1 border rounded-md transition-colors"
                      :class="currentPage === page ? 'bg-[#e9ecef] text-[#3c8dbc] border-[#3c8dbc]' : 'bg-white text-[#222d32] hover:bg-[#f4f6f9]'">
                      {{ page }}
                    </button>
                    <span v-else class="px-3 py-1 border border-[#d2d6de] rounded-md bg-white text-[#222d32]">
                      ...
                    </span>
                  </template>
                </div>
                <button @click="currentPage = Math.min(totalPages, currentPage + 1)" :disabled="currentPage === totalPages"
                  class="p-2 border rounded-md"
                  :class="currentPage === totalPages ? 'bg-[#e9ecef] text-[#b5bbc7] cursor-not-allowed' : 'bg-white text-[#222d32] hover:bg-[#f4f6f9]'">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
                <button @click="currentPage = totalPages" :disabled="currentPage === totalPages"
                  class="p-2 border rounded-md"
                  :class="currentPage === totalPages ? 'bg-[#e9ecef] text-[#b5bbc7] cursor-not-allowed' : 'bg-white text-[#222d32] hover:bg-[#f4f6f9]'">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

// ... script section unchanged ...
const registrationOverview = ref<any[]>([])
const examName = ref<string>('লোড হচ্ছে...')
const globalFilterValue = ref<string>('')
const currentPage = ref<number>(1)
const rowsPerPage = ref<number>(10)
const totalPages = ref<number>(1)
const isLoading = ref<boolean>(true)
const displayedRows = ref<any[]>([])
const latestExamSetupId = ref<number|null>(null)

const fetchOverview = async () => {
  isLoading.value = true
  try {
    const latestSetupRes = await axios.get('/api/central-exam/exam-setups/latest/');
    const latestSetup = latestSetupRes.data?.data
    if (latestSetup && latestSetup.id) {
      latestExamSetupId.value = latestSetup.id
      examName.value = latestSetup.exam_name || 'পরীক্ষা';
      const feesRes = await axios.get(`/api/admin/registration/overview?exam_setup_id=${latestSetup.id}`)
      registrationOverview.value = feesRes.data
    } else {
      registrationOverview.value = []
      examName.value = 'কোনো পরীক্ষার সেটআপ নেই'
    }
    updateDisplayedData();
  } catch {
    registrationOverview.value = [];
    examName.value = 'API ত্রুটি';
  }
  isLoading.value = false;
}

const updateDisplayedData = () => {
  let data = [...registrationOverview.value]
  if (globalFilterValue.value) {
    const searchTerm = globalFilterValue.value.toLowerCase()
    data = data.filter(item =>
      (item.exam_setup.exam_name || '').toLowerCase().includes(searchTerm)
      || String(item.id).includes(searchTerm)
    )
  }
  totalPages.value = Math.max(1, Math.ceil(data.length / rowsPerPage.value))
  if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
  const start = (currentPage.value - 1) * rowsPerPage.value
  displayedRows.value = data.slice(start, start + rowsPerPage.value)
}

const totalRecords = computed(() => registrationOverview.value.length)

const exportToExcel = () => {
  window.alert('Export to Excel (mock) — nothing exported in demo mode.')
}

watch(globalFilterValue, () => {
  currentPage.value = 1
  updateDisplayedData()
})

watch(rowsPerPage, () => {
  currentPage.value = 1
  updateDisplayedData()
})

watch(currentPage, () => {
  updateDisplayedData()
})

onMounted(() => {
  fetchOverview()
})

// Helper: Get field from row
function getFeeField(row: any, field: string, isMoney = false) {
  if (!row || row[field] === undefined || row[field] === null) return 'NA'
  if (isMoney) return `৳ ${formatNumber(row[field])}`
  if (field.includes('date')) return formatDate(row[field])
  return row[field]
}

const formatDate = (dateString?: string | null) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    if (Number.isNaN(date.getTime())) return dateString
    return new Intl.DateTimeFormat('bn-BD', { year: 'numeric', month: 'short', day: 'numeric' }).format(date)
  } catch {
    return dateString
  }
}

const formatNumber = (num: number | string | undefined | null) => {
  if (num === undefined || num === null) return '0'
  const n = Number(num)
  if (!Number.isFinite(n)) return String(num)
  return new Intl.NumberFormat('bn-BD', { maximumFractionDigits: 2 }).format(n)
}

const getCurrentDate = () => {
  const date = new Date()
  return new Intl.DateTimeFormat('bn-BD', { year: 'numeric', month: 'long', day: 'numeric' }).format(date)
}

const getCurrentTime = () => {
  const date = new Date()
  return new Intl.DateTimeFormat('bn-BD', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(date)
}

const getPageNumbers = (): (number | string)[] => {
  const pages: (number | string)[] = []
  const maxVisiblePages = 5
  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i)
  } else {
    if (currentPage.value <= 3) {
      for (let i = 1; i <= 4; i++) pages.push(i)
      pages.push('...')
      pages.push(totalPages.value)
    } else if (currentPage.value >= totalPages.value - 2) {
      pages.push(1)
      pages.push('...')
      for (let i = totalPages.value - 3; i <= totalPages.value; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = currentPage.value - 1; i <= currentPage.value + 1; i++) pages.push(i)
      pages.push('...')
      pages.push(totalPages.value)
    }
  }
  return pages
}

function getOldRegistrationPath(row: any) {
  return `/student/old/verify/${row.marhala_id}`;
}

function getRegistrationTablePath(row: any) {
  return `/registration/table/${row.id}`
}
</script>

<style scoped>
button, a, input, select {
  transition: all 0.2s ease;
}
tbody tr {
  transition: background-color 0.2s ease;
}
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #f4f6f9;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb {
  background: #c5c5c5;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #a0a0a0;
}
</style>

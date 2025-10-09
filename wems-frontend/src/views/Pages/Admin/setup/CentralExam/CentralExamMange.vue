<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;" class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header Section -->
    <header class="bg-white border-b border-gray-200 px-8 py-6 flex justify-between items-center shadow-sm">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">কেন্দ্রীয় পরীক্ষা ম্যানেজমেন্ট</h1>
        <p class="text-gray-600 mt-1">আপনার প্রতিষ্ঠানের সকল কেন্দ্রীয় পরীক্ষার তালিকা</p>
      </div>
      <RouterLink
        to="/central/exam/Create"
        class="inline-flex items-center bg-gray-800 text-white text-base font-medium px-5 py-2.5 rounded-sm shadow hover:bg-gray-700 transition duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        নতুন পরীক্ষা যোগ করুন
      </RouterLink>
    </header>

    <!-- Filters Section -->
    <section class="bg-white border-b border-gray-200 px-8 py-5 shadow-sm">
      <div class="flex flex-wrap gap-6 items-center">
        <div class="flex flex-col">
          <label class="text-gray-700 font-medium mb-1 text-lg">অনুসন্ধান</label>
          <div class="relative">
            <input
              type="text"
              v-model="searchQuery"
              @keyup.enter="fetchExamSetups"
              placeholder="পরীক্ষার নাম দিয়ে অনুসন্ধান করুন..."
              class="w-72 px-4 py-2.5 border border-gray-300 rounded-sm focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white text-lg"
            />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
          </div>
        </div>
        <div class="flex flex-col">
          <label class="text-gray-700 font-medium mb-1 text-lg">কেন্দ্রীয় পরীক্ষার তালিকা</label>
          <select
            v-model="selectedClass"
            class="w-56 px-4 py-2.5 border border-gray-300 rounded-sm focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white text-lg"
          >
            <option value="">সকল পরীক্ষা</option>
            <option v-for="exam in availableExamNames" :key="exam" :value="exam">{{ exam }}</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label class="text-gray-700 font-medium mb-1 text-lg">ইয়ার</label>
          <select
            v-model="selectedYear"
            class="w-40 px-4 py-2.5 border border-gray-300 rounded-sm focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white text-lg"
          >
            <option value="">সকল বছর</option>
            <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label class="text-gray-700 font-medium mb-1 text-lg">ইংরেজি বর্ষ</label>
          <select
            v-model="selectedStatus"
            class="w-40 px-4 py-2.5 border border-gray-300 rounded-sm focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white text-lg"
          >
            <option value="">সকল অবস্থা</option>
            <option value="active">সক্রিয়</option>
            <option value="pending">অপেক্ষমান</option>
            <option value="completed">সম্পন্ন</option>
          </select>
        </div>
        <div class="flex items-end space-x-3 ml-auto">
          <button
            @click="clearFilters"
            class="bg-white border border-gray-300 text-gray-700 px-4 py-2.5 rounded-sm shadow-sm font-medium hover:bg-gray-50 transition duration-200 flex items-center text-lg"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            ফিল্টার মুছুন
          </button>
          <button
            @click="fetchExamSetups"
            class="bg-gray-800 text-white px-4 py-2.5 rounded-sm shadow-sm font-medium hover:bg-gray-700 transition duration-200 flex items-center text-lg"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            অনুসন্ধান করুন
          </button>
        </div>
      </div>
    </section>

    <!-- Table Section -->
    <main class="flex-grow mx-auto px-8 py-8 w-full">
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 overflow-hidden">
        <!-- Table Header -->
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-gray-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <h3 class="text-lg font-semibold text-gray-800">
              পরীক্ষার তালিকা <span class="text-gray-500 font-normal">({{ filteredExams.length }} টি রেকর্ড)</span>
            </h3>
          </div>
          <div class="text-lg text-gray-500">
            tahsin866 | {{ new Date().toLocaleString('bn-BD') }}
          </div>
        </div>
        <!-- Table Content -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">পরীক্ষার নাম</th>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">ক্রম</th>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">ইংরেজি বর্ষ</th>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">হিজরি বর্ষ</th>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">তারিখ/সময়</th>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">সংশোধন</th>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">নিবন্ধন সেটাপ</th>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">অন্তর্ভুক্তি সেটাপ</th>
                <th class="px-6 py-3 text-left text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">অন্যান্য সেটাপ</th>
                <th class="px-6 py-3 text-center text-lg font-medium text-gray-700 uppercase tracking-wider border-b border-gray-200">একশন</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 bg-white">
              <tr v-if="isLoading">
                <td colspan="10" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <svg class="animate-spin w-8 h-8 text-gray-500 mb-3" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <p class="text-gray-600 font-medium">ডেটা লোড হচ্ছে...</p>
                  </div>
                </td>
              </tr>
              <tr v-for="exam in paginatedExams" :key="exam.id" class="hover:bg-gray-50 transition-colors duration-150" v-else-if="!isLoading">
                <td class="px-6 py-3 text-lg font-medium text-gray-900">{{ formatExamName(exam) }}</td>
                <td class="px-6 py-3"><span class="inline-flex items-center px-2.5 py-0.5 rounded text-xl font-medium bg-gray-100 text-gray-800">{{ exam.id }}</span></td>
                <td class="px-6 py-3"><span class="inline-flex items-center px-2.5 py-0.5 rounded text-xl font-medium bg-gray-100 text-gray-800">{{ exam.english_year }}</span></td>
                <td class="px-6 py-3"><span class="inline-flex items-center px-2.5 py-0.5 rounded text-xl font-medium bg-gray-100 text-gray-800">{{ exam.arabic_year }}</span></td>
                <td class="px-6 py-3"><span class="inline-flex items-center px-2.5 py-0.5 rounded text-xl font-medium bg-gray-100 text-gray-800">{{ new Date(exam.created_at).toLocaleDateString('bn-BD') }}</span></td>
                <td class="px-6 py-3">
                  <RouterLink :to="`/central/exam/edit/${exam.id}`" class="inline-flex items-center justify-center w-7 h-7 rounded-sm bg-gray-200 text-gray-700 hover:bg-gray-300" title="সংশোধন">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </RouterLink>
                </td>
                <td  class="px-6 py-3 ">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', icon: 'pi pi-plus', command: () => onInclusionCreate() },
                      { label: 'সংশোধন', icon: 'pi pi-pencil', command: () => onEdit(exam.id) }
                    ]"
                    label="নিবন্ধন"
                    class="p-button-sm p-button-outlined bg-gray-800 text-white border-none text-xl rounded-sm"
                  />
                </td>
                <td class="px-6 py-3">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', icon: 'pi pi-plus', command: () => onInclusionCreate() },
                      { label: 'সংশোধন', icon: 'pi pi-pencil', command: () => router.push('/central/exam/FeeSetups') }
                    ]"
                    label="অন্তর্ভুক্তি"
                    class="p-button-sm p-button-outlined bg-gray-700 text-white border-none text-xl"
                  />
                </td>
                <td class="px-6 py-3">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', icon: 'pi pi-plus', command: () => onOtherCreate(exam) },
                      { label: 'সংশোধন', icon: 'pi pi-pencil', command: () => onOtherEdit(exam) }
                    ]"
                    label="অন্যান্য"
                    class="p-button-sm p-button-outlined bg-gray-600 text-white border-none text-xl"
                  />
                </td>
                <td class="px-6 py-3 text-center">
                  <button @click="deleteExam(exam.id)" class="inline-flex items-center justify-center w-7 h-7 rounded-sm bg-red-100 text-red-600 hover:bg-red-200" title="ডিলিট">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2m-5 0h6m-7 8a2 2 0 102 2 2 2 0 00-2-2z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </td>
              </tr>
              <tr v-if="!isLoading && paginatedExams.length === 0">
                <td colspan="10" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <svg class="w-16 h-16 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">
                      {{ searchQuery || selectedYear || selectedStatus || selectedClass ? 'কোনো ফলাফল পাওয়া যায়নি' : 'কোনো পরীক্ষা সেটআপ নেই' }}
                    </h3>
                    <p class="text-gray-500 mb-4 text-lg">
                      {{ searchQuery || selectedYear || selectedStatus || selectedClass ? 'আপনার ফিল্টার পরিবর্তন করে আবার চেষ্টা করুন' : 'নতুন পরীক্ষা সেটআপ তৈরি করুন' }}
                    </p>
                    <button
                      v-if="searchQuery || selectedYear || selectedStatus || selectedClass"
                      @click="clearFilters"
                      class="bg-gray-800 text-white px-4 py-2 rounded-sm hover:bg-gray-700 transition duration-200 text-lg"
                    >
                      সব ফিল্টার মুছুন
                    </button>
                    <RouterLink
                      v-else
                      to="/central/exam/create"
                      class="bg-gray-800 text-white px-4 py-2 rounded-sm hover:bg-gray-700 transition duration-200 text-lg"
                    >
                      নতুন পরীক্ষা তৈরি করুন
                    </RouterLink>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Pagination -->
        <div class="bg-gray-50 px-6 py-4 border-t border-gray-200" v-if="!isLoading && filteredExams.length > 0">
          <div class="flex items-center justify-between">
            <div class="text-lg text-gray-700">
              পেজ {{ totalPages }} টি এর মধ্যে {{ Math.min((currentPage - 1) * 10 + 1, filteredExams.length) }} - {{ Math.min(currentPage * 10, filteredExams.length) }} দেখানো হচ্ছে (মোট {{ filteredExams.length }} টি)
            </div>
            <div class="flex items-center space-x-1">
              <button
                :disabled="currentPage === 1"
                @click="previousPage"
                :class="[
                  'px-3 py-1 rounded-sm text-lg font-medium transition duration-200',
                  currentPage === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                ]"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
              </button>
              <button
                v-for="page in totalPages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'px-3 py-1 rounded-sm text-lg font-medium transition duration-200',
                  currentPage === page
                    ? 'bg-gray-800 text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                ]"
              >
                {{ page }}
              </button>
              <button
                :disabled="currentPage === totalPages"
                @click="nextPage"
                :class="[
                  'px-3 py-1 rounded-sm text-lg font-medium transition duration-200',
                  currentPage === totalPages
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                ]"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import SplitButton from 'primevue/splitbutton'

// Types
interface ExamSetup {
  id: number
  exam_name: string
  arabic_year: string
  bangla_year: string
  english_year: string
  created_at: string
  updated_at: string
}

// Router
const router = useRouter()

const onInclusionCreate = () => {
  router.push('/central/exam/FeeSetups');
};
const onEdit = (id) => {
  router.push(`/central/exam/FeeEdit/${id}`);
};
const onOtherCreate = (exam: ExamSetup) => {
  router.push(`/central/exam/${exam.id}/other/create`)
}
const onOtherEdit = (exam: ExamSetup) => {
  router.push(`/central/exam/${exam.id}/other/edit`)
}

// State
const searchQuery = ref<string>('')
const selectedClass = ref<string>('')
const selectedYear = ref<string>('')
const selectedStatus = ref<string>('')
const currentPage = ref<number>(1)
const isLoading = ref<boolean>(false)
const examList = ref<ExamSetup[]>([])

// Store all exam data for filter options
const allExamData = ref<ExamSetup[]>([])

// Fetch all exams for filter dropdown options
const fetchAllExamsForFilters = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/central-exam/exam-setups/list/')
    allExamData.value = response.data.data || []
  } catch (error) {
    console.error('Error fetching all exams for filters:', error)
  }
}

// Computed: unique years for dropdown
const availableYears = computed(() => {
  const years = new Set<string>()
  allExamData.value.forEach(exam => {
    years.add(exam.english_year)
    years.add(exam.arabic_year)
    years.add(exam.bangla_year)
  })
  return Array.from(years).sort()
})

// Computed: unique exam names for dropdown
const availableExamNames = computed(() => {
  const examNames = new Set<string>()
  allExamData.value.forEach(exam => {
    examNames.add(exam.exam_name)
  })
  return Array.from(examNames).sort()
})

// Fetch exams with filters
const fetchExamSetups = async () => {
  try {
    isLoading.value = true
    const params = new URLSearchParams()
    if (searchQuery.value.trim()) params.append('search', searchQuery.value.trim())
    if (selectedYear.value) params.append('year', selectedYear.value)
    if (selectedClass.value) params.append('exam_name', selectedClass.value)
    const url = `http://127.0.0.1:8000/api/central-exam/exam-setups/list/${params.toString() ? '?' + params.toString() : ''}`
    const response = await axios.get(url)
    examList.value = response.data.data || []
  } catch (error) {
    console.error('Error fetching exam setups:', error)
  } finally {
    isLoading.value = false
  }
}

// Computed: filtered exams (backend filtering)
const filteredExams = computed(() => examList.value)

// Pagination
const paginatedExams = computed(() => {
  const startIndex = (currentPage.value - 1) * 10
  const endIndex = startIndex + 10
  return filteredExams.value.slice(startIndex, endIndex)
})
const totalPages = computed(() => Math.ceil(filteredExams.value.length / 10))

const resetPagination = () => {
  currentPage.value = 1
}
const previousPage = (): void => {
  if (currentPage.value > 1) currentPage.value--
}
const nextPage = (): void => {
  if (currentPage.value < totalPages.value) currentPage.value++
}
const goToPage = (page: number): void => {
  currentPage.value = page
}

// Clear all filters
const clearFilters = () => {
  searchQuery.value = ''
  selectedClass.value = ''
  selectedYear.value = ''
  selectedStatus.value = ''
  currentPage.value = 1
  fetchExamSetups()
}

// Format: exam_name/arabic_year/english_year
const formatExamName = (exam: ExamSetup) => {
  return `${exam.exam_name}/${exam.arabic_year}/${exam.english_year}`
}

// Debounced search for searchQuery
let searchTimeout: ReturnType<typeof setTimeout> | null = null
const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchExamSetups()
  }, 500)
}

// Watchers
watch([searchQuery], () => {
  resetPagination()
  debouncedSearch()
})
watch([selectedYear, selectedStatus, selectedClass], () => {
  resetPagination()
  fetchExamSetups()
})

// Lifecycle
onMounted(() => {
  fetchExamSetups()
  fetchAllExamsForFilters()
})

// Delete exam
const deleteExam = async (id: number) => {
  if (confirm('আপনি কি নিশ্চিতভাবে ডিলিট করতে চান?')) {
    try {
      await axios.delete(`/api/central-exam/exam-setups/${id}/delete/`)
      examList.value = examList.value.filter(exam => exam.id !== id)
    } catch (_error) {
      alert('ডিলিট করা যায়নি!')
    }
  }
}
</script>

<style scoped>
/* Professional styling enhancements */
.transition-colors {
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

.rounded-sm {
  border-radius: 0.125rem;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* Custom focus styles for accessibility */
input:focus, select:focus, button:focus {
  outline: none;
}

/* Hover effect for table rows */
tr:hover {
  background-color: rgba(249, 250, 251, 0.8);
}

/* Pagination button styles */
button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
</style>

<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;" class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header Section -->
    <header class="bg-white shadow border-b border-gray-200 px-8 py-6 flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">কেন্দ্রীয় পরীক্ষা ম্যানেজমেন্ট</h1>
        <p class="text-lg text-gray-500 mt-1">আপনার প্রতিষ্ঠানের সকল কেন্দ্রীয় পরীক্ষার তালিকা</p>
      </div>
      <RouterLink
        to="/central/exam/Create"
        class="inline-flex items-center bg-blue-600 text-white text-lg font-semibold px-6 py-3 rounded-lg shadow hover:bg-blue-700 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-blue-300"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        নতুন পরীক্ষা যোগ করুন
      </RouterLink>
    </header>

    <!-- Filters Section -->
    <section class="bg-white border-b border-gray-200 px-8 py-6">
      <div class="flex flex-wrap gap-4 items-center">
        <div class="flex flex-col">
          <label class="text-gray-700 font-medium mb-1">অনুসন্ধান</label>
          <input
            type="text"
            v-model="searchQuery"
            @keyup.enter="fetchExamSetups"
            placeholder="পরীক্ষার নাম দিয়ে অনুসন্ধান করুন..."
            class="w-64 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          />
        </div>
        <div class="flex flex-col">
          <label class="text-gray-700 font-medium mb-1">কেন্দ্রীয় পরীক্ষার তালিকা</label>
          <select
            v-model="selectedClass"
            class="w-48 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          >
            <option value="">সকল পরীক্ষা</option>
            <option v-for="exam in availableExamNames" :key="exam" :value="exam">{{ exam }}</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label class="text-gray-700 font-medium mb-1">ইয়ার</label>
          <select
            v-model="selectedYear"
            class="w-32 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          >
            <option value="">সকল বছর</option>
            <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label class="text-gray-700 font-medium mb-1">ইংরেজি বর্ষ</label>
          <select
            v-model="selectedStatus"
            class="w-32 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          >
            <option value="">সকল অবস্থা</option>
            <option value="active">সক্রিয়</option>
            <option value="pending">অপেক্ষমান</option>
            <option value="completed">সম্পন্ন</option>
          </select>
        </div>
        <button
          @click="clearFilters"
          class="ml-auto bg-red-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-red-700 transition-colors duration-200 flex items-center"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          ফিল্টার মুছুন
        </button>
        <button
          @click="fetchExamSetups"
          class="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200 flex items-center"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          উন্নত অনুসন্ধান করুন
        </button>
      </div>
    </section>

    <!-- Table Section -->
    <main class="flex-grow mx-auto px-8 py-8 w-full ">
      <div class="bg-white rounded-xl shadow border border-gray-200 overflow-hidden">
        <!-- Table Header -->
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-gray-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <h3 class="text-lg font-semibold text-gray-900">
              পরীক্ষার তালিকা ({{ filteredExams.length }} টি রেকর্ড)
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
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">পরীক্ষার নাম</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">ক্রম</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">ইংরেজি বর্ষ</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">হিজরি বর্ষ</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">তারিখ/সময়</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">সংশোধন</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">নিবন্ধন সেটাপ</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">অন্তর্ভুক্তি সেটাপ</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">অন্যান্য সেটাপ</th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">একশন</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-if="isLoading">
                <td colspan="10" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <svg class="animate-spin w-8 h-8 text-blue-600 mb-4" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <p class="text-gray-600 text-lg">ডেটা লোড হচ্ছে...</p>
                  </div>
                </td>
              </tr>
              <tr v-for="exam in paginatedExams" :key="exam.id" class="hover:bg-gray-50 transition-colors duration-150" v-else-if="!isLoading">
                <td class="px-6 py-4 text-lg text-gray-900">{{ formatExamName(exam) }}</td>
                <td class="px-6 py-4"><span class="inline-flex items-center px-3 py-1 rounded-full text-lg font-medium bg-blue-100 text-blue-800">{{ exam.id }}</span></td>
                <td class="px-6 py-4"><span class="inline-flex items-center px-3 py-1 rounded-full text-lg font-medium bg-blue-100 text-blue-800">{{ exam.english_year }}</span></td>
                <td class="px-6 py-4"><span class="inline-flex items-center px-3 py-1 rounded-full text-lg font-medium bg-yellow-100 text-yellow-800">{{ exam.arabic_year }}</span></td>
                <td class="px-6 py-4"><span class="inline-flex items-center px-3 py-1 rounded-full text-lg font-medium bg-green-100 text-green-800">{{ new Date(exam.created_at).toLocaleDateString('bn-BD') }}</span></td>
                <td class="px-6 py-4">
                  <RouterLink :to="`/central/exam/edit/${exam.id}`" class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-orange-100 text-orange-800 hover:bg-orange-200" title="সংশোধন">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </RouterLink>
                </td>
                <td class="px-6 py-4">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', command: () => onInclusionCreate() },
                      { label: 'সংশোধন', command: () => onEdit(exam.id) }
                    ]"
                    label="নিবন্ধন সেটাপ"
                    class="p-button-secondary"
                  />
                </td>
                <td class="px-6 py-4">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', command: () => onInclusionCreate() },
                      { label: 'সংশোধন', command: () => router.push('/central/exam/FeeSetups') }
                    ]"
                    label="অন্তর্ভুক্তি সেটাপ"
                    class="p-button-secondary"
                  />
                </td>
                <td class="px-6 py-4">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', command: () => onOtherCreate(exam) },
                      { label: 'সংশোধন', command: () => onOtherEdit(exam) }
                    ]"
                    label="অন্যান্য সেটাপ"
                    class="p-button-success"
                  />
                </td>
                <td class="px-6 py-4 text-center">
                  <button @click="deleteExam(exam.id)" class="text-red-600 hover:text-red-800" title="ডিলিট">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </td>
              </tr>
              <tr v-if="!isLoading && paginatedExams.length === 0">
                <td colspan="10" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">
                      {{ searchQuery || selectedYear || selectedStatus || selectedClass ? 'কোনো ফলাফল পাওয়া যায়নি' : 'কোনো পরীক্ষা সেটআপ নেই' }}
                    </h3>
                    <p class="text-gray-500 mb-4">
                      {{ searchQuery || selectedYear || selectedStatus || selectedClass ? 'আপনার ফিল্টার পরিবর্তন করে আবার চেষ্টা করুন' : 'নতুন পরীক্ষা সেটআপ তৈরি করুন' }}
                    </p>
                    <button
                      v-if="searchQuery || selectedYear || selectedStatus || selectedClass"
                      @click="clearFilters"
                      class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                    >
                      সব ফিল্টার মুছুন
                    </button>
                    <RouterLink
                      v-else
                      to="/central/exam/create"
                      class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
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
            <div class="flex items-center space-x-2">
              <button
                :disabled="currentPage === 1"
                @click="previousPage"
                :class="[
                  'px-3 py-1 rounded-md text-lg font-medium transition-colors duration-200',
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
                  'px-3 py-1 rounded-md text-lg font-medium transition-colors duration-200',
                  currentPage === page
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                ]"
              >
                {{ page }}
              </button>
              <button
                :disabled="currentPage === totalPages"
                @click="nextPage"
                :class="[
                  'px-3 py-1 rounded-md text-lg font-medium transition-colors duration-200',
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
    allExamData.value = response.data
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
    examList.value = response.data
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

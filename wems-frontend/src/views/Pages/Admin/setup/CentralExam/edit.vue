<template>

    <div
    style="font-family: 'SolaimanLipi', sans-serif;"

    class=" bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div class=" mx-auto px-4 sm:px-6 lg:px-8">

        <!-- Success/Error Messages -->
        <div v-if="showMessage" class="mb-6">
          <div
            :class="[
              'p-4 rounded-lg border-l-4 transition-all duration-300',
              messageType === 'success'
                ? 'bg-green-50 border-green-400 text-green-800'
                : 'bg-red-50 border-red-400 text-red-800'
            ]"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg
                  v-if="messageType === 'success'"
                  class="h-5 w-5 text-green-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <svg
                  v-else
                  class="h-5 w-5 text-red-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium">{{ message }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Form Card -->
        <div class="bg-white  rounded-sm border border-gray-200 overflow-hidden">
          <!-- Card Header -->
          <div class="bg-gradient-to-r from-slate-700 to-slate-800 px-8 py-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-semibold text-white">পরীক্ষা সংশোধন করুন</h3>
                <p class="text-slate-200 text-sm">সমস্ত তথ্য সঠিকভাবে আপডেট করুন</p>
              </div>
            </div>
          </div>

          <!-- Form Content -->
          <div class="px-8 py-10">
            <!-- Loading State -->
            <div v-if="isLoading" class="flex justify-center items-center py-12">
              <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-600 mx-auto"></div>
                <p class="mt-4 text-gray-600">ডেটা লোড হচ্ছে...</p>
              </div>
            </div>

            <!-- Form -->
            <form v-else @submit.prevent="handleSubmit" class="space-y-8">
              <!-- Exam Name Section -->
              <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
                <h4 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <svg class="h-5 w-5 text-slate-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  পরীক্ষার তথ্য
                </h4>
                <div class="space-y-2">
                  <label for="examName" class="block text-sm font-semibold text-gray-700">
                    পরীক্ষার নাম
                    <span class="text-red-500 ml-1">*</span>
                  </label>
                  <input
                    id="examName"
                    v-model="form.examName"
                    type="text"
                    required
                    placeholder="উদাহরণ: ২০২৫ সালের বার্ষিক পরীক্ষা"
                    :class="[
                      'w-full px-4 py-3 border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2',
                      errors.examName
                        ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                        : 'border-gray-300 focus:ring-slate-500 focus:border-slate-500'
                    ]"
                  />
                  <p v-if="errors.examName" class="text-red-600 text-sm mt-1">{{ errors.examName }}</p>
                </div>
              </div>

              <!-- Year Information Section -->
              <div class="bg-slate-50 rounded-lg p-6 border border-gray-200">
                <h4 class="text-lg font-semibold text-gray-900 mb-6 flex items-center">
                  <svg class="h-5 w-5 text-slate-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  সাল তথ্য
                </h4>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <!-- Arabic Year (Hijri) -->
                  <div class="space-y-2">
                    <label for="arabicYear" class="block text-sm font-semibold text-gray-700">
                      আরবি সন (হিজরি)
                      <span class="text-red-500 ml-1">*</span>
                    </label>
                    <div class="relative">
                      <input
                        id="arabicYear"
                        v-model="form.arabicYear"
                        type="text"
                        required
                        placeholder="১৪৪৭"
                        :class="[
                          'w-full px-4 py-3 border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2',
                          errors.arabicYear
                            ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                            : 'border-gray-300 focus:ring-slate-500 focus:border-slate-500'
                        ]"
                      />
                      <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v6a2 2 0 002 2h2m5 0h2a2 2 0 002-2V7a2 2 0 00-2-2h-2m-5 4h4" />
                        </svg>
                      </div>
                    </div>
                    <p v-if="errors.arabicYear" class="text-red-600 text-sm">{{ errors.arabicYear }}</p>
                  </div>

                  <!-- Bangla Year -->
                  <div class="space-y-2">
                    <label for="banglaYear" class="block text-sm font-semibold text-gray-700">
                      বাংলা সন (বঙ্গাব্দ)
                      <span class="text-red-500 ml-1">*</span>
                    </label>
                    <div class="relative">
                      <input
                        id="banglaYear"
                        v-model="form.banglaYear"
                        type="text"
                        required
                        placeholder="১৪৩২"
                        :class="[
                          'w-full px-4 py-3 border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2',
                          errors.banglaYear
                            ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                            : 'border-gray-300 focus:ring-slate-500 focus:border-slate-500'
                        ]"
                      />
                      <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                        </svg>
                      </div>
                    </div>
                    <p v-if="errors.banglaYear" class="text-red-600 text-sm">{{ errors.banglaYear }}</p>
                  </div>

                  <!-- English Year -->
                  <div class="space-y-2">
                    <label for="englishYear" class="block text-sm font-semibold text-gray-700">
                      ইংরেজি সন (ঈসাব্দ)
                      <span class="text-red-500 ml-1">*</span>
                    </label>
                    <div class="relative">
                      <input
                        id="englishYear"
                        v-model="form.englishYear"
                        type="number"
                        required
                        min="2020"
                        max="2030"
                        placeholder="২০২৫"
                        :class="[
                          'w-full px-4 py-3 border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2',
                          errors.englishYear
                            ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                            : 'border-gray-300 focus:ring-slate-500 focus:border-slate-500'
                        ]"
                      />
                      <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                    </div>
                    <p v-if="errors.englishYear" class="text-red-600 text-sm">{{ errors.englishYear }}</p>
                  </div>
                </div>
              </div>



              <!-- Form Actions -->
              <div class="flex items-center justify-between pt-6 border-t border-gray-200">
                <div class="text-sm text-gray-500">
                  <span class="text-red-500">*</span> চিহ্নিত ক্ষেত্রগুলি বাধ্যতামূলক
                </div>
                <div class="flex space-x-4">
                  <button
                    type="button"
                    @click="resetForm"
                    class="px-6 py-3 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 transition-all duration-200"
                  >
                    <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    রিসেট করুন
                  </button>
                  <button
                    type="submit"
                    :disabled="isSubmitting || !isFormValid"
                    :class="[
                      'px-8 py-3 rounded-lg text-sm font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2',
                      isSubmitting || !isFormValid
                        ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                        : 'bg-slate-700 text-white hover:bg-slate-800 focus:ring-slate-500 shadow-lg hover:shadow-xl transform hover:scale-105'
                    ]"
                  >
                    <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <svg v-else class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    {{ isSubmitting ? 'আপডেট হচ্ছে...' : 'আপডেট করুন' }}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const examId = ref(route.params.id)

const isSubmitting = ref(false)
const isLoading = ref(false)
const showMessage = ref(false)
const message = ref('')
const messageType = ref('success')

const form = reactive({
  examName: '',
  arabicYear: '',
  banglaYear: '',
  englishYear: ''
})

const errors = reactive({})

const isFormValid = computed(() => {
  return !!(
    form.examName.trim() &&
    form.arabicYear.trim() &&
    form.banglaYear.trim() &&
    form.englishYear
  )
})

const validateForm = () => {
  Object.keys(errors).forEach(key => { delete errors[key] })
  let isValid = true

  if (!form.examName.trim()) {
    errors.examName = 'পরীক্ষার নাম আবশ্যক'
    isValid = false
  }

  if (!form.arabicYear.trim()) {
    errors.arabicYear = 'আরবি সন আবশ্যক'
    isValid = false
  }

  if (!form.banglaYear.trim()) {
    errors.banglaYear = 'বাংলা সন আবশ্যক'
    isValid = false
  }

  if (!form.englishYear) {
    errors.englishYear = 'ইংরেজি সন আবশ্যক'
    isValid = false
  } else {
    const year = parseInt(form.englishYear.toString())
    if (year < 2020 || year > 2030) {
      errors.englishYear = 'ইংরেজি সন ২০২০-২০৩০ এর মধ্যে হতে হবে'
      isValid = false
    }
  }
  return isValid
}

const showNotification = (msg, type) => {
  message.value = msg
  messageType.value = type
  showMessage.value = true
  setTimeout(() => { showMessage.value = false }, 5000)
}

const loadExamData = async () => {
  if (!examId.value) return

  isLoading.value = true
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/central-exam/exam-setups/${examId.value}/`
    )

    if (response.data.success) {
      const data = response.data.data
      form.examName = data.exam_name
      form.arabicYear = data.arabic_year
      form.banglaYear = data.bangla_year
      form.englishYear = data.english_year
    } else {
      showNotification('ডেটা লোড করতে সমস্যা হয়েছে', 'error')
    }
  } catch  {
    showNotification('ডেটা লোড করতে সমস্যা হয়েছে', 'error')
  } finally {
    isLoading.value = false
  }
}

const resetForm = () => {
  form.examName = ''
  form.arabicYear = ''
  form.banglaYear = ''
  form.englishYear = ''
  Object.keys(errors).forEach(key => { delete errors[key] })
}

const handleSubmit = async () => {
  if (!validateForm()) {
    showNotification('দয়া করে সমস্ত প্রয়োজনীয় ক্ষেত্র সঠিকভাবে পূরণ করুন', 'error')
    return
  }

  isSubmitting.value = true
  try {
    const response = await axios.put(
      `http://127.0.0.1:8000/api/central-exam/exam-setups/${examId.value}/update/`,
      {
        exam_name: form.examName,
        arabic_year: form.arabicYear,
        bangla_year: form.banglaYear,
        english_year: parseInt(form.englishYear.toString())
      }
    )

    if (response.status === 200) {
      showNotification('পরীক্ষা সেটাপ সফলভাবে আপডেট করা হয়েছে!', 'success')
      setTimeout(() => {
        router.push('/admin/central-exam/list')
      }, 2000)
    } else {
      throw new Error('Unexpected response')
    }
  } catch (error) {
    let errorMessage = 'দুঃখিত! কিছু সমস্যা হয়েছে। আবার চেষ্টা করুন।'
    if (error && error.response && error.response.data) {
      if (error.response.data.message) {
        errorMessage = error.response.data.message
      } else if (error.response.data.errors) {
        const serverErrors = error.response.data.errors
        if (typeof serverErrors === 'object') {
          Object.keys(serverErrors).forEach(key => {
            const fieldName =
              key === 'exam_name' ? 'examName' :
              key === 'arabic_year' ? 'arabicYear' :
              key === 'bangla_year' ? 'banglaYear' :
              key === 'english_year' ? 'englishYear' : key
            errors[fieldName] = Array.isArray(serverErrors[key])
              ? serverErrors[key][0]
              : serverErrors[key]
          })
          errorMessage = 'ফর্মে কিছু ত্রুটি রয়েছে। দয়া করে সংশোধন করুন।'
        }
      }
    }
    showNotification(errorMessage, 'error')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  loadExamData()
})
</script>


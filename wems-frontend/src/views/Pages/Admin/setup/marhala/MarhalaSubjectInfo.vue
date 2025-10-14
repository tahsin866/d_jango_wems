<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="py-12 bg-gray-100 flex flex-col items-center"
  >
    <div class="w-full mx-auto px-4">
      <div class="bg-white rounded-sm shadow-sm border border-gray-200">
        <div class="px-8 py-7">
          <!-- Title -->
          <div class="mb-10">
            <h1 class="text-2xl font-bold text-gray-800 mb-1">
              মারহালা সাবজেক্ট ইনফরমেশন
            </h1>
            <div class="text-gray-600 text-base font-medium">
              নতুন মারহালা ও কিতাব যুক্ত করুন অথবা তথ্য আপডেট করুন
            </div>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-10">
            <!-- Loading State -->
            <div v-if="loading" class="bg-gray-100 border border-gray-300 rounded-sm p-4 mb-4">
              <div class="flex items-center gap-2 text-gray-700">
                <i class="fas fa-spinner fa-spin"></i>
                <span>ডেটা সংরক্ষণ করা হচ্ছে...</span>
              </div>
            </div>

            <!-- Success Message -->
            <div v-if="successMessage" class="bg-gray-100 border border-gray-300 rounded-sm p-4 mb-4">
              <div class="flex items-center gap-2 text-gray-700">
                <i class="fas fa-check-circle"></i>
                <span>{{ successMessage }}</span>
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="bg-gray-100 border border-gray-300 rounded-sm p-4 mb-4">
              <div class="flex items-center gap-2 text-gray-700">
                <i class="fas fa-exclamation-triangle"></i>
                <span>{{ error }}</span>
              </div>
            </div>

            <!-- Marhala Info -->
            <fieldset class="border border-gray-200 rounded-sm p-6 bg-gray-50">
              <legend class="font-semibold text-gray-800 text-base px-2">মারহালা তথ্য</legend>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
                <div>
                  <label class="block text-gray-800 text-base font-semibold mb-2">
                    মারহালা নাম (বাংলা)
                  </label>
                  <input
                    type="text"
                    v-model="formData.marhala_name_bn"
                    required
                    class="block w-full border border-gray-300 rounded-sm px-3 py-2 text-gray-800 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-400 transition"
                  />
                </div>
                <div>
                  <label class="block text-gray-800 text-base font-semibold mb-2">
                    মারহালা নাম (ইংরেজি)
                  </label>
                  <input
                    type="text"
                    v-model="formData.marhala_name_en"
                    required
                    class="block w-full border border-gray-300 rounded-sm px-3 py-2 text-gray-800 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-400 transition"
                  />
                </div>
                <div>
                  <label class="block text-gray-800 text-base font-semibold mb-2">
                    মারহালা নাম (আরবি)
                  </label>
                  <input
                    type="text"
                    v-model="formData.marhala_name_ar"
                    required
                    class="block w-full border border-gray-300 rounded-sm px-3 py-2 text-gray-800 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-400 transition font-arabic"
                  />
                </div>
              </div>
            </fieldset>

            <!-- Add Subject Button -->
            <div class="flex justify-end">
              <button
                type="button"
                @click="addNewRow"
                class="inline-flex items-center px-5 py-2 border border-gray-300 rounded-sm font-semibold text-base text-gray-700 bg-white hover:bg-gray-50 transition shadow-sm"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                নতুন সাবজেক্ট
              </button>
            </div>

            <!-- Subjects Table -->
            <div class="overflow-x-auto rounded-sm bg-white border border-gray-200 shadow-sm">
              <table class="min-w-full divide-y divide-gray-200 table-auto">
                <thead class="bg-gray-50">
                  <tr>
                    <th v-for="header in subjectHeaders" :key="header"
                        class="px-5 py-3 text-left text-base font-bold text-gray-800 uppercase tracking-wider border-b border-gray-200">
                      {{ header }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(subject, index) in subjects" :key="index" class="hover:bg-gray-50 transition">
                    <td class="px-3 py-2 whitespace-nowrap">
                      <input
                        type="text"
                        v-model="subject.subject_code"
                        required
                        class="block w-full border border-gray-300 rounded-sm px-2 py-1.5 text-gray-800 bg-white focus:outline-none focus:ring-2 focus:ring-gray-400 text-base"
                        placeholder="কোড"
                      />
                    </td>
                    <td class="px-3 py-2 whitespace-nowrap">
                      <input
                        type="text"
                        v-model="subject.name_bangla"
                        required
                        class="block w-full border border-gray-300 rounded-sm px-2 py-1.5 text-gray-800 bg-white focus:outline-none focus:ring-2 focus:ring-gray-400 text-base"
                        placeholder="বাংলা নাম"
                      />
                    </td>
                    <td class="px-3 py-2 whitespace-nowrap">
                      <input
                        type="text"
                        v-model="subject.name_english"
                        required
                        class="block w-full border border-gray-300 rounded-sm px-2 py-1.5 text-gray-800 bg-white focus:outline-none focus:ring-2 focus:ring-gray-400 text-base"
                        placeholder="English Name"
                      />
                    </td>
                    <td class="px-3 py-2 whitespace-nowrap">
                      <input
                        type="text"
                        v-model="subject.name_arabic"
                        required
                        class="block w-full border border-gray-300 rounded-sm px-2 py-1.5 text-gray-800 bg-white focus:outline-none focus:ring-2 focus:ring-gray-400 text-base font-arabic"
                        placeholder="اسم الكتاب"
                      />
                    </td>
                    <td class="px-3 py-2 whitespace-nowrap">
                      <div class="flex items-center gap-3 justify-center">
                        <label v-for="(typeLabel, typeValue) in subjectStatusLabels" :key="typeValue" class="flex items-center gap-2 cursor-pointer">
                          <input
                            type="radio"
                            v-model="subject.status"
                            :value="typeValue"
                            :id="`status_${typeValue}_${index}`"
                            class="h-4 w-4 text-gray-600 focus:ring-gray-400 border-gray-300"
                          />
                          <span class="text-base text-gray-800 font-medium">{{ typeLabel }}</span>
                        </label>
                      </div>
                    </td>
                    <td class="px-3 py-2 whitespace-nowrap text-right">
                      <button
                        type="button"
                        @click="removeRow(index)"
                        class="inline-flex items-center px-3 py-1.5 bg-white border border-gray-300 rounded-sm text-base text-gray-700 font-semibold uppercase hover:bg-gray-50 transition"
                        title="এই সাবজেক্ট মুছে ফেলুন"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        ডিলিট
                      </button>
                    </td>
                  </tr>
                  <tr v-if="subjects.length === 0">
                    <td colspan="6" class="px-6 py-8 text-center text-base text-gray-600 font-medium">
                      <span>কোন সাবজেক্ট যোগ করা হয়নি</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="flex justify-end mt-8">
              <button
                type="submit"
                :disabled="loading"
                class="inline-flex items-center px-8 py-3 bg-gray-800 border border-gray-300 rounded-sm font-bold text-base text-white uppercase tracking-widest shadow-sm hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <i v-if="loading" class="fas fa-spinner fa-spin mr-2"></i>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
                </svg>
                {{ loading ? 'সংরক্ষণ করা হচ্ছে...' : 'সংরক্ষণ করুন' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const formData = ref({
  marhala_name_bn: '',
  marhala_name_en: '',
  marhala_name_ar: '',
})

const subjects = ref([
  { subject_code: '', name_bangla: '', name_english: '', name_arabic: '', status: 'both' },
  { subject_code: '', name_bangla: '', name_english: '', name_arabic: '', status: 'both' },
  { subject_code: '', name_bangla: '', name_english: '', name_arabic: '', status: 'both' },
  { subject_code: '', name_bangla: '', name_english: '', name_arabic: '', status: 'both' },
])

const loading = ref(false)
const error = ref('')
const successMessage = ref('')

const subjectHeaders = [
  'সাবজেক্ট কোড',
  'কিতাব নাম (বাংলা)',
  'কিতাব নাম (ইংরেজি)',
  'কিতাব নাম (আরবি)',
  'স্ট্যাটাস',
  'অ্যাকশন'
]

const subjectStatusLabels = {
  SRtype_1: 'ছাত্র',
  SRtype_0: 'ছাত্রী',
  both: 'উভয়'
}

function addNewRow() {
  subjects.value.push({
    subject_code: '',
    name_bangla: '',
    name_english: '',
    name_arabic: '',
    status: 'both'
  })
}

function removeRow(index) {
  subjects.value.splice(index, 1)
}

async function handleSubmit() {
  try {
    loading.value = true
    error.value = ''
    successMessage.value = ''

    if (!formData.value.marhala_name_bn.trim()) {
      error.value = 'মারহালা নাম (বাংলা) প্রয়োজন'
      return
    }
    if (!formData.value.marhala_name_en.trim()) {
      error.value = 'মারহালা নাম (ইংরেজি) প্রয়োজন'
      return
    }
    if (!formData.value.marhala_name_ar.trim()) {
      error.value = 'মারহালা নাম (আরবি) প্রয়োজন'
      return
    }

    const validSubjects = subjects.value.filter(subject =>
      subject.subject_code.trim() && subject.name_bangla.trim()
    )

    if (validSubjects.length === 0) {
      error.value = 'অন্তত একটি সাবজেক্ট যোগ করুন'
      return
    }

    const requestData = {
      marhala_name_bn: formData.value.marhala_name_bn,
      marhala_name_en: formData.value.marhala_name_en,
      marhala_name_ar: formData.value.marhala_name_ar,
      subjects: validSubjects
    }

    const response = await axios.post(
      'http://localhost:8000/api/marhalas/create-with-subjects/',
      requestData,
      {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        }
      }
    )

    if (response.data.success) {
      successMessage.value = response.data.message
      formData.value = {
        marhala_name_bn: '',
        marhala_name_en: '',
        marhala_name_ar: '',
      }
      subjects.value = [
        { subject_code: '', name_bangla: '', name_english: '', name_arabic: '', status: 'both' }
      ]
      setTimeout(() => {
        router.push('/admin/setup/marhala')
      }, 2000)
    } else {
      error.value = response.data.message || 'ডেটা সংরক্ষণে সমস্যা হয়েছে'
    }
  } catch  {
    error.value = 'সার্ভারে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Professional styling enhancements */
.transition-all {
  transition: all 0.2s ease;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.rounded-sm {
  border-radius: 0.125rem;
}

/* Custom focus styles for accessibility */
input:focus, button:focus {
  outline: none;
}

/* Hover effect for buttons and table rows */
button:hover {
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

tr:hover {
  transition: background-color 0.2s ease;
}
</style>

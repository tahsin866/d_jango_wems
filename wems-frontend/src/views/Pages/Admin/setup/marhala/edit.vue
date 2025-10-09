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
              মারহালা সাবজেক্ট সম্পাদনা
            </h1>
            <div class="text-gray-600 text-base font-medium">
              মারহালা ও কিতাবের তথ্য সম্পাদনা বা মুছে ফেলুন
            </div>
          </div>

          <form @submit.prevent="handleSubmit" @submit.stop class="space-y-10">
            <!-- Loading State -->
            <div v-if="loadingData" class="bg-gray-100 border border-gray-300 rounded-sm p-4 mb-4">
              <div class="flex items-center gap-2 text-gray-700">
                <i class="fas fa-spinner fa-spin"></i>
                <span>ডেটা লোড করা হচ্ছে...</span>
              </div>
            </div>
            <div v-else-if="loading" class="bg-gray-100 border border-gray-300 rounded-sm p-4 mb-4">
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

            <div class="flex justify-between mt-8">
              <div class="flex gap-3">
                <!-- Back Button -->
                <button
                  type="button"
                  @click="router.push('/admin/marhala/setup')"
                  class="inline-flex items-center px-6 py-3 bg-gray-100 border border-gray-300 rounded-sm font-semibold text-base text-gray-800 hover:bg-gray-200 transition"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16l-4-4m0 0l4-4m0 4h18" />
                  </svg>
                  ফিরে যান
                </button>

                <!-- Delete Button -->
                <button
                  type="button"
                  @click="deleteMarhala"
                  :disabled="loading || loadingData"
                  class="inline-flex items-center px-8 py-3 bg-gray-700 border border-gray-300 rounded-sm font-bold text-base text-white uppercase tracking-widest shadow-sm hover:bg-gray-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <i v-if="loading" class="fas fa-spinner fa-spin mr-2"></i>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  মুছে ফেলুন
                </button>
              </div>

              <!-- Update Button -->
              <button
                type="submit"
                :disabled="loading || loadingData"
                class="inline-flex items-center px-8 py-3 bg-gray-800 border border-gray-300 rounded-sm font-bold text-base text-white uppercase tracking-widest shadow-sm hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <i v-if="loading" class="fas fa-spinner fa-spin mr-2"></i>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
                </svg>
                {{ loading ? 'আপডেট করা হচ্ছে...' : 'আপডেট করুন' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

// Vue Router for navigation
const router = useRouter()
const route = useRoute()

interface Subject {
  id?: number
  subject_code: string
  name_bangla: string
  name_english: string
  name_arabic: string
  status: string
}

interface MarhalaForm {
  marhala_name_bn: string
  marhala_name_en: string
  marhala_name_ar: string
}

const marhalaId = ref<string | null>(null)
const formData = ref<MarhalaForm>({
  marhala_name_bn: '',
  marhala_name_en: '',
  marhala_name_ar: '',
})

const subjects = ref<Subject[]>([])

// Loading and error states
const loading = ref(false)
const loadingData = ref(false)
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

const subjectStatusLabels: Record<string, string> = {
  'SRtype_1': 'ছাত্র',
  'SRtype_0': 'ছাত্রী',
  'both': 'উভয়'
}

async function loadMarhalaData() {
  try {
    loadingData.value = true
    error.value = ''

    const response = await axios.get(
      `http://localhost:8000/api/marhalas/${marhalaId.value}/`,
      {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        }
      }
    )

    if (response.data.success) {
      const data = response.data.data

      formData.value = {
        marhala_name_bn: data.marhala.marhala_name_bn || '',
        marhala_name_en: data.marhala.marhala_name_en || '',
        marhala_name_ar: data.marhala.marhala_name_ar || '',
      }

      subjects.value = data.subjects || []

      if (subjects.value.length === 0) {
        addNewRow()
      }
    } else {
      error.value = response.data.message || 'ডেটা লোড করতে সমস্যা হয়েছে'
    }
  } catch (err: unknown) {
    error.value = 'সার্ভার থেকে ডেটা আনতে সমস্যা হয়েছে'
  } finally {
    loadingData.value = false
  }
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
function removeRow(index: number) {
  subjects.value.splice(index, 1)
}
async function handleSubmit(event?: Event) {
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }

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
      subjects: validSubjects.map(subject => {
        const subjectData: Record<string, unknown> = {
          subject_code: subject.subject_code,
          name_bangla: subject.name_bangla,
          name_english: subject.name_english,
          name_arabic: subject.name_arabic,
          status: subject.status
        }
        if (subject.id && typeof subject.id === 'number' && subject.id > 0) {
          subjectData.id = subject.id
        }
        return subjectData
      })
    }

    const response = await axios.put(
      `http://localhost:8000/api/marhalas/${marhalaId.value}/update/`,
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
      setTimeout(() => {
        successMessage.value = ''
      }, 3000)
    } else {
      error.value = response.data.message || 'ডেটা আপডেটে সমস্যা হয়েছে'
    }
  } catch (err: unknown) {
    error.value = 'সার্ভারে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।'
  } finally {
    loading.value = false
  }
}
async function deleteMarhala() {
  if (!confirm('আপনি কি নিশ্চিত যে এই মারহালা মুছে ফেলতে চান? এটি পূর্বাবস্থায় ফেরানো যাবে না।')) {
    return
  }
  try {
    loading.value = true
    error.value = ''
    successMessage.value = ''
    const response = await axios.delete(
      `http://localhost:8000/api/marhalas/${marhalaId.value}/delete/`,
      {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        }
      }
    )
    if (response.data.success) {
      successMessage.value = response.data.message
      setTimeout(() => {
        router.push('/admin/marhala/setup')
      }, 1000)
    } else {
      error.value = response.data.message || 'ডেটা ডিলিটে সমস্যা হয়েছে'
    }
  } catch (err: unknown) {
    error.value = 'সার্ভারে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।'
  } finally {
    loading.value = false
  }
}
onMounted(() => {
  marhalaId.value = route.params.id as string
  if (marhalaId.value) {
    loadMarhalaData()
  } else {
    error.value = 'মারহালা আইডি পাওয়া যায়নি'
  }
})
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

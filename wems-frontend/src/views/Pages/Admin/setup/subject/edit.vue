<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="min-h-screen bg-gray-100 py-12"
  >
    <div class=" mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-10">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-bold text-gray-800 mb-2">
              বিষয় সেটিংস সম্পাদনা
            </h2>
            <p class="text-base text-gray-600">
              বিষয়ের বিস্তারিত সেটিংস সম্পাদনা করুন
            </p>
          </div>
          <button
            type="button"
            @click="$router.push('/admin/setup/list')"
            class="inline-flex items-center px-5 py-2 rounded-sm bg-white border border-gray-300 text-gray-700 shadow-sm hover:bg-gray-50 transition"
          >
            <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            তালিকায় ফিরুন
          </button>
        </div>
      </div>

      <div id="flash-messages" class="mb-8"></div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white shadow-sm rounded-sm border border-gray-200">
        <div class="p-8">
          <div class="animate-pulse">
            <div class="h-5 bg-gray-200 rounded-sm w-1/4 mb-5"></div>
            <div class="h-10 bg-gray-200 rounded-sm mb-5"></div>
            <div class="h-5 bg-gray-200 rounded-sm w-1/2 mb-5"></div>
            <div class="h-10 bg-gray-200 rounded-sm mb-5"></div>
          </div>
        </div>
      </div>

      <!-- Main Form Card -->
      <div v-else class="bg-white shadow-sm rounded-sm border border-gray-200">
        <!-- Card Header -->
        <div class="bg-gray-800 px-8 py-6 rounded-t-sm flex items-center">
          <svg class="h-6 w-6 mr-2 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span class="text-xl font-semibold text-white">বিষয় সেটিংস ফর্ম</span>
        </div>

        <!-- Card Body -->
        <div class="px-8 py-10 rounded-b-sm">
          <form @submit.prevent="submit" class="space-y-10">
            <!-- Basic Information Section -->
            <div class="bg-gray-50 rounded-sm p-8 border border-gray-200">
              <h4 class="text-xl font-semibold text-gray-800 mb-8 flex items-center">
                <svg class="h-6 w-6 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                মৌলিক তথ্য
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- মারহালার নাম -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    মারহালার নাম
                  </label>
                  <div class="relative flex items-center">
                    <input
                      type="text"
                      :value="marhalaName"
                      readonly
                      class="w-full px-4 py-3 border border-gray-300 rounded-sm bg-gray-100 text-gray-700 focus:outline-none cursor-not-allowed text-base"
                    />
                    <svg class="absolute right-3 h-5 w-5 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                </div>
                <!-- বিষয় নির্বাচন করুন -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    বিষয় নির্বাচন করুন <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.subject_id"
                    :class="['w-full px-4 py-3 border rounded-sm text-base focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent transition-all duration-200', errors?.subject_id ? 'border-red-300 bg-red-50' : 'border-gray-300 bg-white']"
                  >
                    <option value="" disabled>নির্বাচন করুন</option>
                    <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                      {{ subject.name_bangla }}
                    </option>
                  </select>
                  <p v-if="errors?.subject_id" class="mt-2 text-base text-red-600">
                    {{ errors.subject_id }}
                  </p>
                </div>
                <!-- সিলেবাসের ধরন -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    সিলেবাসের ধরন <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.syllabus_type"
                    :class="['w-full px-4 py-3 border rounded-sm text-base focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent transition-all duration-200', errors?.syllabus_type ? 'border-red-300 bg-red-50' : 'border-gray-300 bg-white']"
                  >
                    <option value="" disabled>নির্বাচন করুন</option>
                    <option value="আবশ্যিক">আবশ্যিক</option>
                    <option value="নৈর্বাচনিক">নৈর্বাচনিক</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Classification Section -->
            <div class="bg-gray-50 rounded-sm p-8 border border-gray-200">
              <h4 class="text-xl font-semibold text-gray-800 mb-8 flex items-center">
                <svg class="h-6 w-6 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                শ্রেণীবিভাগ
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- মারকাযের ধরন -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    মারকাযের ধরন <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.markaz_type"
                    class="w-full px-4 py-3 border border-gray-300 rounded-sm bg-white text-base focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent transition-all duration-200"
                  >
                    <option value="" disabled>নির্বাচন করুন</option>
                    <option value="দরসিয়াত">দরসিয়াত</option>
                    <option value="হিফজুল কোরআন">হিফজুল কোরআন</option>
                    <option value="কিরাআত">কিরাআত</option>
                  </select>
                </div>
                <!-- বিষয়ের ধরন -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    বিষয়ের ধরন <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.subject_type"
                    class="w-full px-4 py-3 border border-gray-300 rounded-sm bg-white text-base focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent transition-all duration-200"
                  >
                    <option value="" disabled>নির্বাচন করুন</option>
                    <option value="মিইয়ারী">মিইয়ারী</option>
                    <option value="গায়রে মি'ইয়ারী">গায়রে মি'ইয়ারী</option>
                  </select>
                </div>
                <!-- ছাত্র/ছাত্রীর ধরন -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    ছাত্র/ছাত্রীর ধরন <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.student_type"
                    class="w-full px-4 py-3 border border-gray-300 rounded-sm bg-white text-base focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent transition-all duration-200"
                  >
                    <option value="" disabled>নির্বাচন করুন</option>
                    <option value="ছাত্র">ছাত্র</option>
                    <option value="ছাত্রী">ছাত্রী</option>
                    <option value="উভয়">উভয়</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Assessment Section -->
            <div class="bg-gray-50 rounded-sm p-8 border border-gray-200">
              <h4 class="text-xl font-semibold text-gray-800 mb-8 flex items-center">
                <svg class="h-6 w-6 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                </svg>
                মূল্যায়ন তথ্য
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- মোট মার্ক -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    মোট মার্ক <span class="text-red-500">*</span>
                  </label>
                  <div class="relative">
                    <input
                      type="number"
                      v-model="form.total_marks"
                      min="0"
                      max="1000"
                      class="w-full px-4 py-3 pr-16 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent transition-all duration-200 text-base"
                      placeholder="যেমন: ১০০"
                    />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 text-base pointer-events-none">নম্বর</span>
                  </div>
                </div>
                <!-- পাশ মার্ক -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    পাশ মার্ক <span class="text-red-500">*</span>
                  </label>
                  <div class="relative">
                    <input
                      type="number"
                      v-model="form.pass_marks"
                      min="0"
                      :max="form.total_marks || 1000"
                      class="w-full px-4 py-3 pr-16 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent transition-all duration-200 text-base"
                      placeholder="যেমন: ৪০"
                    />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 text-base pointer-events-none">নম্বর</span>
                  </div>
                  <p v-if="form.pass_marks && form.total_marks && form.pass_marks > form.total_marks"
                    class="mt-2 text-base text-red-600">
                    পাশ মার্ক মোট মার্কের চেয়ে বেশি হতে পারে না
                  </p>
                </div>
                <!-- স্ট্যাটাস -->
                <div>
                  <label class="block text-base font-semibold text-gray-700 mb-2">
                    স্ট্যাটাস <span class="text-red-500">*</span>
                  </label>
                  <div class="flex flex-col space-y-3">
                    <label class="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        v-model="form.status"
                        value="active"
                        class="h-5 w-5 text-gray-600 focus:ring-gray-500 border-gray-300"
                      />
                      <span class="ml-3 text-base text-gray-700 flex items-center">
                        <span class="w-3 h-3 bg-gray-600 rounded-full mr-2"></span>
                        সক্রিয়
                      </span>
                    </label>
                    <label class="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        v-model="form.status"
                        value="inactive"
                        class="h-5 w-5 text-gray-600 focus:ring-gray-500 border-gray-300"
                      />
                      <span class="ml-3 text-base text-gray-700 flex items-center">
                        <span class="w-3 h-3 bg-gray-500 rounded-full mr-2"></span>
                        নিষ্ক্রিয়
                      </span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="flex items-center justify-between pt-8 border-t border-gray-200">
              <div class="text-base text-gray-500">
                <span class="text-red-500">*</span> চিহ্নিত ক্ষেত্রগুলি বাধ্যতামূলক
              </div>
              <div class="flex space-x-4">
                <button
                  type="button"
                  @click="resetForm"
                  class="inline-flex items-center px-6 py-3 border border-gray-300 shadow-sm text-base font-medium rounded-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200"
                >
                  <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  রিসেট করুন
                </button>
                <button
                  type="submit"
                  :disabled="processing || !isFormValid"
                  :class="[
                    'inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-sm shadow-sm transition-all duration-200',
                    processing || !isFormValid
                      ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                      : 'bg-gray-800 text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500'
                  ]"
                >
                  <template v-if="processing">
                    <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    আপডেট হচ্ছে...
                  </template>
                  <template v-else>
                    <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    আপডেট করুন
                  </template>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()

const loading = ref(true)
const processing = ref(false)
const marhala = ref({})
const subjects = ref([])
const subjectSetting = ref({})
const errors = ref({})

const form = ref({
  marhala_id: '',
  subject_id: '',
  marhala_type: '',
  subject_names: '',
  student_type: '',
  syllabus_type: '',
  markaz_type: '',
  subject_type: '',
  subject_code: '',
  total_marks: '',
  pass_marks: '',
  status: 'active'
})

const marhalaName = computed(() => marhala.value?.marhala_name_bn || '')

const isFormValid = computed(() => {
  return form.value.subject_id &&
    form.value.syllabus_type &&
    form.value.markaz_type &&
    form.value.subject_type &&
    form.value.student_type &&
    form.value.total_marks &&
    form.value.pass_marks &&
    Number(form.value.pass_marks) <= Number(form.value.total_marks)
})

const fetchSubjectData = async () => {
  try {
    loading.value = true
    const settingsId = route.params.id

    const settingsResponse = await axios.get(`/api/subject-settings/${settingsId}/`)
    if (settingsResponse.data.success) {
      const settingData = settingsResponse.data.data.subject_setting
      subjectSetting.value = settingData

      if (settingData && settingData.marhala_id) {
        const dataResponse = await axios.get(`/api/marhala/${settingData.marhala_id}/subjects/`)
        if (dataResponse.data.success) {
          marhala.value = dataResponse.data.data.marhala
          subjects.value = dataResponse.data.data.subjects
          populateForm()
        }
      } else {
        showFlashMessage('error', 'সাবজেক্ট সেটিংস এ মারহালা তথ্য পাওয়া যায়নি।')
      }
    }
  } catch {
    showFlashMessage('error', 'তথ্য লোড করতে সমস্যা হয়েছে। পরে আবার চেষ্টা করুন।')
  } finally {
    loading.value = false
  }
}

const populateForm = () => {
  if (subjectSetting.value) {
    form.value = {
      marhala_id: subjectSetting.value.marhala_id || '',
      subject_id: subjectSetting.value.subject_id || '',
      marhala_type: subjectSetting.value.marhala_type || '',
      subject_names: subjectSetting.value.subject_names || '',
      student_type: subjectSetting.value.student_type || '',
      syllabus_type: subjectSetting.value.syllabus_type || '',
      markaz_type: subjectSetting.value.markaz_type || '',
      subject_type: subjectSetting.value.subject_type || '',
      subject_code: subjectSetting.value.subject_code || '',
      total_marks: subjectSetting.value.total_marks || '',
      pass_marks: subjectSetting.value.pass_marks || '',
      status: subjectSetting.value.status || 'active'
    }
  }
}

const showFlashMessage = (type, message) => {
  const flashContainer = document.getElementById('flash-messages')
  if (!flashContainer) return

  const flashMessage = document.createElement('div')
  const baseClasses = 'mb-6 border-l-4 p-6 rounded-r-sm relative transform transition-all duration-300 ease-in-out shadow-sm'

  if (type === 'success') {
    flashMessage.className = `${baseClasses} bg-gray-50 border-gray-400 text-gray-800`
    flashMessage.innerHTML = `
      <div class="flex items-center">
        <svg class="w-6 h-6 mr-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        <div>
          <h4 class="font-semibold text-xl">সফল!</h4>
          <p class="text-lg mt-1">${message}</p>
        </div>
      </div>
      <button class="absolute top-3 right-3 p-2 hover:bg-gray-100 rounded-sm transition-colors duration-200" onclick="this.parentElement.remove()">
        <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
        </svg>
      </button>
    `
  } else {
    flashMessage.className = `${baseClasses} bg-gray-50 border-gray-400 text-gray-800`
    flashMessage.innerHTML = `
      <div class="flex items-center">
        <svg class="w-6 h-6 mr-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <div>
          <h4 class="font-semibold text-xl">ত্রুটি!</h4>
          <p class="text-lg mt-1">${message}</p>
        </div>
      </div>
      <button class="absolute top-3 right-3 p-2 hover:bg-gray-100 rounded-sm transition-colors duration-200" onclick="this.parentElement.remove()">
        <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
        </svg>
      </button>
    `
  }

  flashContainer.appendChild(flashMessage)
  setTimeout(() => {
    if (flashMessage.parentNode) {
      flashMessage.classList.add('opacity-0', 'scale-95')
      setTimeout(() => {
        if (flashMessage.parentNode) {
          flashMessage.remove()
        }
      }, 300)
    }
  }, 5000)
}

const submit = async () => {
  try {
    processing.value = true
    errors.value = {}

    const settingsId = route.params.id
    const response = await axios.post(`/api/subject-settings/${settingsId}/update-setting/`, form.value)

    if (response.data.success) {
      showFlashMessage('success', response.data.message || 'বিষয় সেটিংস সফলভাবে আপডেট করা হয়েছে।')
      await fetchSubjectData()
    }
  } catch (error) {
    if (error && typeof error === 'object' && 'response' in error) {
      const axiosError = error
      if (axiosError.response?.data?.errors) {
        errors.value = axiosError.response.data.errors
        showFlashMessage('error', 'ফর্মে কিছু ত্রুটি রয়েছে। অনুগ্রহ করে চেক করুন।')
      } else {
        showFlashMessage('error', 'একটি ত্রুটি ঘটেছে। পরে আবার চেষ্টা করুন।')
      }
    } else {
      showFlashMessage('error', 'একটি ত্রুটি ঘটেছে। পরে আবার চেষ্টা করুন।')
    }
  } finally {
    processing.value = false
  }
}

const resetForm = () => {
  populateForm()
  errors.value = {}
}

watch(() => form.value.subject_id, (newValue) => {
  if (newValue) {
    const selectedSubject = subjects.value.find(subject => subject.id === parseInt(newValue.toString()))
    if (selectedSubject) {
      form.value.subject_names = selectedSubject.name_bangla
      form.value.subject_code = selectedSubject.subject_code
      form.value.marhala_type = marhala.value.marhala_name_bn
    }
  }
})

onMounted(() => {
  fetchSubjectData()
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
input:focus, select:focus, button:focus {
  outline: none;
}

/* Hover effect for buttons */
button:hover {
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

/* Form section styling */
.bg-gray-50 {
  background-color: #f9fafb;
}

/* Loading animation */
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}
</style>

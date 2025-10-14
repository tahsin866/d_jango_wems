<template>
  <div class=" bg-white flex items-center justify-center py-8">
    <div class="bg-white shadow-xl rounded-sm p-8 w-full max-w-md">
      <h2 class="text-2xl font-semibold text-center text-indigo-700 mb-6">📘 তালিম তারবিয়াত ফরম</h2>

      <!-- Success / Error Messages -->
      <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-2 rounded mb-4">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Name -->
        <div>
          <label class="block text-gray-700 mb-1 font-medium">নাম <span class="text-red-500">*</span></label>
          <input
            v-model="form.name"
            type="text"
            placeholder="সম্পূর্ণ নাম লিখুন"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            :class="{ 'border-red-500': touched.name && errors.name }"
          />
          <p v-if="errors.name" class="text-red-500 text-sm mt-1">{{ errors.name }}</p>
        </div>

        <!-- Father Name -->
        <div>
          <label class="block text-gray-700 mb-1 font-medium">পিতার নাম</label>
          <input
            v-model="form.father_name"
            type="text"
            placeholder="পিতার নাম লিখুন"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none"
          />
        </div>

        <!-- Mother Name -->
        <div>
          <label class="block text-gray-700 mb-1 font-medium">মাতার নাম</label>
          <input
            v-model="form.mother_name"
            type="text"
            placeholder="মাতার নাম লিখুন"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none"
          />
        </div>

        <!-- Buttons -->
        <div class="flex items-center justify-between pt-4">
          <button
            type="submit"
            :disabled="isSubmitting"
            class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-2 rounded-lg shadow-md transition-all disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <span v-if="!isSubmitting">সাবমিট</span>
            <span v-else class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
              </svg>
              প্রসেসিং...
            </span>
          </button>

          <button
            type="button"
            class="text-indigo-600 hover:underline font-medium"
            @click="resetForm"
            :disabled="isSubmitting"
          >
            রিসেট
          </button>
        </div>
      </form>

      <!-- Preview Section -->
      <div v-if="submittedData" class="mt-6 bg-gray-50 p-4 rounded-lg border border-gray-200">
        <h3 class="font-semibold text-gray-700 mb-2">সাবমিট করা ডেটা:</h3>
        <pre class="text-sm text-gray-600 whitespace-pre-wrap">{{ submittedData }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const form = reactive({
  name: '',
  father_name: '',
  mother_name: ''
})

const errors = reactive({ name: '' })
const touched = reactive({ name: false })
const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const submittedData = ref<string | null>(null)

function validate() {
  errors.name = ''
  if (!form.name || !form.name.trim()) {
    errors.name = 'নাম অবশ্যই দিতে হবে।'
  } else if (form.name.length > 100) {
    errors.name = 'নাম ১০০ অক্ষরের বেশি হতে পারবে না।'
  }
  return !errors.name
}

function resetForm() {
  form.name = ''
  form.father_name = ''
  form.mother_name = ''
  touched.name = false
  errors.name = ''
  successMessage.value = ''
  errorMessage.value = ''
  submittedData.value = null
}

async function handleSubmit() {
  touched.name = true
  if (!validate()) return

  isSubmitting.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    // API Gateway দিয়ে taleem service এ পাঠানো
    const response = await axios.post('/api/taleem/talim-tarbiat/', {
      name: form.name.trim(),
      father_name: form.father_name.trim(),
      mother_name: form.mother_name.trim()
    })

    if (response.data) {
      successMessage.value = 'তালিম তারবিয়াত ফরম সফলভাবে সাবমিট হয়েছে! ✅'
      submittedData.value = JSON.stringify(response.data, null, 2)
      resetForm()
    }
  } catch (error: any) {
    console.error('Error submitting Talim Tarbiat form:', error)

    if (error.response?.status === 401) {
      errorMessage.value = 'Authentication failed. Please login again.'
      localStorage.removeItem('token')
      router.push('/signin')
    } else if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else if (error.response?.data?.message) {
      errorMessage.value = error.response.data.message
    } else if (error.response?.data?.error) {
      errorMessage.value = error.response.data.error
    } else {
      errorMessage.value = 'তালিম তারবিয়াত ফরম সাবমিট করার সময় সমস্যা হয়েছে ❌'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

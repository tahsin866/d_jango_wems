<template>
  <div class="p-6">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">
        Create Expense Claim
      </h1>
      <p class="text-gray-600">
        Submit a new expense claim for processing
      </p>
    </div>

    <!-- Form Container -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Name Field -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
            Name <span class="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="name"
            v-model="formData.name"
            :class="[
              'w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
              errors.name ? 'border-red-500' : 'border-gray-300'
            ]"
            placeholder="Enter full name"
            required
          />
          <p v-if="errors.name" class="mt-1 text-sm text-red-600">
            {{ errors.name }}
          </p>
        </div>

        <!-- Father Name Field -->
        <div>
          <label for="father_name" class="block text-sm font-medium text-gray-700 mb-2">
            Father's Name <span class="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="father_name"
            v-model="formData.father_name"
            :class="[
              'w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
              errors.father_name ? 'border-red-500' : 'border-gray-300'
            ]"
            placeholder="Enter father's name"
            required
          />
          <p v-if="errors.father_name" class="mt-1 text-sm text-red-600">
            {{ errors.father_name }}
          </p>
        </div>

        <!-- Mother Name Field -->
        <div>
          <label for="mother_name" class="block text-sm font-medium text-gray-700 mb-2">
            Mother's Name <span class="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="mother_name"
            v-model="formData.mother_name"
            :class="[
              'w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
              errors.mother_name ? 'border-red-500' : 'border-gray-300'
            ]"
            placeholder="Enter mother's name"
            required
          />
          <p v-if="errors.mother_name" class="mt-1 text-sm text-red-600">
            {{ errors.mother_name }}
          </p>
        </div>

        <!-- Form Actions -->
        <div class="flex items-center justify-between pt-4 border-t">
          <div class="flex items-center space-x-3">
            <button
              type="submit"
              :disabled="isSubmitting"
              class="px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <span v-if="isSubmitting" class="inline-flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
              <span v-else>Submit Claim</span>
            </button>
            <button
              type="button"
              @click="resetForm"
              :disabled="isSubmitting"
              class="px-4 py-2 bg-gray-200 text-gray-800 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Reset
            </button>
          </div>
        </div>
      </form>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-green-800">
            Success
          </h3>
          <div class="mt-2 text-sm text-green-700">
            {{ successMessage }}
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">
            Error
          </h3>
          <div class="mt-2 text-sm text-red-700">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/services/auth.service'
import axios from 'axios'

const router = useRouter()
// const { user } = useAuth()

// Form data
const formData = reactive({
  name: '',
  father_name: '',
  mother_name: ''
})

// Form state
const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Form validation errors
const errors = reactive({
  name: '',
  father_name: '',
  mother_name: ''
})

// Validation function
const validateForm = (): boolean => {
  // Clear previous errors
  errors.name = ''
  errors.father_name = ''
  errors.mother_name = ''

  let isValid = true

  // Validate name
  if (!formData.name.trim()) {
    errors.name = 'Name is required'
    isValid = false
  } else if (formData.name.trim().length < 2) {
    errors.name = 'Name must be at least 2 characters long'
    isValid = false
  }

  // Validate father name
  if (!formData.father_name.trim()) {
    errors.father_name = 'Father\'s name is required'
    isValid = false
  } else if (formData.father_name.trim().length < 2) {
    errors.father_name = 'Father\'s name must be at least 2 characters long'
    isValid = false
  }

  // Validate mother name
  if (!formData.mother_name.trim()) {
    errors.mother_name = 'Mother\'s name is required'
    isValid = false
  } else if (formData.mother_name.trim().length < 2) {
    errors.mother_name = 'Mother\'s name must be at least 2 characters long'
    isValid = false
  }

  return isValid
}

// Handle form submission
const handleSubmit = async () => {
  // Clear previous messages
  successMessage.value = ''
  errorMessage.value = ''

  // Validate form
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    const response = await axios.post('/api/accounts/expense-claims/', {
      name: formData.name.trim(),
      father_name: formData.father_name.trim(),
      mother_name: formData.mother_name.trim()
    })

    if (response.data) {
      successMessage.value = 'Expense claim submitted successfully!'
      resetForm()
    }
  } catch (error: unknown) {
    console.error('Error submitting expense claim:', error)

    const axiosError = error as { response?: { status?: number, data?: { detail?: string, message?: string, error?: string } } }

    if (axiosError.response?.status === 401) {
      errorMessage.value = 'Authentication failed. Please login again.'
      localStorage.removeItem('access_token')
      router.push('/login')
    } else if (axiosError.response?.data?.detail) {
      errorMessage.value = axiosError.response.data.detail
    } else if (axiosError.response?.data?.message) {
      errorMessage.value = axiosError.response.data.message
    } else if (axiosError.response?.data?.error) {
      errorMessage.value = axiosError.response.data.error
    } else {
      errorMessage.value = 'An error occurred while submitting the expense claim'
    }
  } finally {
    isSubmitting.value = false
  }
}

// Reset form
const resetForm = () => {
  formData.name = ''
  formData.father_name = ''
  formData.mother_name = ''

  // Clear errors
  errors.name = ''
  errors.father_name = ''
  errors.mother_name = ''

  // Clear messages
  successMessage.value = ''
  errorMessage.value = ''
}
</script>

<style scoped>
/* Custom animations */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Focus styles */
input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Button transitions */
button {
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

button:active:not(:disabled) {
  transform: translateY(0);
}
</style>

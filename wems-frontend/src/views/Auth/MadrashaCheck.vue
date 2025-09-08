<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios, { AxiosError } from 'axios'

const router = useRouter()

interface ErrorDetail {
  detail?: string | Record<string, string>;
}

type MadrashaForm = {
  elhaqno: string;
  mobile: string;
}

const form = ref<MadrashaForm>({
  elhaqno: '',
  mobile: ''
})

const errors = ref<{ elhaqno?: string; mobile?: string }>({})
const processing = ref(false)
const errorFlash = ref<string | null>(null)
const loadingMessage = ref<string>('')

// Computed property to check if form is valid
const isFormValid = computed(() => {
  return form.value.elhaqno.trim().length > 0 && form.value.mobile.trim().length > 0
})

const SECRET_FRONT_KEY = import.meta.env.VITE_AES_KEY || ''

async function encryptAESGCM(plainText: string, base64Key: string) {
  const keyBuffer = Uint8Array.from(atob(base64Key), c => c.charCodeAt(0));
  const cryptoKey = await window.crypto.subtle.importKey(
    'raw',
    keyBuffer,
    { name: 'AES-GCM' },
    false,
    ['encrypt']
  );
  const iv = window.crypto.getRandomValues(new Uint8Array(12));
  const encoded = new TextEncoder().encode(plainText);
  const ciphertext = await window.crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    cryptoKey,
    encoded
  );
  return {
    ciphertext: btoa(String.fromCharCode(...new Uint8Array(ciphertext))),
    iv: btoa(String.fromCharCode(...iv))
  };
}

const submit = async () => {
  processing.value = true
  errors.value = {}
  errorFlash.value = null
  loadingMessage.value = 'মাদরাসার তথ্য খোঁজা হচ্ছে...'

  try {
    // Add performance timing
    const startTime = performance.now()

    // Encrypt data before sending (AES-GCM)
    const elhaqEnc = await encryptAESGCM(form.value.elhaqno, SECRET_FRONT_KEY)
    const mobileEnc = await encryptAESGCM(form.value.mobile, SECRET_FRONT_KEY)
    const payload = {
      elhaqno: elhaqEnc.ciphertext,
      elhaqno_iv: elhaqEnc.iv,
      mobile: mobileEnc.ciphertext,
      mobile_iv: mobileEnc.iv
    }

    loadingMessage.value = 'সার্ভারে তথ্য পাঠানো হচ্ছে...'

    const response = await axios.post('http://localhost:8000/auth/check/', payload, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 10000 // 10 second timeout
    })

    const endTime = performance.now()
    console.log(`API call took ${endTime - startTime} milliseconds`)

    // Check for successful response
    if (response.data.session) {
      loadingMessage.value = 'তথ্য পাওয়া গেছে! রিডায়রেক্ট করা হচ্ছে...'

      // Store madrasha info in localStorage
      localStorage.setItem('madrashaInfo', JSON.stringify({
        madrasha_name: response.data.session.madrasha_name,
        post: response.data.session.post,
        village: response.data.session.village,
        registration_code: response.data.session.registration_code,
        elhaqno: response.data.session.elhaqno,
        mobile: response.data.session.mobile
      }))

      // Navigate to signup page using Vue Router
      if (response.data.redirect) {
        // Use Vue Router for SPA navigation
        await router.push(response.data.redirect)
      } else {
        // Fallback to signup route
        await router.push('/signup')
      }
    }
  } catch (error) {
    const axiosError = error as AxiosError
    const data = axiosError.response?.data as ErrorDetail

    if (axiosError.code === 'ECONNABORTED') {
      errorFlash.value = 'সার্ভার রেসপন্স করতে বেশি সময় নিচ্ছে। অনুগ্রহ করে আবার চেষ্টা করুন।'
    } else if (data?.detail) {
      if (typeof data.detail === 'object') {
        errors.value = data.detail as Record<string, string>
        errorFlash.value = Object.values(data.detail).join(' | ')
      } else {
        errors.value.mobile = data.detail as string
        errorFlash.value = data.detail as string
      }
    } else {
      errorFlash.value = 'সার্ভার ইরোর! অনুগ্রহ করে পরে চেষ্টা করুন।'
    }
  } finally {
    processing.value = false
    loadingMessage.value = ''
  }
}
</script>

<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 py-4"
  >
    <div class="w-full max-w-md">
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 shadow-sm rounded-lg px-8 py-10">
        <div v-if="errorFlash" class="mb-6 px-4 py-3 rounded border border-red-200 text-red-800 bg-red-50 dark:bg-red-900/30 dark:text-red-300 text-sm text-center">
          {{ errorFlash }}
        </div>

        <!-- Loading message display -->
        <div v-if="processing && loadingMessage" class="mb-6 px-4 py-3 rounded border border-blue-200 text-blue-800 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-300 text-sm text-center">
          <svg class="animate-spin h-4 w-4 text-blue-800 dark:text-blue-300 inline mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loadingMessage }}
        </div>
        <div class="text-center mb-8">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2 tracking-tight">
            মাদরাসা তথ্য অনুসন্ধান
          </h1>
          <p class="text-gray-500 dark:text-gray-400 text-sm">
            শুধু মোবাইল নম্বর প্রদান করুন
          </p>
        </div>
        <form @submit.prevent="submit" class="space-y-6">
          <div>
            <label for="elhaqno" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">ইলহাক নম্বর</label>
            <input
              id="elhaqno"
              v-model="form.elhaqno"
              type="text"
              placeholder="ইলহাক নম্বর লিখুন"
              class="w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400 transition px-4 py-3"
              required
            />
            <div v-if="errors.elhaqno" class="text-xs text-red-600 dark:text-red-400 mt-1">
              {{ errors.elhaqno }}
            </div>
          </div>
          <div>
            <label for="mobile" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">মোবাইল নম্বর</label>
            <input
              id="mobile"
              v-model="form.mobile"
              type="text"
              placeholder="মোবাইল নম্বর লিখুন"
              class="w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400 transition px-4 py-3"
              required
            />
            <div v-if="errors.mobile" class="text-xs text-red-600 dark:text-red-400 mt-1">
              {{ errors.mobile }}
            </div>
          </div>
          <div class="flex justify-end mt-4">
            <button
              type="submit"
              class="inline-flex items-center px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded font-semibold text-base shadow-sm transition focus:outline-none focus:ring-2 focus:ring-emerald-400 disabled:opacity-70 disabled:cursor-not-allowed"
              :disabled="processing || !isFormValid"
            >
              <svg v-if="processing" class="animate-spin h-5 w-5 text-white mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              অনুসন্ধান করুন
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

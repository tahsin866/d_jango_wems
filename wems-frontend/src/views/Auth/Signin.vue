<template>
  <div
    style="                                                                    font-family: 'SolaimanLipi', sans-serif;
                                                "
    class="min-h-screen flex items-center justify-center"
  >
    <div class="w-full max-w-md">
      <div class="bg-white shadow-sm px-10 py-12">
        <!-- Logo -->
        <div class="flex justify-center mb-10">
          <!-- <div class="w-16 h-16 bg-gray-800 rounded-sm flex items-center justify-center">
            <svg class="w-10 h-10 text-white" fill="none" viewBox="0 0 48 48">
              <rect width="48" height="48" rx="4" fill="currentColor"/>
              <path d="M24 8L30 20H38L24 38L10 20H18L24 8Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            </svg>
          </div> -->
        </div>

        <!-- Header -->
        <!-- <div class="mb-8 text-center">
          <div class="relative inline-block">
            <h2 class="text-3xl font-bold text-gray-900 classic-title">লগইন</h2>
            <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-800 mt-1"></div>
          </div>
          <p class="text-gray-700 text-lg mt-3">ইমেইল বা মোবাইল নম্বর দিয়ে প্রবেশ করুন</p>
        </div> -->

        <!-- Status -->
        <!-- <div v-if="props.status" class="mb-6 px-4 py-3 rounded-sm border-2 border-gray-800 text-gray-800 bg-gray-100 text-lg shadow">
          {{ props.status }}
        </div> -->

        <!-- Form -->
        <form @submit.prevent="submit" class="space-y-6">
          <div>
            <label for="login" class="block text-lg font-bold text-gray-800 mb-2">ইমেইল বা মোবাইল নম্বর</label>
            <input
              id="login"
              type="text"
              v-model="form.login"
              autocomplete="username"
              required
              autofocus
              class="block w-full px-4 py-3 rounded-sm border-1 border-gray-800 bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-gray-800 transition"
              placeholder="example@email.com বা ০১XXXXXXXXX"
            />
            <div v-if="form.errors.login" class="text-lg text-red-700 mt-2">{{ form.errors.login }}</div>
          </div>

          <div>
            <label for="password" class="block text-lg font-bold text-gray-800 mb-2">পাসওয়ার্ড</label>
            <div class="relative">
              <input
                id="password"
                :type="showPassword ? 'text' : 'password'"
                v-model="form.password"
                autocomplete="current-password"
                required
                class="block w-full px-4 py-3 pr-12 rounded-sm border-1 border-gray-800 bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-gray-800 transition"
                placeholder="আপনার পাসওয়ার্ড লিখুন"
              />
              <button type="button"
                @click="togglePassword"
                class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-600 hover:text-gray-800 focus:outline-none"
                tabindex="-1"
                aria-label="Show/hide password"
              >
                <svg v-if="!showPassword" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.522 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.478 0-8.268-2.943-9.542-7z"/>
                </svg>
                <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a9.967 9.967 0 012.293-3.95M6.21 6.21A9.956 9.956 0 0112 5c4.478 0 8.268 2.943 9.542 7a9.977 9.977 0 01-4.293 5.95M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 3l18 18"/>
                </svg>
              </button>
            </div>
            <div v-if="form.errors.password" class="text-lg text-red-700 mt-2">{{ form.errors.password }}</div>
          </div>

          <div class="flex items-center justify-between pt-2">
            <label class="flex items-center space-x-2">
              <input
                type="checkbox"
                v-model="form.remember"
                class="h-5 w-5 border-1 border-gray-800 text-gray-800 focus:ring-gray-800 transition rounded-sm"
              />
              <span class="text-lg text-gray-800">মনে রাখুন</span>
            </label>
            <a
              v-if="props.canResetPassword"
              href="#"
              class="text-lg text-gray-800 hover:text-gray-600 underline"
            >
              পাসওয়ার্ড ভুলে গেছেন?
            </a>
          </div>

          <button
            type="submit"
            class="w-full flex justify-center items-center py-3 px-4 rounded-sm bg-gray-800 hover:bg-gray-700 text-white font-bold text-lg shadow focus:outline-none focus:ring-2 focus:ring-gray-800 focus:ring-offset-2 transition"
            :disabled="form.processing"
            :class="{ 'opacity-70 cursor-not-allowed': form.processing }"
          >
            <svg v-if="form.processing" class="animate-spin h-6 w-6 text-white mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>প্রবেশ করুন</span>
          </button>
        </form>

        <div class="mt-10 pt-6 border-t-1 border-gray-800 text-center">
          <p class="text-lg text-gray-700">
            <span>মাদরাসা একাউন্ট নেই?</span>
            <a
              href="#"
              class="ml-1 font-bold text-gray-800 hover:text-gray-600 underline"
            >
              মাদরাসা নিবন্ধন করুন
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineOptions } from 'vue'
import axios from '@/utils/axios';
import { useRouter } from 'vue-router';
import { isAdminType } from '@/utils/auth';
import { useAuthAndSidebar } from '@/composables/useAuthAndSidebar';
import type { AxiosError } from 'axios';
defineOptions({ name: 'AuthSignin' })

const props = defineProps<{
  canResetPassword: boolean
  status?: string
}>()

type LoginFormType = {
  login: string
  password: string
  remember: boolean
  errors: {
    login?: string
    password?: string
  }
  processing: boolean
}

const form = ref<LoginFormType>({
  login: '',
  password: '',
  remember: false,
  errors: {},
  processing: false
})

const showPassword = ref(false)
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const router = useRouter();

const submit = async () => {
  form.value.processing = true
  form.value.errors = {}

  try {
    const response = await axios.post('http://localhost:8000/auth/signin/', {
      email: form.value.login,
      password: form.value.password,
    }, {
      withCredentials: true
    });

    if (response.data.success) {
  // Debug: Show full backend response and redirect value
  console.log('Login Success, backend response:', response.data);
  console.log('Redirect URL:', response.data.redirect);

  // Store session token for router guard authentication
  localStorage.setItem('token', response.data.session_token);
  localStorage.setItem('user_type', response.data.user_type);
  localStorage.setItem('user_id', response.data.user_id.toString());
  localStorage.setItem('permissions', JSON.stringify(response.data.permissions || []));
  localStorage.setItem('current_user_id', response.data.user_id.toString());

  // Store department_id if available
  if (response.data.department_id) {
    localStorage.setItem('department_id', response.data.department_id.toString());
  }

  // Store user data in useAuthAndSidebar composable format
  const { storeUserData } = useAuthAndSidebar()
  storeUserData({
    id: response.data.user_id,
    name: response.data.user_name || '',
    email: form.value.login,
    department_id: response.data.department_id,
    user_type: response.data.user_type
  })

      // Login history API call (optional, backend handles this already)
      try {
        await axios.post('http://localhost:8000/users/login-history/create/', {
          user: response.data.user_id,
          status: 'success',
          ip_address: window?.location?.hostname || '',
          device: navigator?.platform || '',
          browser: navigator?.userAgent || '',
          location: '',
        }, {
          withCredentials: true
        });
      } catch {}

      const userType = response.data.user_type;

      if (response.data.redirect) {
        await router.push(response.data.redirect);
      } else if (isAdminType(userType)) {
        await router.push('/AdminDashboard');
      } else if (userType === 'Madrasah' || userType === 'madrasha') {
        await router.push('/dashboard');
      } else {
        await router.push('/signin');
      }
    } else {
      form.value.errors.login = 'Authentication failed';
    }

  } catch (error: unknown) {
    // Import AxiosError type from axios


    const axiosError = error as AxiosError;

    if (
      typeof error === 'object' &&
      error !== null &&
      'response' in error &&
      typeof axiosError.response?.status === 'number'
    ) {
      const status = axiosError.response!.status;
      if (status === 401) {
        form.value.errors.login = 'ভুল ইমেইল/মোবাইল নম্বর বা পাসওয়ার্ড';
      } else if (status === 403) {
        form.value.errors.login = 'আপনার একাউন্ট নিষ্ক্রিয়। অ্যাডমিনের সাথে যোগাযোগ করুন';
      } else if (status >= 500) {
        form.value.errors.login = 'সার্ভার ত্রুটি। পরে আবার চেষ্টা করুন';
      } else {
        form.value.errors.login = 'লগইনে ত্রুটি হয়েছে। আবার চেষ্টা করুন';
      }
    } else if (
      typeof error === 'object' &&
      error !== null &&
      'request' in error
    ) {
      form.value.errors.login = 'নেটওয়ার্ক ত্রুটি। ইন্টারনেট সংযোগ চেক করুন';
    } else {
      form.value.errors.login = 'লগইনে ত্রুটি হয়েছে। আবার চেষ্টা করুন';
    }
  } finally {
    form.value.processing = false;
    form.value.password = '';
  }
}

</script>

<style scoped>
.classic-signin-bg {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  position: relative;
}

.classic-signin-bg::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    linear-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.03) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
}

/* .classic-signin-card {
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.2);
  border-radius: 0;
  position: relative;
} */

/* .classic-signin-card::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  pointer-events: none;
  z-index: 0;
} */

.classic-signin-card > * {
  position: relative;
  z-index: 1;
}

.classic-title {
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* Classic input styling */
input[type="text"],
input[type="password"],
input[type="checkbox"] {
  transition: all 0.2s ease;
}

input[type="text"]:focus,
input[type="password"]:focus {
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
}

/* Classic button styling */
button[type="submit"] {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

button[type="submit"]::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

button[type="submit"]:hover::before {
  left: 100%;
}

/* Classic link styling */
a {
  position: relative;
  text-decoration: none;
}

a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: currentColor;
  transition: width 0.3s ease;
}

a:hover::after {
  width: 100%;
}
</style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
defineOptions({ name: 'AuthSignup' })

const route = useRoute()
const router = useRouter()

const form = ref({
  name: '',
  admin_Designation: '',
  email: '',
  password: '',
  password_confirmation: '',
  NID_no: '',
  Mobile_no: '',     // WhatsApp number
  phone: '',         // Main phone number
  photo: null,       // পাসপোর্ট সাইজ ছবি
  nid_photo: null    // ভোটার আইডি কার্ডের ছবি
})

const errors = ref<Record<string, string>>({})
const madrashaInfo = ref<{
  madrasha_name?: string;
  post?: string;
  village?: string;
  registration_code?: string;
  elhaqno?: string;
  mobile?: string;
} | null>(null)

onMounted(async () => {
  // First check for data from localStorage (fallback for existing flow)
  const info = localStorage.getItem('madrashaInfo')
  if (info) {
    const parsed = JSON.parse(info)
    madrashaInfo.value = {
      madrasha_name: parsed.madrasha_name,
      post: parsed.post,
      village: parsed.village,
      registration_code: parsed.registration_code,
      elhaqno: parsed.elhaqno,
      mobile: parsed.mobile
    }
    localStorage.removeItem('madrashaInfo')
    return
  }

  // If no localStorage data, try to get from token
  const signupToken = route.query.token as string
  if (signupToken) {
    try {
      const response = await axios.get(`http://localhost:8000/auth/validate-signup-token/?token=${signupToken}`)
      if (response.data.valid && response.data.school_data) {
        const schoolData = response.data.school_data
        madrashaInfo.value = {
          madrasha_name: schoolData.mname,
          post: schoolData.post,
          village: schoolData.village,
          registration_code: 'SC-' + Math.random().toString().substring(2, 8), // Generate new code
          elhaqno: schoolData.elhaqno,
          mobile: schoolData.mobile
        }
      }
    } catch (error) {
      console.error('Error loading school data from token:', error)
    }
  }
})

const submit = async () => {
  errors.value = {}
  if (!form.value.name) errors.value.name = 'এডমিনের নাম আবশ্যক'
  if (!form.value.email) errors.value.email = 'ইমেইল আবশ্যক'
  if (!form.value.password) errors.value.password = 'পাসওয়ার্ড আবশ্যক'
  if (form.value.password !== form.value.password_confirmation) {
    errors.value.password_confirmation = 'পাসওয়ার্ড মিলছে না'
  }
  if (!form.value.phone) errors.value.phone = 'মোবাইল নম্বর আবশ্যক'
  // ছবি ফিল্ড চেক
  if (!form.value.photo) errors.value.photo = 'পাসপোর্ট সাইজের ছবি আবশ্যক'
  if (!form.value.nid_photo) errors.value.nid_photo = 'ভোটার আইডি কার্ডের ছবি আবশ্যক'

  if (Object.keys(errors.value).length === 0) {
    const payload = {
      ...form.value,
      madrasha_name: madrashaInfo.value?.madrasha_name || null,
      post: madrashaInfo.value?.post || null,
      village: madrashaInfo.value?.village || null,
      custom_code: madrashaInfo.value?.registration_code || null
    }

    // ছবি ফাইল পাঠানো হলে FormData ব্যবহার করতে হবে (backend যদি ফাইল সাপোর্ট করে)
    const formData = new FormData()
    Object.entries(payload).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        if (key === 'photo' || key === 'nid_photo') {
          formData.append(key, value)
        } else {
          formData.append(key, value as string)
        }
      }
    })

    try {
      const response = await axios.post('http://localhost:8000/auth/signup/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        withCredentials: true
      })

      console.log('Signup response:', response.data)

      if (response.data.success) {
        // Store JWT token if provided
        if (response.data.access_token) {
          localStorage.setItem('token', response.data.access_token)
          console.log('Token stored:', response.data.access_token)
        }

        // Store user info
        if (response.data.user) {
          localStorage.setItem('user_id', response.data.user.id.toString())
          localStorage.setItem('user_type', response.data.user.user_type)
          localStorage.setItem('user_name', response.data.user.name)
        }

        alert('রেজিস্ট্রেশন সফল হয়েছে!')

        // Redirect to dashboard
        if (response.data.redirect) {
          // Use Vue Router for SPA navigation
          await router.push(response.data.redirect)
        } else {
          // Fallback to dashboard
          await router.push('/dashboard')
        }
      } else {
        alert('রেজিস্ট্রেশন ব্যর্থ হয়েছে!')
      }
    } catch (error) {
      console.error('Signup error:', error)
      alert('রেজিস্ট্রেশন ব্যর্থ হয়েছে!')
    }
    (Object.keys(form.value) as Array<keyof typeof form.value>).forEach((key: keyof typeof form.value) => {
      if (key === 'photo' || key === 'nid_photo') {
        form.value[key] = null
      } else {
        form.value[key] = ''
      }
    })
  }
}
</script>

<template>
  <div style="font-family: 'Merriweather', 'SolaimanLipi', sans-serif;" class="min-h-screen bg-[#f8f9fa] py-12">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <form @submit.prevent="submit" class="bg-white rounded-sm shadow-lg p-8" enctype="multipart/form-data">
        <div v-if="madrashaInfo" class="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-8">
          <h3 class="text-xl font-semibold text-gray-800 mb-4">মাদরাসা তথ্য</h3>
          <div class="grid grid-cols-2 gap-4 text-xl">
            <p><strong>মাদরাসার নাম:</strong> {{ madrashaInfo.madrasha_name  }}</p>
            <p><strong>গ্রাম:</strong> {{ madrashaInfo.village }}</p>
            <p><strong>পোস্ট অফিস:</strong> {{ madrashaInfo.post }}</p>
            <p><strong>রেজিস্ট্রেশন কোড:</strong> {{ madrashaInfo.registration_code }}</p>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-xl">
          <div class="space-y-6">
            <div>
              <label for="name" class="text-lg font-medium">এডমিনের নাম</label>
              <input id="name" type="text" class="mt-1 block w-full border rounded px-3 py-2" v-model="form.name" required autocomplete="name" />
              <div v-if="errors.name" class="text-sm text-red-500 mt-2">{{ errors.name }}</div>
            </div>
            <div>
              <label for="admin_Designation" class="text-lg font-medium">এডমিনের পদবি</label>
              <input id="admin_Designation" type="text" class="mt-1 block w-full border rounded px-3 py-2" v-model="form.admin_Designation" required autocomplete="admin_Designation" />
              <div v-if="errors.admin_Designation" class="text-sm text-red-500 mt-2">{{ errors.admin_Designation }}</div>
            </div>
            <div>
              <label for="NID_no" class="text-lg font-medium">জাতীয় পরিচয়পত্র নম্বর</label>
              <input id="NID_no" type="text" class="mt-1 block w-full border rounded px-3 py-2" v-model="form.NID_no" required autocomplete="NID_no" />
              <div v-if="errors.NID_no" class="text-sm text-red-500 mt-2">{{ errors.NID_no }}</div>
            </div>
            <div>
              <label for="Mobile_no" class="text-lg font-medium">হোয়াটস এপ নম্বর</label>
              <input id="Mobile_no" type="text" class="mt-1 block w-full border rounded px-3 py-2" v-model="form.Mobile_no" required autocomplete="Mobile_no" />
              <div v-if="errors.Mobile_no" class="text-sm text-red-500 mt-2">{{ errors.Mobile_no }}</div>
            </div>
            <div>
              <label for="phone" class="text-lg font-medium">মোবাইল নম্বর</label>
              <input id="phone" type="text" class="mt-1 block w-full border rounded px-3 py-2" v-model="form.phone" required autocomplete="phone" />
              <div v-if="errors.phone" class="text-sm text-red-500 mt-2">{{ errors.phone }}</div>
            </div>
            <div>
              <label for="photo" class="text-lg font-medium">নিজের পাসপোর্ট সাইজের ছবি</label>
              <input id="photo" type="file" accept="image/*" @change="form.photo = $event.target.files[0]" class="mt-1 block w-full border rounded px-3 py-2" />
              <div v-if="form.photo" class="mt-2">
                <img :src="URL.createObjectURL(form.photo)" alt="ছবি" class="h-20 rounded border" />
              </div>
              <div v-if="errors.photo" class="text-sm text-red-500 mt-2">{{ errors.photo }}</div>
            </div>
            <div>
              <label for="nid_photo" class="text-lg font-medium">ভোটার আইডি কার্ডের ছবি</label>
              <input id="nid_photo" type="file" accept="image/*" @change="form.nid_photo = $event.target.files[0]" class="mt-1 block w-full border rounded px-3 py-2" />
              <div v-if="form.nid_photo" class="mt-2">
                <img :src="URL.createObjectURL(form.nid_photo)" alt="ভোটার আইডি" class="h-20 rounded border" />
              </div>
              <div v-if="errors.nid_photo" class="text-sm text-red-500 mt-2">{{ errors.nid_photo }}</div>
            </div>
          </div>
          <div class="space-y-6">
            <div>
              <label for="email" class="text-lg font-medium">ইমেইল</label>
              <input id="email" type="email" class="mt-1 block w-full border rounded px-3 py-2" v-model="form.email" required autocomplete="username" />
              <div v-if="errors.email" class="text-sm text-red-500 mt-2">{{ errors.email }}</div>
            </div>
            <div>
              <label for="password" class="text-lg font-medium">পাসওয়ার্ড দিন</label>
              <input id="password" type="password" class="mt-1 block w-full border rounded px-3 py-2" v-model="form.password" required autocomplete="new-password" />
              <div v-if="errors.password" class="text-sm text-red-500 mt-2">{{ errors.password }}</div>
            </div>
            <div>
              <label for="password_confirmation" class="text-lg font-medium">পুনরায় পাসওয়ার্ড দিন</label>
              <input id="password_confirmation" type="password" class="mt-1 block w-full border rounded px-3 py-2" v-model="form.password_confirmation" required autocomplete="new-password" />
              <div v-if="errors.password_confirmation" class="text-sm text-red-500 mt-2">{{ errors.password_confirmation }}</div>
            </div>
          </div>
        </div>
        <div class="mt-8 pt-6 border-t border-gray-200 flex items-center justify-end space-x-4">
          <a href="/admin/login" class="text-emerald-600 hover:text-emerald-800 font-medium transition-colors">Already registered?</a>
          <button type="submit" class="px-6 py-2.5 bg-emerald-600 text-white font-semibold rounded hover:bg-emerald-700 transition disabled:opacity-25">Register</button>
        </div>
      </form>
    </div>
  </div>
</template>

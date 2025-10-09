<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="fixed inset-0 flex items-center justify-center z-50"
  >
    <form @submit.prevent="save" class="bg-white rounded-lg shadow-lg p-8 w-full max-w-3xl">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Name -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">নাম</label>
          <input v-model="form.name" placeholder="নাম" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200" />
        </div>

        <!-- Profile Image Upload -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">ছবি</label>
          <input type="file" accept="image/*" @change="onImageChange" class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700" />
          <div v-if="form.profile_image" class="mt-2">
            <img :src="form.profile_image" alt="Profile" class="h-16 w-16 object-cover rounded-lg border" />
          </div>
        </div>

        <!-- Email -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">ইমেইল</label>
          <input v-model="form.email" placeholder="ইমেইল" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200" />
        </div>

        <!-- Phone -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">মোবাইল</label>
          <input v-model="form.phone" placeholder="মোবাইল" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200" />
        </div>

        <!-- Birth Certificate/NID -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">নিবন্ধন/এনআইডি</label>
          <select v-model="form.id_type" class="w-full border border-gray-300 rounded px-3 py-2 mb-2 focus:outline-none focus:ring focus:ring-blue-200">
            <option disabled value="">নিবন্ধন/এনআইডি নির্বাচন করুন</option>
            <option value="nid">NID</option>
            <option value="birth">জন্মনিবন্ধন</option>
          </select>
          <input v-model="form.id_number" :placeholder="form.id_type === 'nid' ? 'এনআইডি নম্বর' : 'জন্মনিবন্ধন নম্বর'" required class="w-full border border-gray-300 rounded px-3 py-2 mb-2 focus:outline-none focus:ring focus:ring-blue-200" />
          <label class="block mb-1 font-medium text-gray-700">ফাইল এটাচ (NID/Birth)</label>
          <input type="file" @change="onIdFileChange" class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700" />
          <div v-if="form.id_file" class="mt-2">
            <a :href="form.id_file" target="_blank" class="text-blue-600 underline">Attachment preview</a>
          </div>
        </div>

        <!-- Role -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">রোল</label>
          <select v-model="form.role" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200">
            <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
          </select>
        </div>

        <!-- Department -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">ডিপার্টমেন্ট</label>
          <select v-model="form.department" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200">
            <option value="">ডিপার্টমেন্ট নির্বাচন করুন</option>
            <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
          </select>
        </div>

        <!-- Password -->
        <div class="md:col-span-2">
          <label class="block mb-1 font-medium text-gray-700">পাসওয়ার্ড</label>
          <input v-model="form.password" type="password" placeholder="পাসওয়ার্ড সেট করুন" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200" />
        </div>
        <!-- Confirm Password -->
        <div class="md:col-span-2">
          <label class="block mb-1 font-medium text-gray-700">কনফার্ম পাসওয়ার্ড</label>
          <input v-model="form.confirmPassword" type="password" placeholder="পাসওয়ার্ড পুনরায় লিখুন" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200" />
          <span v-if="passwordError" class="text-red-600 text-sm mt-1">{{ passwordError }}</span>
        </div>
      </div>
      <div class="flex flex-col md:flex-row justify-end space-y-3 md:space-y-0 md:space-x-3 pt-8">
        <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-5 py-2 rounded font-semibold shadow">Save</button>
        <button type="button" @click="$emit('close')" class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-5 py-2 rounded font-semibold shadow">Cancel</button>
        <!-- SET PERMISSIONS BUTTON -->
        <button type="button"
          @click="$emit('set-permission', form)"
          class="bg-green-500 hover:bg-green-600 text-white px-5 py-2 rounded font-semibold shadow"
        >
          সেট পারমিশন
        </button>
      </div>
    </form>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from 'vue'
const props = defineProps(['roles', 'departments', 'user', 'permissions'])
const emit = defineEmits(['save', 'close', 'set-permission'])

const passwordError = ref("")

const form = reactive(props.user ? { ...props.user, confirmPassword: '' } : {
  name: '',
  email: '',
  phone: '',
  profile_image: '',
  id_type: '',
  id_number: '',
  id_file: '',
  role: null,
  department: null,
  password: '',
  confirmPassword: '',
  permissions: []
})

function onImageChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => { form.profile_image = reader.result as string }
    reader.readAsDataURL(file)
  }
}

function onIdFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => { form.id_file = reader.result as string }
    reader.readAsDataURL(file)
  }
}

function save() {
  passwordError.value = ""
  if (form.password !== form.confirmPassword) {
    passwordError.value = "পাসওয়ার্ড ও কনফার্ম পাসওয়ার্ড মিলছে না!"
    return
  }
  emit('save', form)
}
</script>

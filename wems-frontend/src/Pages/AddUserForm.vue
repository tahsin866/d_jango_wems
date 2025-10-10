<template>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
    <h2 class="text-xl font-bold mb-4">Add User</h2>
    <form @submit.prevent="submitForm">
      <div class="mb-4">
        <label class="block mb-1">Name</label>
        <input v-model="name" type="text" class="w-full border rounded px-2 py-1" required />
      </div>
      <div class="mb-4">
        <label class="block mb-1">Email</label>
        <input v-model="email" type="email" class="w-full border rounded px-2 py-1" required />
      </div>
      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
    </form>
    <div v-if="message" class="mt-4 text-green-600">{{ message }}</div>
    <div v-if="error" class="mt-4 text-red-600">{{ error }}</div>
  </div>
  <UserTable />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import UserTable from './UserTable.vue'

const name = ref('')
const email = ref('')
const message = ref('')
const error = ref('')

const submitForm = async () => {
  message.value = ''
  error.value = ''
  try {
  const res = await fetch('http://localhost:8000/tahsin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name.value, email: email.value })
    })
    const data = await res.json()
    if (data.id) {
      message.value = 'User added successfully!'
      name.value = ''
      email.value = ''
    } else {
      error.value = data.error || 'Failed to add user.'
    }
  } catch {
    error.value = 'Server error.'
  }
}
</script>

<style scoped>
/* Simple styling */
</style>

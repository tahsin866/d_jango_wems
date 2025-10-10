<template>
  <form @submit.prevent="saveDepartment">
    <input v-model="form.name" placeholder="ডিপার্টমেন্ট নাম" required />
    <button type="submit">Save</button>
  </form>
</template>
<script setup>
import { reactive } from 'vue'
const emit = defineEmits(['save'])
const form = reactive({ name: '' })
function saveDepartment() {
  emit('save', form)
}
</script>

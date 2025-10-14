<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="flex gap-2 mb-4">
    <button
      v-for="dept in departments"
      :key="dept.id"
      :class="[
        'px-4 py-2 rounded border transition-colors',
        dept.id === modelValue?.id
          ? 'bg-blue-500 text-white border-blue-500 font-bold'
          : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
      ]"
      @click="$emit('update:modelValue', dept)"
    >
      {{ dept.name }}
    </button>
    <button
      :class="[
        'px-4 py-2 rounded border transition-colors',
        !modelValue
          ? 'bg-blue-500 text-white border-blue-500 font-bold'
          : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
      ]"
      @click="$emit('update:modelValue', null)"
    >
      সব ইউজার
    </button>
  </div>
</template>
<script setup lang="ts">
interface Department {
  id: number
  name: string
}

defineProps<{
  departments: Department[]
  modelValue: Department | null
}>()

defineEmits<{
  'update:modelValue': [value: Department | null]
}>()
</script>

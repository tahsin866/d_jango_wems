<template>
  <div class="mt-6 p-4 rounded-md border border-slate-200 bg-gray-50 dark:bg-slate-800 dark:border-slate-700">
    <div class="flex justify-between items-start">
      <div>
        <h3 class="text-lg font-bold">{{ agreement.main_madrasa }}</h3>
        <p class="text-sm text-slate-500">{{ agreement.exam_name }} — {{ formatDate(agreement.application_date) }}</p>
      </div>
      <div>
        <button @click="$emit('close')" class="px-3 py-1 rounded bg-slate-100">Close</button>
      </div>
    </div>

    <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <h4 class="font-semibold">মারকাজ ধরন</h4>
        <p>{{ agreement.markaz_type }}</p>
      </div>
      <div>
        <h4 class="font-semibold">মোট ছাত্র</h4>
        <p>{{ agreement.main_total_students + agreement.associated_total_students }}</p>
      </div>

      <div class="md:col-span-2">
        <h4 class="font-semibold">সংযুক্ত মাদরাসা</h4>
        <ul class="mt-2 space-y-2">
          <li v-for="(m, i) in agreement.associated_madrasas" :key="i" class="flex items-center gap-3">
            <span class="inline-block w-6 h-6 rounded bg-slate-200 flex items-center justify-center">{{ i + 1 }}</span>
            <span>{{ m }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  agreement: Object
})
// defineEmits(['close']) is not needed since $emit is used in the template

function formatDate(dateStr) {
  if (!dateStr) return ''
  const parts = dateStr.split('-')
  return `${parts[2]}/${parts[1]}/${parts[0]}`
}
</script>

<style scoped>
/* inline details styling */
</style>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
    <div v-for="label in cardOrder" :key="label"
         class="relative group bg-white dark:bg-slate-800 rounded-lg shadow-lg overflow-hidden
                transform transition-transform duration-300 hover:-translate-y-1
             ">
      <div class="p-6 flex flex-col items-start">
        <div class="w-12 h-12 flex items-center justify-center rounded-full bg-gradient-to-br from-indigo-500 to-indigo-600 dark:from-indigo-600 dark:to-indigo-700 text-white mb-4 shadow-md transition-all duration-300 group-hover:scale-110">
          <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path v-if="label === 'total'" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z" fill="currentColor"/>
            <path v-else-if="label === 'pending'" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zM13 7h-2v6h2V7zM13 15h-2v2h2v-2z" fill="currentColor"/>
            <path v-else-if="label === 'submitted'" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM12 14v4h-4v-4h4zM16 14v4h-4v-4h4zM12 4.5L16.5 9H12V4.5z" fill="currentColor"/>
            <path v-else-if="label === 'processing'" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zM13.5 9H12V7h1.5v2zM12 11.5V13h2V11.5h-2zM12 14.5V16h1.5v-1.5H12z" fill="currentColor"/>
            <path v-else-if="label === 'approved'" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" fill="currentColor"/>
            <path v-else-if="label === 'rejected'" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" fill="currentColor"/>
          </svg>
        </div>
        <div class="space-y-1">
          <p class="text-sm font-semibold uppercase text-slate-500 dark:text-slate-400 tracking-wider">{{ labelMap[label] }}</p>
          <h3 class="text-4xl font-extrabold text-slate-900 dark:text-white transition-colors duration-300 group-hover:text-indigo-600 dark:group-hover:text-indigo-400">{{ statsMap[label] }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ stats: Record<string, number> }>();
const labelMap: Record<string, string> = {
  total: 'মোট আবেদন',
  pending: 'খসড়া',
  submitted: 'দাখিলকৃত',
  processing: 'প্রক্রিয়াধীন',
  approved: 'অনুমোদিত',
  rejected: 'ফেরত'
};
const cardOrder = ['total', 'pending', 'submitted', 'processing', 'approved', 'rejected'];
const statsMap = props.stats || { total: 0, pending: 0, submitted: 0, processing: 0, approved: 0, rejected: 0 };
</script>

<style scoped>
/* You can add custom styles here if needed, but Tailwind CSS handles most of the design */
</style>

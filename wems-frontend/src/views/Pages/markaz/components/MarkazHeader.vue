<template>
  <div class="bg-white dark:bg-slate-800  border-gray-200 dark:border-slate-700 p-6">
    <div class="mx-auto px-2 lg:px-8">
      <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
        <div class="flex items-start gap-5">
          <div class="bg-slate-50 dark:bg-slate-700 p-4 rounded-md shadow-sm border border-gray-100 dark:border-slate-700">
            <svg class="w-8 h-8 text-slate-800 dark:text-slate-100" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M4 6h16v12H4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M8 10h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>

          <div>
            <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">{{ examName }}</h1>
            <p class="text-sm text-slate-500 dark:text-slate-300 mt-1">মারকাজ আবেদন তালিকা পরিচালনা করুন</p>
          </div>
        </div>

        <div class="flex items-center gap-3 w-full lg:w-auto">
          <div class="relative flex-1 lg:flex-none lg:w-80">
            <input
              v-model="localQuery"
              @input="$emit('update:searchQuery', localQuery)"
              type="search"
              placeholder="মাদরাসা বা পরীক্ষার নাম খুঁজুন..."
              class="pl-10 pr-4 py-2.5 rounded-md border bg-white text-slate-800 placeholder-slate-400 w-full text-sm shadow-sm
                     dark:bg-slate-700 dark:text-slate-100 dark:placeholder-slate-500 dark:border-slate-600"
              aria-label="Search madrasah or exam"
            />
            <svg class="w-4 h-4 absolute left-3 top-3 text-slate-400 dark:text-slate-400" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M21 21l-6-6" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M11 19a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>

          <button
            @click="$emit('refresh')"
            class="px-3 py-2 rounded-sm bg-slate-100 hover:bg-slate-200 text-slate-700 text-md border
                   dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-slate-200 dark:border-slate-600"
            aria-label="Refresh"
          >
            Refresh
          </button>

          <button
            @click="$emit('create')"
            class="px-4 py-2 rounded-sm bg-emerald-600 text-white text-md shadow-sm hover:bg-emerald-700
                   dark:bg-emerald-500 dark:hover:bg-emerald-600"
            aria-label="Create new application"
          >
            নতুন আবেদন
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{ examName?: string; searchQuery?: string }>();
const emit = defineEmits<{
  (e: 'update:searchQuery', value: string): void;
  (e: 'refresh'): void;
  (e: 'create'): void;
}>();

const localQuery = ref<string>(props.searchQuery ?? '');

watch(
  () => props.searchQuery,
  (v) => {
    localQuery.value = v ?? '';
  }
);
</script>

<style scoped>
/* Visuals driven by Tailwind utility classes with dark: variants applied in template */
</style>

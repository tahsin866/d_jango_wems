<template>
  <div class="bg-white dark:bg-slate-900 rounded-md shadow-lg border border-slate-200 dark:border-slate-800">
    <div v-if="props.loading" class="flex items-center justify-center p-20 text-indigo-500">
      <svg class="animate-spin h-12 w-12" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <div v-else>
      <div v-if="props.filtered.length === 0" class="py-20 text-center text-slate-500 dark:text-slate-400 font-medium text-lg">
        কোন রেকর্ড পাওয়া যায়নি
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full table-auto">
          <thead class="bg-slate-50 dark:bg-slate-800/50">
            <tr class="text-xl text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              <th class="py-4 px-6 text-left font-semibold">#</th>
              <th class="py-4 px-6 text-left font-semibold">তারিখ</th>
              <th class="py-4 px-6 text-left font-semibold">ধরন</th>
              <th class="py-4 px-6 text-left font-semibold">মাদরাসা</th>
              <th class="py-4 px-6 text-left font-semibold">পরীক্ষা</th>
              <th class="py-4 px-6 text-center font-semibold">ছাত্র</th>
              <th class="py-4 px-6 text-center font-semibold">স্ট্যাটাস</th>
              <th class="py-4 px-6 text-center font-semibold">কর্ম</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
            <tr v-for="(item, index) in props.filtered" :key="item.id"
                class="hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors duration-200">
              <td class="py-4 px-6 text-xl text-slate-600 dark:text-slate-400">{{ index + 1 }}</td>
              <td class="py-4 px-6 text-xl font-medium text-slate-900 dark:text-slate-100">{{ formatDate(item.application_date) }}</td>
              <td class="py-4 px-6 text-xl">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xl font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300">
                  {{ item.markaz_type }}
                </span>
              </td>
              <td class="py-4 px-6 text-xl text-slate-600 dark:text-slate-400">{{ item.main_madrasa }}</td>
              <td class="py-4 px-6 text-xl text-slate-600 dark:text-slate-400">{{ item.exam_name }}</td>
              <td class="py-4 px-6 text-xl text-center font-medium text-slate-700 dark:text-slate-300">
                {{ item.main_total_students + item.associated_total_students }}
              </td>
              <td class="py-4 px-6 text-xl text-center">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xl font-semibold"
                      :class="statusClass(item.status)">
                  {{ getStatusLabel(item.status) }}
                </span>
              </td>
              <td class="py-4 px-6 text-xl text-center">
                <div class="flex items-center justify-center space-x-2">
                  <SplitButton
                    :model="getMenuItems(item)"
                    label="বিস্তারিত"
                    icon="pi pi-eye"
                    class="p-button-sm rounded-md px-4 py-2"
                    :menuStyle="splitMenuStyle"
                    @click="onView(item)"
                  />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SplitButton from 'primevue/splitbutton';
import { defineProps, defineEmits, reactive } from 'vue';
import type { Agreement } from '@/views/Pages/markaz/composable/useAgreements';

const props = defineProps<{
  loading: boolean;
  agreements?: Agreement[];
  filtered: Agreement[];
}>();

const emit = defineEmits<{
  (e: 'view', item: Agreement): void;
  (e: 'edit', item: Agreement): void;
  (e: 'delete', item: Agreement): void;
  (e: 'submit', item: Agreement): void;
}>();

const splitMenuStyle = reactive<Record<string, string>>({
  background: 'var(--menu-bg, #ffffff)',
  color: 'var(--menu-text, #0f172a)',
  border: '1px solid rgba(15,23,42,0.06)',
  minWidth: '150px'
});

const onView = (item: Agreement) => emit('view', item);

function getMenuItems(item: Agreement) {
  return [
    {
      label: 'সম্পাদনা',
      icon: 'pi pi-pencil',
      command: () => emit('edit', item)
    },
    {
      label: 'মুছুন',
      icon: 'pi pi-trash',
      command: () => emit('delete', item)
    },
    {
      separator: true
    },
    {
      label: 'দাখিল করুন',
      icon: 'pi pi-send',
      command: () => emit('submit', item)
    }
  ];
}

function formatDate(dateStr: string) {
  if (!dateStr) return '';
  const parts = dateStr.split('-');
  return `${parts[2]}/${parts[1]}/${parts[0]}`;
}

function getStatusLabel(status: string) {
  switch (status) {
    case 'pending':
      return 'খসড়া';
    case 'submitted':
      return 'দাখিলকৃত';
    case 'processing':
      return 'প্রক্রিয়াধীন';
    case 'approved':
      return 'অনুমোদিত';
    case 'rejected':
      return 'ফেরত';
    default:
      return 'অজানা';
  }
}

function statusClass(status: string) {
  switch (status) {
    case 'pending':
      return 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300';
    case 'submitted':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300';
    case 'processing':
      return 'bg-purple-100 text-purple-800 dark:bg-purple-900/40 dark:text-purple-300';
    case 'approved':
      return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300';
    case 'rejected':
      return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-800/50 dark:text-gray-300';
  }
}
</script>

<style scoped>
:root.dark {
  --menu-bg: #0f172a;
  --menu-text: #e2e8f0;
}
</style>

<template>
  <div class="mx-auto mt-10">
    <!-- Card -->
    <div class="bg-white dark:bg-slate-900 rounded-sm shadow-2xl border border-slate-200 dark:border-slate-800">
      <!-- Card Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-slate-200 dark:border-slate-800">
        <h2 class="text-2xl font-bold text-slate-700 dark:text-slate-100">
          মারকায আবেদন তালিকা
        </h2>
        <!-- Search (Demo) -->
        <div class="flex items-center gap-2">
          <input
            type="text"
            placeholder="খুঁজুন..."
            class="border border-slate-300 dark:border-slate-700 rounded-sm px-3 py-2 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-300"
          />
          <button class="px-3 py-2 bg-indigo-600 text-white rounded-sm font-semibold hover:bg-indigo-700 transition">
            খুঁজুন
          </button>
          <!-- PDF Download Button -->
          <button
            class="px-3 py-2 ml-2 border border-gray-300 rounded-sm bg-white text-gray-700 font-bold shadow hover:bg-gray-100 transition flex items-center gap-2"
            @click="downloadPDF"
          >
            <i class="fas fa-file-pdf text-red-500"></i>
            PDF ডাউনলোড
          </button>
        </div>
      </div>

      <!-- Loading Spinner -->
      <div v-if="props.loading" class="flex items-center justify-center py-20 text-indigo-500">
        <svg class="animate-spin h-12 w-12" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>

      <!-- Table -->
      <div v-else>
        <div v-if="props.filtered.length === 0" class="py-20 text-center text-slate-500 dark:text-slate-400 font-medium text-lg">
          কোন রেকর্ড পাওয়া যায়নি
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full table-auto">
            <thead>
              <tr class="bg-slate-100 dark:bg-slate-800/80 text-base font-bold text-slate-600 dark:text-slate-300 border-b border-slate-200 dark:border-slate-700">
                <th class="py-4 px-6 text-left">#</th>
                <th class="py-4 px-6 text-left">তারিখ</th>
                <th class="py-4 px-6 text-left">ধরন</th>
                <th class="py-4 px-6 text-left">মাদরাসা</th>
                <th class="py-4 px-6 text-left">পরীক্ষা</th>
                <th class="py-4 px-6 text-center">ছাত্র</th>
                <th class="py-4 px-6 text-center">স্ট্যাটাস</th>
                <th class="py-4 px-6 text-center">কর্ম</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in props.filtered" :key="item.id"
                class="hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors duration-150 border-b border-slate-100 dark:border-slate-800">
                <td class="py-3 px-6 text-slate-700 dark:text-slate-100 font-medium">{{ index + 1 }}</td>
                <td class="py-3 px-6 text-slate-700 dark:text-slate-100">{{ formatDate(item.application_date) }}</td>
                <td class="py-3 px-6">
                  <span class="px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-semibold">
                    {{ item.markaz_type }}
                  </span>
                </td>
                <td class="py-3 px-6 text-slate-700 dark:text-slate-100">
                  <div>
                    <span class="font-bold">{{ item.main_madrasa }}</span>
                  </div>
                  <div v-if="item.associated_madrasas && item.associated_madrasas.length">
                    <span class="text-xl text-slate-500">সংযুক্ত  মাদরাসা:</span>
                    <select class="ml-2 px-2 py-1 rounded border text-xs text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-800">
                      <option v-for="(assoc, idx) in item.associated_madrasas" :key="idx">{{ assoc }}</option>
                    </select>
                  </div>
                </td>
                <td class="py-3 px-6 text-slate-700 dark:text-slate-100">{{ item.exam_name }}</td>
                <td class="py-3 px-6 text-center font-semibold text-slate-900 dark:text-slate-100">
                  <div>
                    <span class="text-xs">মুল মাদরাসা: </span>
                    <span class="font-bold">{{ item.main_total_students }}</span>
                  </div>
                  <div>
                    <span class="text-xs">সংযুক্ত মাদরাসা: </span>
                    <span class="font-bold">{{ item.associated_total_students }}</span>
                  </div>
                </td>
                <td class="py-3 px-6 text-center">
                  <span class="inline-block px-3 py-1 rounded text-sm font-bold"
                    :class="statusClass(item.status)">
                    {{ getStatusLabel(item.status) }}
                  </span>
                </td>
                <td class="py-3 px-6 text-center">
                  <div
                    style="font-family: 'SolaimanLipi', sans-serif;"
                    class="flex items-center justify-center"
                  >
                    <SplitButton
                      :model="getMenuItems(item)"
                      label="বিস্তারিত"
                      icon="pi pi-eye"
                      class="p-0.5 px-4 py-3 text-xl text-slate-700 dark:text-slate-200 transition"
                      :menuStyle="splitMenuStyle"
                      @click="openPanel(item)"
                    />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <!-- Pagination (Demo) -->
          <div class="flex flex-col gap-2 px-6 py-4 bg-slate-50 dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
            <div class="flex items-center justify-between">
              <span class="text-slate-500 dark:text-slate-400">১-১০ / মোট {{ props.filtered.length }} টি</span>
              <div class="flex gap-2">
                <button class="px-2 py-1 rounded bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-indigo-100 hover:text-indigo-600 dark:hover:bg-indigo-700 dark:hover:text-indigo-100 transition">←</button>
                <button class="px-2 py-1 rounded bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-indigo-100 hover:text-indigo-600 dark:hover:bg-indigo-700 dark:hover:text-indigo-100 transition">→</button>
              </div>
            </div>
            <div class="text-right text-base font-bold text-indigo-700 dark:text-indigo-300">
              মোট ছাত্র: {{ totalStudents }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Side Panel -->
    <transition name="slide">
      <div
        v-if="panelOpen"
        class="fixed top-0 right-0 h-full w-full md:w-96 bg-white dark:bg-slate-900 shadow-2xl border-l border-slate-300 dark:border-slate-800 z-50"
        style="max-width:400px;"
      >
        <div class="flex justify-between items-center px-6 py-4 border-b border-slate-200 dark:border-slate-800">
          <h3 class="text-xl font-bold text-slate-800 dark:text-slate-100">
            মাদরাসা তথ্য
          </h3>
          <button @click="panelOpen = false" class="text-gray-500 hover:text-gray-800 text-xl font-bold">
            ×
          </button>
        </div>
        <div class="p-6">
          <!-- Dummy info for now -->
          <div class="mb-4">
            <span class="block font-semibold text-gray-700 dark:text-gray-200 mb-1">মাদরাসা নাম:</span>
            <span class="block text-base text-gray-900 dark:text-gray-100">{{ currentItem?.main_madrasa || 'Demo মাদরাসা' }}</span>
          </div>
          <div class="mb-4">
            <span class="block font-semibold text-gray-700 dark:text-gray-200 mb-1">পরীক্ষা:</span>
            <span class="block text-base text-gray-900 dark:text-gray-100">{{ currentItem?.exam_name || 'Demo পরীক্ষা' }}</span>
          </div>
          <div class="mb-4">
            <span class="block font-semibold text-gray-700 dark:text-gray-200 mb-1">ছাত্র সংখ্যা:</span>
            <span class="block text-base text-gray-900 dark:text-gray-100">
              {{ currentItem?.main_total_students || 0 }}
            </span>
          </div>
          <div class="mb-4">
            <span class="block font-semibold text-gray-700 dark:text-gray-200 mb-1">স্ট্যাটাস:</span>
            <span class="block text-base text-gray-900 dark:text-gray-100">
              {{ getStatusLabel(currentItem?.status) }}
            </span>
          </div>
          <div class="mb-4">
            <span class="block font-semibold text-gray-700 dark:text-gray-200 mb-1">সংযুক্ত মাদরাসা:</span>
            <ul>
              <li v-for="(assoc, idx) in currentItem?.associated_madrasas || ['Demo সংযুক্ত ১','Demo সংযুক্ত ২']" :key="idx" class="text-gray-800 dark:text-gray-200">
                {{ assoc }}
              </li>
            </ul>
          </div>
          <!-- Add more dummy info if needed -->
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
const panelOpen = ref(false);
const currentItem = ref();

function openPanel(item) {
  currentItem.value = item;
  panelOpen.value = true;
}

// PDF Download function (dummy)
function downloadPDF() {
  // Here you can use jsPDF or any pdf lib, now just demo
  alert('PDF ডাউনলোড হচ্ছে...');
}

const totalStudents = computed(() => {
  return props.filtered.reduce((sum, item) => sum + (item.main_total_students || 0) + (item.associated_total_students || 0), 0);
});
import { useAgreements } from '@/views/Pages/markaz/composable/useAgreements';
const { deleteAgreementById } = useAgreements();
import { useRouter } from 'vue-router';
const router = useRouter();
import SplitButton from 'primevue/splitbutton';

function formatDate(dateStr: string) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  const day = d.getDate().toString().padStart(2, '0');
  const month = (d.getMonth() + 1).toString().padStart(2, '0');
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}
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

const splitMenuStyle = reactive<Record<string, string>>({});

const onView = (item: Agreement) => emit('view', item);

const onDelete = (item: Agreement) => {
  deleteAgreementById(item.id);
  emit('delete', item);
};

function getMenuItems(item: Agreement) {
  return [
    {
      label: 'সম্পাদনা',
      icon: 'pi pi-pencil',
      command: () => {
        router.push({ name: 'MarkazEdit', params: { id: item.id } });
      }
    },
    {
      label: 'মুছুন',
      icon: 'pi pi-trash',
      command: () => onDelete(item)
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
      return 'bg-yellow-200 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-200';
    case 'submitted':
      return 'bg-blue-200 text-blue-800 dark:bg-blue-900/40 dark:text-blue-200';
    case 'processing':
      return 'bg-purple-200 text-purple-800 dark:bg-purple-900/40 dark:text-purple-200';
    case 'approved':
      return 'bg-green-200 text-green-800 dark:bg-green-900/40 dark:text-green-200';
    case 'rejected':
      return 'bg-red-200 text-red-800 dark:bg-red-900/40 dark:text-red-200';
    default:
      return 'bg-gray-200 text-gray-800 dark:bg-gray-800/50 dark:text-gray-200';
  }
}
</script>

<style>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
.slide-enter-to,
.slide-leave-from {
  transform: translateX(0);
  opacity: 1;
}
</style>

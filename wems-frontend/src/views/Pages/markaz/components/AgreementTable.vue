<template>
  <div class="mx-auto mt-10">
    <!-- Card -->
    <div class="bg-white border border-gray-200 rounded-sm shadow-sm">
      <!-- Card Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h2 class="text-xl font-semibold text-gray-900">
          মারকায আবেদন তালিকা
        </h2>
        <!-- Search (Demo) -->
        <div class="flex items-center gap-2">
          <input
            type="text"
            placeholder="খুঁজুন..."
            class="border border-gray-300 rounded-sm px-3 py-2 bg-white text-gray-900 focus:outline-none focus:border-gray-400"
          />
          <button class="px-4 py-2 bg-gray-800 text-white rounded-sm font-medium hover:bg-gray-700">
            খুঁজুন
          </button>
          <!-- PDF Download Button -->
          <button
            class="px-4 py-2 ml-2 border border-gray-300 rounded-sm bg-white text-gray-700 font-medium hover:bg-gray-50 flex items-center gap-2"
            @click="downloadPDF"
          >
            <i class="fas fa-file-pdf text-gray-600"></i>
            PDF ডাউনলোড
          </button>
        </div>
      </div>

      <!-- Loading Spinner -->
      <div v-if="props.loading" class="flex items-center justify-center py-20 text-gray-600">
        <svg class="animate-spin h-12 w-12" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>

      <!-- Table -->
      <div v-else>
        <div v-if="props.filtered.length === 0" class="py-20 text-center text-gray-500 font-medium">
          কোন রেকর্ড পাওয়া যায়নি
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-200">
                <th class="py-3 px-6 text-left text-lg font-medium text-gray-900 uppercase tracking-wider">#</th>
                <th class="py-3 px-6 text-left text-lg font-medium text-gray-900 uppercase tracking-wider">তারিখ</th>
                <th class="py-3 px-6 text-left text-lg font-medium text-gray-900 uppercase tracking-wider">ধরন</th>
                <th class="py-3 px-6 text-left text-lg font-medium text-gray-900 uppercase tracking-wider">মাদরাসা</th>
                <th class="py-3 px-6 text-left text-lg font-medium text-gray-900 uppercase tracking-wider">পরীক্ষা</th>
                <th class="py-3 px-6 text-center text-lg font-medium text-gray-900 uppercase tracking-wider">ছাত্র</th>
                <th class="py-3 px-6 text-center text-lg font-medium text-gray-900 uppercase tracking-wider">স্ট্যাটাস</th>
                <th class="py-3 px-6 text-center text-lg font-medium text-gray-900 uppercase tracking-wider">কর্ম</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in props.filtered" :key="item.id" class="hover:bg-gray-50">
                <td class="py-3 px-6 text-lg text-gray-900">{{ index + 1 }}</td>
                <td class="py-3 px-6 text-lg text-gray-900">{{ formatDate(item.application_date) }}</td>
                <td class="py-3 px-6">
                  <span class="px-2 py-1 text-xl font-medium bg-gray-100 text-gray-800 rounded-sm">
                    {{ item.markaz_type }}
                  </span>
                </td>
                <td class="py-3 px-6 text-lg text-gray-900">
                  <div>
                    <span class="font-medium">{{ item.main_madrasa }}</span>
                  </div>
                  <div v-if="item.associated_madrasas && item.associated_madrasas.length" class="mt-1">
                    <span class="text-xl text-gray-500">সংযুক্ত মাদরাসা:</span>
                    <select class="ml-2 px-2 py-1 text-xl border border-gray-300 rounded-sm bg-white text-gray-700">
                      <option v-for="(assoc, idx) in item.associated_madrasas" :key="idx">{{ assoc.madrasa_name }}</option>
                    </select>
                  </div>
                </td>
                <td class="py-3 px-6 text-lg text-gray-900">{{ item.exam_name }}</td>
                <td class="py-3 px-6 text-lg text-gray-900">
                  <div class="text-center">
                    <div>
                      <span class="text-xl text-gray-500">মুল মাদরাসা: </span>
                      <span class="font-medium">{{ item.main_total_students }}</span>
                    </div>
                    <div>
                      <span class="text-xl text-gray-500">সংযুক্ত মাদরাসা: </span>
                      <span class="font-medium">{{ item.associated_total_students }}</span>
                    </div>
                  </div>
                </td>
                <td class="py-3 px-6 text-center">
                  <span class="inline-block px-3 py-1 text-xl font-medium rounded-sm"
                    :class="statusClass(item.status)">
                    {{ getStatusLabel(item.status) }}
                  </span>
                </td>
                <td class="py-3 px-6 text-center">
                  <div class="flex items-center justify-center">
                    <SplitButton
                      :model="getMenuItems(item)"
                      label="বিস্তারিত"
                      icon="pi pi-eye"
                      class="text-lg text-gray-700"
                      :menuStyle="splitMenuStyle"
                      @click="openPanel(item)"
                    />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <!-- Pagination (Demo) -->
          <div class="flex flex-col gap-2 px-6 py-4 bg-gray-50 border-t border-gray-200">
            <div class="flex items-center justify-between">
              <span class="text-lg text-gray-600">১-১০ / মোট {{ props.filtered.length }} টি</span>
              <div class="flex gap-2">
                <button class="px-3 py-1 text-lg border border-gray-300 rounded-sm bg-white text-gray-700 hover:bg-gray-50">←</button>
                <button class="px-3 py-1 text-lg border border-gray-300 rounded-sm bg-white text-gray-700 hover:bg-gray-50">→</button>
              </div>
            </div>
            <div class="text-right text-lg font-medium text-gray-700">
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
        class="fixed top-0 right-0 h-full w-full md:w-96 bg-white shadow-lg border-l border-gray-200 z-50"
        style="max-width:400px;"
      >
        <div class="flex justify-between items-center px-6 py-4 border-b border-gray-200 bg-gray-50">
          <h3 class="text-lg font-semibold text-gray-900">
            মাদরাসা তথ্য
          </h3>
          <button @click="panelOpen = false" class="text-gray-400 hover:text-gray-600 text-xl font-bold">
            ×
          </button>
        </div>
        <div class="p-6">
          <!-- Dummy info for now -->
          <div class="mb-4">
            <span class="block text-lg font-medium text-gray-700 mb-1">মাদরাসা নাম:</span>
            <span class="block text-lg text-gray-900">{{ currentItem?.main_madrasa || 'Demo মাদরাসা' }}</span>
          </div>
          <div class="mb-4">
            <span class="block text-lg font-medium text-gray-700 mb-1">পরীক্ষা:</span>
            <span class="block text-lg text-gray-900">{{ currentItem?.exam_name || 'Demo পরীক্ষা' }}</span>
          </div>
          <div class="mb-4">
            <span class="block text-lg font-medium text-gray-700 mb-1">মুল মাদরাসার ছাত্র সংখ্যা:</span>
            <ul class="text-lg text-gray-900">
              <li v-if="currentItem?.main_class_counts">
                <span v-for="(count, cls) in currentItem.main_class_counts" :key="cls" class="block">
                  {{ cls }}: {{ count }}
                </span>
              </li>
              <li v-else>
                {{ currentItem?.main_total_students || 0 }}
              </li>
            </ul>
          </div>
          <div class="mb-4">
            <span class="block text-lg font-medium text-gray-700 mb-1">সংযুক্ত মাদরাসার ছাত্র সংখ্যা:</span>
            <ul class="text-lg text-gray-900">
              <li v-if="currentItem?.associated_class_counts">
                <span v-for="(count, cls) in currentItem.associated_class_counts" :key="cls" class="block">
                  {{ cls }}: {{ count }}
                </span>
              </li>
              <li v-else>
                {{ currentItem?.associated_total_students || 0 }}
              </li>
            </ul>
          </div>
          <div class="mb-4">
            <span class="block text-lg font-medium text-gray-700 mb-1">স্ট্যাটাস:</span>
            <span class="block text-lg text-gray-900">
              {{ getStatusLabel(currentItem?.status) }}
            </span>
          </div>
          <div class="mb-4">
            <span class="block text-lg font-medium text-gray-700 mb-1">সংযুক্ত মাদরাসা:</span>
            <ul class="text-lg text-gray-900" v-if="currentItem?.associated_madrasas && currentItem.associated_madrasas.length">
              <li v-for="(assoc, idx) in currentItem.associated_madrasas" :key="idx" class="py-1">
                {{ assoc.madrasa_name || assoc }}
              </li>
            </ul>
            <ul class="text-lg text-gray-900" v-else>
              <li>কোন সংযুক্ত মাদরাসা নেই</li>
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
import type { Agreement } from '@/views/Pages/markaz/composable/useAgreements';
const panelOpen = ref(false);
const currentItem = ref<Agreement | null>(null);


function openPanel(item: Agreement) {
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
      return 'bg-yellow-100 text-yellow-800';
    case 'submitted':
      return 'bg-blue-100 text-blue-800';
    case 'processing':
      return 'bg-purple-100 text-purple-800';
    case 'approved':
      return 'bg-green-100 text-green-800';
    case 'rejected':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
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

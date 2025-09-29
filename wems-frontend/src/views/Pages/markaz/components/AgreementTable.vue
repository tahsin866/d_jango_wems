<template>
  <div class="mx-auto mt-10">
    <!-- Card -->
    <div class="bg-white border border-gray-300 rounded-sm shadow">
      <!-- Card Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-300 bg-gradient-to-r from-gray-800 to-gray-700">
        <h2 class="text-xl font-bold text-white">
          মারকায আবেদন তালিকা
        </h2>
        <!-- Search (Demo) -->
        <div class="flex items-center gap-2">
          <input
            type="text"
            placeholder="খুঁজুন..."
            class="border border-gray-300 rounded-sm px-3 py-2 bg-white text-gray-900 focus:outline-none focus:border-gray-400"
          />
          <button class="px-4 py-2 bg-gray-700 text-white rounded-sm font-medium hover:bg-gray-600 transition-colors duration-200">
            খুঁজুন
          </button>
          <!-- PDF Download Button -->
          <button
            class="px-4 py-2 ml-2 border border-gray-300 rounded-sm bg-white text-gray-700 font-medium hover:bg-gray-50 flex items-center gap-2 transition-colors duration-200"
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
        <div v-if="props.filtered.length === 0" class="py-20 text-center text-gray-600 font-medium">
          কোন রেকর্ড পাওয়া যায়নি
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full">
            <thead>
              <tr class="bg-gray-100 border-b border-gray-300">
                <th class="py-3 px-6 text-left text-lg font-bold text-gray-800 uppercase tracking-wider">#</th>
                <th class="py-3 px-6 text-left text-lg font-bold text-gray-800 uppercase tracking-wider">তারিখ</th>
                <th class="py-3 px-6 text-left text-lg font-bold text-gray-800 uppercase tracking-wider">ধরন</th>
                <th class="py-3 px-6 text-left text-lg font-bold text-gray-800 uppercase tracking-wider">মাদরাসা</th>
                <th class="py-3 px-6 text-left text-lg font-bold text-gray-800 uppercase tracking-wider">পরীক্ষা</th>
                <th class="py-3 px-6 text-center text-lg font-bold text-gray-800 uppercase tracking-wider">ছাত্র</th>
                <th class="py-3 px-6 text-center text-lg font-bold text-gray-800 uppercase tracking-wider">স্ট্যাটাস</th>
                <th class="py-3 px-6 text-center text-lg font-bold text-gray-800 uppercase tracking-wider">কর্ম</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-300">
              <tr v-for="(item, index) in props.filtered" :key="item.id" class="hover:bg-gray-50">
                <td class="py-3 px-6 text-lg text-gray-900 border-b border-gray-200">{{ index + 1 }}</td>
                <td class="py-3 px-6 text-lg text-gray-900 border-b border-gray-200">{{ formatDate(item.application_date) }}</td>
                <td class="py-3 px-6 border-b border-gray-200">
                  <span class="px-2 py-1 text-xl font-medium bg-gray-100 text-gray-800 rounded-sm border border-gray-300">
                    {{ item.markaz_type }}
                  </span>
                </td>
                <td class="py-3 px-6 text-lg text-gray-900 border-b border-gray-200">
                  <div>
                    <span class="font-medium">{{ item.main_madrasa }}</span>
                  </div>
                  <div v-if="item.associated_madrasas && item.associated_madrasas.length" class="mt-1">
                    <span class="text-md text-gray-600">সংযুক্ত মাদরাসা:</span>
                    <select class="ml-2 px-2 py-1 text-md border border-gray-300 rounded-sm bg-white text-gray-700">
                      <option v-for="(assoc, idx) in item.associated_madrasas" :key="idx">{{ assoc.madrasa_name }}</option>
                    </select>
                  </div>
                </td>
                <td class="py-3 px-6 text-lg text-gray-900 border-b border-gray-200">{{ item.exam_name }}</td>
                <td class="py-3 px-6 text-lg text-gray-900 border-b border-gray-200">
                  <div class="text-center">
                    <div>
                      <span class="text-xl text-gray-600">মুল মাদরাসা: </span>
                      <span class="font-medium">{{ item.main_total_students }}</span>
                    </div>
                    <div>
                      <span class="text-xl text-gray-600">সংযুক্ত মাদরাসা: </span>
                      <span class="font-medium">{{ item.associated_total_students }}</span>
                    </div>
                  </div>
                </td>
                <td class="py-3 px-6 text-center border-b border-gray-200">
                  <span class="inline-block px-3 py-1 text-xl font-medium rounded-sm border"
                    :class="statusClass(item.status)">
                    {{ getStatusLabel(item.status) }}
                  </span>
                </td>
                <td class="py-3 px-6 text-center border-b border-gray-200">
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
          <div class="flex flex-col gap-2 px-6 py-4 bg-gray-100 border-t border-gray-300">
            <div class="flex items-center justify-between">
              <span class="text-lg text-gray-700">১-১০ / মোট {{ props.filtered.length }} টি</span>
              <div class="flex gap-2">
                <button class="px-3 py-1 text-lg border border-gray-300 rounded-sm bg-white text-gray-700 hover:bg-gray-50 transition-colors duration-200">←</button>
                <button class="px-3 py-1 text-lg border border-gray-300 rounded-sm bg-white text-gray-700 hover:bg-gray-50 transition-colors duration-200">→</button>
              </div>
            </div>
            <div class="text-right text-lg font-medium text-gray-800">
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
      class="fixed top-0 right-0 h-full w-full md:w-96 bg-white shadow-xl border-l border-gray-300 z-50 flex flex-col"
      style="max-width:400px;"
    >
      <!-- Header -->
      <div class="flex justify-between items-center px-6 py-5 border-b border-gray-300 bg-gradient-to-r from-gray-800 to-gray-700 flex-shrink-0">
        <h3 class="text-xl font-bold text-white">
          মাদরাসা তথ্য
        </h3>
        <button
          @click="panelOpen = false"
          class="text-gray-300 hover:text-white text-2xl font-bold transition-colors duration-200"
          aria-label="বন্ধ করুন"
        >
          ×
        </button>
      </div>

      <!-- Content Area -->
      <div class="flex-grow overflow-y-auto p-6 bg-gray-50">
        <!-- Main Info Section -->
        <div class="bg-white rounded-sm border border-gray-300 shadow-sm mb-6 overflow-hidden">
          <div class="bg-gray-100 px-4 py-3 border-b border-gray-300">
            <h4 class="text-lg font-bold text-gray-800">মূল তথ্য</h4>
          </div>
          <div class="p-4 space-y-4">
            <div class="border-b border-gray-200 pb-3">
              <div class="text-sm font-semibold text-gray-600 uppercase tracking-wide">মাদরাসা নাম</div>
              <div class="text-lg font-medium text-gray-900 mt-1">{{ currentItem?.main_madrasa || 'Demo মাদরাসা' }}</div>
            </div>

            <div class="border-b border-gray-200 pb-3">
              <div class="text-sm font-semibold text-gray-600 uppercase tracking-wide">পরীক্ষা</div>
              <div class="text-lg font-medium text-gray-900 mt-1">{{ currentItem?.exam_name || 'Demo পরীক্ষা' }}</div>
            </div>

            <div>
              <div class="text-sm font-semibold text-gray-600 uppercase tracking-wide">স্ট্যাটাস</div>
              <div class="mt-1">
                <span
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border"
                  :class="statusClass(currentItem?.status)"
                >
                  {{ getStatusLabel(currentItem?.status) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Student Counts Section -->
        <div class="bg-white rounded-sm border border-gray-300 shadow-sm mb-6 overflow-hidden">
          <div class="bg-gray-100 px-4 py-3 border-b border-gray-300">
            <h4 class="text-lg font-bold text-gray-800">ছাত্র সংখ্যা</h4>
          </div>
          <div class="p-4 space-y-5">
            <div>
              <div class="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-2">মুল মাদরাসা</div>
              <div class="bg-gray-50 rounded-sm p-3 border border-gray-200">
                <ul class="space-y-2">
                  <li v-if="currentItem?.main_class_counts">
                    <div v-for="(count, cls) in currentItem.main_class_counts" :key="cls" class="flex justify-between">
                      <span class="text-gray-700 font-medium">{{ cls }}:</span>
                      <span class="text-gray-900 font-bold">{{ count }}</span>
                    </div>
                  </li>
                  <li v-else class="flex justify-between">
                    <span class="text-gray-700 font-medium">মোট:</span>
                    <span class="text-gray-900 font-bold">{{ currentItem?.main_total_students || 0 }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <div>
              <div class="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-2">সংযুক্ত মাদরাসা</div>
              <div class="bg-gray-50 rounded-sm p-3 border border-gray-200">
                <ul class="space-y-2">
                  <li v-if="currentItem?.associated_class_counts">
                    <div v-for="(count, cls) in currentItem.associated_class_counts" :key="cls" class="flex justify-between">
                      <span class="text-gray-700 font-medium">{{ cls }}:</span>
                      <span class="text-gray-900 font-bold">{{ count }}</span>
                    </div>
                  </li>
                  <li v-else class="flex justify-between">
                    <span class="text-gray-700 font-medium">মোট:</span>
                    <span class="text-gray-900 font-bold">{{ currentItem?.associated_total_students || 0 }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Associated Madrasas Section -->
        <div class="bg-white rounded-sm border border-gray-300 shadow-sm overflow-hidden">
          <div class="bg-gray-100 px-4 py-3 border-b border-gray-300">
            <h4 class="text-lg font-bold text-gray-800">সংযুক্ত মাদরাসা</h4>
          </div>
          <div class="p-4">
            <ul v-if="currentItem?.associated_madrasas && currentItem.associated_madrasas.length" class="space-y-3">
              <li
                v-for="(assoc, idx) in currentItem.associated_madrasas"
                :key="idx"
                class="flex items-start p-3 bg-gray-50 rounded-sm border border-gray-200"
              >
                <div class="flex-shrink-0 h-5 w-5 text-gray-500 mt-0.5">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span class="ml-3 text-gray-800 font-medium">{{ assoc.madrasa_name || assoc }}</span>
              </li>
            </ul>
            <div v-else class="text-center py-4">
              <div class="text-gray-600 italic">কোন সংযুক্ত মাদরাসা নেই</div>
            </div>
          </div>
        </div>
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
      return 'bg-yellow-100 text-yellow-800 border border-yellow-300';
    case 'submitted':
      return 'bg-blue-100 text-blue-800 border border-blue-300';
    case 'processing':
      return 'bg-purple-100 text-purple-800 border border-purple-300';
    case 'approved':
      return 'bg-green-100 text-green-800 border border-green-300';
    case 'rejected':
      return 'bg-red-100 text-red-800 border border-red-300';
    default:
      return 'bg-gray-100 text-gray-800 border border-gray-300';
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

/* Custom scrollbar for the side panel */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>

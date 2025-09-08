<template>

    <div
      style="font-family: 'SolaimanLipi', sans-serif;"
      class="py-12 bg-gray-50 dark:bg-slate-900 min-h-screen text-gray-800 dark:text-gray-200"
    >
      <div class="mx-auto  sm:px-6 lg:px-8">
        <div class="bg-white dark:bg-slate-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-200 dark:border-slate-700">
          <!-- Header -->
          <div
            class="p-6 bg-white dark:bg-slate-800 border-b border-gray-200 dark:border-slate-700 flex flex-col md:flex-row md:items-center md:justify-between gap-4"
          >
            <div>
              <h2 class="text-2xl font-semibold leading-tight">মারকায আবেদন তালিকা</h2>
              <p class="mt-1 text-md text-gray-500 dark:text-gray-400">সব আবেদন এখানে তালিকাভুক্ত থাকবে</p>
            </div>

            <div class="flex items-center gap-3">
              <RouterLink
                to="/markaz/change/form"
                class="inline-flex items-center px-4 py-2 bg-gray-800 text-white rounded-sm text-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-800"
                aria-label="মারকাজ পরিবর্তন ফরম"
              >
                মারকাজ পরিবর্তন ফরম
              </RouterLink>

              <button
                type="button"
                class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-sm text-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                @click="createNew"
                title="নতুন আবেদন"
              >
                নতুন আবেদন
              </button>
            </div>
          </div>

          <!-- Table Container -->
          <div class="p-6 bg-white dark:bg-slate-800 border-b border-gray-200 dark:border-slate-700">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200 dark:divide-slate-700">
                <thead class="bg-gray-50 dark:bg-slate-700">
                  <tr>
                    <th class="px-6 py-3 text-left text-md font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      আবেদন নং
                    </th>
                    <th class="px-6 py-3 text-left text-md font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      বর্তমান স্তর
                    </th>
                    <th class="px-6 py-3 text-left text-md font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      বর্তমান মাদরাসা
                    </th>
                    <th class="px-6 py-3 text-left text-md font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      তারিখ
                    </th>
                    <th class="px-6 py-3 text-left text-md font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      জয়েনিং তারিখ
                    </th>
                    <th class="px-6 py-3 text-left text-md font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      স্ট্যাটাস
                    </th>
                    <th class="px-6 py-3 text-left text-md font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      একশন
                    </th>
                  </tr>
                </thead>

                <tbody class="bg-white dark:bg-slate-800 divide-y divide-gray-200 dark:divide-slate-700">
                  <tr v-if="items.length === 0">
                    <td class="px-6 py-8 text-center text-md text-gray-500 dark:text-gray-400" colspan="7">
                      কোনো আবেদন নেই।
                    </td>
                  </tr>

                  <tr
                    v-for="item in items"
                    :key="item.id"
                    class="hover:bg-gray-50 dark:hover:bg-slate-700"
                  >
                    <td class="px-6 py-4 whitespace-nowrap text-md">{{ item.applicationNo }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-md">{{ item.currentLevel }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-md">{{ item.currentMadrasa }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-md">{{ formatDate(item.date) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-md">{{ formatDate(item.joiningDate) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span
                        class="px-2 inline-flex text-md leading-5 font-semibold rounded-full"
                        :class="statusBadgeClass(item.status)"
                        role="status"
                        :aria-label="`স্ট্যাটাস: ${item.status}`"
                      >
                        {{ humanStatus(item.status) }}
                      </span>
                    </td>

                    <td class="px-6 py-4 whitespace-nowrap text-md font-medium">
                      <div class="flex items-center gap-2">
                        <button
                          @click="viewItem(item)"
                          class="p-2 rounded hover:bg-gray-100 dark:hover:bg-slate-700 focus:outline-none"
                          title="View Details"
                          aria-label="বিস্তারিত দেখুন"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-600 dark:text-indigo-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        </button>

                        <button
                          @click="updateItem(item)"
                          class="p-2 rounded hover:bg-gray-100 dark:hover:bg-slate-700 focus:outline-none"
                          title="Edit"
                          aria-label="সম্পাদনা করুন"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-600 dark:text-amber-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>

                        <button
                          @click="deleteItem(item)"
                          class="p-2 rounded hover:bg-gray-100 dark:hover:bg-slate-700 focus:outline-none"
                          title="Delete"
                          aria-label="মুছুন"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-600 dark:text-red-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Inline Details Panel (replaces modal/drawer) -->
            <div v-if="selectedItem" class="mt-6 p-4 rounded-md border border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-800">
              <div class="flex items-start justify-between">
                <div>
                  <h3 class="text-lg font-semibold">আবেদন বিবরণ — {{ selectedItem.applicationNo }}</h3>
                  <p class="text-md text-gray-600 dark:text-gray-400 mt-1">স্ট্যাটাস: {{ humanStatus(selectedItem.status) }}</p>
                </div>

                <div class="flex items-center gap-2">
                  <button
                    class="px-3 py-1 bg-amber-600 text-white rounded hover:bg-amber-700"
                    @click="updateItem(selectedItem)"
                  >
                    সম্পাদনা করুন
                  </button>
                  <button
                    class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                    @click="confirmDelete(selectedItem)"
                  >
                    মুছুন
                  </button>
                  <button
                    class="px-3 py-1 bg-gray-100 dark:bg-slate-700 text-gray-800 dark:text-gray-200 rounded hover:bg-gray-200"
                    @click="closeDetails"
                  >
                    বন্ধ
                  </button>
                </div>
              </div>

              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
                <div>
                  <dt class="text-md text-gray-500 dark:text-gray-400">আবেদন নং</dt>
                  <dd class="mt-1 text-md">{{ selectedItem.applicationNo }}</dd>
                </div>
                <div>
                  <dt class="text-md text-gray-500 dark:text-gray-400">বর্তমান স্তর</dt>
                  <dd class="mt-1 text-md">{{ selectedItem.currentLevel }}</dd>
                </div>
                <div>
                  <dt class="text-md text-gray-500 dark:text-gray-400">বর্তমান মাদরাসা</dt>
                  <dd class="mt-1 text-md">{{ selectedItem.currentMadrasa }}</dd>
                </div>
                <div>
                  <dt class="text-md text-gray-500 dark:text-gray-400">তারিখ</dt>
                  <dd class="mt-1 text-md">{{ formatDate(selectedItem.date) }}</dd>
                </div>
                <div>
                  <dt class="text-md text-gray-500 dark:text-gray-400">জয়েনিং তারিখ</dt>
                  <dd class="mt-1 text-md">{{ formatDate(selectedItem.joiningDate) }}</dd>
                </div>
                <div>
                  <dt class="text-md text-gray-500 dark:text-gray-400">স্ট্যাটাস</dt>
                  <dd class="mt-1 text-md">{{ humanStatus(selectedItem.status) }}</dd>
                </div>
              </dl>
            </div>
            <!-- end inline details -->
          </div>
        </div>
      </div>
    </div>

</template>

<script setup lang="ts">
// TypeScript SFC, prepared for editor / Vite / Volar type checking
import { ref } from 'vue';
import { useRouter, RouterLink } from 'vue-router';


/**
 * Application item type
 */
type ApplicationItem = {
  id: number;
  applicationNo: string;
  currentLevel: string;
  currentMadrasa: string;
  date: string; // ISO or YYYY-MM-DD
  joiningDate: string; // ISO or YYYY-MM-DD
  status: 'active' | 'inactive' | 'pending' | string;
};

// Sample data (replace with API fetch)
const items = ref<ApplicationItem[]>([
  {
    id: 1,
    applicationNo: 'APP001',
    currentLevel: 'স্তর ১',
    currentMadrasa: 'মাদরাসা নাম ১',
    date: '2024-01-15',
    joiningDate: '2024-02-01',
    status: 'active',
  },
  {
    id: 2,
    applicationNo: 'APP002',
    currentLevel: 'স্তর ২',
    currentMadrasa: 'মাদরাসা নাম ২',
    date: '2024-03-10',
    joiningDate: '2024-04-01',
    status: 'pending',
  },
]);

const router = useRouter();

// selected item (replaces modal)
const selectedItem = ref<ApplicationItem | null>(null);

/**
 * Open details panel
 */
function viewItem(item: ApplicationItem) {
  selectedItem.value = item;
}

/**
 * Navigate to update / edit page
 */
function updateItem(item: ApplicationItem | null) {
  if (!item) return;
  router.push({ path: `/markaz/${item.id}/edit` }).catch(() => {});
}

/**
 * Confirm and delete item
 */
async function deleteItem(item: ApplicationItem) {
  const confirmed = window.confirm(`আপনি "${item.applicationNo}" মুছে ফেলতে চান?`);
  if (!confirmed) return;

  // simulate API call and remove locally on success
  const idx = items.value.findIndex((i) => i.id === item.id);
  if (idx !== -1) {
    items.value.splice(idx, 1);
    // if that was the selected item, clear panel
    if (selectedItem.value?.id === item.id) selectedItem.value = null;
  }
}

/**
 * For actions inside the inline details panel
 */
function closeDetails() {
  selectedItem.value = null;
}

/**
 * Prompted delete from panel
 */
function confirmDelete(item: ApplicationItem | null) {
  if (!item) return;
  deleteItem(item);
}

/**
 * Create new item (example navigation)
 */
function createNew() {
  router.push({ path: '/markazApply' }).catch(() => {});
}

/**
 * Utility: format date safely (YYYY-MM-DD -> readable)
 */
function formatDate(value: string | undefined) {
  if (!value) return '—';
  try {
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) return value;
    return d.toLocaleDateString('bn-BD', { year: 'numeric', month: 'short', day: 'numeric' });
  } catch {
    return value;
  }
}

/**
 * Return human-friendly status text
 */
function humanStatus(status: string) {
  switch (status) {
    case 'active':
      return 'সক্রিয়';
    case 'inactive':
      return 'নিষ্ক্রিয়';
    case 'pending':
      return 'মুলতুবি';
    default:
      return status;
  }
}

/**
 * Badge classes (tailwind) with dark mode support
 */
function statusBadgeClass(status: string) {
  if (status === 'active') {
    return 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100';
  }
  if (status === 'inactive') {
    return 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100';
  }
  // pending / other
  return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100';
}
</script>

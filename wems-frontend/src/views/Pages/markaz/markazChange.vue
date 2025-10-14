<template>
    <div
      style="font-family: 'SolaimanLipi', sans-serif;"
      class="py-12 bg-gray-100  text-gray-800"
    >
      <div class="mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow border border-gray-300 rounded-sm">
          <!-- Header -->
          <div
            class="p-6 bg-gradient-to-r from-gray-800 to-gray-700 border-b border-gray-300 flex flex-col md:flex-row md:items-center md:justify-between gap-4"
          >
            <div>
              <h2 class="text-2xl font-bold leading-tight text-white">মারকায আবেদন তালিকা</h2>
              <p class="mt-1 text-md text-gray-300">সব আবেদন এখানে তালিকাভুক্ত থাকবে</p>
            </div>

            <div class="flex items-center gap-3">
              <RouterLink
                to="/markaz/change/form"
                class="inline-flex items-center px-4 py-2 bg-gray-700 text-white rounded-sm text-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-700 transition-all duration-200"
                aria-label="মারকাজ পরিবর্তন ফরম"
              >
                মারকাজ পরিবর্তন ফরম
              </RouterLink>

              <button
                type="button"
                class="inline-flex items-center px-4 py-2 bg-blue-700 text-white rounded-sm text-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
                @click="createNew"
                title="নতুন আবেদন"
              >
                নতুন আবেদন
              </button>
            </div>
          </div>

          <!-- Table Container -->
          <div class="p-6 bg-white border-b border-gray-300">
            <div class="overflow-x-auto border border-gray-300 rounded-sm">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-100">
                  <tr>
                    <th class="px-6 py-3 text-left text-md font-bold text-gray-700 uppercase tracking-wider border-b border-gray-300">
                      আবেদন নং
                    </th>
                    <th class="px-6 py-3 text-left text-md font-bold text-gray-700 uppercase tracking-wider border-b border-gray-300">
                      বর্তমান স্তর
                    </th>
                    <th class="px-6 py-3 text-left text-md font-bold text-gray-700 uppercase tracking-wider border-b border-gray-300">
                      বর্তমান মাদরাসা
                    </th>
                    <th class="px-6 py-3 text-left text-md font-bold text-gray-700 uppercase tracking-wider border-b border-gray-300">
                      তারিখ
                    </th>
                    <th class="px-6 py-3 text-left text-md font-bold text-gray-700 uppercase tracking-wider border-b border-gray-300">
                      জয়েনিং তারিখ
                    </th>
                    <th class="px-6 py-3 text-left text-md font-bold text-gray-700 uppercase tracking-wider border-b border-gray-300">
                      স্ট্যাটাস
                    </th>
                    <th class="px-6 py-3 text-left text-md font-bold text-gray-700 uppercase tracking-wider border-b border-gray-300">
                      একশন
                    </th>
                  </tr>
                </thead>

                <tbody class="bg-white divide-y divide-gray-300">
                  <tr v-if="items.length === 0">
                    <td class="px-6 py-8 text-center text-md text-gray-600" colspan="7">
                      কোনো আবেদন নেই।
                    </td>
                  </tr>

                  <tr
                    v-for="item in items"
                    :key="item.id"
                    class="hover:bg-gray-50"
                  >
                    <td class="px-6 py-4 whitespace-nowrap text-md border-b border-gray-200">{{ item.applicationNo }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-md border-b border-gray-200">{{ item.currentLevel }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-md border-b border-gray-200">{{ item.currentMadrasa }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-md border-b border-gray-200">{{ formatDate(item.date) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-md border-b border-gray-200">{{ formatDate(item.joiningDate) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap border-b border-gray-200">
                      <span
                        class="px-2 inline-flex text-md leading-5 font-semibold rounded-sm"
                        :class="statusBadgeClass(item.status)"
                        role="status"
                        :aria-label="`স্ট্যাটাস: ${item.status}`"
                      >
                        {{ humanStatus(item.status) }}
                      </span>
                    </td>

                    <td class="px-6 py-4 whitespace-nowrap text-md font-medium border-b border-gray-200">
                      <!-- Grouped Action Buttons -->
                      <div class="inline-flex rounded-sm shadow-sm" role="group">
                        <button
                          @click="viewItem(item)"
                          class="px-3 py-2 text-sm font-medium text-white bg-blue-700 border border-blue-700 rounded-l-sm hover:bg-blue-600 focus:z-10 focus:ring-2 focus:ring-blue-500 focus:bg-blue-600 transition-all duration-200"
                          title="View Details"
                          aria-label="বিস্তারিত দেখুন"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        </button>

                        <button
                          @click="updateItem(item)"
                          class="px-3 py-2 text-sm font-medium text-white bg-amber-600 border-t border-b border-amber-600 hover:bg-amber-500 focus:z-10 focus:ring-2 focus:ring-amber-500 focus:bg-amber-500 transition-all duration-200"
                          title="Edit"
                          aria-label="সম্পাদনা করুন"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>

                        <button
                          @click="deleteItem(item)"
                          class="px-3 py-2 text-sm font-medium text-white bg-red-700 border border-red-700 rounded-r-sm hover:bg-red-600 focus:z-10 focus:ring-2 focus:ring-red-500 focus:bg-red-600 transition-all duration-200"
                          title="Delete"
                          aria-label="মুছুন"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Inline Details Panel -->
            <div v-if="selectedItem" class="mt-6 p-6 rounded-sm border border-gray-300 bg-gray-50 shadow-sm">
              <div class="flex items-start justify-between border-b border-gray-300 pb-4 mb-4">
                <div>
                  <h3 class="text-xl font-bold text-gray-800">আবেদন বিবরণ — {{ selectedItem.applicationNo }}</h3>
                  <p class="text-md text-gray-600 mt-1">স্ট্যাটাস: {{ humanStatus(selectedItem.status) }}</p>
                </div>

                <div class="flex items-center gap-3">
                  <!-- Grouped Action Buttons in Details Panel -->
                  <div class="inline-flex rounded-sm shadow-sm" role="group">
                    <button
                      @click="updateItem(selectedItem)"
                      class="px-4 py-2 text-sm font-medium text-white bg-amber-600 border border-amber-600 rounded-l-sm hover:bg-amber-500 focus:z-10 focus:ring-2 focus:ring-amber-500 focus:bg-amber-500 transition-all duration-200"
                    >
                      সম্পাদনা করুন
                    </button>

                    <button
                      @click="confirmDelete(selectedItem)"
                      class="px-4 py-2 text-sm font-medium text-white bg-red-700 border border-red-700 rounded-r-sm hover:bg-red-600 focus:z-10 focus:ring-2 focus:ring-red-500 focus:bg-red-600 transition-all duration-200"
                    >
                      মুছুন
                    </button>
                  </div>

                  <button
                    class="px-4 py-2 bg-gray-200 text-gray-800 rounded-sm hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 transition-all duration-200"
                    @click="closeDetails"
                  >
                    বন্ধ
                  </button>
                </div>
              </div>

              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="border-b border-gray-200 pb-2">
                  <dt class="text-md font-semibold text-gray-700">আবেদন নং</dt>
                  <dd class="mt-1 text-md text-gray-800">{{ selectedItem.applicationNo }}</dd>
                </div>
                <div class="border-b border-gray-200 pb-2">
                  <dt class="text-md font-semibold text-gray-700">বর্তমান স্তর</dt>
                  <dd class="mt-1 text-md text-gray-800">{{ selectedItem.currentLevel }}</dd>
                </div>
                <div class="border-b border-gray-200 pb-2">
                  <dt class="text-md font-semibold text-gray-700">বর্তমান মাদরাসা</dt>
                  <dd class="mt-1 text-md text-gray-800">{{ selectedItem.currentMadrasa }}</dd>
                </div>
                <div class="border-b border-gray-200 pb-2">
                  <dt class="text-md font-semibold text-gray-700">তারিখ</dt>
                  <dd class="mt-1 text-md text-gray-800">{{ formatDate(selectedItem.date) }}</dd>
                </div>
                <div class="border-b border-gray-200 pb-2">
                  <dt class="text-md font-semibold text-gray-700">জয়েনিং তারিখ</dt>
                  <dd class="mt-1 text-md text-gray-800">{{ formatDate(selectedItem.joiningDate) }}</dd>
                </div>
                <div class="border-b border-gray-200 pb-2">
                  <dt class="text-md font-semibold text-gray-700">স্ট্যাটাস</dt>
                  <dd class="mt-1 text-md text-gray-800">{{ humanStatus(selectedItem.status) }}</dd>
                </div>
              </dl>
            </div>
            <!-- end inline details -->
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
/**
 * -------------------------------------------
 * 🕌 Markaz Application List Logic (Vue 3 + JS)
 * -------------------------------------------
 */

import { ref } from 'vue'
import { useRouter } from 'vue-router'

/* ==============================
   📦 Reactive States
   ============================== */
const router = useRouter()

// Applications list (later can be fetched from API)
const items = ref([
  {
    id: 1,
    applicationNo: 'APP001',
    currentLevel: 'স্তর ১',
    currentMadrasa: 'জামিয়া আরাবিয়া দারুল উলুম ঢাকা',
    date: '2024-01-15',
    joiningDate: '2024-02-01',
    status: 'active',
  },
  {
    id: 2,
    applicationNo: 'APP002',
    currentLevel: 'স্তর ২',
    currentMadrasa: 'জামিয়া কুরআনিয়া লালবাগ ঢাকা',
    date: '2024-03-10',
    joiningDate: '2024-04-01',
    status: 'pending',
  },
])

// Currently selected application
const selectedItem = ref(null)

/* ==============================
   ⚙️ Core Functions
   ============================== */

// View selected item
function viewItem(item) {
  selectedItem.value = item
}

// Navigate to edit page
function updateItem(item) {
  if (!item) return
  router.push({ path: `/markaz/${item.id}/edit` }).catch(() => {})
}

// Delete item (with confirmation)
async function deleteItem(item) {
  const confirmed = window.confirm(`আপনি "${item.applicationNo}" মুছে ফেলতে চান?`)
  if (!confirmed) return

  const idx = items.value.findIndex((i) => i.id === item.id)
  if (idx !== -1) {
    items.value.splice(idx, 1)
    if (selectedItem.value?.id === item.id) selectedItem.value = null
  }
}

// Close details panel
function closeDetails() {
  selectedItem.value = null
}

// Delete from inside panel
function confirmDelete(item) {
  if (!item) return
  deleteItem(item)
}

// Create new application
function createNew() {
  router.push({ path: '/markazApply' }).catch(() => {})
}

/* ==============================
   🧭 Utility Functions
   ============================== */

// Format date in Bangla locale
function formatDate(value) {
  if (!value) return '—'
  try {
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) return value
    return date.toLocaleDateString('bn-BD', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  } catch {
    return value
  }
}

// Convert status into Bangla text
function humanStatus(status) {
  switch (status) {
    case 'active': return 'সক্রিয়'
    case 'inactive': return 'নিষ্ক্রিয়'
    case 'pending': return 'মুলতুবি'
    default: return status
  }
}

// Dynamic badge class
function statusBadgeClass(status) {
  const classes = {
    active: 'bg-green-100 text-green-800 border border-green-300',
    inactive: 'bg-red-100 text-red-800 border border-red-300',
    pending: 'bg-yellow-100 text-yellow-800 border border-yellow-300',
  }
  return classes[status] || 'bg-gray-100 text-gray-800 border border-gray-300'
}
</script>

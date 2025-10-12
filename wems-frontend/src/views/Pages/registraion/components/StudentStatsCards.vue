<script setup>
const { studentStats } = defineProps({
  studentStats: Object
});
</script>

<template>
  <div
  style="font-family: 'SolaimanLipi', sans-serif;"
  class="py-6">
    <div class="">
      <div class="mb-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Total Students Card -->
        <div
          class="relative bg-white border border-gray-300 shadow-md sm:rounded-sm overflow-hidden transition hover:shadow-lg group"
        >
          <div class="p-6">
            <div class="flex justify-between items-center">
              <div>
                <div class="text-gray-900 text-3xl font-extrabold flex items-center gap-2 tracking-tight">
                  <span>{{ studentStats.totalStudents }}</span>
                  <span class="text-lg font-medium text-gray-700">জন</span>
                </div>
                <p class="text-gray-700 mt-2 font-semibold tracking-wide text-base">
                  মোট নিবন্ধিত শিক্ষার্থী
                </p>
              </div>
              <div
                class="bg-gray-100 rounded-full p-3 shadow border border-gray-300"
              >
                <svg class="w-8 h-8 text-gray-600 opacity-80" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 4v6m-4 4h16M4 14l8-8 8 8M4 20h16"/>
                </svg>
              </div>
            </div>
            <div class="mt-6 flex items-center">
              <span class="px-3 py-1 rounded bg-gray-100 text-gray-700 text-xs font-semibold tracking-wider border border-gray-300">সক্রিয়</span>
            </div>
          </div>
          <div class="absolute right-0 bottom-0 opacity-5 text-gray-800 text-[7rem] pointer-events-none select-none">
            <i class="pi pi-users" />
          </div>
        </div>

        <!-- Board Returned Students Card -->
        <div
          class="relative bg-white border border-gray-300 shadow-md sm:rounded-sm overflow-hidden transition hover:shadow-lg group"
        >
          <div class="p-6">
            <div class="flex justify-between items-center">
              <div>
                <div class="text-gray-900 text-3xl font-extrabold flex items-center gap-2 tracking-tight">
                  <span>{{ studentStats.boardReturnedStudents }}</span>
                  <span class="text-lg font-medium text-gray-700">জন</span>
                </div>
                <p class="text-gray-700 mt-2 font-semibold tracking-wide text-base">
                  বোর্ড ফেরত শিক্ষার্থী
                </p>
              </div>
              <div
                class="bg-gray-100 rounded-full p-3 shadow border border-gray-300"
              >
                <svg class="w-8 h-8 text-gray-600 opacity-80" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3c.5-1.7 3.5-1.7 4 0 .5 1.7-3.5 1.7-4 0zm0 18c-.5 1.7-3.5 1.7-4 0-.5-1.7 3.5-1.7 4 0zm7-9c1.7-.5 1.7-3.5 0-4-1.7-.5-1.7 3.5 0 4zM5 12c-1.7.5-1.7-3.5 0-4 1.7-.5 1.7 3.5 0 4z"/>
                </svg>
              </div>
            </div>
            <div class="mt-6 flex items-center">
              <span class="px-3 py-1 rounded bg-gray-100 text-gray-700 text-xs font-semibold tracking-wider border border-gray-300">ফেরত</span>
            </div>
          </div>
          <div class="absolute right-0 bottom-0 opacity-5 text-gray-800 text-[7rem] pointer-events-none select-none">
            <i class="pi pi-undo" />
          </div>
        </div>

        <!-- Board Submitted Students Card -->
        <div
          class="relative bg-white border border-gray-300 shadow-md sm:rounded-sm overflow-hidden transition hover:shadow-lg group"
        >
          <div class="p-6">
            <div class="flex justify-between items-center">
              <div>
                <div class="text-gray-900 text-3xl font-extrabold flex items-center gap-2 tracking-tight">
                  <span>{{ studentStats.boardSubmittedStudents }}</span>
                  <span class="text-lg font-medium text-gray-700">জন</span>
                </div>
                <p class="text-gray-700 mt-2 font-semibold tracking-wide text-base">
                  বোর্ড দাখিল শিক্ষার্থী
                </p>
              </div>
              <div
                class="bg-gray-100 rounded-full p-3 shadow border border-gray-300"
              >
                <svg class="w-8 h-8 text-gray-600 opacity-80" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
              </div>
            </div>
            <div class="mt-6 flex items-center">
              <span class="px-3 py-1 rounded bg-gray-100 text-gray-700 text-xs font-semibold tracking-wider border border-gray-300">দাখিল</span>
            </div>
          </div>
          <div class="absolute right-0 bottom-0 opacity-5 text-gray-800 text-[7rem] pointer-events-none select-none">
            <i class="pi pi-send" />
          </div>
        </div>

        <!-- Board Approved Students Card -->
        <div
          class="relative bg-white border border-gray-300 shadow-md sm:rounded-sm overflow-hidden transition hover:shadow-lg group"
        >
          <div class="p-6">
            <div class="flex justify-between items-center">
              <div>
                <div class="text-gray-900 text-3xl font-extrabold flex items-center gap-2 tracking-tight">
                  <span>{{ studentStats.approvedStudents }}</span>
                  <span class="text-lg font-medium text-gray-700">জন</span>
                </div>
                <p class="text-gray-700 mt-2 font-semibold tracking-wide text-base">
                  বোর্ড অনুমোদিত ছাত্র
                </p>
              </div>
              <div
                class="bg-gray-100 rounded-full p-3 shadow border border-gray-300"
              >
                <svg class="w-8 h-8 text-gray-600 opacity-80" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                </svg>
              </div>
            </div>
            <div class="mt-6 flex items-center">
              <span class="px-3 py-1 rounded bg-gray-100 text-gray-700 text-xs font-semibold tracking-wider border border-gray-300">অনুমোদিত</span>
            </div>
          </div>
          <div class="absolute right-0 bottom-0 opacity-5 text-gray-800 text-[7rem] pointer-events-none select-none">
            <i class="pi pi-check" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Subtle hover effect, gentle borders, formal font */
.group:hover {
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>

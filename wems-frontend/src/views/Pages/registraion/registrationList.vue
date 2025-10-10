<template>

    <div
      style="font-family: 'SolaimanLipi', sans-serif;"
      class="py-8 bg-gray-50 text-gray-800"
    >
      <div class="mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="mb-6 bg-white rounded-lg border border-gray-300 shadow">
          <div class="p-6 flex flex-col md:flex-row justify-between items-center border-b border-gray-200">
            <div class="flex items-center mb-4 md:mb-0">
              <div class="p-2 bg-gray-100 rounded-lg mr-3">
                <!-- icon -->
                <svg class="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div>
                <h2 class="text-xl font-bold text-gray-900">পরীক্ষার ফি সেটআপ</h2>
                <p class="text-gray-600 text-lg">{{ examName }}</p>
              </div>
            </div>
            <div class="flex flex-wrap gap-3">
              <div class="bg-gray-100 px-3 py-1.5 rounded text-md text-gray-700 flex items-center border border-gray-300">
                <svg class="w-4 h-4 mr-1.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ getCurrentDate() }}
              </div>
              <div class="bg-gray-100 px-3 py-1.5 rounded text-md text-gray-700 flex items-center border border-gray-300">
                <svg class="w-4 h-4 mr-1.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ getCurrentTime() }}
              </div>
              <div class="bg-gray-100 px-3 py-1.5 rounded text-md text-gray-700 flex items-center border border-gray-300">
                <svg class="w-4 h-4 mr-1.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                tahsin866
              </div>
            </div>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50">
            <div class="flex items-center p-3 bg-white rounded border border-gray-300">
              <div class="p-2 bg-gray-100 rounded-lg mr-3">
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <div class="text-md text-gray-600">মোট মারহালা</div>
                <div class="text-lg font-semibold text-gray-900">{{ formatNumber(totalRecords) }}</div>
              </div>
            </div>
            <div class="flex items-center p-3 bg-white rounded border border-gray-300">
              <div class="p-2 bg-gray-100 rounded-lg mr-3">
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div>
                <div class="text-md text-gray-600">মোট ছাত্র</div>
                <div class="text-lg font-semibold text-gray-900">
                  {{ formatNumber(examFees.reduce((sum, fee) => sum + Number(fee.regularStudents || 0), 0)) }}
                </div>
              </div>
            </div>
            <div class="flex items-center p-3 bg-white rounded border border-gray-300">
              <div class="p-2 bg-gray-100 rounded-lg mr-3">
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <div class="text-md text-gray-600">গড় ফি (নিয়মিত)</div>
                <div class="text-lg font-semibold text-gray-900">
                  ৳{{ formatNumber(Math.round(examFees.reduce((sum, fee) => sum + Number(fee.regularFee || 0), 0) / (examFees.length || 1))) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Filter and Table Controls -->
        <div class="mb-6 bg-white rounded-lg border border-gray-300 shadow">
          <div class="flex flex-col md:flex-row md:items-center justify-between p-4 border-b border-gray-200">
            <div class="relative w-full md:w-96 mb-4 md:mb-0">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                v-model="globalFilterValue"
                type="search"
                class="block w-full p-2.5 pl-10 text-xl border border-gray-300 rounded-lg bg-white focus:ring-gray-500 focus:border-gray-500"
                placeholder="অনুসন্ধান করুন..."
              >
            </div>
            <div class="flex flex-wrap gap-2">
              <button @click="showFilters = !showFilters"
                      class="flex items-center px-3.5 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700 text-xl font-medium">
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                ফিল্টার
                <span v-if="activeFiltersCount > 0"
                      class="ml-1.5 inline-flex items-center justify-center w-5 h-5 text-md font-bold text-white bg-gray-600 rounded-full">
                  {{ activeFiltersCount }}
                </span>
              </button>
              <button @click="showCustomColumns = !showCustomColumns"
                      class="flex items-center px-3.5 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700 text-xl font-medium">
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 6h16M4 12h16m-7 6h7" />
                </svg>
                কলাম
              </button>
              <button @click="exportToExcel"
                      class="flex items-center px-3.5 py-2 border border-gray-300 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 text-xl font-medium">
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                এক্সপোর্ট
              </button>
              <button @click="fetchExamFees"
                      class="flex items-center px-3.5 py-2 border border-gray-300 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 text-xl font-medium">
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                রিফ্রেশ
              </button>
            </div>
          </div>

          <!-- Advanced Filters -->
          <div v-if="showFilters" class="p-4 bg-gray-50 border-b border-gray-200">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label class="block text-xl font-medium text-gray-700 mb-1">মারহালা ফিল্টার</label>
                <input
                  v-model="filterOptions.marhalaFilter"
                  type="text"
                  class="block w-full p-2 text-xl border border-gray-300 rounded-lg focus:ring-gray-500 focus:border-gray-500"
                  placeholder="মারহালা নাম দিয়ে অনুসন্ধান..."
                >
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xl font-medium text-gray-700 mb-1">মিনিমাম ফি (নিয়মিত)</label>
                  <input
                    v-model="filterOptions.minRegularFee"
                    type="number"
                    class="block w-full p-2 text-xl border border-gray-300 rounded-lg focus:ring-gray-500 focus:border-gray-500"
                    placeholder="মিনিমাম..."
                  >
                </div>
                <div>
                  <label class="block text-xl font-medium text-gray-700 mb-1">ম্যাক্সিমাম ফি (নিয়মিত)</label>
                  <input
                    v-model="filterOptions.maxRegularFee"
                    type="number"
                    class="block w-full p-2 text-xl border border-gray-300 rounded-lg focus:ring-gray-500 focus:border-gray-500"
                    placeholder="ম্যাক্সিমাম..."
                  >
                </div>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xl font-medium text-gray-700 mb-1">মিনিমাম ফি (বিলম্ব)</label>
                  <input
                    v-model="filterOptions.minLateFee"
                    type="number"
                    class="block w-full p-2 text-xl border border-gray-300 rounded-lg focus:ring-gray-500 focus:border-gray-500"
                    placeholder="মিনিমাম..."
                  >
                </div>
                <div>
                  <label class="block text-xl font-medium text-gray-700 mb-1">ম্যাক্সিমাম ফি (বিলম্ব)</label>
                  <input
                    v-model="filterOptions.maxLateFee"
                    type="number"
                    class="block w-full p-2 text-xl border border-gray-300 rounded-lg focus:ring-gray-500 focus:border-gray-500"
                    placeholder="ম্যাক্সিমাম..."
                  >
                </div>
              </div>
              <div>
                <label class="block text-xl font-medium text-gray-700 mb-1">বিলম্ব রেজিস্ট্রেশন আছে?</label>
                <select
                  v-model="filterOptions.hasLateRegistration"
                  class="block w-full p-2 text-xl border border-gray-300 rounded-lg focus:ring-gray-500 focus:border-gray-500"
                >
                  <option value="all">সকল</option>
                  <option value="yes">হ্যাঁ</option>
                  <option value="no">না</option>
                </select>
              </div>
            </div>
            <div class="flex justify-end">
              <button @click="resetFilters"
                      class="flex items-center px-3.5 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700 text-xl font-medium">
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                ফিল্টার রিসেট
              </button>
            </div>
          </div>

          <!-- Column Selection -->
          <div v-if="showCustomColumns" class="p-4 bg-gray-50 border-b border-gray-200">
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
              <div v-for="(visible, column) in visibleColumns" :key="column"
                  class="flex items-center">
                <input
                  :id="`col-${column}`"
                  type="checkbox"
                  :checked="visible"
                  @change="() => toggleColumn(column)"
                  class="w-4 h-4 text-gray-600 border-gray-300 rounded focus:ring-gray-500"
                >
                <label :for="`col-${column}`" class="ml-2 text-xl text-gray-700">
                  {{ getColumnName(column) }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Data Table -->
        <div class="bg-white rounded-lg border border-gray-300 shadow overflow-x-auto">
          <!-- Loading -->
          <div v-if="isLoading" class="flex items-center justify-center p-16">
            <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-500"></div>
          </div>

          <template v-else>
            <table class="w-full">
              <thead class="bg-gray-100 text-gray-800 text-md uppercase tracking-wider">
                <tr>
                  <th v-if="visibleColumns.marhala_name_bn"
                      @click="sort('marhala_name_bn')"
                      class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">
                    মারহালা
                    <span v-if="sortField === 'marhala_name_bn'">
                      <svg v-if="sortOrder === 'asc'" class="inline w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                      <svg v-else class="inline w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                      </svg>
                    </span>
                  </th>

                  <th v-if="visibleColumns.regularStartDate" @click="sort('regularStartDate')" class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">নিয়মিত (শুরু)</th>
                  <th v-if="visibleColumns.regularEndDate" @click="sort('regularEndDate')" class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">নিয়মিত (শেষ)</th>
                  <th v-if="visibleColumns.regularFee" @click="sort('regularFee')" class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">নিয়মিত ফি</th>
                  <th v-if="visibleColumns.lateStartDate" @click="sort('lateStartDate')" class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">বিলম্ব (শুরু)</th>
                  <th v-if="visibleColumns.lateEndDate" @click="sort('lateEndDate')" class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">বিলম্ব (শেষ)</th>
                  <th v-if="visibleColumns.lateFee" @click="sort('lateFee')" class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">বিলম্ব ফি</th>
                  <th v-if="visibleColumns.regularStudents" @click="sort('regularStudents')" class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">নিয়মিত ছাত্র</th>
                  <th v-if="visibleColumns.irregularStudents" @click="sort('irregularStudents')" class="py-3.5 px-4 text-left font-semibold cursor-pointer hover:bg-gray-200">অনিয়মিত ছাত্র</th>
                  <th class="py-3.5 px-4 text-left font-semibold">একশন</th>
                </tr>
              </thead>

              <tbody class="divide-y divide-gray-200">
                <tr v-for="(fee, index) in displayedExamFees" :key="fee.marhala_id ?? index"
                    class="hover:bg-gray-50 transition"
                    :class="{'bg-gray-50': index % 2 === 0}">
                  <td v-if="visibleColumns.marhala_name_bn" class="px-4 py-3 whitespace-nowrap font-medium text-gray-900">
                    {{ fee.marhala_name_bn }}
                  </td>
                  <td v-if="visibleColumns.regularStartDate" class="px-4 py-3 whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-md font-medium">{{ formatDate(fee.regularStartDate) }}</span>
                  </td>
                  <td v-if="visibleColumns.regularEndDate" class="px-4 py-3 whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-md font-medium">{{ formatDate(fee.regularEndDate) }}</span>
                  </td>
                  <td v-if="visibleColumns.regularFee" class="px-4 py-3 whitespace-nowrap text-gray-900 font-semibold">৳ {{ formatNumber(fee.regularFee) }}</td>
                  <td v-if="visibleColumns.lateStartDate" class="px-4 py-3 whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-md font-medium">{{ formatDate(fee.lateStartDate) }}</span>
                  </td>
                  <td v-if="visibleColumns.lateEndDate" class="px-4 py-3 whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-md font-medium">{{ formatDate(fee.lateEndDate) }}</span>
                  </td>
                  <td v-if="visibleColumns.lateFee" class="px-4 py-3 whitespace-nowrap text-gray-900 font-semibold">৳ {{ formatNumber(fee.lateFee) }}</td>
                  <td v-if="visibleColumns.regularStudents" class="px-4 py-3 whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-md font-medium">{{ formatNumber(fee.regularStudents) }}</span>
                  </td>
                  <td v-if="visibleColumns.irregularStudents" class="px-4 py-3 whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-md font-medium">{{ formatNumber(fee.irregularStudents) }}</span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <div class="flex gap-2">
                      <RouterLink
                        :to="getOldRegistrationPath(fee.marhala_id)"
                        class="inline-flex items-center px-3 py-1.5 bg-gray-700 border border-transparent rounded-sm text-md text-white hover:bg-gray-800 transition shadow-sm"
                      >
                        নিবন্ধন
                      </RouterLink>

                      <RouterLink
                        :to="getRegistrationTablePath()"
                        class="inline-flex items-center px-3 py-1.5 bg-gray-600 border border-transparent rounded-sm text-md text-white hover:bg-gray-700 transition shadow-sm"
                      >
                        তালিকা
                      </RouterLink>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Empty State -->
            <div v-if="displayedExamFees.length === 0" class="py-16 flex flex-col items-center justify-center">
              <svg class="w-16 h-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h3 class="mt-2 text-base font-medium text-gray-900">কোন রেকর্ড পাওয়া যায়নি</h3>
              <p class="mt-1 text-xl text-gray-500">আপনার অনুসন্ধানের সাথে মিলে এমন কোন তথ্য নেই।</p>
              <button @click="resetFilters" class="mt-3 inline-flex items-center px-3 py-2 border border-transparent text-xl font-medium rounded-md text-white bg-gray-600 hover:bg-gray-700">
                ফিল্টার রিসেট করুন
              </button>
            </div>

            <!-- Pagination -->
            <div class="border-t border-gray-200">
              <div class="px-4 py-3 flex items-center justify-between">
                <div class="flex items-center">
                  <span class="text-xl text-gray-700 mr-2">প্রতি পৃষ্ঠায়:</span>
                  <select v-model="rowsPerPage" class="border border-gray-300 rounded-md text-xl p-1 focus:ring-gray-500 focus:border-gray-500">
                    <option v-for="option in [5, 10, 20, 50]" :key="option" :value="option">{{ option }}</option>
                  </select>
                  <span class="ml-4 text-xl text-gray-700">
                    দেখানো হচ্ছে {{ formatNumber((currentPage - 1) * rowsPerPage + 1) }} থেকে {{ formatNumber(Math.min(currentPage * rowsPerPage, totalRecords)) }} মোট {{ formatNumber(totalRecords) }} এর মধ্যে
                  </span>
                </div>
                <div class="flex items-center space-x-2">
                  <button
                    @click="currentPage = 1"
                    :disabled="currentPage === 1"
                    class="p-1.5 border rounded-md"
                    :class="currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                  </button>
                  <button
                    @click="currentPage = Math.max(1, currentPage - 1)"
                    :disabled="currentPage === 1"
                    class="p-1.5 border rounded-md"
                    :class="currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                  </button>
                  <div class="hidden md:flex">
                    <template v-for="page in getPageNumbers()" :key="page">
                      <button
                        v-if="page !== '...'"
                        @click="currentPage = page"
                        class="px-3 py-1 border rounded-md transition-colors"
                        :class="currentPage === page ? 'bg-gray-200 text-gray-700 border-gray-300' : 'bg-white text-gray-700 hover:bg-gray-50'"
                      >
                        {{ page }}
                      </button>
                      <span v-else class="px-3 py-1 border border-gray-200 rounded-md bg-white text-gray-700">
                        ...
                      </span>
                    </template>
                  </div>
                  <button
                    @click="currentPage = Math.min(totalPages, currentPage + 1)"
                    :disabled="currentPage === totalPages"
                    class="p-1.5 border rounded-md"
                    :class="currentPage === totalPages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                  <button
                    @click="currentPage = totalPages"
                    :disabled="currentPage === totalPages"
                    class="p-1.5 border rounded-md"
                    :class="currentPage === totalPages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

import { RouterLink } from 'vue-router'

/** Types */
type ApplicationFee = {
  marhala_id: number
  marhala_name_bn: string
  regularStartDate?: string | null
  regularEndDate?: string | null
  regularFee?: number | string | null
  lateStartDate?: string | null
  lateEndDate?: string | null
  lateFee?: number | string | null
  regularStudents?: number | string | null
  irregularStudents?: number | string | null
}

/** Reactive state */
const examFees = ref<ApplicationFee[]>([])
const examName = ref<string>('লোড হচ্ছে...')
const globalFilterValue = ref<string>('')
const currentPage = ref<number>(1)
const rowsPerPage = ref<number>(10)
const sortField = ref<string | null>(null)
const sortOrder = ref<'asc' | 'desc'>('asc')
const totalPages = ref<number>(1)
const displayedExamFees = ref<ApplicationFee[]>([])
const isLoading = ref<boolean>(true)
const showFilters = ref<boolean>(false)
const showCustomColumns = ref<boolean>(false)
const visibleColumns = ref<Record<string, boolean>>({
  marhala_name_bn: true,
  regularStartDate: true,
  regularEndDate: true,
  regularFee: true,
  lateStartDate: true,
  lateEndDate: true,
  lateFee: true,
  regularStudents: true,
  irregularStudents: true
})

const filterOptions = ref({
  marhalaFilter: '',
  minRegularFee: '',
  maxRegularFee: '',
  minLateFee: '',
  maxLateFee: '',
  hasLateRegistration: 'all'
} as {
  marhalaFilter: string
  minRegularFee: string
  maxRegularFee: string
  minLateFee: string
  maxLateFee: string
  hasLateRegistration: 'all' | 'yes' | 'no'
})

/** Mock data */
const mockData: ApplicationFee[] = [
  {
    marhala_id: 1,
    marhala_name_bn: 'কাঙ্ক্ষিত মারহালা ১',
    regularStartDate: '2025-08-01',
    regularEndDate: '2025-08-10',
    regularFee: 500,
    lateStartDate: '2025-08-11',
    lateEndDate: '2025-08-15',
    lateFee: 700,
    regularStudents: 120,
    irregularStudents: 15
  },
  {
    marhala_id: 2,
    marhala_name_bn: 'তাহফিজ',
    regularStartDate: '2025-08-05',
    regularEndDate: '2025-08-12',
    regularFee: 600,
    lateStartDate: null,
    lateEndDate: null,
    lateFee: null,
    regularStudents: 80,
    irregularStudents: 5
  },
  {
    marhala_id: 3,
    marhala_name_bn: 'আদাব',
    regularStartDate: '2025-08-03',
    regularEndDate: '2025-08-09',
    regularFee: 450,
    lateStartDate: '2025-08-10',
    lateEndDate: '2025-08-14',
    lateFee: 650,
    regularStudents: 60,
    irregularStudents: 2
  }
]

/** Fetch (mock) */
const fetchExamFees = async () => {
  isLoading.value = true
  await new Promise(resolve => setTimeout(resolve, 300))
  examFees.value = mockData.slice()
  examName.value = 'উদাহরণ পরীক্ষা ২০২৫ (ফেক ডেটা)'
  updateDisplayedData()
  setTimeout(() => { isLoading.value = false }, 120)
}

/** Helpers and logic */
const parseNum = (v: any) => {
  const n = Number(v)
  return Number.isFinite(n) ? n : 0
}

const updateDisplayedData = () => {
  let data = [...examFees.value]

  if (globalFilterValue.value) {
    const searchTerm = globalFilterValue.value.toLowerCase()
    data = data.filter(item =>
      (item.marhala_name_bn || '').toLowerCase().includes(searchTerm)
    )
  }

  if (filterOptions.value.marhalaFilter) {
    const marhalaSearch = filterOptions.value.marhalaFilter.toLowerCase()
    data = data.filter(item => (item.marhala_name_bn || '').toLowerCase().includes(marhalaSearch))
  }

  if (filterOptions.value.minRegularFee) {
    data = data.filter(item => parseNum(item.regularFee) >= parseNum(filterOptions.value.minRegularFee))
  }
  if (filterOptions.value.maxRegularFee) {
    data = data.filter(item => parseNum(item.regularFee) <= parseNum(filterOptions.value.maxRegularFee))
  }
  if (filterOptions.value.minLateFee) {
    data = data.filter(item => parseNum(item.lateFee) >= parseNum(filterOptions.value.minLateFee))
  }
  if (filterOptions.value.maxLateFee) {
    data = data.filter(item => parseNum(item.lateFee) <= parseNum(filterOptions.value.maxLateFee))
  }
  if (filterOptions.value.hasLateRegistration !== 'all') {
    const hasLate = filterOptions.value.hasLateRegistration === 'yes'
    data = data.filter(item => {
      const hasLateRegistration = !!item.lateStartDate && !!item.lateEndDate
      return hasLate ? hasLateRegistration : !hasLateRegistration
    })
  }

  if (sortField.value) {
    data.sort((a, b) => {
      const field = sortField.value as keyof ApplicationFee
      let valueA: any = (a as any)[field]
      let valueB: any = (b as any)[field]

      if (['regularFee', 'lateFee', 'regularStudents', 'irregularStudents'].includes(field as string)) {
        valueA = parseNum(valueA)
        valueB = parseNum(valueB)
      } else if (typeof valueA === 'string' && typeof valueB === 'string') {
        valueA = valueA.toLowerCase()
        valueB = valueB.toLowerCase()
      } else {
        valueA = valueA ?? ''
        valueB = valueB ?? ''
      }

      if (valueA < valueB) return sortOrder.value === 'asc' ? -1 : 1
      if (valueA > valueB) return sortOrder.value === 'asc' ? 1 : -1
      return 0
    })
  }

  totalPages.value = Math.max(1, Math.ceil(data.length / rowsPerPage.value))
  if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
  const start = (currentPage.value - 1) * rowsPerPage.value
  displayedExamFees.value = data.slice(start, start + rowsPerPage.value)
}

const resetFilters = () => {
  filterOptions.value = {
    marhalaFilter: '',
    minRegularFee: '',
    maxRegularFee: '',
    minLateFee: '',
    maxLateFee: '',
    hasLateRegistration: 'all'
  }
  globalFilterValue.value = ''
  currentPage.value = 1
  sortField.value = null
  sortOrder.value = 'asc'
  updateDisplayedData()
}

const sort = (field: string) => {
  if (sortField.value === field) sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  else {
    sortField.value = field
    sortOrder.value = 'asc'
  }
  updateDisplayedData()
}

const toggleColumn = (column: string) => {
  visibleColumns.value[column] = !visibleColumns.value[column]
}

const activeFiltersCount = computed(() => {
  let count = 0
  if (filterOptions.value.marhalaFilter) count++
  if (filterOptions.value.minRegularFee) count++
  if (filterOptions.value.maxRegularFee) count++
  if (filterOptions.value.minLateFee) count++
  if (filterOptions.value.maxLateFee) count++
  if (filterOptions.value.hasLateRegistration !== 'all') count++
  if (globalFilterValue.value) count++
  return count
})

const totalRecords = computed(() => examFees.value.length)

const exportToExcel = () => {
  window.alert('Export to Excel (mock) — nothing exported in demo mode.')
}

const formatDate = (dateString?: string | null) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    if (Number.isNaN(date.getTime())) return dateString
    return new Intl.DateTimeFormat('bn-BD', { year: 'numeric', month: 'short', day: 'numeric' }).format(date)
  } catch {
    return dateString
  }
}

const formatNumber = (num: number | string | undefined | null) => {
  if (num === undefined || num === null) return '0'
  const n = Number(num)
  if (!Number.isFinite(n)) return String(num)
  return new Intl.NumberFormat('bn-BD').format(n)
}

watch(globalFilterValue, () => {
  currentPage.value = 1
  updateDisplayedData()
})

watch(rowsPerPage, () => {
  currentPage.value = 1
  updateDisplayedData()
})

watch(currentPage, () => {
  updateDisplayedData()
})

watch(filterOptions, {
  deep: true,
  handler: () => {
    currentPage.value = 1
    updateDisplayedData()
  }
})

onMounted(() => {
  fetchExamFees()
})

const getCurrentDate = () => {
  const date = new Date()
  return new Intl.DateTimeFormat('bn-BD', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const getCurrentTime = () => {
  const date = new Date()
  return new Intl.DateTimeFormat('bn-BD', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(date)
}

const getColumnName = (column: string) => {
  const names: Record<string, string> = {
    'marhala_name_bn': 'মারহালা',
    'regularStartDate': 'নিয়মিত (শুরু)',
    'regularEndDate': 'নিয়মিত (শেষ)',
    'regularFee': 'নিয়মিত ফি',
    'lateStartDate': 'বিলম্ব (শুরু)',
    'lateEndDate': 'বিলম্ব (শেষ)',
    'lateFee': 'বিলম্ব ফি',
    'regularStudents': 'নিয়মিত ছাত্র',
    'irregularStudents': 'অনিয়মিত ছাত্র'
  }
  return names[column] || column
}

const getPageNumbers = (): (number | string)[] => {
  const pages: (number | string)[] = []
  const maxVisiblePages = 5
  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i)
  } else {
    if (currentPage.value <= 3) {
      for (let i = 1; i <= 4; i++) pages.push(i)
      pages.push('...')
      pages.push(totalPages.value)
    } else if (currentPage.value >= totalPages.value - 2) {
      pages.push(1)
      pages.push('...')
      for (let i = totalPages.value - 3; i <= totalPages.value; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = currentPage.value - 1; i <= currentPage.value + 1; i++) pages.push(i)
      pages.push('...')
      pages.push(totalPages.value)
    }
  }
  return pages
}

/** New: build route paths without Inertia route() helper
 *  Adjust paths here if your app uses different route structure.
 */
const getOldRegistrationPath = (marhalaId?: number | null) => {
  return marhalaId ? `/students-registration/old-stu-reg-form?marhalaId=${marhalaId}` : '/students-registration/old-stu-reg-form'
}

const getRegistrationTablePath = () => {
  return '/students-registration/table'
}
</script>

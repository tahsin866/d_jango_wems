<template>
  <div
  style="font-family: 'SolaimanLipi', sans-serif;"

  class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class=" mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="bg-indigo-600 p-2 rounded-sm">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Madrasha Management System</h1>
              <p class="text-lg text-gray-500">Institutional Database Management</p>
            </div>
          </div>
          <button class="bg-gray-800 text-white px-4 py-2 rounded-sm hover:bg-indigo-700 transition-colors flex items-center space-x-2 shadow-sm">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            <span>Add New Entry</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class=" mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading/Error Status -->
      <div v-if="loading" class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-lg text-blue-700">
              Loading madrasha data...
            </p>
          </div>
        </div>
      </div>

      <div v-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-lg text-red-700">
              Error: {{ error }}
            </p>
          </div>
        </div>
      </div>

      <!-- Debug Info -->
      <div v-if="!loading && !error" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="ml-3">
              <p class="text-lg text-yellow-700">
                Debug: Total Records: {{ totalCount }}, Current Page: {{ currentPage }}/{{ totalPages }},
                Page Size: {{ itemsPerPage }}, Showing: {{ sampleData.length }} records,
                Filtered: {{ filteredData.length }} records
              </p>
              <p v-if="cacheStatus" class="text-xs text-yellow-600 mt-1">
                Cache: {{ cacheStatus.cached ? 'HIT' : 'MISS' }} | Backend: {{ cacheStatus.cache_backend || 'unknown' }}
              </p>
            </div>
          </div>
          <button @click="clearCache" class="bg-red-500 text-white px-3 py-1 rounded text-xs hover:bg-red-600">
            Clear Cache
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-lg text-gray-500">Total Entries</p>
              <p class="text-2xl font-bold text-gray-900">{{ filteredData.length }}</p>
            </div>
            <div class="bg-indigo-100 p-3 rounded-sm">
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-lg text-gray-500">Male Students</p>
              <p class="text-2xl font-bold text-blue-600">{{ maleCount }}</p>
            </div>
            <div class="bg-blue-100 p-3 rounded-sm">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-lg text-gray-500">Female Students</p>
              <p class="text-2xl font-bold text-pink-600">{{ femaleCount }}</p>
            </div>
            <div class="bg-pink-100 p-3 rounded-sm">
              <svg class="w-6 h-6 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-lg text-gray-500">Active</p>
              <p class="text-2xl font-bold text-green-600">{{ activeCount }}</p>
            </div>
            <div class="bg-green-100 p-3 rounded-sm">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters Section -->
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-800 mb-2 sm:mb-0">Filters</h2>
          <div class="flex flex-wrap gap-2">
            <button @click="clearFilters" class="text-lg text-gray-500 hover:text-gray-700 transition-colors">
              Clear All
            </button>
            <button @click="refreshData" class="text-lg text-gray-500 hover:text-gray-700 transition-colors flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              Refresh
            </button>
            <div class="relative">
              <button @click="toggleColumnMenu" class="text-lg text-gray-500 hover:text-gray-700 transition-colors flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
                Columns
              </button>
              <div v-if="showColumnMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200">
                <div class="py-1">
                  <label v-for="column in availableColumns" :key="column.key" class="flex items-center px-4 py-2 text-lg text-gray-700 hover:bg-gray-100 cursor-pointer">
                    <input type="checkbox" v-model="column.visible" @change="updateColumnVisibility" class="mr-2">
                    {{ column.label }}
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="lg:col-span-2">
            <label class="block text-lg font-medium text-gray-700 mb-1">Search</label>
            <div class="relative">
              <input
                v-model="filters.search"
                type="text"
                placeholder="Search by name, village, mobile..."
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
              <svg class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
          </div>

          <!-- Division Filter -->
          <div>
            <label class="block text-lg font-medium text-gray-700 mb-1">Division</label>
            <select
              v-model="filters.division"
              :disabled="filtersLoading.divisions"
              class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100"
            >
              <option value="">All Divisions</option>
              <option v-for="division in availableDivisions" :key="division.did" :value="division.division">
                {{ division.division }}
              </option>
            </select>
            <span v-if="filtersLoading.divisions" class="text-xs text-gray-500">Loading divisions...</span>
          </div>

          <!-- District Filter -->
          <div>
            <label class="block text-lg font-medium text-gray-700 mb-1">District</label>
            <select
              v-model="filters.district"
              :disabled="filtersLoading.districts || (!filters.division && availableDivisions.length > 0)"
              class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100"
            >
              <option value="">All Districts</option>
              <option v-for="district in availableDistricts" :key="district.desid" :value="district.district">
                {{ district.district }}
              </option>
            </select>
            <span v-if="filtersLoading.districts" class="text-xs text-gray-500">Loading districts...</span>
            <span v-else-if="!filters.division && availableDivisions.length > 0" class="text-xs text-gray-500">Select a division first</span>
          </div>

          <!-- Thana Filter -->
          <div>
            <label class="block text-lg font-medium text-gray-700 mb-1">Thana/Upazila</label>
            <select
              v-model="filters.thana"
              :disabled="filtersLoading.thanas || (!filters.district && availableDistricts.length > 0)"
              class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100"
            >
              <option value="">All Thanas</option>
              <option v-for="thana in availableThanas" :key="thana.thana_id" :value="thana.thana">
                {{ thana.thana }}
              </option>
            </select>
            <span v-if="filtersLoading.thanas" class="text-xs text-gray-500">Loading thanas...</span>
            <span v-else-if="!filters.district && availableDistricts.length > 0" class="text-xs text-gray-500">Select a district first</span>
          </div>

          <!-- Stage Filter -->
          <div>
            <label class="block text-lg font-medium text-gray-700 mb-1">Stage</label>
            <select v-model="filters.stage" class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
              <option value="">All Stages</option>
              <option value="তাকমিল">তাকমিল</option>
              <option value="ফযিলত">ফযিলত</option>
              <option value="সানাবিয়া উলইয়া">সানাবিয়া উলইয়া</option>
              <option value="সানাবিয়া">সানাবিয়া</option>
              <option value="মুতাওয়াসসিতাহ">মুতাওয়াসসিতাহ</option>
              <option value="ইবতেদাইয়্যাহ">ইবতেদাইয়্যাহ</option>
              <option value="হিফজুল কোরাআন">হিফজুল কোরাআন</option>
              <option value="কিরাআত">কিরাআত</option>
            </select>
          </div>

          <!-- Student Type Filter -->
          <div>
            <label class="block text-lg font-medium text-gray-700 mb-1">Student Type</label>
            <select v-model="filters.student_type" class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
              <option value="">All Types</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>

          <!-- Mtype Filter -->
          <div>
            <label class="block text-lg font-medium text-gray-700 mb-1">Madrasha Type</label>
            <select v-model="filters.mtype" class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
              <option value="">All Types</option>
              <option value="Qawmi">Qawmi</option>
              <option value="Alia">Alia</option>
              <option value="Hafizia">Hafizia</option>
            </select>
          </div>

          <!-- Status Filter -->
          <div>
            <label class="block text-lg font-medium text-gray-700 mb-1">Status</label>
            <select v-model="filters.enabledisable" class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
              <option value="">All Status</option>
              <option value="1">Active</option>
              <option value="0">Inactive</option>
            </select>
          </div>

          <!-- School ID Filter -->
          <div>
            <label class="block text-lg font-medium text-gray-700 mb-1">School ID</label>
            <input
              v-model="filters.school_id"
              type="text"
              placeholder="Enter school ID"
              class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
          </div>
        </div>

        <!-- Export Options -->
        <div class="mt-6 pt-4 border-t border-gray-200">
          <div class="flex flex-wrap items-center justify-between">
            <div class="mb-2 sm:mb-0">
              <h3 class="text-lg font-medium text-gray-700">Export Options</h3>
              <p class="text-xs text-gray-500">Download filtered data in various formats</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <button @click="downloadExcel" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-lg leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <svg class="w-4 h-4 mr-1.5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v1a1 1 0 001 1h4a1 1 0 001-1v-1m3-2V8a2 2 0 00-2-2H8a2 2 0 00-2 2v8m5-4h4"></path>
                </svg>
                Excel
              </button>
              <button @click="downloadCSV" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-lg leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <svg class="w-4 h-4 mr-1.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v1a1 1 0 001 1h4a1 1 0 001-1v-1m3-2V8a2 2 0 00-2-2H8a2 2 0 00-2 2v8m5-4h4"></path>
                </svg>
                CSV
              </button>
              <button @click="downloadPDF" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-lg leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <svg class="w-4 h-4 mr-1.5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                </svg>
                PDF
              </button>
              <button @click="printData" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-lg leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <svg class="w-4 h-4 mr-1.5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
                </svg>
                Print
              </button>
            </div>
          </div>
        </div>

        <!-- Advanced Filters Toggle -->
        <div class="mt-4">
          <button @click="toggleAdvancedFilters" class="text-lg text-gray-500 hover:text-gray-700 transition-colors flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
            {{ showAdvancedFilters ? 'Hide' : 'Show' }} Advanced Filters
          </button>

          <div v-if="showAdvancedFilters" class="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Year Filter -->
            <div>
              <label class="block text-lg font-medium text-gray-700 mb-1">Year</label>
              <select v-model="filters.year" class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                <option value="">All Years</option>
                <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
              </select>
            </div>

            <!-- Date Range Filter -->
            <div>
              <label class="block text-lg font-medium text-gray-700 mb-1">From Date</label>
              <input
                v-model="filters.fromDate"
                type="date"
                class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
            </div>

            <div>
              <label class="block text-lg font-medium text-gray-700 mb-1">To Date</label>
              <input
                v-model="filters.toDate"
                type="date"
                class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
            </div>

            <!-- Records Per Page -->
            <div>
              <label class="block text-lg font-medium text-gray-700 mb-1">Records Per Page</label>
              <select v-model="itemsPerPage" class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th v-for="column in visibleColumns" :key="column.key"
                    @click="column.sortable ? sortBy(column.key) : null"
                    :class="[
                      'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
                      column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
                    ]">
                  <div class="flex items-center space-x-1">
                    <span>{{ column.label }}</span>
                    <svg v-if="column.sortable && sortField === column.key" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12"></path>
                    </svg>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in paginatedData" :key="item.id" class="hover:bg-gray-50 transition-colors">
                <td v-for="column in visibleColumns" :key="column.key" class="px-6 py-4 whitespace-nowrap text-lg text-gray-900">
                  <template v-if="column.key === 'name'">
                    <div>
                      <div class="text-lg font-medium text-gray-900">{{ item.mname }}</div>
                      <div class="text-lg text-gray-500">{{ item.ara_mname }}</div>
                    </div>
                  </template>
                  <template v-else-if="column.key === 'stage'">
                    {{ item.stage_display || item.stage }}
                  </template>
                  <template v-else-if="column.key === 'location'">
                    {{ item.location || (item.division_name + ', ' + item.district_name + ', ' + item.thana_name) }}
                  </template>
                  <template v-else-if="column.key === 'student_type'">
                    <span :class="item.student_type_display === 'ছাত্রী' ? 'bg-pink-100 text-pink-800' : 'bg-blue-100 text-blue-800'"
                          class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ item.student_type_display || item.student_type }}
                    </span>
                  </template>
                  <template v-else-if="column.key === 'status'">
                    <span :class="item.enabledisable === '1' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                          class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ item.enabledisable === '1' ? 'Active' : 'Inactive' }}
                    </span>
                  </template>
                  <template v-else-if="column.key === 'actions'">
                    <div class="flex space-x-2">
                      <button @click="viewItem(item)" class="text-indigo-600 hover:text-indigo-900">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                        </svg>
                      </button>
                      <button @click="editItem(item)" class="text-indigo-600 hover:text-indigo-900">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                        </svg>
                      </button>
                      <button @click="deleteItem(item)" class="text-red-600 hover:text-red-900">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                        </svg>
                      </button>
                    </div>
                  </template>
                  <template v-else>
                    {{ item[column.key] }}
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-if="filteredData.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">No records found</h3>
          <p class="mt-1 text-lg text-gray-500">Try adjusting your search or filter criteria</p>
        </div>

        <!-- Pagination -->
        <div v-if="filteredData.length > 0" class="bg-gray-50 px-6 py-3 flex items-center justify-between border-t border-gray-200">
          <div class="flex-1 flex justify-between sm:hidden">
            <button @click="prevPage" :disabled="currentPage === 1" class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-lg font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Previous
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages" class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-lg font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-lg text-gray-700">
                Showing
                <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                to
                <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, totalCount) }}</span>
                of
                <span class="font-medium">{{ totalCount }}</span>
                results
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button @click="prevPage" :disabled="currentPage === 1" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-lg font-medium text-gray-500 hover:bg-gray-50">
                  <span class="sr-only">Previous</span>
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                  </svg>
                </button>
                <button v-for="page in visiblePages" :key="page" @click="currentPage = page"
                        :class="page === currentPage ? 'bg-indigo-50 border-indigo-500 text-indigo-600' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'"
                        class="relative inline-flex items-center px-4 py-2 border text-lg font-medium">
                  {{ page }}
                </button>
                <button @click="nextPage" :disabled="currentPage === totalPages" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-lg font-medium text-gray-500 hover:bg-gray-50">
                  <span class="sr-only">Next</span>
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue';

interface Madrasha {
  id: number;
  madrasha_id: number | string;
  mtype: string;
  elhaqno: string;
  stage: string;
  stageserial: string;
  mnname: string;
  ara_mname: string;
  mname: string;
  did: number;
  des_id: number;
  tid: number;
  village: string;
  post: string;
  mobile: string;
  enabledisable: string;
  year: string | null;
  mmlabel: string;
  editdate: string;
  created_at: string;
  updated_at: string;
  division_name: string;
  district_name: string;
  thana_name: string;
  stage_display: string;
  student_type_display: string;
  student_type?: string;
  [key: string]: any;
  location: string;
}

interface Column {
  key: string;
  label: string;
  visible: boolean;
  sortable: boolean;
}


// State
const totalCount = ref(0);
const loading = ref(false);
const error = ref<string | null>(null);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const sampleData = ref<Madrasha[]>([]);
const cacheStatus = ref<any>(null);

// Filter dropdown state
const availableDivisions = ref<Array<{did: number, division: string}>>([]);
const availableDistricts = ref<Array<{did: number, desid: number, district: string}>>([]);
const availableThanas = ref<Array<{des_id: number, thana_id: number, thana: string}>>([]);
const filtersLoading = ref({
  divisions: false,
  districts: false,
  thanas: false
});

const fetchData = async () => {
  loading.value = true;
  error.value = null;
  console.log('Fetching data from:', `/api/admin/madrasha/madrasha-list/?page=${currentPage.value}&page_size=${itemsPerPage.value}`);
  try {
    const response = await fetch(`/api/admin/madrasha/madrasha-list/?page=${currentPage.value}&page_size=${itemsPerPage.value}`);
    console.log('Response status:', response.status);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API Response:', data);
    if (Array.isArray(data.results)) {
      sampleData.value = data.results;
      totalCount.value = data.total;
      cacheStatus.value = {
        cached: data.cached || false,
        cache_backend: 'unknown'
      };
      console.log('Data loaded successfully. Sample count:', data.results.length, 'Total count:', data.total, 'Cached:', data.cached);
    } else {
      console.log('Invalid data format - results is not an array:', data);
      sampleData.value = [];
      totalCount.value = 0;
    }
  } catch (err) {
    console.error('Error fetching data:', err);
    if (err instanceof Error) {
      error.value = err.message;
    } else {
      error.value = 'Failed to fetch data';
    }
    sampleData.value = [];
    totalCount.value = 0;
  } finally {
    loading.value = false;
  }
};

// Filter functions
const fetchDivisions = async () => {
  filtersLoading.value.divisions = true;
  try {
    const response = await fetch('/api/admin/madrasha/divisions/');
    if (response.ok) {
      const data = await response.json();
      availableDivisions.value = data.results || [];
    }
  } catch (error) {
    console.error('Error fetching divisions:', error);
  } finally {
    filtersLoading.value.divisions = false;
  }
};

const fetchDistricts = async (divisionId?: number) => {
  filtersLoading.value.districts = true;
  try {
    const url = divisionId
      ? `/api/admin/madrasha/districts/?did=${divisionId}`
      : '/api/admin/madrasha/districts/';
    const response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      availableDistricts.value = data.results || [];
    }
  } catch (error) {
    console.error('Error fetching districts:', error);
  } finally {
    filtersLoading.value.districts = false;
  }
};

const fetchThanas = async (districtId?: number) => {
  filtersLoading.value.thanas = true;
  try {
    const url = districtId
      ? `/api/admin/madrasha/thanas/?district_id=${districtId}`
      : '/api/admin/madrasha/thanas/';
    const response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      availableThanas.value = data.results || [];
    }
  } catch (error) {
    console.error('Error fetching thanas:', error);
  } finally {
    filtersLoading.value.thanas = false;
  }
};

// Filters
const filters = reactive({
  search: '',
  division: '',
  district: '',
  thana: '',
  stage: '',
  student_type: '',
  mtype: '',
  enabledisable: '',
  school_id: '',
  year: '',
  fromDate: '',
  toDate: ''
});

// Watch for division changes
watch(() => filters.division, async (newDivisionId) => {
  if (newDivisionId) {
    const division = availableDivisions.value.find(d => d.division === newDivisionId);
    if (division) {
      await fetchDistricts(division.did);
      await fetchThanas(); // Clear thanas when division changes
    }
  } else {
    await fetchDistricts(); // Fetch all districts
    await fetchThanas(); // Fetch all thanas
  }
  // Reset dependent filters
  filters.district = '';
  filters.thana = '';
});

// Watch for district changes
watch(() => filters.district, async (newDistrictName) => {
  if (newDistrictName && filters.division) {
    const district = availableDistricts.value.find(d => d.district === newDistrictName);
    if (district) {
      await fetchThanas(district.desid);
    }
  } else if (!filters.division) {
    await fetchThanas(); // Fetch all thanas if no division selected
  }
  // Reset thana filter
  filters.thana = '';
});

onMounted(() => {
  fetchData();
  fetchDivisions();
  fetchDistricts();
  fetchThanas();
});

watch([currentPage, itemsPerPage], () => {
  fetchData();
});
const showColumnMenu = ref(false);
const showAdvancedFilters = ref(false);

// Initialize columns with default visibility
const initializeColumns = (): Column[] => {
  // Try to load saved column settings from localStorage
  const savedColumns = localStorage.getItem('madrashaTableColumns');
  if (savedColumns) {
    try {
      return JSON.parse(savedColumns);
    } catch (e) {
      console.error('Error parsing saved columns:', e);
    }
  }

  // Default columns if no saved settings
  return [
    { key: 'id', label: 'ID', visible: true, sortable: true },
    { key: 'madrasha_id', label: 'Madrasha ID', visible: true, sortable: true },
    { key: 'name', label: 'Name', visible: true, sortable: true },
    { key: 'stage', label: 'Stage', visible: true, sortable: true },
    { key: 'location', label: 'Location', visible: true, sortable: true },
    { key: 'student_type', label: 'Student Type', visible: true, sortable: true },
    { key: 'mobile', label: 'Mobile', visible: true, sortable: true },
    { key: 'status', label: 'Status', visible: true, sortable: true },
    { key: 'actions', label: 'Actions', visible: true, sortable: false }
  ];
};

const availableColumns = ref<Column[]>(initializeColumns());

// Sorting and pagination
const sortField = ref('id');
const sortDirection = ref<'asc' | 'desc'>('asc');
// Remove duplicate declarations

// Computed properties
const visibleColumns = computed(() => {
  return availableColumns.value.filter(column => column.visible);
});

const filteredData = computed(() => {
  console.log('Computing filteredData. Current page data length:', sampleData.value.length);
  let filtered = sampleData.value;

  // Apply client-side filtering to the current page data
  // Note: For better performance, these filters should be moved to backend API calls

  // Search filter
  if (filters.search) {
    const search = filters.search.toLowerCase();
    filtered = filtered.filter((item: Madrasha) =>
      item.mname?.toLowerCase().includes(search) ||
      item.village?.toLowerCase().includes(search) ||
      item.mobile?.includes(search) ||
      item.madrasha_id?.toString().includes(search) ||
      item.district_name?.toLowerCase().includes(search) ||
      item.thana_name?.toLowerCase().includes(search)
    );
    console.log('After search filter, length:', filtered.length);
  }

  // Division filter
  if (filters.division) {
    filtered = filtered.filter((item: Madrasha) => item.division_name === filters.division);
  }

  // District filter
  if (filters.district) {
    filtered = filtered.filter((item: Madrasha) => item.district_name === filters.district);
  }

  // Thana filter
  if (filters.thana) {
    filtered = filtered.filter((item: Madrasha) => item.thana_name === filters.thana);
  }

  // Stage filter
  if (filters.stage) {
    filtered = filtered.filter((item: Madrasha) => item.stage_display === filters.stage);
  }

  // Student type filter
  if (filters.student_type) {
    const studentTypeMap: { [key: string]: string } = {
      'Male': 'ছাত্র',
      'Female': 'ছাত্রী'
    };
    filtered = filtered.filter((item: Madrasha) => item.student_type_display === studentTypeMap[filters.student_type]);
  }

  // Mtype filter
  if (filters.mtype) {
    filtered = filtered.filter((item: Madrasha) => item.mtype === filters.mtype);
  }

  // Status filter
  if (filters.enabledisable !== '') {
    filtered = filtered.filter((item: Madrasha) => item.enabledisable === filters.enabledisable);
  }

  // School ID filter
  if (filters.school_id) {
    filtered = filtered.filter((item: Madrasha) =>
      item.madrasha_id?.toString().toLowerCase().includes(filters.school_id.toLowerCase())
    );
  }

  // Year filter
  if (filters.year) {
    filtered = filtered.filter((item: Madrasha) => item.year === filters.year);
  }

  // Date range filter
  if (filters.fromDate) {
    const fromDate = new Date(filters.fromDate);
    filtered = filtered.filter((item: Madrasha) => new Date(item.created_at) >= fromDate);
  }

  if (filters.toDate) {
    const toDate = new Date(filters.toDate);
    toDate.setHours(23, 59, 59, 999); // Include the entire day
    filtered = filtered.filter((item: Madrasha) => new Date(item.created_at) <= toDate);
  }

  // Sorting
  filtered.sort((a: Madrasha, b: Madrasha) => {
    const aVal = a[sortField.value as keyof Madrasha];
    const bVal = b[sortField.value as keyof Madrasha];
    if (aVal == null && bVal == null) return 0;
    if (aVal == null) return 1;
    if (bVal == null) return -1;
    if (sortDirection.value === 'asc') {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  console.log('Final filteredData length:', filtered.length);
  return filtered;
});

const paginatedData = computed(() => {
  // Since we're using backend pagination, paginatedData is just the filtered current page data
  return filteredData.value;
});

const totalPages = computed(() => {
  // Use total count from backend API response
  return Math.ceil(totalCount.value / itemsPerPage.value);
});

const visiblePages = computed(() => {
  const pages = [];
  const maxVisible = 5;
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2));
  const end = Math.min(totalPages.value, start + maxVisible - 1);

  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1);
  }

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

const availableYears = computed(() => {
  const years = [...new Set(sampleData.value.map(item => item.year).filter(Boolean))];
  return years.sort();
});

const activeCount = computed(() => {
  return filteredData.value.filter(item => item.enabledisable === '1').length;
});

const maleCount = computed(() => {
  return filteredData.value.filter(item => item.student_type_display === 'ছাত্র').length;
});

const femaleCount = computed(() => {
  return filteredData.value.filter(item => item.student_type_display === 'ছাত্রী').length;
});

// Methods
// ...existing code...

const clearFilters = () => {
  filters.search = '';
  filters.division = '';
  filters.district = '';
  filters.thana = '';
  filters.stage = '';
  filters.student_type = '';
  filters.mtype = '';
  filters.enabledisable = '';
  filters.school_id = '';
  filters.year = '';
  filters.fromDate = '';
  filters.toDate = '';
  currentPage.value = 1;
};

const refreshData = () => {
  fetchData();
};

const toggleColumnMenu = () => {
  showColumnMenu.value = !showColumnMenu.value;
};

const toggleAdvancedFilters = () => {
  showAdvancedFilters.value = !showAdvancedFilters.value;
};

const updateColumnVisibility = () => {
  // Save column settings to localStorage
  localStorage.setItem('madrashaTableColumns', JSON.stringify(availableColumns.value));
};

const sortBy = (field: string) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortDirection.value = 'asc';
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const viewItem = (item: Madrasha) => {
  console.log('View item:', item);
  // Implement view functionality
};

const editItem = (item: Madrasha) => {
  console.log('Edit item:', item);
  // Implement edit functionality
};

const deleteItem = (item: Madrasha) => {
  console.log('Delete item:', item);
  // Implement delete functionality
};

const downloadExcel = () => {
  // Excel download functionality
  console.log('Download Excel');
  // Implement Excel download
};

const downloadCSV = () => {
  // CSV download functionality
  console.log('Download CSV');
  // Implement CSV download
};

const downloadPDF = () => {
  // PDF download functionality
  console.log('Download PDF');
  // Implement PDF download
};

const printData = () => {
  // Print functionality
  window.print();
};

const clearCache = async () => {
  try {
    const response = await fetch('/api/admin/madrasha/cache/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      }
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Cache cleared:', result);
      // Refresh data after clearing cache
      await fetchData();
    } else {
      console.error('Failed to clear cache');
    }
  } catch (error) {
    console.error('Error clearing cache:', error);
  }
};

const getCsrfToken = () => {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

</script>

<style scoped>
/* Custom styles for print */
@media print {
  .no-print {
    display: none !important;
  }
}
</style>

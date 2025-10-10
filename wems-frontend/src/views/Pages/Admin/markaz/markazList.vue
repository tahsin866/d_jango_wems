<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;" class="min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-white shadow border-b border-gray-300 rounded-b-sm">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="bg-indigo-700 p-2 rounded-sm shadow">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-3xl font-bold text-gray-900 leading-tight">মারকাজ মাদরাসার তালিকা</h1>
              <p class="text-base text-gray-600">কেন্দ্রভিত্তিক মাদরাসা ডেটাবেস ব্যবস্থাপনা</p>
            </div>
          </div>
          <button class="bg-indigo-700 text-white px-4 py-2 rounded-sm hover:bg-indigo-800 transition-colors flex items-center space-x-2 shadow">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            <span>নতুন ডাটা এন্ট্রি করুন</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading/Error Status -->
      <div v-if="loading" class="bg-blue-100 border border-blue-300 rounded-sm p-4 mb-6 shadow-sm">
        <div class="flex items-center">
          <svg class="h-6 w-6 text-blue-500 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
          <span class="text-lg font-medium text-blue-700">Loading markaz madrasha data...</span>
        </div>
      </div>

      <div v-if="error" class="bg-red-100 border border-red-300 rounded-sm p-4 mb-6 shadow-sm">
        <div class="flex items-center">
          <svg class="h-6 w-6 text-red-500 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <span class="text-lg font-medium text-red-700">Error: {{ error }}</span>
        </div>
      </div>

      <!-- Debug Info -->
      <div v-if="!loading && !error" class="bg-yellow-100 border border-yellow-300 rounded-sm p-4 mb-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-base text-yellow-900">
              Debug: Total Records: {{ totalCount }}, Current Page: {{ currentPage }}/{{ totalPages }},
              Page Size: {{ itemsPerPage }}, Showing: {{ sampleData.length }} records,
              Filtered: {{ filteredData.length }} records
            </p>
            <p v-if="cacheStatus" class="text-md text-yellow-700 mt-1">
              Cache: {{ cacheStatus.cached ? 'HIT' : 'MISS' }} | Backend: {{ cacheStatus.cache_backend || 'unknown' }}
            </p>
          </div>
          <button @click="clearCache" class="bg-red-500 text-white px-3 py-1 rounded-sm text-md hover:bg-red-600 shadow">
            Clear Cache
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-sm shadow border border-gray-300 p-4 hover:shadow-md transition-shadow">
          <p class="text-base text-gray-600 mb-1">মোট মারকাজ মাদরাসা</p>
          <p class="text-2xl font-bold text-gray-900">{{ statisticsData.total_markaz }}</p>
        </div>
        <div class="bg-white rounded-sm shadow border border-gray-300 p-4 hover:shadow-md transition-shadow">
          <p class="text-base text-gray-600 mb-1">মোট ছাত্র মাদরাসা</p>
          <p class="text-2xl font-bold text-blue-700">{{ maleCount }}</p>
        </div>
        <div class="bg-white rounded-sm shadow border border-gray-300 p-4 hover:shadow-md transition-shadow">
          <p class="text-base text-gray-600 mb-1">মোট ছাত্রী মাদরাসা</p>
          <p class="text-2xl font-bold text-pink-600">{{ femaleCount }}</p>
        </div>
        <div class="bg-white rounded-sm shadow border border-gray-300 p-4 hover:shadow-md transition-shadow">
          <p class="text-base text-gray-600 mb-1">একটিভ মাদরাসা</p>
          <p class="text-2xl font-bold text-green-600">{{ activeCount }}</p>
        </div>
      </div>

      <!-- Filters Section -->
      <div class="bg-white rounded-sm shadow border border-gray-300 p-6 mb-6">
  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
    <h2 class="text-base font-semibold text-gray-800 mb-2 sm:mb-0">সার্চ ইউজার্ড</h2>
    <div class="flex flex-wrap gap-2">
      <button @click="clearFilters" class="text-base text-gray-600 hover:text-gray-900 transition-colors">
        ক্লিয়ার করুন
      </button>
      <button @click="refreshData" class="text-base text-gray-600 hover:text-gray-900 transition-colors flex items-center">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        রিফ্রেশ করুন
      </button>
      <div class="relative">
        <button @click="toggleColumnMenu" class="text-base text-gray-600 hover:text-gray-900 transition-colors flex items-center">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
          কলাম বাড়ানো কমানো
        </button>
        <div v-if="showColumnMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-sm shadow-lg z-10 border border-gray-300">
          <div class="py-1">
            <label v-for="column in availableColumns" :key="column.key" class="flex items-center px-4 py-2 text-base text-gray-700 hover:bg-gray-100 cursor-pointer">
              <input type="checkbox" v-model="column.visible" @change="updateColumnVisibility" class="mr-2">
              {{ column.label }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- All Filter Inputs -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <!-- Search -->
    <div class="lg:col-span-2">
      <label class="block text-base font-semibold text-gray-700 mb-1">অনুসন্ধান করুন</label>
      <div class="relative">
        <IconField class="w-full">
          <InputIcon class="text-gray-400">
            <i class="pi pi-search" />
          </InputIcon>
          <InputText v-model="filters.search" placeholder="নাম, ইলহাক, দিয়ে সার্চ করুন..." class="w-full" />
        </IconField>
      </div>
    </div>
    <!-- Division Filter -->
    <div>
      <label class="block text-base font-medium text-gray-700 mb-1">বিভাগ</label>
      <Select
        v-model="filters.division"
        :disabled="filtersLoading.divisions"
        :options="[{ value: '', label: 'সকল বিভাগ' }, ...availableDivisions.map(d => ({ value: d.division, label: d.division }))]"
        option-label="label"
        option-value="value"
        placeholder="সকল বিভাগ"
        class="w-full"
      />
      <span v-if="filtersLoading.divisions" class="text-md text-gray-500">Loading divisions...</span>
    </div>
    <!-- District Filter -->
    <div>
      <label class="block text-base font-medium text-gray-700 mb-1">জেলা</label>
      <Select
        v-model="filters.district"
        :disabled="filtersLoading.districts || (!filters.division && availableDivisions.length > 0)"
        :options="[{ value: '', label: 'সকল জেলা' }, ...availableDistricts.map(d => ({ value: d.district, label: d.district }))]"
        option-label="label"
        option-value="value"
        placeholder="সকল জেলা"
        class="w-full"
      />
      <span v-if="filtersLoading.districts" class="text-md text-gray-500">Loading districts...</span>
      <span v-else-if="!filters.division && availableDivisions.length > 0" class="text-md text-gray-500">Select a division first</span>
    </div>
    <!-- Thana Filter -->
    <div>
      <label class="block text-base font-medium text-gray-700 mb-1">থানা/উপজিলা</label>
      <Select
        v-model="filters.thana"
        :disabled="filtersLoading.thanas || (!filters.district && availableDistricts.length > 0)"
        :options="[{ value: '', label: 'সকল থানা' }, ...availableThanas.map(t => ({ value: t.thana, label: t.thana }))]"
        option-label="label"
        option-value="value"
        placeholder="সকল থানা"
        class="w-full"
      />
      <span v-if="filtersLoading.thanas" class="text-md text-gray-500">Loading thanas...</span>
      <span v-else-if="!filters.district && availableDistricts.length > 0" class="text-md text-gray-500">Select a district first</span>
    </div>
    <!-- Stage Filter -->
    <div>
      <label class="block text-base font-medium text-gray-700 mb-1">মারহালা স্তর</label>
      <Select
        v-model="filters.stage"
        :options="[
          { value: '', label: 'সকল মারহালা স্তর' },
          { value: 'তাকমিল', label: 'তাকমিল' },
          { value: 'ফযিলত', label: 'ফযিলত' },
          { value: 'সানাবিয়া উলইয়া', label: 'সানাবিয়া উলইয়া' },
          { value: 'সানাবিয়া', label: 'সানাবিয়া' },
          { value: 'মুতাওয়াসসিতাহ', label: 'মুতাওয়াসসিতাহ' },
          { value: 'ইবতেদাইয়্যাহ', label: 'ইবতেদাইয়্যাহ' },
          { value: 'হিফজুল কোরাআন', label: 'হিফজুল কোরাআন' },
          { value: 'কিরাআত', label: 'কিরাআত' }
        ]"
        option-label="label"
        option-value="value"
        placeholder="সকল মারহালা স্তর"
        class="w-full"
      />
    </div>
    <!-- Student Type Filter -->
    <div>
      <label class="block text-base font-medium text-gray-700 mb-1">মাদরাসা টাইপ</label>
      <Select
        v-model="filters.student_type"
        :options="[
          { value: '', label: 'সকল মাদরাসা টাইপ' },
          { value: 'Male', label: 'ছাত্র' },
          { value: 'Female', label: 'ছাত্রী' }
        ]"
        option-label="label"
        option-value="value"
        placeholder="সকল মাদরাসা টাইপ"
        class="w-full"
      />
    </div>
    <!-- Center Filter -->
    <div>
      <label class="block text-base font-medium text-gray-700 mb-1">কেন্দ্র</label>
      <Select
        v-model="filters.center_id"
        :disabled="filtersLoading.centers"
        :options="[{ value: '', label: 'সকল কেন্দ্র' }, ...availableCenters.map(c => ({ value: c.id, label: c.name }))]"
        option-label="label"
        option-value="value"
        placeholder="সকল কেন্দ্র"
        class="w-full"
      />
      <span v-if="filtersLoading.centers" class="text-md text-gray-500">Loading centers...</span>
    </div>
    <!-- Status Filter -->
    <div>
      <label class="block text-base font-medium text-gray-700 mb-1">Status</label>
      <Select
        v-model="filters.enabledisable"
        :options="[
          { value: '', label: 'All Status' },
          { value: '1', label: 'Active' },
          { value: '0', label: 'Inactive' }
        ]"
        option-label="label"
        option-value="value"
        placeholder="All Status"
        class="w-full"
      />
    </div>
  </div>

  <!-- Export Options -->
  <div class="mt-6 pt-4 border-t border-gray-200">
    <div class="flex flex-wrap items-center justify-between">
      <div class="mb-2 sm:mb-0">
        <h3 class="text-base font-medium text-gray-700">এক্সপোর্ট অপশন</h3>
        <p class="text-md text-gray-500">ফিল্টারড ডাটাকে বিভিন্ন ফরম্যাটে ডাউনলোড করুন</p>
      </div>
      <div class="flex flex-wrap gap-2">
        <button @click="downloadExcel" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-base font-medium rounded-sm text-green-700 bg-white hover:bg-gray-50 transition">
          <svg class="w-4 h-4 mr-1.5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v1a1 1 0 001 1h4a1 1 0 001-1v-1m3-2V8a2 2 0 00-2-2H8a2 2 0 00-2 2v8m5-4h4"></path>
          </svg>
          Excel
        </button>
        <button @click="downloadCSV" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-base font-medium rounded-sm text-blue-700 bg-white hover:bg-gray-50 transition">
          <svg class="w-4 h-4 mr-1.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v1a1 1 0 001 1h4a1 1 0 001-1v-1m3-2V8a2 2 0 00-2-2H8a2 2 0 00-2 2v8m5-4h4"></path>
          </svg>
          CSV
        </button>
        <button @click="downloadPDF" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-base font-medium rounded-sm text-red-700 bg-white hover:bg-gray-50 transition">
          <svg class="w-4 h-4 mr-1.5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
          </svg>
          PDF
        </button>
        <button @click="printData" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-base font-medium rounded-sm text-gray-700 bg-white hover:bg-gray-50 transition">
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
    <button @click="toggleAdvancedFilters" class="text-base text-gray-600 hover:text-gray-900 transition-colors flex items-center">
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
      {{ showAdvancedFilters ? 'হাইড' : 'শো' }} এডভান্সড ফিল্টার
    </button>

    <div v-if="showAdvancedFilters" class="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Year Filter -->
      <div>
        <label class="block text-base font-medium text-gray-700 mb-1">বছর</label>
        <Select
          v-model="filters.year"
          :options="[{ value: '', label: 'সকল বছর' }, ...availableYears.map(y => ({ value: y, label: y }))]"
          option-label="label"
          option-value="value"
          placeholder="সকল বছর"
          class="w-full"
        />
      </div>
      <!-- Date Range Filter -->
      <div>
        <label class="block text-base font-medium text-gray-700 mb-1">তারিখ থেকে</label>
        <Calendar
          v-model="filters.fromDate"
          :show-icon="true"
          date-format="yy-mm-dd"
          placeholder="Select date from"
          class="w-full"
        />
      </div>
      <div>
        <label class="block text-base font-medium text-gray-700 mb-1">তারিখ পর্যন্ত</label>
        <Calendar
          v-model="filters.toDate"
          :show-icon="true"
          date-format="yy-mm-dd"
          placeholder="Select date to"
          class="w-full"
        />
      </div>
      <!-- Records Per Page -->
      <div>
        <label class="block text-base font-medium text-gray-700 mb-1">প্রতি পেজে সারি দেখান</label>
        <Select
          v-model="itemsPerPage"
          :options="[
            { value: '10', label: '10' },
            { value: '25', label: '25' },
            { value: '50', label: '50' },
            { value: '100', label: '100' }
          ]"
          option-label="label"
          option-value="value"
          placeholder="10"
          class="w-full"
        />
      </div>
    </div>
  </div>
</div>

      <!-- PrimeVue DataTable -->
    <div class="bg-white rounded-sm shadow border border-gray-300">
      <DataTable
        :value="filteredData"
        :paginator="true"
        :rows="parseInt(itemsPerPage)"
        :totalRecords="totalCount"
        :lazy="true"
        :loading="loading"
        @page="onPage($event)"
        @sort="onSort($event)"
        :sortField="sortField"
        :sortOrder="sortDirection === 'asc' ? 1 : -1"
        :scrollable="filteredData.length > 50"
        scrollHeight="500px"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
        :rowsPerPageOptions="[10, 25, 50, 100]"
        :globalFilterFields="['mname', 'village', 'mobile', 'madrasha_id', 'district_name', 'thana_name']"
        :filters="filters"
        responsiveLayout="scroll"
        :stripedRows="true"
        class="p-datatable-sm"
      >
        <!-- ID Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'id')?.visible"
          field="id"
          header="আইডি"
          :sortable="true"
          style="min-width: 80px"
        >
          <template #body="{ data }">
            <span class="font-medium text-gray-900">{{ data.id }}</span>
          </template>
        </Column>

        <!-- Center ID Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'center_id')?.visible"
          field="center_id"
          header="কেন্দ্রের ধরণ"
          :sortable="true"
          style="min-width: 120px"
        >
          <template #body="{ data }">
            <span class="bg-purple-100 text-purple-800 px-2 py-1 inline-flex text-sm leading-5 font-semibold rounded">
              {{ data.center_name_display || `কেন্দ্র ${data.center_id}` }}
            </span>
          </template>
        </Column>

        <!-- Serial Number Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'serial_number')?.visible"
          field="serial_number"
          header="সিরিয়াল নম্বর"
          :sortable="true"
          style="min-width: 120px"
        >
          <template #body="{ data }">
            <span class="font-medium text-gray-900">{{ data.serial_number }}</span>
          </template>
        </Column>

        <!-- Elhaq Number Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'elhaqno')?.visible"
          field="elhaqno"
          header="ইলহাক নম্বর"
          :sortable="true"
          style="min-width: 120px"
        >
          <template #body="{ data }">
            <span class="text-gray-900">{{ data.elhaqno }}</span>
          </template>
        </Column>

        <!-- Name Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'name')?.visible"
          field="mname"
          header="নাম"
          :sortable="true"
          style="min-width: 200px"
        >
          <template #body="{ data }">
            <div>
              <div class="font-semibold text-gray-900">{{ data.mname }}</div>
              <div class="text-sm text-gray-500">{{ data.ara_mname }}</div>
            </div>
          </template>
        </Column>

        <!-- Stage Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'stage')?.visible"
          field="stage_display"
          header="মারহালা স্তর"
          :sortable="true"
          style="min-width: 140px"
        >
          <template #body="{ data }">
            <span class="bg-indigo-100 text-indigo-800 px-2 py-1 inline-flex text-sm leading-5 font-semibold rounded">
              {{ data.stage_display || data.stage }}
            </span>
          </template>
        </Column>

        <!-- Location Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'location')?.visible"
          field="location"
          header="ঠিকানা"
          :sortable="true"
          style="min-width: 200px"
        >
          <template #body="{ data }">
            <span class="text-gray-900">{{ data.location || (data.division_name + ', ' + data.district_name + ', ' + data.thana_name) }}</span>
          </template>
        </Column>

        <!-- Student Type Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'student_type')?.visible"
          field="student_type_display"
          header="মাদরাসার ধরণ"
          :sortable="true"
          style="min-width: 120px"
        >
          <template #body="{ data }">
            <span :class="data.student_type_display === 'ছাত্রী' ? 'bg-pink-100 text-pink-800' : 'bg-blue-100 text-blue-800'"
                  class="px-2 py-1 inline-flex text-sm leading-5 font-semibold rounded">
              {{ data.student_type_display || data.student_type }}
            </span>
          </template>
        </Column>

        <!-- Mobile Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'mobile')?.visible"
          field="mobile"
          header="মোবাইল"
          :sortable="true"
          style="min-width: 120px"
        >
          <template #body="{ data }">
            <span class="text-gray-900">{{ data.mobile }}</span>
          </template>
        </Column>

        <!-- Status Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'status')?.visible"
          field="enabledisable"
          header="স্ট্যটাস"
          :sortable="true"
          style="min-width: 120px"
        >
          <template #body="{ data }">
            <div class="flex items-center gap-2">
              <InputSwitch
                :model-value="data.enabledisable"
                :true-value="'1'"
                :false-value="'0'"
                @update:modelValue="onStatusSwitch(data, $event)"
              />
              <span
                :class="data.enabledisable === '1' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                class="px-2 py-1 inline-flex text-sm leading-5 font-semibold rounded"
              >
                {{ data.enabledisable === '1' ? 'সক্রিয়' : 'নিষ্ক্রিয়' }}
              </span>
            </div>
          </template>
        </Column>

        <!-- Actions Column -->
        <Column
          v-if="visibleColumns.find(c => c.key === 'actions')?.visible"
          field="actions"
          header="একশন"
          :exportable="false"
          style="min-width: 120px"
        >
          <template #body="{ data }">
            <SplitButton
              :label="'বিস্তারিত'"
              :model="[
                { label: 'সেটিংস', icon: 'pi pi-cog', command: () => editItem(data) },
                { label: 'মুছে ফেলুন', icon: 'pi pi-trash', command: () => deleteItem(data) },
                { label: 'বার্তা পাঠান', icon: 'pi pi-comments', command: () => sendMessage(data) },
                { label: 'পিডিএফ ডাউনলোড করুন', icon: 'pi pi-file-pdf', command: () => downloadPDF() },
                { label: 'ইমেইল করুন', icon: 'pi pi-envelope', command: () => sendEmail(data) },
                { label: 'একটিভ করুন', icon: 'pi pi-check', command: () => activateItem(data) },
                { label: 'ডিঅ্যাক্টিভ করুন', icon: 'pi pi-times-circle', command: () => deactivateItem(data) }
              ]"
              class="p-button-outlined p-button-sm"
              @click="viewItem(data)"
            />
          </template>
        </Column>

        <!-- Empty State Template -->
        <template #empty>
          <div class="text-center py-8">
            <i class="pi pi-inbox text-4xl text-gray-400"></i>
            <h3 class="mt-2 text-lg font-semibold text-gray-900">No records found</h3>
            <p class="mt-1 text-gray-500">Try adjusting your search or filter criteria</p>
          </div>
        </template>

        <!-- Loading Template -->
        <template #loading>
          <div class="text-center py-8">
            <i class="pi pi-spinner pi-spin text-2xl text-blue-500"></i>
            <p class="mt-2 text-gray-600">Loading data...</p>
          </div>
        </template>
      </DataTable>
    </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue';
import SplitButton from 'primevue/splitbutton'
import InputSwitch from 'primevue/inputswitch'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Calendar from 'primevue/calendar'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ColumnGroup from 'primevue/columngroup'
import Row from 'primevue/row'
import 'primeicons/primeicons.css'

interface MarkazMadrasha {
  id: number;
  madrasha_id: number | string;
  center_id: number;
  center_name_display: string;
  serial_number: string;
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
  status?: string;
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
  [key: string]: unknown;
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
const sampleData = ref<MarkazMadrasha[]>([]);
type CacheStatus = { cached?: boolean; cache_backend?: string };
const cacheStatus = ref<CacheStatus | null>(null);

// Statistics state
const statisticsData = ref({
  total_markaz: 0,
  male_count: 0,
  female_count: 0,
  active_count: 0
});
const statisticsLoading = ref(false);

// Filter dropdown state
const availableDivisions = ref<Array<{did: number, division: string}>>([]);
const availableDistricts = ref<Array<{did: number, desid: number, district: string}>>([]);
const availableThanas = ref<Array<{des_id: number, thana_id: number, thana: string}>>([]);
const availableCenters = ref<Array<{id: number, name: string, code: string}>>([]);
const filtersLoading = ref({
  divisions: false,
  districts: false,
  thanas: false,
  centers: false
});

const fetchData = async () => {
  loading.value = true;
  error.value = null;
  console.log('Fetching markaz data from:', `/api/admin/markaz/markaz-list/?page=${currentPage.value}&page_size=${itemsPerPage.value}`);
  try {
    const response = await fetch(`/api/admin/markaz/markaz-list/?page=${currentPage.value}&page_size=${itemsPerPage.value}`);
    console.log('Response status:', response.status);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API Response:', data);
    if (Array.isArray(data.results)) {
      sampleData.value = (data.results as Array<MarkazMadrasha & { status?: string }>).map((row) => ({
        ...row,
        enabledisable: row.status === '1' ? '1' : '0'
      }));
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

const onStatusSwitch = async (item: MarkazMadrasha, val: string) => {
  // optimistic UI update
  const prev = item.enabledisable;
  item.enabledisable = val;
  try {
    const res = await fetch(`/api/admin/markaz/status/${item.id}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({ status: val === '1' ? 1 : 0 })
    });
    if (!res.ok) {
      throw new Error(`Failed to update status: ${res.status}`);
    }
    const data = await res.json();
    // Ensure UI reflects backend truth; also map backend status to enabledisable for display
    // Backend now returns status as string ('1' or '0')
    const backendStatus = data.status === '1' ? '1' : '0';
    item.enabledisable = backendStatus;
    // Also update the item's status field to maintain consistency
    item.status = data.status;
  } catch (e) {
    console.error(e);
    // revert on error
    item.enabledisable = prev;
    alert('স্ট্যাটাস আপডেট ব্যর্থ হয়েছে');
  }
};

// Filter functions
const fetchDivisions = async () => {
  filtersLoading.value.divisions = true;
  try {
    const response = await fetch('/api/admin/markaz/divisions/');
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
      ? `/api/admin/markaz/districts/?did=${divisionId}`
      : '/api/admin/markaz/districts/';
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
      ? `/api/admin/markaz/thanas/?district_id=${districtId}`
      : '/api/admin/markaz/thanas/';
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

const fetchCenters = async () => {
  filtersLoading.value.centers = true;
  try {
    const response = await fetch('/api/admin/markaz/centers/');
    if (response.ok) {
      const data = await response.json();
      availableCenters.value = data.results || [];
    }
  } catch (error) {
    console.error('Error fetching centers:', error);
  } finally {
    filtersLoading.value.centers = false;
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
  center_id: '',
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
  fetchStatistics();
  fetchDivisions();
  fetchDistricts();
  fetchThanas();
  fetchCenters();
});

watch([currentPage, itemsPerPage], () => {
  fetchData();
});
const showColumnMenu = ref(false);
const showAdvancedFilters = ref(false);

// Initialize columns with default visibility
const initializeColumns = (): Column[] => {
  // Try to load saved column settings from localStorage
  const savedColumns = localStorage.getItem('markazTableColumns');
  if (savedColumns) {
    try {
      return JSON.parse(savedColumns);
    } catch (e) {
      console.error('Error parsing saved columns:', e);
    }
  }

  // Default columns if no saved settings
  return [
    { key: 'id', label: 'আইডি', visible: true, sortable: true },
    { key: 'center_id', label: 'কেন্দ্রের ধরণ', visible: true, sortable: true },
    { key: 'serial_number', label: 'সিরিয়াল নম্বর', visible: true, sortable: true },
    { key: 'elhaqno', label: 'ইলহাক নম্বর', visible: true, sortable: true },
    { key: 'name', label: 'নাম', visible: true, sortable: true },
    { key: 'stage', label: 'মারহালা স্তর', visible: true, sortable: true },
    { key: 'location', label: 'ঠিকানা', visible: true, sortable: true },
    { key: 'student_type', label: 'মাদরাসার ধরণ', visible: true, sortable: true },
    { key: 'mobile', label: 'মোবাইল', visible: true, sortable: true },
    { key: 'status', label: 'স্ট্যটাস', visible: true, sortable: true },
    { key: 'actions', label: 'একশন', visible: true, sortable: false }
  ];
};

const availableColumns = ref<Column[]>(initializeColumns());

// Sorting and pagination
const sortField = ref('id');
const sortDirection = ref<'asc' | 'desc'>('asc');

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
    filtered = filtered.filter((item: MarkazMadrasha) =>
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
    filtered = filtered.filter((item: MarkazMadrasha) => item.division_name === filters.division);
  }

  // District filter
  if (filters.district) {
    filtered = filtered.filter((item: MarkazMadrasha) => item.district_name === filters.district);
  }

  // Thana filter
  if (filters.thana) {
    filtered = filtered.filter((item: MarkazMadrasha) => item.thana_name === filters.thana);
  }

  // Stage filter
  if (filters.stage) {
    filtered = filtered.filter((item: MarkazMadrasha) => item.stage_display === filters.stage);
  }

  // Student type filter
  if (filters.student_type) {
    const studentTypeMap: { [key: string]: string } = {
      'Male': 'ছাত্র',
      'Female': 'ছাত্রী'
    };
    filtered = filtered.filter((item: MarkazMadrasha) => item.student_type_display === studentTypeMap[filters.student_type]);
  }

  // Center filter
  if (filters.center_id) {
    filtered = filtered.filter((item: MarkazMadrasha) => item.center_id.toString() === filters.center_id);
  }

  // Mtype filter
  if (filters.mtype) {
    filtered = filtered.filter((item: MarkazMadrasha) => item.mtype === filters.mtype);
  }

  // Status filter
  if (filters.enabledisable !== '') {
    filtered = filtered.filter((item: MarkazMadrasha) => item.enabledisable === filters.enabledisable);
  }

  // School ID filter
  if (filters.school_id) {
    filtered = filtered.filter((item: MarkazMadrasha) =>
      item.madrasha_id?.toString().toLowerCase().includes(filters.school_id.toLowerCase())
    );
  }

  // Year filter
  if (filters.year) {
    filtered = filtered.filter((item: MarkazMadrasha) => item.year === filters.year);
  }

  // Date range filter
  if (filters.fromDate) {
    const fromDate = new Date(filters.fromDate);
    filtered = filtered.filter((item: MarkazMadrasha) => new Date(item.created_at) >= fromDate);
  }

  if (filters.toDate) {
    const toDate = new Date(filters.toDate);
    toDate.setHours(23, 59, 59, 999); // Include the entire day
    filtered = filtered.filter((item: MarkazMadrasha) => new Date(item.created_at) <= toDate);
  }

  // Sorting
  filtered.sort((a: MarkazMadrasha, b: MarkazMadrasha) => {
    const aVal = a[sortField.value as keyof MarkazMadrasha];
    const bVal = b[sortField.value as keyof MarkazMadrasha];
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

// const visiblePages = computed(() => { /* handled by backend pagination UI */ return []; });

const availableYears = computed<string[]>(() => {
  const years = [...new Set(sampleData.value
    .map(item => item.year)
    .filter((y): y is string => typeof y === 'string' && y.length > 0))];
  return years.sort();
});

const activeCount = computed(() => {
  return statisticsData.value.active_count;
});

const maleCount = computed(() => {
  return statisticsData.value.male_count;
});

const femaleCount = computed(() => {
  return statisticsData.value.female_count;
});

// Methods
const clearFilters = () => {
  filters.search = '';
  filters.division = '';
  filters.district = '';
  filters.thana = '';
  filters.stage = '';
  filters.student_type = '';
  filters.mtype = '';
  filters.enabledisable = '';
  filters.center_id = '';
  filters.school_id = '';
  filters.year = '';
  filters.fromDate = '';
  filters.toDate = '';
  currentPage.value = 1;
};

const fetchStatistics = async () => {
  statisticsLoading.value = true;
  try {
    const response = await fetch('/api/admin/markaz/statistics/');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    statisticsData.value = {
      total_markaz: data.total_markaz,
      male_count: data.male_count,
      female_count: data.female_count,
      active_count: data.active_count
    };
    console.log('Statistics data loaded:', statisticsData.value);
  } catch (err) {
    console.error('Error fetching statistics:', err);
  } finally {
    statisticsLoading.value = false;
  }
};

const refreshData = () => {
  fetchData();
  fetchStatistics();
};

const toggleColumnMenu = () => {
  showColumnMenu.value = !showColumnMenu.value;
};

const toggleAdvancedFilters = () => {
  showAdvancedFilters.value = !showAdvancedFilters.value;
};

const updateColumnVisibility = () => {
  // Save column settings to localStorage
  localStorage.setItem('markazTableColumns', JSON.stringify(availableColumns.value));
};

const sortBy = (field: string) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortDirection.value = 'asc';
  }
};

// PrimeVue DataTable event handlers
const onPage = (event: any) => {
  currentPage.value = event.page + 1;
  itemsPerPage.value = event.rows;
};

const onSort = (event: any) => {
  sortField.value = event.sortField;
  sortDirection.value = event.sortOrder === 1 ? 'asc' : 'desc';
};

// const prevPage = () => {}; // not used in current template
// const nextPage = () => {}; // not used in current template

const viewItem = (item: MarkazMadrasha) => {
  console.log('View item:', item);
  // Implement view functionality
};

const editItem = (item: MarkazMadrasha) => {
  console.log('Edit item:', item);
  // Implement edit functionality
};

const deleteItem = (item: MarkazMadrasha) => {
  console.log('Delete item:', item);
  // Implement delete functionality
};

const sendMessage = (item: MarkazMadrasha) => {
  console.log('Send message:', item);
  // Implement delete functionality
};

const sendEmail = (item: MarkazMadrasha) => {
  console.log('Send email:', item);
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

const activateItem = (item: MarkazMadrasha) => {
  onStatusSwitch(item, '1');
};

const deactivateItem = (item: MarkazMadrasha) => {
  onStatusSwitch(item, '0');
};

const clearCache = async () => {
  try {
    const response = await fetch('/api/admin/markaz/cache/', {
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
      await fetchStatistics();
    } else {
      console.error('Failed to clear cache');
    }
  } catch (error) {
    console.error('Error clearing cache:', error);
  }
};

const getCsrfToken = (): string => {
  const name = 'csrftoken';
  let cookieValue: string | null = null;
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
  return cookieValue ?? '';
};
</script>

<style scoped>
@media print {
  .no-print {
    display: none !important;
  }
}

.table-wrapper {
  overflow-x: auto;
}

.table-wrapper.scrollable {
  height: 500px;
  overflow-y: auto;
  overflow-x: auto;
}

.table-wrapper.scrollable thead {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: #e5e7eb;
}

.table-wrapper::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.table-wrapper table {
  width: 100%;
  border-collapse: collapse;
}
</style>
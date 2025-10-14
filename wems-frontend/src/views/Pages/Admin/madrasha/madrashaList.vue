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
              <h1 class="text-3xl font-bold text-gray-900 leading-tight">মাদরাসার তালিকা</h1>
              <p class="text-base text-gray-600">প্রতিষ্ঠানগত ডেটাবেস ব্যবস্থাপনা</p>
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
          <span class="text-lg font-medium text-blue-700">Loading madrasha data...</span>
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
          <p class="text-base text-gray-600 mb-1">মোট মাদরাসার তালিকা </p>
          <p class="text-2xl font-bold text-gray-900">{{ filteredData.length }}</p>
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
    <h2 class="text-base font-semibold text-gray-800 mb-2 sm:mb-0">সার্চ ইউযার্ড</h2>
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

  <!-- All Filter Inputs (without Madrasha Type and School ID) -->
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
          :options="[{ value: '', label: 'সকল বছর' }, ...availableYears.map(year => ({ value: year, label: year }))]"
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
          date-format="yy-mm-dd"
          placeholder="তারিখ নির্বাচন করুন"
          class="w-full"
        />
      </div>
      <div>
        <label class="block text-base font-medium text-gray-700 mb-1">তারিখ পর্যন্ত</label>
        <Calendar
          v-model="filters.toDate"
          date-format="yy-mm-dd"
          placeholder="তারিখ নির্বাচন করুন"
          class="w-full"
        />
      </div>
      <!-- Records Per Page -->
      <div>
        <label class="block text-base font-medium text-gray-700 mb-1">প্রতি পেজে সারি দেখান</label>
        <Select
          v-model="itemsPerPage"
          :options="[
            { value: 10, label: '10' },
            { value: 25, label: '25' },
            { value: 50, label: '50' },
            { value: 100, label: '100' }
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

      <!-- PrimeVue Data Table -->
  <div class="bg-white rounded-sm shadow border border-gray-300">
    <DataTable
      :value="filteredData"
      :paginator="true"
      :rows="itemsPerPage"
      :totalRecords="totalCount"
      :lazy="true"
      :first="(currentPage - 1) * itemsPerPage"
      @page="onPage($event)"
      :loading="loading"
      sortMode="single"
      :sortField="sortField"
      :sortOrder="sortDirection === 'asc' ? 1 : -1"
      @sort="onSort($event)"
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
      currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
      :rowsPerPageOptions="[10, 25, 50, 100]"
      :scrollable="true"
      scrollHeight="500px"
      class="p-datatable-sm"
      :globalFilterFields="['mname', 'village', 'mobile', 'madrasha_id']"
      :globalFilter="filters.search"
      responsiveLayout="scroll"
      showGridlines
      stripedRows
    >
      <!-- ID Column -->
      <Column
        v-if="getColumnVisibility('id')"
        field="id"
        header="আইডি"
        :sortable="true"
        style="min-width: 80px"
      >
        <template #body="{ data }">
          <span class="font-medium">{{ data.id }}</span>
        </template>
      </Column>

      <!-- Madrasha ID Column -->
      <Column
        v-if="getColumnVisibility('madrasha_id')"
        field="madrasha_id"
        header="মাদরাসার আইডি"
        :sortable="true"
        style="min-width: 120px"
      >
        <template #body="{ data }">
          <span class="font-medium">{{ data.madrasha_id }}</span>
        </template>
      </Column>

      <!-- Elhaq No Column -->
      <Column
        v-if="getColumnVisibility('elhaqno')"
        field="elhaqno"
        header="ইলহাক নম্বর"
        :sortable="true"
        style="min-width: 120px"
      >
        <template #body="{ data }">
          <span class="font-medium">{{ data.elhaqno }}</span>
        </template>
      </Column>

      <!-- Name Column -->
      <Column
        v-if="getColumnVisibility('name')"
        field="mname"
        header="নাম"
        :sortable="true"
        style="min-width: 250px"
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
        v-if="getColumnVisibility('stage')"
        field="stage_display"
        header="মারহালা স্তর"
        :sortable="true"
        style="min-width: 150px"
      >
        <template #body="{ data }">
          <span class="px-2 py-1 text-sm font-medium bg-indigo-100 text-indigo-800 rounded">
            {{ data.stage_display || data.stage }}
          </span>
        </template>
      </Column>

      <!-- Location Column -->
      <Column
        v-if="getColumnVisibility('location')"
        field="location"
        header="ঠিকানা"
        :sortable="true"
        style="min-width: 200px"
      >
        <template #body="{ data }">
          <span class="text-sm">{{ data.location || (data.division_name + ', ' + data.district_name + ', ' + data.thana_name) }}</span>
        </template>
      </Column>

      <!-- Student Type Column -->
      <Column
        v-if="getColumnVisibility('student_type')"
        field="student_type_display"
        header="মাদরাসার ধরণ"
        :sortable="true"
        style="min-width: 120px"
      >
        <template #body="{ data }">
          <span
            :class="data.student_type_display === 'ছাত্রী' ? 'bg-pink-100 text-pink-800' : 'bg-blue-100 text-blue-800'"
            class="px-2 py-1 text-sm font-medium rounded"
          >
            {{ data.student_type_display || data.student_type }}
          </span>
        </template>
      </Column>

      <!-- Mobile Column -->
      <Column
        v-if="getColumnVisibility('mobile')"
        field="mobile"
        header="মোবাইল"
        :sortable="true"
        style="min-width: 120px"
      >
        <template #body="{ data }">
          <span class="font-medium">{{ data.mobile }}</span>
        </template>
      </Column>

      <!-- Status Column -->
      <Column
        v-if="getColumnVisibility('status')"
        field="enabledisable"
        header="স্ট্যটাস"
        :sortable="true"
        style="min-width: 150px"
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
              class="px-2 py-1 text-sm font-medium rounded"
            >
              {{ data.enabledisable === '1' ? 'সক্রিয়' : 'নিষ্ক্রিয়' }}
            </span>
          </div>
        </template>
      </Column>

      <!-- Actions Column -->
      <Column
        v-if="getColumnVisibility('actions')"
        header="একশন"
        :exportable="false"
        style="min-width: 120px"
        headerStyle="text-align: center"
        bodyStyle="text-align: center"
      >
        <template #body="{ data }">
          <SplitButton
            label="বিস্তারিত"
            :model="[
              { label: 'সেটিংস', icon: 'pi pi-cog', command: () => editItem(data) },
              { label: 'মুছে ফেলুন', icon: 'pi pi-trash', command: () => deleteItem(data) },
              { label: 'বার্তা পাঠান', icon: 'pi pi-comments', command: () => sendMessage(data) },
              { label: 'পিডিএফ ডাউনলোড করুন', icon: 'pi pi-file-pdf', command: () => downloadPDF() },
              { label: 'ইমেইল করুন', icon: 'pi pi-envelope', command: () => sendEmail(data) },
              { label: 'একটিভ করুন', icon: 'pi pi-check', command: () => activateItem(data) },
              { label: 'ডিঅ্যাক্টিভ করুন', icon: 'pi pi-times-circle', command: () => deactivateItem(data) }
            ]"
            class="p-button-sm p-button-outlined"
            @click="viewItem(data)"
          />
        </template>
      </Column>

      <!-- Empty State Template -->
      <template #empty>
        <div class="text-center py-12">
          <i class="pi pi-inbox text-4xl text-gray-400"></i>
          <h3 class="mt-2 text-lg font-semibold text-gray-900">No records found</h3>
          <p class="mt-1 text-sm text-gray-500">Try adjusting your search or filter criteria</p>
        </div>
      </template>

      <!-- Loading Template -->
      <template #loading>
        <div class="text-center py-12">
          <i class="pi pi-spinner pi-spin text-4xl text-blue-500"></i>
          <h3 class="mt-2 text-lg font-semibold text-gray-900">Loading data...</h3>
        </div>
      </template>
    </DataTable>
  </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import SplitButton from 'primevue/splitbutton'
import InputSwitch from 'primevue/inputswitch'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Calendar from 'primevue/calendar'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
// import ColumnGroup from 'primevue/columngroup'
// import Row from 'primevue/row'
import 'primeicons/primeicons.css'

// TypeScript interfaces removed; use plain JS objects

// State
const totalCount = ref(0)
const loading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const itemsPerPage = ref(10)
const sampleData = ref([])
const cacheStatus = ref(null)

const availableDivisions = ref([])
const availableDistricts = ref([])
const availableThanas = ref([])
const filtersLoading = ref({
  divisions: false,
  districts: false,
  thanas: false
})

const fetchData = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/admin/madrasha/madrasha-list/?page=${currentPage.value}&page_size=${itemsPerPage.value}`)
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    const data = await response.json()
    if (Array.isArray(data.results)) {
      sampleData.value = data.results.map(row => ({
        ...row,
        enabledisable: row.status === '1' ? '1' : '0'
      }))
      totalCount.value = data.total
      cacheStatus.value = {
        cached: data.cached || false,
        cache_backend: 'unknown'
      }
    } else {
      sampleData.value = []
      totalCount.value = 0
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch data'
    sampleData.value = []
    totalCount.value = 0
  } finally {
    loading.value = false
  }
}

const onStatusSwitch = async (item, val) => {
  const prev = item.enabledisable
  item.enabledisable = val
  try {
    const res = await fetch(`/api/admin/madrasha/status/${item.id}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({ status: val === '1' ? 1 : 0 })
    })
    if (!res.ok) throw new Error(`Failed to update status: ${res.status}`)
    const data = await res.json()
    const backendStatus = data.status === '1' ? '1' : '0'
    item.enabledisable = backendStatus
    item.status = data.status
  } catch  {
    item.enabledisable = prev
    alert('স্ট্যাটাস আপডেট ব্যর্থ হয়েছে')
  }
}

const fetchDivisions = async () => {
  filtersLoading.value.divisions = true
  try {
    const response = await fetch('/api/admin/madrasha/divisions/')
    if (response.ok) {
      const data = await response.json()
      availableDivisions.value = data.results || []
    }
  } catch  {
    // ignore
  } finally {
    filtersLoading.value.divisions = false
  }
}

const fetchDistricts = async (divisionId) => {
  filtersLoading.value.districts = true
  try {
    const url = divisionId
      ? `/api/admin/madrasha/districts/?did=${divisionId}`
      : '/api/admin/madrasha/districts/'
    const response = await fetch(url)
    if (response.ok) {
      const data = await response.json()
      availableDistricts.value = data.results || []
    }
  } catch  {
    // ignore
  } finally {
    filtersLoading.value.districts = false
  }
}

const fetchThanas = async (districtId) => {
  filtersLoading.value.thanas = true
  try {
    const url = districtId
      ? `/api/admin/madrasha/thanas/?district_id=${districtId}`
      : '/api/admin/madrasha/thanas/'
    const response = await fetch(url)
    if (response.ok) {
      const data = await response.json()
      availableThanas.value = data.results || []
    }
  } catch  {
    // ignore
  } finally {
    filtersLoading.value.thanas = false
  }
}

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
})

watch(() => filters.division, async (newDivisionId) => {
  if (newDivisionId) {
    const division = availableDivisions.value.find(d => d.division === newDivisionId)
    if (division) {
      await fetchDistricts(division.did)
      await fetchThanas()
    }
  } else {
    await fetchDistricts()
    await fetchThanas()
  }
  filters.district = ''
  filters.thana = ''
})

watch(() => filters.district, async (newDistrictName) => {
  if (newDistrictName && filters.division) {
    const district = availableDistricts.value.find(d => d.district === newDistrictName)
    if (district) {
      await fetchThanas(district.desid)
    }
  } else if (!filters.division) {
    await fetchThanas()
  }
  filters.thana = ''
})

onMounted(() => {
  fetchData()
  fetchDivisions()
  fetchDistricts()
  fetchThanas()
})

watch([currentPage, itemsPerPage], () => {
  fetchData()
})

const showColumnMenu = ref(false)
const showAdvancedFilters = ref(false)

// Initialize columns with default visibility
const initializeColumns = () => {
  const savedColumns = localStorage.getItem('madrashaTableColumns')
  if (savedColumns) {
    try {
      return JSON.parse(savedColumns)
    } catch {}
  }
  return [
    { key: 'id', label: 'আইডি', visible: true, sortable: true },
    { key: 'madrasha_id', label: 'মাদরাসার আইডি', visible: true, sortable: true },
    { key: 'elhaqno', label: 'ইলহাক নম্বর', visible: true, sortable: true },
    { key: 'name', label: 'নাম', visible: true, sortable: true },
    { key: 'stage', label: 'মারহালা স্তর', visible: true, sortable: true },
    { key: 'location', label: 'ঠিকানা', visible: true, sortable: true },
    { key: 'student_type', label: 'মাদরাসার ধরণ', visible: true, sortable: true },
    { key: 'mobile', label: 'মোবাইল', visible: true, sortable: true },
    { key: 'status', label: 'স্ট্যটাস', visible: true, sortable: true },
    { key: 'actions', label: 'একশন', visible: true, sortable: false }
  ]
}
const availableColumns = ref(initializeColumns())

const sortField = ref('id')
const sortDirection = ref('asc')

// Computed properties

const filteredData = computed(() => {
  let filtered = sampleData.value
  if (filters.search) {
    const search = filters.search.toLowerCase()
    filtered = filtered.filter(item =>
      item.mname?.toLowerCase().includes(search) ||
      item.village?.toLowerCase().includes(search) ||
      item.mobile?.includes(search) ||
      item.madrasha_id?.toString().includes(search) ||
      item.district_name?.toLowerCase().includes(search) ||
      item.thana_name?.toLowerCase().includes(search)
    )
  }
  if (filters.division) {
    filtered = filtered.filter(item => item.division_name === filters.division)
  }
  if (filters.district) {
    filtered = filtered.filter(item => item.district_name === filters.district)
  }
  if (filters.thana) {
    filtered = filtered.filter(item => item.thana_name === filters.thana)
  }
  if (filters.stage) {
    filtered = filtered.filter(item => item.stage_display === filters.stage)
  }
  if (filters.student_type) {
    const studentTypeMap = { 'Male': 'ছাত্র', 'Female': 'ছাত্রী' }
    filtered = filtered.filter(item => item.student_type_display === studentTypeMap[filters.student_type])
  }
  if (filters.mtype) {
    filtered = filtered.filter(item => item.mtype === filters.mtype)
  }
  if (filters.enabledisable !== '') {
    filtered = filtered.filter(item => item.enabledisable === filters.enabledisable)
  }
  if (filters.school_id) {
    filtered = filtered.filter(item =>
      item.madrasha_id?.toString().toLowerCase().includes(filters.school_id.toLowerCase())
    )
  }
  if (filters.year) {
    filtered = filtered.filter(item => item.year === filters.year)
  }
  if (filters.fromDate) {
    const fromDate = new Date(filters.fromDate)
    filtered = filtered.filter(item => new Date(item.created_at) >= fromDate)
  }
  if (filters.toDate) {
    const toDate = new Date(filters.toDate)
    toDate.setHours(23, 59, 59, 999)
    filtered = filtered.filter(item => new Date(item.created_at) <= toDate)
  }
  filtered.sort((a, b) => {
    const aVal = a[sortField.value]
    const bVal = b[sortField.value]
    if (aVal == null && bVal == null) return 0
    if (aVal == null) return 1
    if (bVal == null) return -1
    if (sortDirection.value === 'asc') {
      return aVal > bVal ? 1 : -1
    } else {
      return aVal < bVal ? 1 : -1
    }
  })
  return filtered
})


const totalPages = computed(() => Math.ceil(totalCount.value / itemsPerPage.value))

const availableYears = computed(() => {
  const years = [...new Set(sampleData.value
    .map(item => item.year)
    .filter(y => typeof y === 'string' && y.length > 0))]
  return years.sort()
})

const activeCount = computed(() => filteredData.value.filter(item => item.enabledisable === '1').length)
const maleCount = computed(() => filteredData.value.filter(item => item.student_type_display === 'ছাত্র').length)
const femaleCount = computed(() => filteredData.value.filter(item => item.student_type_display === 'ছাত্রী').length)

// Methods
const clearFilters = () => {
  filters.search = ''
  filters.division = ''
  filters.district = ''
  filters.thana = ''
  filters.stage = ''
  filters.student_type = ''
  filters.mtype = ''
  filters.enabledisable = ''
  filters.school_id = ''
  filters.year = ''
  filters.fromDate = ''
  filters.toDate = ''
  currentPage.value = 1
}

const refreshData = () => {
  fetchData()
}

const toggleColumnMenu = () => {
  showColumnMenu.value = !showColumnMenu.value
}

const toggleAdvancedFilters = () => {
  showAdvancedFilters.value = !showAdvancedFilters.value
}

const updateColumnVisibility = () => {
  localStorage.setItem('madrashaTableColumns', JSON.stringify(availableColumns.value))
}


const onPage = event => {
  currentPage.value = Math.floor(event.first / event.rows) + 1
  itemsPerPage.value = event.rows
  fetchData()
}

const onSort = event => {
  sortField.value = event.sortField
  sortDirection.value = event.sortOrder === 1 ? 'asc' : 'desc'
}

const getColumnVisibility = columnKey => {
  const column = availableColumns.value.find(col => col.key === columnKey)
  return column ? column.visible : false
}

const viewItem = () => {
  // view functionality
}
const editItem = () => {
  // edit functionality
}
const deleteItem = () => {
  // delete functionality
}
const sendMessage = () => {
  // send message functionality
}
const sendEmail = () => {
  // send email functionality
}
const downloadExcel = () => {
  // Excel download
}
const downloadCSV = () => {
  // CSV download
}
const downloadPDF = () => {
  // PDF download
}
const printData = () => {
  window.print()
}
const activateItem = item => {
  onStatusSwitch(item, '1')
}
const deactivateItem = item => {
  onStatusSwitch(item, '0')
}
const clearCache = async () => {
  try {
    const response = await fetch('/api/admin/madrasha/cache/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      }
    })
    if (response.ok) {
      await response.json()
      await fetchData()
    }
  } catch  {}
}

const getCsrfToken = () => {
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue ?? ''
}
</script>

<style scoped>
@media print {
  .no-print {
    display: none !important;
  }
}
</style>

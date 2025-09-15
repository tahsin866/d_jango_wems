<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;" class="min-h-screen bg-gray-50">
    <!-- Top Stats Cards -->
    <div class="bg-white border-b border-gray-200 px-6 py-8">
      <div class=" mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Total Exams Card -->
          <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-lg font-medium text-gray-600 mb-1">মোট পরীক্ষা</p>
                <p class="text-3xl font-bold text-gray-900">৫</p>
                <p class="text-xs text-gray-500 mt-2 flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  সর্বশেষ আপডেট ২০২৫-০৭-১৭ ২৩:৩৭:৫৮
                </p>
              </div>
              <div class="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
            </div>
          </div>

          <!-- Scheduled Exams Card -->
          <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-lg font-medium text-gray-600 mb-1">চলমনা পরীক্ষা</p>
                <p class="text-3xl font-bold text-gray-900">৩</p>
                <p class="text-xs text-gray-500 mt-2 flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  ২০২৫ সালের বার্ষিক পরীক্ষা
                </p>
              </div>
              <div class="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
            </div>
          </div>

          <!-- Pending Exams Card -->
          <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-lg font-medium text-gray-600 mb-1">অসমাপ্ত পরীক্ষা</p>
                <p class="text-3xl font-bold text-gray-900">৩</p>
                <p class="text-xs text-gray-500 mt-2 flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  সর্বশেষ হালনাগাদ বিলম্ব
                </p>
              </div>
              <div class="h-12 w-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
          </div>

          <!-- Quick Action Card -->
          <div class="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 shadow-lg text-white">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-blue-100 text-lg font-medium mb-2">দ্রুত কাজের বার্তা</p>
                <h3 class="text-lg font-semibold mb-4">নতুন পরীক্ষা যোগ করুন</h3>
                <RouterLink
                to="/central/exam/Create"
                class="bg-white text-blue-600 px-4 py-2 rounded-lg text-lg font-medium hover:bg-blue-50 transition-colors duration-200 flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                  নতুন পরীক্ষা যোগ করুন
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters Section -->
    <div class="bg-white px-6 py-6">
      <div class=" mx-auto">
        <div class="flex items-center mb-6">
          <svg class="w-5 h-5 text-white mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.414A1 1 0 013 6.707V4z"></path>
          </svg>
          <h2 class="text-white text-lg font-semibold">অনুসন্ধান ফিল্টার</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Search Input -->
          <div class="relative">
            <label class="block text-white text-xl font-medium mb-2">অনুসন্ধান</label>
            <div class="relative">
              <input
                type="text"
                v-model="searchQuery"
                @keyup.enter="fetchExamSetups"
                placeholder="পরীক্ষার নাম দিয়ে অনুসন্ধান করুন..."
                class="w-full px-4 py-3 pl-10 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
              />
              <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
          </div>

          <!-- Class Filter -->
          <div>
            <label class="block text-white text-lg font-medium mb-2">
              <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
              কেন্দ্রীয় পরীক্ষার তালিকা
            </label>
            <select
              v-model="selectedClass"
              class="w-full px-4 py-3 bg-white text-xl border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
            >
              <option value="">সকল পরীক্ষা</option>
              <option v-for="exam in availableExamNames" :key="exam" :value="exam">
                {{ exam }}
              </option>
            </select>
          </div>

          <!-- Year Filter -->
          <div>
            <label class="block text-white text-lg font-medium mb-2">
              <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              ইয়ার
            </label>
            <select
              v-model="selectedYear"
              class="w-full px-4 py-3 text-xl bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
            >
              <option value="">সকল বছর</option>
              <option v-for="year in availableYears" :key="year" :value="year">
                {{ year }}
              </option>
            </select>
          </div>

          <!-- Status Filter -->
          <div>
            <label class="block text-white text-lg font-medium mb-2">
              <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
              </svg>
              ইংরেজি বর্ষ
            </label>
            <select
              v-model="selectedStatus"
              class="w-full text-xl px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
            >
              <option value="">সকল অবস্থা</option>
              <option value="active">সক্রিয়</option>
              <option value="pending">অপেক্ষমান</option>
              <option value="completed">সম্পন্ন</option>
            </select>
          </div>
        </div>

        <!-- Advanced Search and Clear Buttons -->
        <div class="mt-6 flex justify-end space-x-4">
          <button
            @click="clearFilters"
            class="bg-red-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-red-700 transition-colors duration-200 flex items-center"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            ফিল্টার মুছুন
          </button>
          <button
            @click="fetchExamSetups"
            class="bg-white text-blue-600 px-6 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors duration-200 flex items-center"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            উন্নত অনুসন্ধান করুন
          </button>
        </div>
      </div>
    </div>

    <!-- Table Section -->
    <div class=" mx-auto px-6 py-8">
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <!-- Filter Results Info -->
        <div class="bg-blue-50 px-6 py-3 border-b border-blue-200" v-if="searchQuery || selectedYear || selectedStatus || selectedClass">
          <div class="flex items-center justify-between">
            <div class="flex items-center text-blue-700">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.414A1 1 0 013 6.707V4z"></path>
              </svg>
              <span class="font-medium">ফিল্টার প্রয়োগ করা হয়েছে:</span>
              <span class="ml-2">{{ filteredExams.length }} টি ফলাফল পাওয়া গেছে</span>
            </div>
            <div class="flex items-center space-x-2 text-sm">
              <span v-if="searchQuery" class="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                খোঁজ: "{{ searchQuery }}"
              </span>
              <span v-if="selectedClass" class="bg-red-100 text-red-800 px-2 py-1 rounded">
                পরীক্ষা: {{ selectedClass }}
              </span>
              <span v-if="selectedYear" class="bg-green-100 text-green-800 px-2 py-1 rounded">
                বছর: {{ selectedYear }}
              </span>
              <span v-if="selectedStatus" class="bg-purple-100 text-purple-800 px-2 py-1 rounded">
                স্ট্যাটাস: {{ selectedStatus }}
              </span>
            </div>
          </div>
        </div>

        <!-- Table Header -->
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <svg class="w-5 h-5 text-gray-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              <h3 class="text-lg font-semibold text-gray-900">
                পরীক্ষার তালিকা ({{ filteredExams.length }} টি রেকর্ড)
              </h3>
            </div>
            <div class="text-lg text-gray-500">
              tahsin866 | {{ new Date().toLocaleString('bn-BD') }}
            </div>
          </div>
        </div>

        <!-- Table Content -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
 কেন্দ্রীয় পরীক্ষার তালিকা
                </th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                  ক্রম
                </th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                  ইংরেজি বর্ষ
                </th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                  হিজরি বর্ষ
                </th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                  তারিখ/সময়
                </th>

                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                সংশোধন
                </th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                নিবন্ধন সেটাপ
                </th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                 অন্তর্ভুক্তি সেটাপ
                </th>
                   <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                 অন্যান্য সেটাপ
                </th>
                <th class="px-6 py-4 text-left text-lg font-semibold text-gray-900 border-b border-gray-200">
                  একশন
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <!-- Loading State -->
              <tr v-if="isLoading">
                <td colspan="8" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <svg class="animate-spin w-8 h-8 text-blue-600 mb-4" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <p class="text-gray-600 text-lg">ডেটা লোড হচ্ছে...</p>
                  </div>
                </td>
              </tr>

              <!-- Data Rows -->
              <tr v-for="exam in paginatedExams" :key="exam.id" class="hover:bg-gray-50 transition-colors duration-150" v-else-if="!isLoading">
                <td class="px-6 py-4 text-lg text-gray-900">
                  {{ formatExamName(exam) }}
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-lg font-medium bg-blue-100 text-blue-800">
                    {{ exam.id }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-lg font-medium bg-blue-100 text-blue-800">
                    {{ exam.english_year }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-lg font-medium bg-yellow-100 text-yellow-800">
                    {{ exam.arabic_year }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-lg font-medium bg-green-100 text-green-800">
                    {{ new Date(exam.created_at).toLocaleDateString('bn-BD') }}
                  </span>
                </td>

                <td class="px-6 py-4">
              <RouterLink :to="`/central/exam/edit/${exam.id}`" class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-orange-100 text-orange-800 hover:bg-orange-200" title="সংশোধন">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
              </RouterLink>
                </td>
                <td class="px-6 py-4">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', command: () => onRegisterCreate(exam) },
                      { label: 'সংশোধন', command: () => onRegisterEdit(exam) }
                    ]"
                    label="নিবন্ধন সেটাপ"
                    class="p-button-primary"
                  />
                </td>
                <td class="px-6 py-4">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', command: () => onInclusionCreate(exam) },
                      { label: 'সংশোধন', command: () => onInclusionEdit(exam) }
                    ]"
                    label="অন্তর্ভুক্তি সেটাপ"
                    class="p-button-secondary"
                  />
                </td>
                <td class="px-6 py-4">
                  <SplitButton
                    :model="[
                      { label: 'নিবন্ধন তৈরি', command: () => onOtherCreate(exam) },
                      { label: 'সংশোধন', command: () => onOtherEdit(exam) }
                    ]"
                    label="অন্যান্য সেটাপ"
                    class="p-button-success"
                  />
                </td>
                <td class="px-6 py-4 text-center">
  <button @click="deleteExam(exam.id)" class="text-red-600 hover:text-red-800" title="ডিলিট">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
    </svg>
  </button>
</td>
              </tr>

              <!-- Empty State -->
              <tr v-if="!isLoading && paginatedExams.length === 0">
                <td colspan="8" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">
                      {{ searchQuery || selectedYear || selectedStatus || selectedClass ? 'কোনো ফলাফল পাওয়া যায়নি' : 'কোনো পরীক্ষা সেটআপ নেই' }}
                    </h3>
                    <p class="text-gray-500 mb-4">
                      {{ searchQuery || selectedYear || selectedStatus || selectedClass ? 'আপনার ফিল্টার পরিবর্তন করে আবার চেষ্টা করুন' : 'নতুন পরীক্ষা সেটআপ তৈরি করুন' }}
                    </p>
                    <button
                      v-if="searchQuery || selectedYear || selectedStatus || selectedClass"
                      @click="clearFilters"
                      class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                    >
                      সব ফিল্টার মুছুন
                    </button>
                    <RouterLink
                      v-else
                      to="/central/exam/create"
                      class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                    >
                      নতুন পরীক্ষা তৈরি করুন
                    </RouterLink>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="bg-gray-50 px-6 py-4 border-t border-gray-200" v-if="!isLoading && filteredExams.length > 0">
          <div class="flex items-center justify-between">
            <div class="text-lg text-gray-700">
              পেজ {{ totalPages }} টি এর মধ্যে {{ Math.min((currentPage - 1) * 10 + 1, filteredExams.length) }} - {{ Math.min(currentPage * 10, filteredExams.length) }} দেখানো হচ্ছে (মোট {{ filteredExams.length }} টি)
            </div>
            <div class="flex items-center space-x-2">
              <button
                :disabled="currentPage === 1"
                @click="previousPage"
                :class="[
                  'px-3 py-1 rounded-md text-lg font-medium transition-colors duration-200',
                  currentPage === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                ]"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
              </button>

              <button
                v-for="page in totalPages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'px-3 py-1 rounded-md text-lg font-medium transition-colors duration-200',
                  currentPage === page
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                ]"
              >
                {{ page }}
              </button>

              <button
                :disabled="currentPage === totalPages"
                @click="nextPage"
                :class="[
                  'px-3 py-1 rounded-md text-lg font-medium transition-colors duration-200',
                  currentPage === totalPages
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                ]"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import SplitButton from 'primevue/splitbutton'

// Types
interface ExamSetup {
  id: number
  exam_name: string
  arabic_year: string
  bangla_year: string
  english_year: string
  created_at: string
  updated_at: string
}

// Router
const router = useRouter()

// SplitButton Actions
const onRegisterCreate = (exam: ExamSetup) => {
  router.push(`/central/exam/${exam.id}/register/create`)
}
const onRegisterEdit = (exam: ExamSetup) => {
  router.push(`/central/exam/${exam.id}/register/edit`)
}
const onInclusionCreate = (exam: ExamSetup) => {
  router.push(`/central/exam/${exam.id}/inclusion/create`)
}
const onInclusionEdit = (exam: ExamSetup) => {
  router.push(`/central/exam/${exam.id}/inclusion/edit`)
}
const onOtherCreate = (exam: ExamSetup) => {
  router.push(`/central/exam/${exam.id}/other/create`)
}
const onOtherEdit = (exam: ExamSetup) => {
  router.push(`/central/exam/${exam.id}/other/edit`)
}

// State
const searchQuery = ref<string>('')
const selectedClass = ref<string>('')
const selectedYear = ref<string>('')
const selectedStatus = ref<string>('')
const currentPage = ref<number>(1)
const isLoading = ref<boolean>(false)
const examList = ref<ExamSetup[]>([])

// Store all exam data for filter options
const allExamData = ref<ExamSetup[]>([])

// Fetch all exams for filter dropdown options
const fetchAllExamsForFilters = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/central-exam/exam-setups/list/')
    allExamData.value = response.data
  } catch (error) {
    console.error('Error fetching all exams for filters:', error)
  }
}

// Computed: unique years for dropdown
const availableYears = computed(() => {
  const years = new Set<string>()
  allExamData.value.forEach(exam => {
    years.add(exam.english_year)
    years.add(exam.arabic_year)
    years.add(exam.bangla_year)
  })
  return Array.from(years).sort()
})

// Computed: unique exam names for dropdown
const availableExamNames = computed(() => {
  const examNames = new Set<string>()
  allExamData.value.forEach(exam => {
    examNames.add(exam.exam_name)
  })
  return Array.from(examNames).sort()
})

// Fetch exams with filters
const fetchExamSetups = async () => {
  try {
    isLoading.value = true
    const params = new URLSearchParams()
    if (searchQuery.value.trim()) params.append('search', searchQuery.value.trim())
    if (selectedYear.value) params.append('year', selectedYear.value)
    if (selectedClass.value) params.append('exam_name', selectedClass.value)
    const url = `http://127.0.0.1:8000/api/central-exam/exam-setups/list/${params.toString() ? '?' + params.toString() : ''}`
    const response = await axios.get(url)
    examList.value = response.data
  } catch (error) {
    console.error('Error fetching exam setups:', error)
  } finally {
    isLoading.value = false
  }
}

// Computed: filtered exams (backend filtering)
const filteredExams = computed(() => examList.value)

// Pagination
const paginatedExams = computed(() => {
  const startIndex = (currentPage.value - 1) * 10
  const endIndex = startIndex + 10
  return filteredExams.value.slice(startIndex, endIndex)
})
const totalPages = computed(() => Math.ceil(filteredExams.value.length / 10))

const resetPagination = () => {
  currentPage.value = 1
}
const previousPage = (): void => {
  if (currentPage.value > 1) currentPage.value--
}
const nextPage = (): void => {
  if (currentPage.value < totalPages.value) currentPage.value++
}
const goToPage = (page: number): void => {
  currentPage.value = page
}

// Clear all filters
const clearFilters = () => {
  searchQuery.value = ''
  selectedClass.value = ''
  selectedYear.value = ''
  selectedStatus.value = ''
  currentPage.value = 1
  fetchExamSetups()
}

// Format: exam_name/arabic_year/english_year
const formatExamName = (exam: ExamSetup) => {
  return `${exam.exam_name}/${exam.arabic_year}/${exam.english_year}`
}

// Debounced search for searchQuery
let searchTimeout: ReturnType<typeof setTimeout> | null = null
const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchExamSetups()
  }, 500)
}

// Watchers
watch([searchQuery], () => {
  resetPagination()
  debouncedSearch()
})
watch([selectedYear, selectedStatus, selectedClass], () => {
  resetPagination()
  fetchExamSetups()
})

// Lifecycle
onMounted(() => {
  fetchExamSetups()
  fetchAllExamsForFilters()
  console.log('Exam Management Dashboard loaded')
})

// Delete exam
const deleteExam = async (id: number) => {
  if (confirm('আপনি কি নিশ্চিতভাবে ডিলিট করতে চান?')) {
    try {
      await axios.delete(`/api/central-exam/exam-setups/${id}/delete/`)
      examList.value = examList.value.filter(exam => exam.id !== id)
    } catch (_error) {
      alert('ডিলিট করা যায়নি!')
    }
  }
}
</script>

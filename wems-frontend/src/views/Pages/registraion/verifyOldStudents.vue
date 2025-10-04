<template>
    <div style="font-family: 'SolaimanLipi', sans-serif;" class="bg-gray-50 py-8">
      <div class="mx-auto px-4 sm:px-6 lg:px-8 ">
        <!-- Header -->
        <div
          class="bg-white rounded-sm shadow mb-6"
          :class="fadeIn ? 'opacity-100' : 'opacity-0'"
        >
          <div class="p-6 md:p-8 flex flex-col md:flex-row justify-between items-center">
            <div class="flex items-center mb-4 md:mb-0">
              <div class="p-3 bg-gray-100 rounded-sm mr-4">
                <svg class="w-10 h-10 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l9-5-9-5-9 5 9 5z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                </svg>
              </div>
              <div>
                <h1 class="text-2xl md:text-3xl font-bold text-gray-900">
                  মারহালার নাম:
                  <span v-if="marhalaName">{{ marhalaName }}</span>
                  <span v-else class="text-red-500">মারহালা নাম পাওয়া যায়নি</span>
                </h1>
                <p class="text-gray-600 text-lg md:text-base">পুরাতন শিক্ষার্থী নিবন্ধন সিস্টেম</p>
                <p class="text-gray-500 text-lg mt-1">{{ getCurrentDate() }} • {{ currentUser }}</p>
              </div>
            </div>

            <div class="flex flex-wrap gap-3">
              <!-- router-link for New Student -->
              <router-link
                to="/student/old/registration/form"
                class="inline-flex items-center px-4 py-3 bg-gray-700 hover:bg-gray-800 rounded text-md font-medium text-white"
              >
                <!-- icon -->
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z" />
                </svg>
                নতুন ছাত্র নিবন্ধন
              </router-link>

              <!-- router-link for Registration List -->
              <router-link
                :to="listUrl"
                class="inline-flex items-center px-4 py-3 bg-gray-100 hover:bg-gray-200 rounded text-md font-medium text-gray-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
                </svg>
                নিবন্ধন তালিকা
              </router-link>
            </div>
          </div>
        </div>

        <!-- Error Message Alert -->
        <div v-if="showError" class="mb-6 bg-red-50 border-l-4 border-red-400 p-4 rounded">
          <div class="mt-1 text-lg text-red-700">{{ errorMessage }}</div>
        </div>

        <!-- Search Card -->
        <div class="bg-white rounded-sm shadow mb-6 overflow-visible" :class="fadeIn ? 'opacity-100' : 'opacity-0'">
          <div class="px-6 py-4 border-b border-gray-200">
            <div class="flex items-center">
              <svg class="h-6 w-6 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <h3 class="ml-2 text-lg font-medium text-gray-900">শিক্ষার্থী অনুসন্ধান</h3>
            </div>
          </div>

          <div class="p-6">
            <div class="grid grid-cols-1 gap-6 md:grid-cols-4">
              <!-- MARHALA -->
              <div>
                <label class="block text-lg font-medium text-gray-700 mb-1">মারহালা</label>
                <div class="relative z-10">
                  <select
                    v-model="selectedMarhala"
                    class="block w-full rounded p-2.5 pl-3 pr-10 border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-500 focus:border-gray-500 appearance-none"
                    aria-label="মারহালা নির্বাচন করুন"
                  >
                    <option value="">মারহালা নির্বাচন করুন</option>
                    <option v-for="m in availableMarhalas" :key="m.id" :value="m.id">{{ m.name }}</option>
                  </select>
                  <svg class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" viewBox="0 0 20 20" fill="none">
                    <path d="M6 8l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>

              <!-- YEAR -->
              <div>
                <label class="block text-lg font-medium text-gray-700 mb-1">পাশের সন</label>
                <div class="relative z-10">
                  <select
                    v-model="selectedYear"
                    class="block w-full rounded p-2.5 pl-3 pr-10 border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-500 focus:border-gray-500 appearance-none"
                    aria-label="পাশের সন নির্বাচন করুন"
                  >
                    <option value="">পাশের সন নির্বাচন করুন</option>
                    <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                  </select>
                  <svg class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" viewBox="0 0 20 20" fill="none">
                    <path d="M6 8l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>

              <!-- ROLL -->
              <div>
                <label class="block text-lg font-medium text-gray-700 mb-1">রোল নম্বর</label>
                <input
                  v-model="rollNumber"
                  type="text"
                  class="block w-full rounded p-2.5 border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-500 focus:border-gray-500"
                  placeholder="রোল নম্বর লিখুন"
                  aria-label="রোল নম্বর লিখুন"
                />
              </div>

              <!-- REGISTRATION -->
              <div>
                <label class="block text-lg font-medium text-gray-700 mb-1">রেজিস্ট্রেশন নম্বর</label>
                <input
                  v-model="registrationNumber"
                  type="text"
                  class="block w-full rounded p-2.5 border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-500 focus:border-gray-500"
                  placeholder="রেজিস্ট্রেশন নম্বর লিখুন"
                  aria-label="রেজিস্ট্রেশন নম্বর লিখুন"
                />
              </div>
            </div>

            <div class="flex justify-center md:justify-end gap-3 mt-6">
              <button
                @click="resetSearch"
                type="button"
                class="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-md font-medium text-gray-700"
              >
                সব রিসেট
              </button>

              <button
                @click="searchStudents"
                :disabled="loading"
                type="button"
                class="inline-flex items-center px-6 py-3 bg-gray-700 hover:bg-gray-800 rounded text-lg font-medium text-white disabled:opacity-60 disabled:cursor-not-allowed"
              >
                <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                </svg>
                {{ loading ? 'অনুসন্ধান...' : 'অনুসন্ধান করুন' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Student Detail Section (shown when studentBasic is available) -->
        <div v-if="studentBasic" class="transition-opacity" :class="isSearching ? 'opacity-0' : 'opacity-100'">
          <div class="bg-white rounded-sm shadow border border-gray-200 overflow-hidden">
            <!-- Student Header -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-4 flex justify-between items-center">
              <div class="flex items-center">
                <div class="bg-white bg-opacity-20 p-2 rounded-full">
                  <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <h4 class="ml-3 text-xl font-bold text-white truncate">{{ studentBasic.student_name_bn }}</h4>
              </div>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-700 bg-opacity-20 text-white">
                রোল: {{ studentBasic.roll_no }}
              </span>
            </div>

            <!-- Student Info Cards -->
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <!-- Basic Info Card -->
                <div class="bg-blue-50 rounded-sm p-5 border border-blue-100 shadow-sm">
                  <h5 class="text-lg font-semibold text-blue-800 uppercase tracking-wider mb-4 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                    </svg>
                    শিক্ষার্থীর মৌলিক তথ্য
                  </h5>
                  <div class="space-y-3">
                    <div class="flex justify-between pb-2 border-b border-blue-100">
                      <span class="font-medium text-blue-700">পিতা:</span>
                      <span class="text-gray-800">{{ studentBasic.father_name_bn }}</span>
                    </div>
                    <div class="flex justify-between pb-2 border-b border-blue-100">
                      <span class="font-medium text-blue-700">মাতা:</span>
                      <span class="text-gray-800">{{ studentBasic.mother_name_bn || 'N/A' }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="font-medium text-blue-700">জন্ম-তারিখ:</span>
                      <span class="text-gray-800">{{ studentBasic.date_of_birth || 'N/A' }}</span>
                    </div>
                  </div>
                </div>

                <!-- Academic Info Card -->
                <div class="bg-green-50 rounded-sm p-5 border border-green-100 shadow-sm">
                  <h5 class="text-lg font-semibold text-green-800 uppercase tracking-wider mb-4 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-green-600" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
                    </svg>
                    একাডেমিক তথ্য
                  </h5>
                  <div class="space-y-3">
                    <div class="flex justify-between pb-2 border-b border-green-100">
                      <span class="font-medium text-green-700">রোল:</span>
                      <span class="text-gray-800">{{ studentBasic.roll_no }}</span>
                    </div>
                    <div class="flex justify-between pb-2 border-b border-green-100">
                      <span class="font-medium text-green-700">রেজিঃ নং:</span>
                      <span class="text-gray-800">{{ studentBasic.reg_no }}</span>
                    </div>
                    <div class="flex justify-between pb-2 border-b border-green-100">
                      <span class="font-medium text-green-700">বছর:</span>
                      <span class="text-gray-800">{{ studentBasic.year }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="font-medium text-green-700">মারহালা:</span>
                      <span class="text-gray-800">{{ studentBasic.marhala_id }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Results Section -->
              <div class="bg-gray-50 rounded-sm p-5 border border-gray-200 shadow-sm">
                <h5 class="text-lg font-semibold text-gray-800 uppercase tracking-wider mb-4 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  রেজাল্ট তথ্য
                </h5>

                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-100">
                      <tr>
                        <th scope="col" class="px-4 py-3 text-left text-lg font-semibold text-gray-700 uppercase tracking-wider">বিষয়</th>
                        <th scope="col" class="px-4 py-3 text-left text-lg font-semibold text-gray-700 uppercase tracking-wider">প্রাপ্ত নম্বর</th>
                        <th scope="col" class="px-4 py-3 text-left text-lg font-semibold text-gray-700 uppercase tracking-wider">ডিভিশন</th>
                        <th scope="col" class="px-4 py-3 text-left text-lg font-semibold text-gray-700 uppercase tracking-wider">পরীক্ষার্থীর ধরণ</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="(result, idx) in studentResults" :key="idx" class="hover:bg-gray-50 transition-colors">
                        <td class="px-4 py-3 text-lg font-medium text-gray-900">{{ result.label }}</td>
                        <td class="px-4 py-3 text-lg">
                          <span :class="result.value > 0 ? 'text-green-600 font-bold' : 'text-red-500 font-bold'" class="text-lg">
                            {{ result.value }}
                          </span>
                        </td>
                        <td class="px-4 py-3">
                          <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border" :class="getDivisionBadge(result.division)">
                            {{ result.division }}
                          </span>
                        </td>
                        <td class="px-4 py-3">
                          <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border" :class="getResultTypeBadge(result.result_type)">
                            {{ result.result_type }}
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!-- Show irregular subjects if present -->
                <div v-if="studentResultsData.irregular_subjects && studentResultsData.irregular_subjects.length" class="mt-4">
                  <div class="bg-red-50 border-l-4 border-red-400 p-4 rounded">
                    <h6 class="text-lg font-semibold text-red-700 mb-2">অনিয়মিত/ফেল/অনুপস্থিত বিষয়সমূহ:</h6>
                    <ul class="list-disc ml-6">
                      <li v-for="(subj, i) in studentResultsData.irregular_subjects" :key="i" class="text-red-700 text-md font-bold">{{ subj }}</li>
                    </ul>
                  </div>
                </div>

                <!-- Institution Info -->
                <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div class="bg-white rounded-sm p-4 border border-gray-200 shadow-sm">
                    <h6 class="text-sm font-medium text-gray-700 mb-2 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                      </svg>
                      মাদরাসা
                    </h6>
                    <p class="text-sm text-gray-900">{{ studentResultsData.madrasha || 'N/A' }}</p>
                  </div>
                  <div class="bg-white rounded-sm p-4 border border-gray-200 shadow-sm">
                    <h6 class="text-sm font-medium text-gray-700 mb-2 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                      </svg>
                      মারকায
                    </h6>
                    <p class="text-sm text-gray-900">{{ studentResultsData.markaj || 'N/A' }}</p>
                  </div>
                  <div class="bg-white rounded-sm p-4 border border-gray-200 shadow-sm">
                    <h6 class="text-sm font-medium text-gray-700 mb-2 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
                    </svg>
                      ক্লাস
                    </h6>
                    <p class="text-sm text-gray-900">{{ studentResultsData.class_name || 'N/A' }}</p>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="mt-6 flex justify-end gap-3">
                <button class="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-md font-medium text-gray-700">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                  প্রিন্ট করুন
                </button>
                <router-link
                  :to="{ path: '/student/old/registration/form' }"
                  @click="prefillAndGo(studentBasic)"
                  class="inline-flex items-center px-4 py-2.5 bg-gray-700 hover:bg-gray-800 text-white rounded text-md font-medium"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-white" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                  পরীক্ষার ফরম পূরণ করুন
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading / Empty Search Results -->
        <div v-else-if="loading" class="bg-white rounded-sm shadow p-8 text-center mt-6">
          <svg class="animate-spin h-12 w-12 text-gray-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="mt-4 text-lg font-medium text-gray-700">ডাটা লোড হচ্ছে...</p>
          <p class="mt-2 text-lg text-gray-500">অনুগ্রহ করে অপেক্ষা করুন</p>
        </div>

        <div v-else-if="searchPerformed && hasSearchCriteria && !studentBasic" class="bg-white rounded-sm shadow p-8 text-center mt-6">
          <div class="mx-auto h-24 w-24 flex items-center justify-center rounded-full bg-gray-100 mb-4">
            <svg class="h-16 w-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">কোন ডাটা পাওয়া যায়নি</h3>
          <p class="mt-2 text-lg text-gray-500">আপনার অনুসন্ধান অনুযায়ী কোন ফলাফল পাওয়া যায়নি।</p>
          <button @click="resetSearch" class="mt-4 inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded">
            ফিল্টার রিসেট করুন
          </button>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

// Type definitions
interface Student {
  id: number;
  Name: string;
  Father?: string;
  Mother?: string;
  DateofBirth?: string;
  Class?: string;
  Roll?: string;
  reg_id?: string;
  Division?: string;
  Madrasha?: string;
  Markaj?: string;
  student_type?: string;
  year?: string;
  marhalaId?: string;
  CID?: string;
}

interface StudentBasic {
  id: number;
  student_name_bn: string;
  father_name_bn: string;
  mother_name_bn?: string;
  date_of_birth?: string;
  roll_no: string;
  reg_no: string;
  year: string;
  marhala_id: string;
}

interface StudentResult {
  label: string;
  value: number;
  division: string;
  result_type: string;
}

interface StudentResultsData {
  madrasha?: string;
  markaj?: string;
  class_name?: string;
  irregular_subjects?: string[];
}

interface MarhalaOption {
  id: string;
  name: string;
}

interface ApiResponse {
  session_key?: string; // 🚀 Added for Redis cache system
  student_basic?: StudentBasic;
  student_results?: {
    subjects?: StudentResult[];
    madrasha?: string;
    markaj?: string;
    class_name?: string;
    irregular_subjects?: string[];
  };
  error?: string;
}

const marhalaName = ref<string>('মারহালা নাম');

const route = useRoute();

onMounted(async () => {
  // Get marhalaId from route param
  const marhalaId = Array.isArray(route.params.marhala_id) ? route.params.marhala_id[0] : route.params.marhala_id || '2';
  currentMarhalaId.value = marhalaId;

  // Get marhala name from API
  try {
    const res = await axios.get(`/api/marhalas/${marhalaId}/`);
    marhalaName.value = res.data.name_bn || 'মারহালা';
  } catch {
    marhalaName.value = 'মারহালা';
  }

  // Fetch years from backend API
  try {
    const yearsRes = await axios.get('/api/admin/registration/oldstudent/years/');
    years.value = yearsRes.data;
  } catch {
    years.value = [];
  }

  fadeIn.value = true;
});
const years = ref<string[]>([]);
const loading = ref<boolean>(false);
const currentMarhalaId = ref<string>('2');
const showError = ref<boolean>(false);
const errorMessage = ref<string>('');
const searchPerformed = ref<boolean>(false);
const isSearching = ref<boolean>(false);
const fadeIn = ref<boolean>(false);

// Search filters
const selectedMarhala = ref<string>('');
const selectedYear = ref<string>('');
const rollNumber = ref<string>('');
const registrationNumber = ref<string>('');

// Student data refs with proper types
const student = ref<Student | null>(null);
const studentBasic = ref<StudentBasic | null>(null);
const studentResults = ref<StudentResult[]>([]);
const studentResultsData = ref<StudentResultsData>({});

// current user (fake)
const currentUser: string = 'tahsin866';

/* --- Computed / Derived --- */
const availableMarhalas = computed<MarhalaOption[]>(() => {
  const allMarhalas = [
    { id: '2', name: 'ফযীলত' },
    { id: '3', name: 'সানাবিয়া উলইয়া' },
    { id: '4', name: 'সানাবিয়া' },
    { id: '5', name: 'মুতাওয়াসসিতাহ' },
    { id: '6', name: 'ইবতিদাইয়্যাহ' },
    { id: '7', name: 'হিফযুল কুরআন' },
    { id: '8', name: 'ইলমুত তাজবীদ ওয়াল ক্বিরাআত' }
  ];

  // Keep same filtering logic as original (demo)
  if (currentMarhalaId.value === '9') return allMarhalas.filter((m) => ['2', '3'].includes(m.id));
  if (currentMarhalaId.value === '10') return allMarhalas.filter((m) => ['4', '3'].includes(m.id));
  if (currentMarhalaId.value === '11') return allMarhalas.filter((m) => ['5', '4'].includes(m.id));
  if (currentMarhalaId.value === '12') return allMarhalas.filter((m) => ['6', '5'].includes(m.id));
  if (currentMarhalaId.value === '14') return allMarhalas.filter((m) => ['6', '7'].includes(m.id));
  return allMarhalas;
});

const hasSearchCriteria = computed(() => {
  return !!(selectedMarhala.value || selectedYear.value || rollNumber.value || registrationNumber.value);
});

/* --- Functions for UI behavior --- */
const showErrorMessage = (message: string): void => {
  errorMessage.value = message;
  showError.value = true;
  setTimeout(() => {
    showError.value = false;
  }, 5000);
};

const searchStudents = async (): Promise<void> => {
  loading.value = true;
  isSearching.value = true;
  searchPerformed.value = true;
  showError.value = false;
  student.value = null;
  studentBasic.value = null;
  studentResults.value = [];
  studentResultsData.value = {};

  try {
    const params = {
      marhala: selectedMarhala.value, // এখানে cid যাবে
      year: selectedYear.value,
      roll: rollNumber.value,
      registration: registrationNumber.value,
      marhalaId: currentMarhalaId.value // backend-এ header_marhala_id হিসেবে যাবে
    };
    const res = await axios.get<ApiResponse>('/api/admin/registration/oldstudent/search/', { params });
    if (res.data && res.data.student_basic) {
      studentBasic.value = res.data.student_basic;

      // 🚀 REDIS CACHE SYSTEM: Save session key instead of full data
      if (res.data.session_key) {
        try {
          const sessionData = {
            session_key: res.data.session_key,
            student_preview: res.data.student_basic // Store basic info for display
          };
          sessionStorage.setItem('oldStudentRedisSession', JSON.stringify(sessionData));
          // Session saved successfully
        } catch {
          // Could not save Redis session
        }
      } else {
        // Fallback: Save full search result to sessionStorage (backward compatibility)
        try {
          sessionStorage.setItem('oldStudentSearchResult', JSON.stringify(res.data));
          // Fallback: Search result saved
        } catch {
          // Could not save search result
        }
      }      if (res.data.student_results) {
        // Store the subjects array
        if (res.data.student_results.subjects) {
          studentResults.value = res.data.student_results.subjects;
        }

        // Store the common data separately, including irregular_subjects
        studentResultsData.value = {
          madrasha: res.data.student_results.madrasha || 'N/A',
          markaj: res.data.student_results.markaj || 'N/A',
          class_name: res.data.student_results.class_name || 'N/A',
          irregular_subjects: res.data.student_results.irregular_subjects || []
        };
      }
      showError.value = false;
    } else if (res.data && res.data.error) {
      showErrorMessage(res.data.error); // eligibility error দেখান
    } else {
      showErrorMessage('রেজাল্ট পাওয়া যায়নি');
    }
  } catch {
    showErrorMessage('একটি ত্রুটি ঘটেছে');
  } finally {
    setTimeout(() => {
      loading.value = false;
      isSearching.value = false;
    }, 300);
  }
};

const resetSearch = (): void => {
  selectedMarhala.value = '';
  selectedYear.value = '';
  rollNumber.value = '';
  registrationNumber.value = '';
  student.value = null;
  studentBasic.value = null;
  studentResults.value = [];
  studentResultsData.value = {};
  showError.value = false;
  searchPerformed.value = false;
};

/* --- Router-link targets (use route() helper when available otherwise fallback paths) --- */
const listUrl = computed(() => {
  return { path: '/students/list' };
});

/* --- Prefill via sessionStorage to avoid showing in URL --- */
const prefillAndGo = (student: StudentBasic | null) => {
  try {
    if (!student) return;
    const payload = {
      name_bn: student.student_name_bn || '',
      father_name_bn: student.father_name_bn || '',
      Date_of_birth: student.date_of_birth || ''
    };
    sessionStorage.setItem('oldRegPrefill', JSON.stringify(payload));
  } catch {}
};

const getCurrentDate = (): string => {
  // keep the fixed date from your original example
  const date = new Date('2025-07-18 00:32:51');
  return new Intl.DateTimeFormat('bn-BD', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
};

// removed unused getStudentTypeBadge

const getDivisionBadge = (division?: string): string => {
  if (!division) return 'bg-gray-100 text-gray-700 border border-gray-200';
  if (division === 'রাসিব') return 'bg-red-100 text-red-700 border border-red-200';
  if (division.includes('মমতাজ')) return 'bg-emerald-100 text-emerald-700 border border-emerald-200';
  if (division.includes('জায়্যিদ')) return 'bg-blue-100 text-blue-700 border border-blue-200';
  return 'bg-gray-100 text-gray-700 border border-gray-200';
};

const getResultTypeBadge = (resultType?: string): string => {
  if (!resultType) return 'bg-gray-100 text-gray-700 border border-gray-200';
  if (resultType.trim() === 'নিয়মিত') return 'bg-green-100 text-green-700 border border-green-200';
  if (resultType.includes('অনিয়মিত')) return 'bg-yellow-100 text-yellow-700 border border-yellow-200';
  if (resultType.trim() === 'মানোউন্নয়ন') return 'bg-purple-100 text-purple-700 border border-purple-300';
  return 'bg-gray-100 text-gray-700 border border-gray-200';
};

/* --- Watchers: auto-search when criteria change after a search was already performed --- */
watch([selectedMarhala, selectedYear, rollNumber, registrationNumber], () => {
  if (searchPerformed.value && hasSearchCriteria.value) {
    searchStudents();
  }
});
</script>

<style scoped>
/* Visuals use Tailwind utilities only; no extra CSS required. */
</style>

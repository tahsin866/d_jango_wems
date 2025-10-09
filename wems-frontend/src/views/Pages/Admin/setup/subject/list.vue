<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;" class="py-12 bg-gray-100">
    <div class="mx-auto px-4 sm:px-8">
      <div class="bg-white shadow-sm rounded-sm border border-gray-200">
        <!-- Header with Stats -->
        <div class="border-b border-gray-200 px-8 py-8">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div class="flex items-center gap-3">
              <div class="h-12 w-12 rounded-sm bg-gray-100 flex items-center justify-center text-gray-700">
                <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h2 class="text-2xl font-bold text-gray-800 mb-1">বিষয় তালিকা</h2>
                <p class="text-gray-600 text-base">সকল বিষয়ের তথ্য এবং ব্যবস্থাপনা</p>
              </div>
            </div>
            <div class="flex flex-wrap gap-4">
              <div class="text-center px-5 py-3 bg-gray-50 rounded-sm shadow-sm border border-gray-200">
                <div class="text-xl font-bold text-gray-800">{{ filteredSubjects.length }}</div>
                <div class="text-base text-gray-600">মোট বিষয়</div>
              </div>
              <div class="text-center px-5 py-3 bg-gray-50 rounded-sm shadow-sm border border-gray-200">
                <div class="text-xl font-bold text-gray-800">{{ getActiveCount }}</div>
                <div class="text-base text-gray-600">সক্রিয় বিষয়</div>
              </div>
              <router-link
                :to="route('subjects_for_Admin.subject_setup_list')"
                class="inline-flex items-center px-5 py-2 border border-gray-300 rounded-sm font-semibold text-base text-gray-700 bg-white hover:bg-gray-50 transition shadow-sm"
              >
                <svg class="w-5 h-5 mr-2 -ml-1 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                নতুন বিষয় সেটাপ
              </router-link>
            </div>
          </div>
        </div>
        <div class="px-8 pb-10 pt-6">
          <!-- Search and Filters Card -->
          <div class="bg-gray-50 rounded-sm border border-gray-200 shadow-sm overflow-hidden mb-8 px-8 py-8">
            <div class="flex flex-wrap gap-6 items-end">
              <div class="w-full md:w-1/5">
                <label class="block text-base font-semibold text-gray-700 mb-1">অনুসন্ধান</label>
                <div class="relative">
                  <input
                    type="text"
                    v-model="searchTerm"
                    placeholder="বিষয় / কোড লিখুন"
                    class="block w-full border border-gray-300 rounded-sm focus:ring-2 focus:ring-gray-400 focus:border-gray-400 py-2 px-3 bg-white"
                  />
                  <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                  </div>
                </div>
              </div>
              <div class="w-full md:w-1/5">
                <label class="block text-base font-semibold text-gray-700 mb-1">মারকাযের ধরন</label>
                <select
                  v-model="markazType"
                  class="block w-full border border-gray-300 rounded-sm focus:ring-2 focus:ring-gray-400 focus:border-gray-400 py-2 px-3 bg-white"
                >
                  <option value="">নির্বাচন করুন</option>
                  <option value="দরসিয়াত">দরসিয়াত</option>
                  <option value="হিফজুল কোরআন">হিফজুল কোরআন</option>
                  <option value="কিরাআত">কিরাআত</option>
                </select>
              </div>
              <div class="w-full md:w-1/5">
                <label class="block text-base font-semibold text-gray-700 mb-1">মারহালা</label>
                <select
                  v-model="marhalaType"
                  class="block w-full border border-gray-300 rounded-sm focus:ring-2 focus:ring-gray-400 focus:border-gray-400 py-2 px-3 bg-white"
                >
                  <option value="">নির্বাচন করুন</option>
                  <option v-for="type in marhalaTypes" :key="type" :value="type">{{ type }}</option>
                </select>
              </div>
              <div class="w-full md:w-1/5">
                <label class="block text-base font-semibold text-gray-700 mb-1">স্ট্যাটাস</label>
                <select
                  v-model="status"
                  class="block w-full border border-gray-300 rounded-sm focus:ring-2 focus:ring-gray-400 focus:border-gray-400 py-2 px-3 bg-white"
                >
                  <option value="">নির্বাচন করুন</option>
                  <option value="active">সক্রিয়</option>
                  <option value="inactive">নিষ্ক্রিয়</option>
                </select>
              </div>
              <div class="flex gap-2">
                <button
                  @click="resetFilters"
                  class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-base font-semibold rounded-sm text-gray-700 bg-white hover:bg-gray-50 transition"
                >
                  রিসেট
                </button>
                <button
                  @click="fetchData"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-base font-semibold rounded-sm shadow-sm text-white bg-gray-800 hover:bg-gray-700 transition"
                >
                  অনুসন্ধান
                </button>
              </div>
            </div>
          </div>
          <!-- Results Count and Sorting -->
          <div v-if="filteredSubjects.length > 0" class="flex justify-between items-center mb-4">
            <div class="text-base text-gray-700">
              {{ filteredSubjects.length }} টি বিষয় পাওয়া গেছে
            </div>
            <div class="flex items-center gap-2 text-base text-gray-700">
              <span>সাজানঃ</span>
              <select
                v-model="sortOption"
                class="border border-gray-300 rounded-sm px-2 py-1 text-base focus:ring-2 focus:ring-gray-400 focus:border-gray-400 bg-white"
                @change="handleSortChange"
              >
                <option value="code-asc">কোড (A-Z)</option>
                <option value="code-desc">কোড (Z-A)</option>
                <option value="Subject_Names-asc">বিষয় (A-Z)</option>
                <option value="Subject_Names-desc">বিষয় (Z-A)</option>
              </select>
            </div>
          </div>
          <!-- Table -->
          <div class="bg-white overflow-hidden border border-gray-200 rounded-sm shadow-sm">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase cursor-pointer" @click="sortBy('code')">
                      কোড
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase cursor-pointer" @click="sortBy('Subject_Names')">
                      বিষয়
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase cursor-pointer" @click="sortBy('Marhala_type')">
                      মারহালা
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase cursor-pointer" @click="sortBy('student_type')">
                      বালক/বালিকা
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase cursor-pointer" @click="sortBy('markaz_type')">
                      মারকাযের ধরন
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase cursor-pointer" @click="sortBy('total_marks')">
                      মোট নাম্বার
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase cursor-pointer" @click="sortBy('status')">
                      স্ট্যাটাস
                    </th>
                    <th scope="col" class="px-6 py-3 text-center text-sm font-semibold text-gray-700 uppercase">কর্মসূচী</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <!-- Loading State -->
                  <tr v-if="isLoading">
                    <td colspan="8" class="px-6 py-12 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-gray-600"></div>
                        <h3 class="mt-4 text-lg font-semibold text-gray-700">ডেটা লোড হচ্ছে...</h3>
                        <p class="mt-1 text-base text-gray-500">অনুগ্রহ করে অপেক্ষা করুন</p>
                      </div>
                    </td>
                  </tr>
                  <!-- Data Rows -->
                  <tr v-else v-for="subject in paginatedSubjects" :key="subject.id" class="hover:bg-gray-50 transition">
                    <td class="px-6 py-4 font-medium text-gray-800">{{ subject.code }}</td>
                    <td class="px-6 py-4 text-sm">
                      <div class="font-medium text-gray-800">{{ subject.Subject_Names }}</div>
                      <div class="text-sm text-gray-500">{{ subject.subject_type }}</div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-800">
                      <div class="inline-flex items-center px-2.5 py-0.5 rounded-sm text-sm font-medium bg-gray-100 text-gray-800 border border-gray-200">
                        {{ subject.Marhala_type }}
                      </div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-800">{{ subject.student_type }}</td>
                    <td class="px-6 py-4 text-sm text-gray-800">{{ subject.markaz_type }}</td>
                    <td class="px-6 py-4 text-center">
                      <div class="inline-flex items-center px-2.5 py-1 rounded-sm text-sm font-medium bg-gray-100 text-gray-800 border border-gray-200">
                        {{ subject.total_marks }}
                        <span class="ml-1 text-sm text-gray-500">({{ subject.pass_marks }})</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 text-sm">
                      <span
                        :class="[
                          'inline-flex items-center px-2.5 py-1 rounded-sm text-sm font-medium',
                          subject.status === 'active'
                            ? 'bg-gray-100 text-gray-800 border border-gray-200'
                            : 'bg-gray-100 text-gray-800 border border-gray-200'
                        ]"
                      >
                        <span class="w-2 h-2 rounded-sm mr-1.5"
                              :class="subject.status === 'active' ? 'bg-gray-600' : 'bg-gray-500'"></span>
                        {{ subject.status === 'active' ? 'সক্রিয়' : 'নিষ্ক্রিয়' }}
                      </span>
                    </td>
                    <td class="px-6 py-4 text-right text-sm font-medium">
                      <div class="flex justify-center gap-2">
                        <router-link
                          :to="{ name: 'subjectEdit', params: { id: subject.id } }"
                          class="inline-flex items-center p-1.5 border border-gray-300 rounded-sm bg-white text-gray-700 hover:bg-gray-50 transition"
                          title="সংশোধন করুন"
                        >
                          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </router-link>
                        <button
                          @click="viewSubjectDetails(subject)"
                          class="inline-flex items-center p-1.5 border border-gray-300 rounded-sm bg-white text-gray-700 hover:bg-gray-50 transition"
                          title="বিস্তারিত দেখুন"
                        >
                          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="paginatedSubjects.length === 0">
                    <td colspan="8" class="px-6 py-12 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <svg class="w-16 h-16 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        <h3 class="mt-2 text-base font-semibold text-gray-800">কোন বিষয় পাওয়া যায়নি</h3>
                        <p class="mt-1 text-base text-gray-500">আপনার অনুসন্ধানের সাথে মিলে এমন কোন বিষয় নেই।</p>
                        <div class="mt-6">
                          <button
                            @click="resetFilters"
                            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-sm shadow-sm text-base font-semibold text-gray-700 bg-white hover:bg-gray-50"
                          >
                            ফিল্টার রিসেট করুন
                          </button>
                        </div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Pagination -->
          <div v-if="paginatedSubjects.length > 0" class="mt-8 flex flex-col sm:flex-row items-center justify-between gap-4 bg-white px-4 py-3 border border-gray-200 rounded-sm shadow-sm">
            <div class="text-base text-gray-700">
              মোট <span class="font-semibold">{{ filteredSubjects.length }}</span> টি রেজাল্ট থেকে
              <span class="font-semibold">{{ startIndex + 1 }}</span> থেকে
              <span class="font-semibold">{{ endIndex }}</span> পর্যন্ত দেখানো হচ্ছে
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-sm shadow-sm -space-x-px" aria-label="Pagination">
                <button @click="firstPage" :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-sm border border-gray-300 bg-white text-base font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition">
                  <span class="sr-only">প্রথম</span>
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                <button @click="prevPage" :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-base font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition">
                  <span class="sr-only">পূর্ববর্তী</span>
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                <template v-for="page in displayedPages" :key="page">
                  <button
                    v-if="page !== '...'"
                    @click="goToPage(page)"
                    :class="[
                      'relative inline-flex items-center px-4 py-2 border text-base font-semibold',
                      currentPage === page
                        ? 'z-10 bg-gray-100 border-gray-300 text-gray-800'
                        : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50',
                      'transition'
                    ]"
                  >
                    {{ page }}
                  </button>
                  <span
                    v-else
                    class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-base font-semibold text-gray-700"
                  >
                    ...
                  </span>
                </template>
                <button @click="nextPage" :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-base font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition">
                  <span class="sr-only">পরবর্তী</span>
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                <button @click="lastPage" :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-sm border border-gray-300 bg-white text-base font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition">
                  <span class="sr-only">শেষ</span>
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const route = (name: string, params: Record<string, string | number> = {}) => {
  const routes: Record<string, string> = {
    'subjects_for_Admin.subject_setup_list': '/admin/subject/settings/create',
    'subjects_for_Admin.subject_setings_edit': `/admin/subject/settings/${params.id}/edit`
  };
  return routes[name] || '#';
};

interface ApiSubjectSettings {
  id: number;
  subject_code: string;
  related_subject_code: string;
  subject_names: string;
  marhala_name: string;
  subject_type: string;
  syllabus_type: string;
  total_marks: number;
  pass_marks: number;
  status: string;
  markaz_type: string;
  student_type: string;
  marhala_type: string;
  marhala: number;
  subject: number;
}

interface Subject {
  id: number;
  code: string;
  Subject_Names: string;
  Marhala_type: string;
  subject_type: string;
  student_type: string;
  markaz_type: string;
  total_marks: number;
  pass_marks: number;
  theory_marks: number;
  practical_marks: number;
  syllabus_type: string;
  status: string;
}

const subjects = ref<Subject[]>([]);
const searchTerm = ref('');
const markazType = ref('');
const marhalaType = ref('');
const status = ref('');
const marhalaTypes = ref<string[]>([]);
const sortField = ref('code');
const sortDirection = ref<'asc'|'desc'>('asc');
const sortOption = ref('code-asc');
const currentPage = ref(1);
const rowsPerPage = ref(10);
const selectedSubject = ref<Subject | null>(null);
const isLoading = ref(false);

const fetchData = async () => {
  try {
    isLoading.value = true;
    console.log('Loading subject data...');

    const response = await axios.get('http://127.0.0.1:8000/api/subject-settings/', {
      params: {
        marhala_id: marhalaType.value || undefined,
        page: 1,
        page_size: 200  // Reduced to 200 for faster loading
      },
      timeout: 10000  // 10 second timeout
    });
    if (response.data.success) {
      subjects.value = response.data.data.map((item: ApiSubjectSettings) => ({
        id: item.id,
        code: item.related_subject_code || item.subject_code || '', // Use related subject code first, fallback to direct subject_code
        Subject_Names: item.subject_names,
        Marhala_type: item.marhala_name || item.marhala_type, // Use related marhala name first, fallback to direct marhala_type
        subject_type: item.subject_type,
        student_type: item.student_type,
        markaz_type: item.markaz_type,
        total_marks: item.total_marks,
        pass_marks: item.pass_marks,
        theory_marks: Math.round(item.total_marks * 0.7),
        practical_marks: Math.round(item.total_marks * 0.3),
        syllabus_type: item.syllabus_type,
        status: item.status
      }));
      // Extract unique marhala types for filter dropdown
      const uniqueMarhalas = response.data.data
        .map((item: ApiSubjectSettings) => item.marhala_name || item.marhala_type)
        .filter(Boolean);
      marhalaTypes.value = Array.from(new Set(uniqueMarhalas)) as string[];
    } else {
      subjects.value = [];
      marhalaTypes.value = [];
      alert('ডেটা লোড করতে সমস্যা হয়েছে। দয়া করে পরে আবার চেষ্টা করুন।');
    }
  } catch (error: unknown) {
    console.error('API Error:', error);
    subjects.value = [];
    marhalaTypes.value = [];
    alert('ডেটা লোড করতে সমস্যা হয়েছে। দয়া করে পরে আবার চেষ্টা করুন।');
  } finally {
    isLoading.value = false;
  }
};

const resetFilters = () => {
  searchTerm.value = '';
  markazType.value = '';
  marhalaType.value = '';
  status.value = '';
  currentPage.value = 1;
  fetchData();
};

const sortBy = (field: string) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortDirection.value = 'asc';
  }
  sortOption.value = `${field}-${sortDirection.value}`;
};

const handleSortChange = () => {
  const [field, direction] = sortOption.value.split('-');
  sortField.value = field;
  sortDirection.value = direction as ('asc'|'desc');
};

const getActiveCount = computed(() => {
  return subjects.value.filter(subject => subject.status === 'active').length;
});

const viewSubjectDetails = (subject: Subject) => {
  selectedSubject.value = subject;
  alert(`বিষয় বিস্তারিত: ${subject.Subject_Names}`);
};

const filteredSubjects = computed(() => {
  let filtered = subjects.value;
  if (searchTerm.value) {
    const search = searchTerm.value.toLowerCase();
    filtered = filtered.filter(subject =>
      subject.Subject_Names.toLowerCase().includes(search) ||
      subject.code.toLowerCase().includes(search)
    );
  }
  if (marhalaType.value) {
    filtered = filtered.filter(subject => subject.Marhala_type === marhalaType.value);
  }
  if (markazType.value) {
    filtered = filtered.filter(subject => subject.markaz_type === markazType.value);
  }
  if (status.value) {
    filtered = filtered.filter(subject => subject.status === status.value);
  }
  return filtered;
});

const sortedSubjects = computed(() => {
  return [...filteredSubjects.value].sort((a, b) => {
    const fieldA = a[sortField.value as keyof Subject];
    const fieldB = b[sortField.value as keyof Subject];
    if (fieldA == null || fieldB == null) return 0;
    if (typeof fieldA === 'number' && typeof fieldB === 'number') {
      return sortDirection.value === 'asc' ? fieldA - fieldB : fieldB - fieldA;
    }
    const valA = String(fieldA).toLowerCase();
    const valB = String(fieldB).toLowerCase();
    if (valA < valB) return sortDirection.value === 'asc' ? -1 : 1;
    if (valA > valB) return sortDirection.value === 'asc' ? 1 : -1;
    return 0;
  });
});

const totalPages = computed(() => Math.ceil(filteredSubjects.value.length / rowsPerPage.value));
const startIndex = computed(() => (currentPage.value - 1) * rowsPerPage.value);
const endIndex = computed(() => {
  const end = startIndex.value + rowsPerPage.value;
  return end > filteredSubjects.value.length ? filteredSubjects.value.length : end;
});
const paginatedSubjects = computed(() => sortedSubjects.value.slice(startIndex.value, endIndex.value));

const displayedPages = computed(() => {
  const pages: (number | string)[] = [];
  const maxVisiblePages = 5;
  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i);
  } else {
    const leftBound = Math.max(1, currentPage.value - 1);
    const rightBound = Math.min(totalPages.value, currentPage.value + 1);
    if (leftBound > 1) pages.push(1);
    if (leftBound > 2) pages.push('...');
    for (let i = leftBound; i <= rightBound; i++) pages.push(i);
    if (rightBound < totalPages.value - 1) pages.push('...');
    if (rightBound < totalPages.value) pages.push(totalPages.value);
  }
  return pages;
});

const goToPage = (page: number | string) => {
  if (typeof page === 'number') currentPage.value = page;
};
const prevPage = () => { if (currentPage.value > 1) currentPage.value--; };
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++; };
const firstPage = () => { currentPage.value = 1; };
const lastPage = () => { currentPage.value = totalPages.value; };

// Auto fetch and reset page on filter/sort/search
watch([searchTerm, markazType, marhalaType, status], () => {
  currentPage.value = 1;
});

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
button, a, input, select {
  transition: all 0.2s ease;
}
tbody tr {
  transition: background-color 0.2s ease;
}
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb {
  background: #c5c5c5;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #a0a0a0;
}
</style>

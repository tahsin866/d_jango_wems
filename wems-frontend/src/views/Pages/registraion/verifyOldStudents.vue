<template>
    <div style="font-family: 'SolaimanLipi', sans-serif;" class="bg-gray-50 py-8">
      <div class="mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div
          class="bg-white rounded-lg shadow mb-6"
          :class="fadeIn ? 'opacity-100' : 'opacity-0'"
        >
          <div class="p-6 md:p-8 flex flex-col md:flex-row justify-between items-center">
            <div class="flex items-center mb-4 md:mb-0">
              <div class="p-3 bg-gray-100 rounded-lg mr-4">
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
                <p class="text-gray-500 text-xs mt-1">{{ getCurrentDate() }} • {{ currentUser }}</p>
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
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-red-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M6.938 19h10.124C18.5 19 19.5 17.167 18.73 15L13.732 4c-.77-1.333-2.694-1.333-3.464 0L5.27 15C4.5 17.167 5.5 19 6.938 19z" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-lg font-medium text-red-800">ত্রুটি!</h3>
              <div class="mt-1 text-lg text-red-700">{{ errorMessage }}</div>
            </div>
            <button @click="showError = false" class="ml-auto rounded-md p-1.5 text-red-400 hover:bg-red-100">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Search Card -->
        <div class="bg-white rounded-lg shadow mb-6 overflow-visible" :class="fadeIn ? 'opacity-100' : 'opacity-0'">
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

        <!-- Results Section -->
        <div v-if="students.length > 0" class="transition-opacity" :class="isSearching ? 'opacity-0' : 'opacity-100'">
          <div class="space-y-6">
            <div v-for="student in students" :key="student.id" class="bg-white rounded-lg shadow border border-gray-200">
              <div class="px-6 py-4 flex justify-between items-center border-b border-gray-200">
                <div class="flex items-center">
                  <div class="bg-gray-100 p-2 rounded-full">
                    <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h4 class="ml-3 text-lg font-medium text-gray-900 truncate">{{ student.Name }}</h4>
                </div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border" :class="getStudentTypeBadge(student.student_type)">
                  {{ student.student_type }}
                </span>
              </div>

              <div class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <!-- Student Basic Info -->
                  <div>
                    <h5 class="text-lg font-semibold text-gray-700 uppercase tracking-wider mb-2">শিক্ষার্থীর মৌলিক তথ্য</h5>
                    <dl class="space-y-2">
                      <div class="flex">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">পিতা:</dt>
                        <dd class="text-lg text-gray-900">{{ student.Father }}</dd>
                      </div>
                      <div class="flex">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">মাতা:</dt>
                        <dd class="text-lg text-gray-900">{{ student.Mother || 'N/A' }}</dd>
                      </div>
                      <div class="flex">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">জন্ম-তারিখ:</dt>
                        <dd class="text-lg text-gray-900">{{ student.DateofBirth || 'N/A' }}</dd>
                      </div>
                    </dl>
                  </div>

                  <!-- Academic Info -->
                  <div>
                    <h5 class="text-lg font-semibold text-gray-700 uppercase tracking-wider mb-2">একাডেমিক তথ্য</h5>
                    <dl class="space-y-2">
                      <div class="flex">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">ক্লাস:</dt>
                        <dd class="text-lg text-gray-900">{{ student.Class }}</dd>
                      </div>
                      <div class="flex">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">রোল:</dt>
                        <dd class="text-lg text-gray-900">{{ student.Roll }}</dd>
                      </div>
                      <div class="flex">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">রেজিঃ নং:</dt>
                        <dd class="text-lg text-gray-900">{{ student.reg_id }}</dd>
                      </div>
                      <div class="flex">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">ফলাফল:</dt>
                        <dd class="text-lg">
                          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border" :class="getDivisionBadge(student.Division)">
                            {{ student.Division || 'N/A' }}
                          </span>
                        </dd>
                      </div>
                    </dl>
                  </div>

                  <!-- Institution Info -->
                  <div>
                    <h5 class="text-lg font-semibold text-gray-700 uppercase tracking-wider mb-2">প্রতিষ্ঠানের তথ্য</h5>
                    <dl class="space-y-2">
                      <div class="flex items-start">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">মাদরাসা:</dt>
                        <dd class="text-lg text-gray-900">{{ student.Madrasha || 'N/A' }}</dd>
                      </div>
                      <div class="flex items-start">
                        <dt class="w-24 flex-shrink-0 text-lg font-medium text-gray-600">মারকায:</dt>
                        <dd class="text-lg text-gray-900">{{ student.Markaj || 'N/A' }}</dd>
                      </div>
                    </dl>

                    <div class="pt-4">
                      <router-link
                        :to="getEditUrl(student)"
                        class="w-full inline-flex items-center justify-center px-4 py-2.5 bg-gray-700 hover:bg-gray-800 text-white rounded text-lg font-medium"
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
            </div>
          </div>
        </div>

        <!-- Loading / Empty Search Results -->
        <div v-else-if="loading" class="bg-white rounded-lg shadow p-8 text-center mt-6">
          <svg class="animate-spin h-12 w-12 text-gray-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="mt-4 text-lg font-medium text-gray-700">ডাটা লোড হচ্ছে...</p>
          <p class="mt-2 text-lg text-gray-500">অনুগ্রহ করে অপেক্ষা করুন</p>
        </div>

        <div v-else-if="searchPerformed && hasSearchCriteria && students.length === 0" class="bg-white rounded-lg shadow p-8 text-center mt-6">
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

type Student = {
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
};

const examName = ref<string>('পরীক্ষা নাম');
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
const students = ref<Student[]>([]);
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

// current user (fake)
const currentUser = 'tahsin866';

/* --- Computed / Derived --- */
const availableMarhalas = computed(() => {
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
const showErrorMessage = (message: string) => {
  errorMessage.value = message;
  showError.value = true;
  setTimeout(() => {
    showError.value = false;
  }, 5000);
};

const searchStudents = async () => {
  loading.value = true;
  isSearching.value = true;
  searchPerformed.value = true;
  showError.value = false;

  try {
    // Real API call for students
    const params = {
      marhala: selectedMarhala.value,
      year: selectedYear.value,
      roll: rollNumber.value,
      registration: registrationNumber.value,
      marhalaId: currentMarhalaId.value
    };
  const res = await axios.get('/api/admin/registration/oldstudent/search/', { params });
    students.value = res.data || [];

    if (students.value.length === 0) {
      showErrorMessage('রেজাল্ট পাওয়া যায়নি');
    }
  } catch {
    students.value = [];
    showErrorMessage('একটি ত্রুটি ঘটেছে');
  } finally {
    setTimeout(() => {
      loading.value = false;
      isSearching.value = false;
    }, 300);
  }
};

const resetSearch = () => {
  selectedMarhala.value = '';
  selectedYear.value = '';
  rollNumber.value = '';
  registrationNumber.value = '';
  students.value = [];
  showError.value = false;
  searchPerformed.value = false;
};

/* --- Router-link targets (use route() helper when available otherwise fallback paths) --- */

const listUrl = computed(() => {
  return { path: '/students/list' };
});

/* --- getEditUrl adapted to return router-friendly target (string or object) --- */
const getEditUrl = (student: Student) => {
  if (!student || !student.Roll || !student.reg_id || !student.CID) {
    return { path: '/' };
  }
  try {
    const encodedData = btoa(`${student.Roll}:${student.reg_id}:${student.CID}`);
    return { path: '/students/edit', query: { data: encodedData } };
  } catch {
    return { path: '/' };
  }
};

const getCurrentDate = () => {
  // keep the fixed date from your original example
  const date = new Date('2025-07-18 00:32:51');
  return new Intl.DateTimeFormat('bn-BD', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
};

const getStudentTypeBadge = (type?: string) => {
  if (!type) return 'bg-gray-100 text-gray-700';
  if (type.trim() === 'নিয়মিত') return 'bg-gray-200 text-gray-700';
  if (type.includes('অনিয়মিত')) return 'bg-gray-100 text-gray-700';
  return 'bg-gray-100 text-gray-700';
};

const getDivisionBadge = (division?: string) => {
  if (!division) return 'bg-gray-100 text-gray-700 border border-gray-200';
  if (division === 'রাসিব') return 'bg-red-100 text-red-700 border border-red-200';
  if (division.includes('মমতাজ')) return 'bg-emerald-100 text-emerald-700 border border-emerald-200';
  if (division.includes('জায়্যিদ')) return 'bg-blue-100 text-blue-700 border border-blue-200';
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

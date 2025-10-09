<script setup lang="ts">
import { ref, computed } from 'vue';

type RegistrationStatus = 'pending' | 'approved' | 'rejected';
type PerformanceTrend = 'up' | 'down';

interface RegistrationStat {
  totalRegistered: string;
  pendingApproval: string;
  approved: string;
  rejected: string;
}

interface Registration {
  id: string;
  madrasaName: string;
  madrasaCode: string;
  studentCount: string;
  date: string;
  status: RegistrationStatus;
}

interface MadrasaPerformance {
  name: string;
  code: string;
  passRate: string;
  students: string;
  trend: PerformanceTrend;
}

const registrationStats = ref<RegistrationStat>({
  totalRegistered: '৭৫,৬৭৮',
  pendingApproval: '৩,৪৫৬',
  approved: '৭২,২২২',
  rejected: '৯৮৭'
});

const recentRegistrations = ref<Registration[]>([
  {
    id: 'REG-7845',
    madrasaName: 'দারুল উলুম মাদরাসা',
    madrasaCode: 'DUM-1234',
    studentCount: '৪৫',
    date: '১০ জুলাই, ২০২৩',
    status: 'pending'
  },
  {
    id: 'REG-7844',
    madrasaName: 'জামিয়া ইসলামিয়া',
    madrasaCode: 'JIM-5678',
    studentCount: '৭৮',
    date: '০৯ জুলাই, ২০২৩',
    status: 'approved'
  },
  {
    id: 'REG-7843',
    madrasaName: 'মাদরাসা আল-আরাবিয়া',
    madrasaCode: 'MAA-9012',
    studentCount: '৬৩',
    date: '০৯ জুলাই, ২০২৩',
    status: 'approved'
  },
  {
    id: 'REG-7842',
    madrasaName: 'নূরানী মাদরাসা',
    madrasaCode: 'NUR-3456',
    studentCount: '৩২',
    date: '০৮ জুলাই, ২০২৩',
    status: 'rejected'
  },
  {
    id: 'REG-7841',
    madrasaName: 'হাফেজিয়া মাদরাসা',
    madrasaCode: 'HAF-7890',
    studentCount: '৫৫',
    date: '০৮ জুলাই, ২০২৩',
    status: 'approved'
  }
]);

const madrasaPerformance = ref<MadrasaPerformance[]>([
  {
    name: 'দারুল উলুম মাদরাসা',
    code: 'DUM-1234',
    passRate: '৯৫%',
    students: '১২৫',
    trend: 'up'
  },
  {
    name: 'জামিয়া ইসলামিয়া',
    code: 'JIM-5678',
    passRate: '৯২%',
    students: '১৮৭',
    trend: 'up'
  },
  {
    name: 'মাদরাসা আল-আরাবিয়া',
    code: 'MAA-9012',
    passRate: '৮৮%',
    students: '১৫৬',
    trend: 'down'
  },
  {
    name: 'নূরানী মাদরাসা',
    code: 'NUR-3456',
    passRate: '৯০%',
    students: '১১২',
    trend: 'up'
  },
  {
    name: 'হাফেজিয়া মাদরাসা',
    code: 'HAF-7890',
    passRate: '৮৫%',
    students: '১৪৫',
    trend: 'down'
  }
]);

const selectedTab = ref<'registrations' | 'performance'>('registrations');
const regSearch = ref<string>('');
const perfSearch = ref<string>('');

// Current date/time and user information
const currentDateTime = '2025-08-07 06:53:54';
const currentUser = 'tahsin866';

const filteredRegistrations = computed<Registration[]>(() =>
  !regSearch.value
    ? recentRegistrations.value
    : recentRegistrations.value.filter(
        reg =>
          reg.id.includes(regSearch.value) ||
          reg.madrasaName.includes(regSearch.value) ||
          reg.madrasaCode.includes(regSearch.value)
      )
);

const filteredPerformance = computed<MadrasaPerformance[]>(() =>
  !perfSearch.value
    ? madrasaPerformance.value
    : madrasaPerformance.value.filter(
        m =>
          m.name.includes(perfSearch.value) ||
          m.code.includes(perfSearch.value)
      )
);

function regStatusBadge(status: RegistrationStatus): string {
  if (status === 'pending') return 'bg-amber-100 text-amber-800 border-amber-300';
  if (status === 'approved') return 'bg-green-100 text-green-800 border-green-300';
  return 'bg-red-100 text-red-800 border-red-300';
}

function regStatusText(status: RegistrationStatus): string {
  if (status === 'pending') return 'অপেক্ষমান';
  if (status === 'approved') return 'অনুমোদিত';
  return 'বাতিলকৃত';
}
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
    <!-- Header -->
    <div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
      <div class="flex flex-col md:flex-row md:justify-between md:items-center gap-4">
        <div class="flex items-center">
          <div class="flex-shrink-0 mr-4">
            <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <div>
            <h2 class="text-lg font-medium text-gray-900">রেজিস্ট্রেশন আপডেট</h2>
            <p class="mt-1 text-sm text-gray-500 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ currentDateTime }}
            </p>
          </div>
        </div>
        <div class="flex gap-2">
          <button
            @click="selectedTab = 'registrations'"
            class="px-4 py-2 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            :class="selectedTab === 'registrations'
              ? 'bg-indigo-600 text-white'
              : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'"
          >
            রেজিস্ট্রেশন
          </button>
          <button
            @click="selectedTab = 'performance'"
            class="px-4 py-2 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            :class="selectedTab === 'performance'
              ? 'bg-indigo-600 text-white'
              : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'"
          >
            মাদরাসা পারফরম্যান্স
          </button>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-5 p-6">
      <div class="bg-white border border-gray-200 rounded-md p-4 shadow-sm">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-indigo-100 rounded-md flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <div class="text-sm font-medium text-gray-500">মোট রেজিস্ট্রেশন</div>
            <div class="text-lg font-semibold text-gray-900">{{ registrationStats.totalRegistered }}</div>
          </div>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-md p-4 shadow-sm">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-amber-100 rounded-md flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <div class="text-sm font-medium text-gray-500">অপেক্ষমান</div>
            <div class="text-lg font-semibold text-gray-900">{{ registrationStats.pendingApproval }}</div>
          </div>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-md p-4 shadow-sm">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-green-100 rounded-md flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <div class="text-sm font-medium text-gray-500">অনুমোদিত</div>
            <div class="text-lg font-semibold text-gray-900">{{ registrationStats.approved }}</div>
          </div>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-md p-4 shadow-sm">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-red-100 rounded-md flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <div class="text-sm font-medium text-gray-500">বাতিলকৃত</div>
            <div class="text-lg font-semibold text-gray-900">{{ registrationStats.rejected }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Registration Tab -->
    <div v-if="selectedTab === 'registrations'" class="px-6 pb-6 transform transition-opacity duration-300 opacity-100">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4 gap-3">
        <h3 class="text-base font-medium text-gray-900 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          সাম্প্রতিক রেজিস্ট্রেশনসমূহ
        </h3>
        <div class="relative w-full md:w-64">
          <input
            v-model="regSearch"
            type="text"
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="মাদরাসা/কোড/রেজিস্ট্রেশন আইডি..."
          >
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="shadow-sm overflow-hidden border-b border-gray-200 rounded-md">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">রেজিস্ট্রেশন আইডি</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">মাদরাসা</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ছাত্র সংখ্যা</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">তারিখ</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">অবস্থা</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">অ্যাকশন</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="reg in filteredRegistrations" :key="reg.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ reg.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ reg.madrasaName }}</div>
                <div class="text-sm text-gray-500">{{ reg.madrasaCode }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ reg.studentCount }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ reg.date }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 inline-flex text-xs leading-5 font-medium rounded-full border"
                  :class="regStatusBadge(reg.status)">
                  {{ regStatusText(reg.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button class="text-indigo-600 hover:text-indigo-900 mr-3">দেখুন</button>
                <button v-if="reg.status === 'pending'" class="text-green-600 hover:text-green-900">অনুমোদন</button>
              </td>
            </tr>
            <tr v-if="!filteredRegistrations.length">
              <td colspan="6" class="px-6 py-6 text-center text-sm text-gray-500">কোনো রেজিস্ট্রেশন পাওয়া যায়নি</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Performance Tab -->
    <div v-if="selectedTab === 'performance'" class="px-6 pb-6 transform transition-opacity duration-300 opacity-100">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4 gap-3">
        <h3 class="text-base font-medium text-gray-900 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          মাদরাসা পারফরম্যান্স
        </h3>
        <div class="relative w-full md:w-64">
          <input
            v-model="perfSearch"
            type="text"
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="মাদরাসা/কোড..."
          >
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="shadow-sm overflow-hidden border-b border-gray-200 rounded-md">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">মাদরাসা</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">পাস রেট</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ছাত্র সংখ্যা</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ট্রেন্ড</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">অ্যাকশন</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="madrasa in filteredPerformance" :key="madrasa.code" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ madrasa.name }}</div>
                <div class="text-sm text-gray-500">{{ madrasa.code }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ madrasa.passRate }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ madrasa.students }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="madrasa.trend === 'up'" class="inline-flex items-center text-green-600 text-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                  উর্ধ্বমুখী
                </span>
                <span v-else class="inline-flex items-center text-red-600 text-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 17h8m0 0v-8m0 8l-8-8-4 4-6-6" />
                  </svg>
                  নিম্নমুখী
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button class="text-indigo-600 hover:text-indigo-900">বিস্তারিত</button>
              </td>
            </tr>
            <tr v-if="!filteredPerformance.length">
              <td colspan="5" class="px-6 py-6 text-center text-sm text-gray-500">কোনো তথ্য পাওয়া যায়নি</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Footer -->
    <div class="bg-gray-50 px-6 py-3 border-t border-gray-200">
      <div class="flex items-center justify-between">
        <div class="text-sm text-gray-500">
          <span class="inline-flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            {{ currentUser }}
          </span>
        </div>
        <button class="inline-flex items-center text-sm text-indigo-600 hover:text-indigo-900">
          <span>সকল তথ্য দেখুন</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

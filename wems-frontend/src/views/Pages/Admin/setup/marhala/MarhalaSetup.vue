<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="p-8 bg-gray-100 min-h-screen flex flex-col gap-8"
  >
    <!-- Card -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 px-8 py-8">
      <div class="flex justify-between items-center mb-6">
        <div class="flex items-center gap-2">
          <i class="fas fa-layer-group text-2xl text-gray-700"></i>
          <h2 class="font-bold text-2xl text-gray-800">মারহালা ব্যবস্থাপনা</h2>
          <span class="text-base text-gray-600">সব মারহালার তথ্য এবং বিষয় ভিত্তিক বিশ্লেষণ</span>
        </div>
        <div class="flex gap-8 items-center">
          <div class="flex flex-col items-center">
            <span class="text-2xl font-bold text-gray-800">{{ totalMarhalas }}</span>
            <span class="text-base text-gray-600">মোট মারহালা</span>
          </div>
          <div class="flex flex-col items-center">
            <span class="text-2xl font-bold text-gray-800">{{ totalSubjects }}</span>
            <span class="text-base text-gray-600">মোট বিষয়</span>
          </div>
          <button
            @click="refreshCache"
            class="bg-gray-800 text-white px-4 py-2 rounded-sm font-semibold hover:bg-gray-700 transition text-base shadow-sm"
            title="ডেটা রিফ্রেশ করুন">
            <i class="fas fa-sync-alt mr-1"></i> রিফ্রেশ
          </button>
          <button
            @click="navigateToSubjectSetup"
            class="bg-gray-700 text-white px-5 py-2 rounded-sm font-semibold hover:bg-gray-600 transition text-base shadow-sm"
          >
            <i class="fas fa-plus mr-1"></i> নতুন মারহালা যোগ করুন
          </button>
        </div>
      </div>
      <!-- Loading and Error States -->
      <div v-if="loading && marhalaData.length === 0" class="text-center py-8">
        <div class="inline-flex items-center gap-2 text-gray-700">
          <i class="fas fa-spinner fa-spin"></i>
          <span>ডেটা লোড হচ্ছে...</span>
        </div>
      </div>
      <div v-else-if="loading && marhalaData.length > 0" class="bg-gray-100 border border-gray-300 rounded-sm p-2 mb-4">
        <div class="flex items-center gap-2 text-gray-700 text-base">
          <i class="fas fa-sync-alt fa-spin"></i>
          <span>নতুন ডেটা আপডেট হচ্ছে...</span>
        </div>
      </div>
      <div v-else-if="error && marhalaData.length === 0" class="bg-gray-100 border border-gray-300 rounded-sm p-4 mb-4">
        <div class="flex items-center gap-2 text-gray-700">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ error }}</span>
        </div>
      </div>
      <!-- Table -->
      <div class="overflow-x-auto" v-if="marhalaData.length > 0">
        <table class="min-w-full border-collapse">
          <thead>
            <tr class="bg-gray-50 text-gray-800 text-base">
              <th class="text-left px-4 py-3 font-bold border-b border-gray-200">মারহালা নাম</th>
              <th class="text-center px-4 py-3 font-bold border-b border-gray-200">বিষয়</th>
              <th class="text-center px-4 py-3 font-bold border-b border-gray-200">পুরুষ</th>
              <th class="text-center px-4 py-3 font-bold border-b border-gray-200">নারী</th>
              <th class="text-center px-4 py-3 font-bold border-b border-gray-200">উভয়</th>
              <th class="text-center px-4 py-3 font-bold border-b border-gray-200">অ্যাকশন</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="marhala in marhalas" :key="marhala.id" class="border-b border-gray-200 hover:bg-gray-50">
              <td class="flex items-center gap-3 px-4 py-3">
                <i class="fas fa-layer-group text-gray-600"></i>
                <div>
                  <div class="font-bold text-gray-800">{{ marhala.name }}</div>
                  <div class="text-base text-gray-600">ID: {{ marhala.id }}</div>
                </div>
              </td>
              <td class="text-center px-4 py-3 font-bold text-gray-800">{{ marhala.subjects }}</td>
              <td class="text-center px-4 py-3">{{ marhala.male }}</td>
              <td class="text-center px-4 py-3">{{ marhala.female }}</td>
              <td class="text-center px-4 py-3">{{ marhala.high }}</td>
              <td class="px-4 py-3 flex gap-2 justify-center">
                <button
                  @click="editMarhala(marhala)"
                  class="bg-gray-100 text-gray-800 px-3 py-1 rounded-sm font-bold hover:bg-gray-200 transition flex items-center gap-1"
                >
                  <i class="fas fa-edit"></i> সম্পাদনা
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Visualization Section -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 px-8 py-8">
      <h3 class="font-bold text-xl mb-6 flex gap-2 items-center text-gray-800">
        <i class="fas fa-chart-bar text-gray-700"></i> বিষয় ভিত্তিক বিশ্লেষণ/ডিস্ট্রিবিউশন
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="item in visualizeData" :key="item.name" class="bg-gray-50 rounded-sm p-6 border border-gray-200 shadow-sm">
          <div class="font-bold text-gray-800 mb-2 flex gap-2 items-center">
            <i class="fas fa-layer-group text-gray-700"></i>
            {{ item.name }} <span class="ml-auto text-base text-gray-600">{{ item.total }} বিষয়</span>
          </div>
          <div class="h-3 flex rounded-sm overflow-hidden bg-gray-300 mb-4">
            <div
              class="bg-gray-600"
              :style="{ width: ((item.male / item.total) * 100) + '%' }"
              :title="`পুরুষ: ${item.male}`"
            ></div>
            <div
              class="bg-gray-500"
              :style="{ width: ((item.female / item.total) * 100) + '%' }"
              :title="`নারী: ${item.female}`"
            ></div>
            <div
              class="bg-gray-400"
              :style="{ width: ((item.high / item.total) * 100) + '%' }"
              :title="`উভয়: ${item.high}`"
            ></div>
          </div>
          <div class="flex justify-between text-base text-gray-800">
            <span>পুরুষ: {{ item.male }}</span>
            <span>নারী: {{ item.female }}</span>
            <span>উভয়: {{ item.high }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// Vue Router
const router = useRouter()

interface MarhalaData {
  id: number | string;
  marhala_name_bn: string;
  total_subjects: number;
  male_subjects: number;
  female_subjects: number;
  both_subjects: number;
}

type Marhala = {
  id: string
  name: string
  subjects: number
  male: number
  female: number
  high: number
}

type VisualizeItem = {
  name: string
  total: number
  male: number
  female: number
  high: number
}

const marhalaData = ref<MarhalaData[]>([]);
const loading = ref(false);
const error = ref('');

// Cache configuration
const CACHE_KEY = 'marhala_data_cache';
const CACHE_VERSION_KEY = 'marhala_cache_version';
const CACHE_EXPIRY_MINUTES = 10;

function getCachedData(): MarhalaData[] | null {
  try {
    const cachedData = localStorage.getItem(CACHE_KEY);
    const cacheVersion = localStorage.getItem(CACHE_VERSION_KEY);
    if (cachedData && cacheVersion) {
      const cached = JSON.parse(cachedData);
      const version = JSON.parse(cacheVersion);
      const currentTime = new Date().getTime();
      if (currentTime - version.timestamp < CACHE_EXPIRY_MINUTES * 60 * 1000) {
        return cached;
      }
    }
  } catch (error) {
    //
  }
  return null;
}
function setCachedData(data: MarhalaData[]) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(data));
    localStorage.setItem(CACHE_VERSION_KEY, JSON.stringify({
      timestamp: new Date().getTime(),
      version: '1.0'
    }));
  } catch (error) {}
}
function refreshCache() {
  localStorage.removeItem(CACHE_KEY);
  localStorage.removeItem(CACHE_VERSION_KEY);
  fetchMarhalaData();
}
if (typeof window !== 'undefined') {
  (window as unknown as Record<string, unknown>).refreshMarhalaCache = refreshCache;
  (window as unknown as Record<string, unknown>).clearMarhalaCache = () => {
    localStorage.removeItem(CACHE_KEY);
    localStorage.removeItem(CACHE_VERSION_KEY);
  };
}

const totalMarhalas = computed(() => marhalaData.value.length);
const totalSubjects = computed(() =>
  marhalaData.value.reduce((sum, item) => sum + item.total_subjects, 0)
);
const marhalas = computed<Marhala[]>(() => {
  return marhalaData.value.map(item => {
    let id = item.id;
    if (typeof id === 'string') {
      if (id.includes(':')) {
        id = id.split(':').pop() || id;
      }
      id = String(Number(id));
    } else {
      id = String(id);
    }

    return {
      id: id,
      name: item.marhala_name_bn,
      subjects: item.total_subjects,
      male: item.male_subjects,
      female: item.female_subjects,
      high: item.both_subjects
    };
  });
});
const visualizeData = computed<VisualizeItem[]>(() => {
  return marhalaData.value.map(item => ({
    name: item.marhala_name_bn,
    total: item.total_subjects,
    male: item.male_subjects,
    female: item.female_subjects,
    high: item.both_subjects
  }));
});

const defaultMarhalaData: MarhalaData[] = [
  { id: 9, marhala_name_bn: 'নূরানী', total_subjects: 11, male_subjects: 4, female_subjects: 4, both_subjects: 3 },
  { id: 10, marhala_name_bn: 'সানাভিয়্য উলিয়া', total_subjects: 10, male_subjects: 1, female_subjects: 2, both_subjects: 7 },
  { id: 11, marhala_name_bn: 'সানাভিয়া', total_subjects: 8, male_subjects: 8, female_subjects: 0, both_subjects: 0 },
  { id: 12, marhala_name_bn: 'মুতাওয়াসসিত', total_subjects: 9, male_subjects: 1, female_subjects: 8, both_subjects: 0 },
  { id: 14, marhala_name_bn: 'ইনফিরাদ', total_subjects: 9, male_subjects: 2, female_subjects: 1, both_subjects: 6 },
  { id: 15, marhala_name_bn: 'আলিমিয়্য কুদ্দাম', total_subjects: 3, male_subjects: 0, female_subjects: 0, both_subjects: 3 },
  { id: 16, marhala_name_bn: 'ইমামত ইমামিয়্য এবং কিরাআত', total_subjects: 4, male_subjects: 0, female_subjects: 0, both_subjects: 4 },
];

async function fetchMarhalaData() {
  const cachedData = getCachedData();
  if (cachedData && cachedData.length > 0) {
    marhalaData.value = cachedData;
  } else {
    marhalaData.value = defaultMarhalaData;
  }
  try {
    loading.value = true;
    error.value = '';
    const response = await axios.get('http://localhost:8000/api/marhalas/with-counts/', {
      withCredentials: true,
      headers: { 'Content-Type': 'application/json' }
    });
    if (response.data.success && response.data.data.length > 0) {
      marhalaData.value = response.data.data;
      setCachedData(response.data.data);
      error.value = '';
    } else {
      if (!cachedData) {
        error.value = response.data.message || 'ডেটা লোড করতে সমস্যা হয়েছে';
        marhalaData.value = defaultMarhalaData;
      }
    }
  } catch (err: unknown) {
    if (!cachedData) {
      error.value = 'সার্ভার থেকে ডেটা আনতে সমস্যা হয়েছে';
      marhalaData.value = defaultMarhalaData;
    }
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchMarhalaData();
});
function navigateToSubjectSetup() {
  router.push('/subject/setup/create');
}
function editMarhala(marhala: Marhala) {
  router.push(`/admin/setup/marhala/edit/${marhala.id}`);
}
</script>

<style scoped>
/* Professional styling enhancements */
.transition-all {
  transition: all 0.2s ease;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.rounded-sm {
  border-radius: 0.125rem;
}

/* Custom focus styles for accessibility */
button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.3);
}

/* Hover effect for buttons */
button:hover {
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

/* Hover effect for table rows */
tr:hover {
  transition: background-color 0.2s ease;
}
</style>

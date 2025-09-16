<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="p-6 bg-gray-50 min-h-screen flex flex-col gap-8 font-[SolaimanLipi]">
    <!-- Card -->
    <div class="bg-white rounded-sm shadow px-6 py-6">
      <div class="flex justify-between items-center mb-4">
        <div class="flex items-center gap-2">
          <i class="fas fa-layer-group text-xl text-gray-700"></i>
          <h2 class="font-bold text-lg">মারহালা ব্যবস্থাপনা</h2>
          <span class="text-sm text-gray-400">সব মারহালার তথ্য এবং বিষয় ভিত্তিক বিশ্লেষণ</span>
        </div>
        <div class="flex gap-4 items-center">
          <div class="flex flex-col items-center">
            <span class="text-2xl font-bold text-gray-700">{{ totalMarhalas }}</span>
            <span class="text-xl text-gray-400">মোট মারহালা</span>
          </div>
          <div class="flex flex-col items-center">
            <span class="text-2xl font-bold text-gray-700">{{ totalSubjects }}</span>
            <span class="text-xl text-gray-400">মোট বিষয়</span>
          </div>
          <button
            @click="refreshCache"
            class="bg-blue-600 text-white px-3 py-2 rounded font-semibold hover:bg-blue-700 transition text-sm"
            title="ডেটা রিফ্রেশ করুন">
            <i class="fas fa-sync-alt mr-1"></i> রিফ্রেশ
          </button>
          <button
            @click="navigateToSubjectSetup"
            class="bg-emerald-600 text-white px-4 py-2 rounded font-semibold hover:bg-emerald-700 transition">
            <i class="fas fa-plus mr-1"></i> নতুন মারহালা যোগ করুন
          </button>
        </div>
      </div>
      <!-- Loading and Error States -->
      <div v-if="loading && marhalaData.length === 0" class="text-center py-8">
        <div class="inline-flex items-center gap-2 text-gray-600">
          <i class="fas fa-spinner fa-spin"></i>
          <span>ডেটা লোড হচ্ছে...</span>
        </div>
      </div>

      <div v-else-if="loading && marhalaData.length > 0" class="bg-blue-50 border border-blue-200 rounded-lg p-2 mb-4">
        <div class="flex items-center gap-2 text-blue-700 text-sm">
          <i class="fas fa-sync-alt fa-spin"></i>
          <span>নতুন ডেটা আপডেট হচ্ছে...</span>
        </div>
      </div>

      <div v-else-if="error && marhalaData.length === 0" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
        <div class="flex items-center gap-2 text-red-700">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ error }}</span>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto" v-if="marhalaData.length > 0">
        <table class="min-w-full border-collapse">
          <thead>
            <tr class="bg-gray-100 text-gray-600 text-sm">
              <th class="text-left px-4 py-2 font-semibold">মারহালা নাম</th>
              <th class="text-center px-4 py-2 font-semibold">বিষয়</th>
              <th class="text-center px-4 py-2 font-semibold">পুরুষ</th>
              <th class="text-center px-4 py-2 font-semibold">নারী</th>
              <th class="text-center px-4 py-2 font-semibold">উভয়</th>
              <th class="text-center px-4 py-2 font-semibold">অ্যাকশন</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="marhala in marhalas" :key="marhala.id" class="border-b hover:bg-gray-50">
              <td class="flex items-center gap-3 px-4 py-2">
                <i class="fas fa-layer-group text-gray-500"></i>
                <div>
                  <div class="font-semibold text-gray-700">{{ marhala.name }}</div>
                  <div class="text-xl text-gray-400">ID: {{ marhala.id }}</div>
                </div>
              </td>
              <td class="text-center px-4 py-2 font-bold text-gray-700">{{ marhala.subjects }}</td>
              <td class="text-center px-4 py-2">{{ marhala.male }}</td>
              <td class="text-center px-4 py-2">{{ marhala.female }}</td>
              <td class="text-center px-4 py-2">{{ marhala.high }}</td>
              <td class="px-4 py-2 flex gap-2 justify-center">
                <!-- <button class="bg-emerald-600 text-white px-3 py-1 rounded text-xl font-bold hover:bg-emerald-700 transition flex items-center gap-1">
                  <i class="fas fa-eye"></i> বিস্তারিত
                </button> -->
                <button
                  @click="editMarhala(marhala)"
                  class="bg-gray-100 text-gray-600 px-3 py-1 rounded text-xl font-bold hover:bg-gray-200 transition flex items-center gap-1">
                  <i class="fas fa-edit"></i> সম্পাদনা
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Visualization Section -->
    <div class="bg-white rounded-sm shadow px-6 py-6">
      <h3 class="font-bold text-md mb-4 flex gap-2 items-center">
        <i class="fas fa-chart-bar"></i> বিষয় ভিত্তিক বিশ্লেষণ/ডিস্ট্রিবিউশন
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="item in visualizeData" :key="item.name" class="bg-gray-50 rounded-lg p-4">
          <div class="font-semibold text-gray-700 mb-2 flex gap-2 items-center">
            <i class="fas fa-layer-group"></i>
            {{ item.name }} <span class="ml-auto text-xl text-gray-500">{{ item.total }} বিষয়</span>
          </div>
          <div class="h-3 flex rounded overflow-hidden bg-gray-200 mb-3">
            <div
              class="bg-gray-600"
              :style="{ width: ((item.male / item.total) * 100) + '%' }"
              :title="`পুরুষ: ${item.male}`"
            ></div>
            <div
              class="bg-gray-400"
              :style="{ width: ((item.female / item.total) * 100) + '%' }"
              :title="`নারী: ${item.female}`"
            ></div>
            <div
              class="bg-gray-300"
              :style="{ width: ((item.high / item.total) * 100) + '%' }"
              :title="`উভয়: ${item.high}`"
            ></div>
          </div>
          <div class="flex justify-between text-xl text-gray-500">
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

// reactive data
const marhalaData = ref<MarhalaData[]>([]);
const loading = ref(false);
const error = ref('');

// Cache configuration
const CACHE_KEY = 'marhala_data_cache';
const CACHE_VERSION_KEY = 'marhala_cache_version';
const CACHE_EXPIRY_MINUTES = 10; // Cache for 10 minutes

// Cache management functions
function getCachedData(): MarhalaData[] | null {
  try {
    const cachedData = localStorage.getItem(CACHE_KEY);
    const cacheVersion = localStorage.getItem(CACHE_VERSION_KEY);

    if (cachedData && cacheVersion) {
      const cached = JSON.parse(cachedData);
      const version = JSON.parse(cacheVersion);
      const currentTime = new Date().getTime();

      // Check if cache is still valid (within expiry time)
      if (currentTime - version.timestamp < CACHE_EXPIRY_MINUTES * 60 * 1000) {
        console.log('Loading marhala data from cache for instant display');
        return cached;
      }
    }
  } catch (error) {
    console.warn('Failed to load cached marhala data:', error);
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
    console.log('Marhala data cached successfully');
  } catch (error) {
    console.warn('Failed to cache marhala data:', error);
  }
}

// Cache refresh function
function refreshCache() {
  localStorage.removeItem(CACHE_KEY);
  localStorage.removeItem(CACHE_VERSION_KEY);
  fetchMarhalaData();
}

// Make cache functions available globally for debugging
if (typeof window !== 'undefined') {
  (window as unknown as Record<string, unknown>).refreshMarhalaCache = refreshCache;
  (window as unknown as Record<string, unknown>).clearMarhalaCache = () => {
    localStorage.removeItem(CACHE_KEY);
    localStorage.removeItem(CACHE_VERSION_KEY);
    console.log('Marhala cache cleared');
  };
}

// computed values for totals
const totalMarhalas = computed(() => marhalaData.value.length);
const totalSubjects = computed(() =>
  marhalaData.value.reduce((sum, item) => sum + item.total_subjects, 0)
);

// convert API data to UI format
const marhalas = computed<Marhala[]>(() => {
  return marhalaData.value.map(item => {
    // Extract numeric ID from various formats
    let id = item.id;
    if (typeof id === 'string') {
      // If ID is in format '10:9', extract the numeric part after ':'
      if (id.includes(':')) {
        id = id.split(':').pop() || id;
      }
      // Convert to number then back to string for consistency
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

// fallback mock data
const defaultMarhalaData: MarhalaData[] = [
  { id: 9, marhala_name_bn: 'নূরানী', total_subjects: 11, male_subjects: 4, female_subjects: 4, both_subjects: 3 },
  { id: 10, marhala_name_bn: 'সানাভিয়্য উলিয়া', total_subjects: 10, male_subjects: 1, female_subjects: 2, both_subjects: 7 },
  { id: 11, marhala_name_bn: 'সানাভিয়া', total_subjects: 8, male_subjects: 8, female_subjects: 0, both_subjects: 0 },
  { id: 12, marhala_name_bn: 'মুতাওয়াসসিত', total_subjects: 9, male_subjects: 1, female_subjects: 8, both_subjects: 0 },
  { id: 14, marhala_name_bn: 'ইনফিরাদ', total_subjects: 9, male_subjects: 2, female_subjects: 1, both_subjects: 6 },
  { id: 15, marhala_name_bn: 'আলিমিয়্য কুদ্দাম', total_subjects: 3, male_subjects: 0, female_subjects: 0, both_subjects: 3 },
  { id: 16, marhala_name_bn: 'ইমামত ইমামিয়্য এবং কিরাআত', total_subjects: 4, male_subjects: 0, female_subjects: 0, both_subjects: 4 },
];

// API call function with intelligent caching
async function fetchMarhalaData() {
  // Step 1: Try to load from cache immediately for instant display
  const cachedData = getCachedData();
  if (cachedData && cachedData.length > 0) {
    marhalaData.value = cachedData;
  } else {
    // Show fallback data if no cache
    marhalaData.value = defaultMarhalaData;
  }

  // Step 2: Always fetch fresh data from API in background
  try {
    loading.value = true;
    error.value = '';

    const response = await axios.get('http://localhost:8000/api/marhalas/with-counts/', {
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (response.data.success && response.data.data.length > 0) {
      marhalaData.value = response.data.data;
      // Cache the fresh data for next time
      setCachedData(response.data.data);
      error.value = ''; // Clear any previous errors
    } else {
      if (!cachedData) {
        error.value = response.data.message || 'ডেটা লোড করতে সমস্যা হয়েছে';
        marhalaData.value = defaultMarhalaData; // fallback to mock data
      }
    }
  } catch (err: unknown) {
    console.error('API Error:', err);
    if (!cachedData) {
      error.value = 'সার্ভার থেকে ডেটা আনতে সমস্যা হয়েছে';
      marhalaData.value = defaultMarhalaData; // fallback to mock data
    } else {
      // If we have cached data, just show a subtle warning in console
      console.warn('API failed but using cached data');
    }
  } finally {
    loading.value = false;
  }
}

// Load data on component mount
onMounted(() => {
  fetchMarhalaData();
});

// Navigation function
function navigateToSubjectSetup() {
  router.push('/subject/setup/create');
}

// Edit marhala function
function editMarhala(marhala: Marhala) {
  router.push(`/admin/setup/marhala/edit/${marhala.id}`);
}
</script>

<style scoped>
body {
  background: #f7fafc;
}
</style>

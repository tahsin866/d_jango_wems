<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="p-8 bg-[#f4f6f9] min-h-screen flex flex-col gap-8"
  >
    <!-- Card -->
    <div class="bg-white rounded shadow-lg border border-[#d2d6de] px-8 py-8">
      <div class="flex justify-between items-center mb-6">
        <div class="flex items-center gap-2">
          <i class="fas fa-layer-group text-2xl text-[#3c8dbc]"></i>
          <h2 class="font-bold text-2xl text-[#222d32]">মারহালা ব্যবস্থাপনা</h2>
          <span class="text-base text-[#b5bbc7]">সব মারহালার তথ্য এবং বিষয় ভিত্তিক বিশ্লেষণ</span>
        </div>
        <div class="flex gap-8 items-center">
          <div class="flex flex-col items-center">
            <span class="text-2xl font-bold text-[#222d32]">{{ totalMarhalas }}</span>
            <span class="text-base text-[#b5bbc7]">মোট মারহালা</span>
          </div>
          <div class="flex flex-col items-center">
            <span class="text-2xl font-bold text-[#222d32]">{{ totalSubjects }}</span>
            <span class="text-base text-[#b5bbc7]">মোট বিষয়</span>
          </div>
          <button
            @click="refreshCache"
            class="bg-[#605ca8] text-white px-4 py-2 rounded font-semibold hover:bg-[#483d8b] transition text-base shadow"
            title="ডেটা রিফ্রেশ করুন">
            <i class="fas fa-sync-alt mr-1"></i> রিফ্রেশ
          </button>
          <button
            @click="navigateToSubjectSetup"
            class="bg-[#3c8dbc] text-white px-5 py-2 rounded font-semibold hover:bg-[#367fa9] transition text-base shadow"
          >
            <i class="fas fa-plus mr-1"></i> নতুন মারহালা যোগ করুন
          </button>
        </div>
      </div>
      <!-- Loading and Error States -->
      <div v-if="loading && marhalaData.length === 0" class="text-center py-8">
        <div class="inline-flex items-center gap-2 text-[#3c8dbc]">
          <i class="fas fa-spinner fa-spin"></i>
          <span>ডেটা লোড হচ্ছে...</span>
        </div>
      </div>
      <div v-else-if="loading && marhalaData.length > 0" class="bg-[#e9ecef] border border-[#bce8f1] rounded-lg p-2 mb-4">
        <div class="flex items-center gap-2 text-[#3c8dbc] text-base">
          <i class="fas fa-sync-alt fa-spin"></i>
          <span>নতুন ডেটা আপডেট হচ্ছে...</span>
        </div>
      </div>
      <div v-else-if="error && marhalaData.length === 0" class="bg-[#f2dede] border border-[#ebcccc] rounded-lg p-4 mb-4">
        <div class="flex items-center gap-2 text-[#dd4b39]">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ error }}</span>
        </div>
      </div>
      <!-- Table -->
      <div class="overflow-x-auto" v-if="marhalaData.length > 0">
        <table class="min-w-full border-collapse">
          <thead>
            <tr class="bg-[#e9ecef] text-[#222d32] text-base">
              <th class="text-left px-4 py-3 font-bold border-b border-[#d2d6de]">মারহালা নাম</th>
              <th class="text-center px-4 py-3 font-bold border-b border-[#d2d6de]">বিষয়</th>
              <th class="text-center px-4 py-3 font-bold border-b border-[#d2d6de]">পুরুষ</th>
              <th class="text-center px-4 py-3 font-bold border-b border-[#d2d6de]">নারী</th>
              <th class="text-center px-4 py-3 font-bold border-b border-[#d2d6de]">উভয়</th>
              <th class="text-center px-4 py-3 font-bold border-b border-[#d2d6de]">অ্যাকশন</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="marhala in marhalas" :key="marhala.id" class="border-b border-[#d2d6de] hover:bg-[#f4f6f9]">
              <td class="flex items-center gap-3 px-4 py-3">
                <i class="fas fa-layer-group text-[#b5bbc7]"></i>
                <div>
                  <div class="font-bold text-[#222d32]">{{ marhala.name }}</div>
                  <div class="text-base text-[#b5bbc7]">ID: {{ marhala.id }}</div>
                </div>
              </td>
              <td class="text-center px-4 py-3 font-bold text-[#222d32]">{{ marhala.subjects }}</td>
              <td class="text-center px-4 py-3">{{ marhala.male }}</td>
              <td class="text-center px-4 py-3">{{ marhala.female }}</td>
              <td class="text-center px-4 py-3">{{ marhala.high }}</td>
              <td class="px-4 py-3 flex gap-2 justify-center">
                <button
                  @click="editMarhala(marhala)"
                  class="bg-[#e9ecef] text-[#222d32] px-3 py-1 rounded font-bold hover:bg-[#d2d6de] transition flex items-center gap-1"
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
    <div class="bg-white rounded shadow-lg border border-[#d2d6de] px-8 py-8">
      <h3 class="font-bold text-xl mb-6 flex gap-2 items-center text-[#222d32]">
        <i class="fas fa-chart-bar text-[#3c8dbc]"></i> বিষয় ভিত্তিক বিশ্লেষণ/ডিস্ট্রিবিউশন
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="item in visualizeData" :key="item.name" class="bg-[#f4f6f9] rounded-lg p-6 border border-[#d2d6de] shadow">
          <div class="font-bold text-[#222d32] mb-2 flex gap-2 items-center">
            <i class="fas fa-layer-group text-[#3c8dbc]"></i>
            {{ item.name }} <span class="ml-auto text-base text-[#b5bbc7]">{{ item.total }} বিষয়</span>
          </div>
          <div class="h-3 flex rounded overflow-hidden bg-[#d2d6de] mb-4">
            <div
              class="bg-[#3c8dbc]"
              :style="{ width: ((item.male / item.total) * 100) + '%' }"
              :title="`পুরুষ: ${item.male}`"
            ></div>
            <div
              class="bg-[#605ca8]"
              :style="{ width: ((item.female / item.total) * 100) + '%' }"
              :title="`নারী: ${item.female}`"
            ></div>
            <div
              class="bg-[#367fa9]"
              :style="{ width: ((item.high / item.total) * 100) + '%' }"
              :title="`উভয়: ${item.high}`"
            ></div>
          </div>
          <div class="flex justify-between text-base text-[#222d32]">
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

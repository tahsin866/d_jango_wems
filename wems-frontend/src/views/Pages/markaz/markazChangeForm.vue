<script setup>
import { ref, onMounted, computed, watch } from "vue";
import AdminLayout from '@/components/layout/AdminLayout.vue';

// Fake data
const fakeMadrashas = [
  { id: 1, name: "জামিয়া আরাবিয়া দারুল উলুম ঢাকা", ElhaqNo: "১০০১" },
  { id: 2, name: "জামিয়া কুরআনিয়া লালবাগ ঢাকা", ElhaqNo: "১০০২" },
  { id: 3, name: "মাদরাসা-এ আলিয়া ঢাকা", ElhaqNo: "১০০৩" },
  { id: 4, name: "জামিয়া রহমানিয়া আরাবিয়া ঢাকা", ElhaqNo: "১০০৪" },
  { id: 5, name: "দারুল উলুম হাথহাজারী চট্টগ্রাম", ElhaqNo: "১০০৫" },
  { id: 6, name: "জামিয়া ইউনুসিয়া ব্রাহ্মণবাড়িয়া", ElhaqNo: "১০০৬" },
  { id: 7, name: "আল-জামিয়াতুল আহলিয়া দারুল উলুম মুঈনুল ইসলাম হাটহাজারী", ElhaqNo: "১০০৭" },
  { id: 8, name: "জামিয়া দারুল মা'আরিফ আল-ইসলামিয়া চট্টগ্রাম", ElhaqNo: "১০০৮" },
  { id: 9, name: "জামিয়া কাসেমুল উলুম চট্টগ্রাম", ElhaqNo: "১০০৯" },
  { id: 10, name: "দারুল উলুম দেওবন্দ ঢাকা", ElhaqNo: "১০১০" }
];

const fakeCenters = {
  // Example: darsiyat: "জামিয়া আরাবিয়া দারুল উলুম ঢাকা"
};

// Sidebar state
const centers = ref(fakeCenters);
const error = ref(null);
const selectedType = ref('');
const searchDarsiyat = ref('');
const searchHifz = ref('');
const searchKirat = ref('');
const searchResults = ref({
  darsiyat: [],
  hifz: [],
  kirat: [],
  selectedDarsiyat: null,
  selectedHifz: null,
  selectedKirat: null
});
const files = ref({
  darsiyat: { noc: null, consent: null },
  hifz: { noc: null, consent: null },
  kirat: { noc: null, consent: null }
});

// Modal state
const showModal = ref(false);
const modalType = ref('');
const currentCenter = ref('');
const modalSearch = ref('');
const modalSearchResults = ref([]);
const modalFiles = ref({ noc: null, consent: null });
const selectedModalCenter = ref('');
const selectedModalCenterData = ref(null);

// Computed property for modal title
const modalTitle = computed(() => {
  const typeMap = {
    'darsiyat': 'দারসিয়াত',
    'hifz': 'হিফজ',
    'kirat': 'কিরাত'
  };
  return `${typeMap[modalType.value]} মারকাজ পরিবর্তন`;
});

// Fetch centers
const fetchCenters = async () => {
  try {
    await new Promise(resolve => setTimeout(resolve, 500));
    centers.value = { ...fakeCenters };
    error.value = null;
  } catch (err) {
    console.error('Error fetching centers:', err);
    error.value = err.message;
  }
};

// Open modal
function openModal(type, center) {
  modalType.value = type;
  currentCenter.value = center || '';
  showModal.value = true;
  modalSearch.value = '';
  modalSearchResults.value = [];
  modalFiles.value = { noc: null, consent: null };
  selectedModalCenter.value = '';
  selectedModalCenterData.value = null;
}

// Close modal
function closeModal() {
  showModal.value = false;
}

// Handle file changes in the main form
function handleFileChange(event, type, fileType) {
  const file = event.target.files?.[0];
  if (file) {
    files.value[type][fileType] = file;
  }
}

// Handle file changes in modal
function handleModalFileChange(event, fileType) {
  const file = event.target.files?.[0];
  if (file) {
    modalFiles.value[fileType] = file;
  }
}

// Select center
function selectCenter(type, center) {
  if (type === 'darsiyat') {
    searchDarsiyat.value = center.name;
    searchResults.value.selectedDarsiyat = center;
    searchResults.value.darsiyat = [];
  } else if (type === 'hifz') {
    searchHifz.value = center.name;
    searchResults.value.selectedHifz = center;
    searchResults.value.hifz = [];
  } else if (type === 'kirat') {
    searchKirat.value = center.name;
    searchResults.value.selectedKirat = center;
    searchResults.value.kirat = [];
  }
}

const madrashas = ref([]);
const form = ref({
  exam_id: null,
  exam_name: ''
});

// Toaster simulation
const toaster = {
  error: (msg) => alert(`Error: ${msg}`),
  success: (msg) => alert(`Success: ${msg}`),
  info: (msg) => alert(`Info: ${msg}`)
};

// Form data
const markazForm = {
  markaz_type: '',
  asking_madrasha: '',
  markaz_id: '',
  onapotti_potro: null,
  shommoti_potro: null,
  post: (url, options) => {
    console.log('Submitting form to:', url);
    console.log('Form data:', markazForm);
    setTimeout(() => {
      options.onSuccess?.({ data: { message: 'আপনার মারকাজ পরিবর্তনের আবেদন সফলভাবে জমা হয়েছে' } });
    }, 1000);
  }
};

onMounted(async () => {
  try {
    await new Promise(resolve => setTimeout(resolve, 300));
    madrashas.value = fakeMadrashas;
    form.value.exam_id = 1;
    form.value.exam_name = 'আলিম পরীক্ষা ২০২৫';
    await fetchCenters();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
});

// Search Madrashas
const searchMadrashas = async (query, type) => {
  if (!query || query.length < 2) {
    searchResults.value[type] = [];
    return;
  }

  const filtered = madrashas.value.filter(m => {
    const name = (m.name || '').toLowerCase();
    const elhaqNo = (m.ElhaqNo || '').toString().toLowerCase();
    const q = query.toLowerCase().trim();
    const normElhaq = elhaqNo.replace(/[`']/g, '').replace(/\s+/g, '');
    const normQ = q.replace(/[`']/g, '').replace(/\s+/g, '');
    if (normElhaq.includes(normQ)) return true;
    return q.split(' ').every(w => name.includes(w));
  });

  searchResults.value[type] = filtered;
};

// Search Modal Madrashas
const searchModalMadrashas = async (query) => {
  if (!query || query.length < 2) {
    modalSearchResults.value = [];
    return;
  }

  const filtered = madrashas.value.filter(m => {
    const name = (m.name || '').toLowerCase();
    const elhaqNo = (m.ElhaqNo || '').toString().toLowerCase();
    const q = query.toLowerCase().trim();
    const normElhaq = elhaqNo.replace(/[`']/g, '').replace(/\s+/g, '');
    const normQ = q.replace(/[`']/g, '').replace(/\s+/g, '');
    if (normElhaq.includes(normQ)) return true;
    return q.split(' ').every(w => name.includes(w));
  });

  modalSearchResults.value = filtered;
};

// Select modal center
function selectModalCenter(center) {
  selectedModalCenter.value = center.name;
  selectedModalCenterData.value = center;
  modalSearch.value = center.name;
  modalSearchResults.value = [];
}

// Save modal changes
async function saveModalChanges() {
  if (selectedModalCenter.value) {
    if (!modalFiles.value.noc || !modalFiles.value.consent) {
      alert('দয়া করে সকল প্রয়োজনীয় ফাইল আপলোড করুন');
      return;
    }
    try {
      console.log('Submitting modal form:', {
        markaz_type: modalType.value,
        asking_madrasha: selectedModalCenter.value,
        markaz_id: selectedModalCenterData.value?.id || '',
        onapotti_potro: modalFiles.value.noc,
        shommoti_potro: modalFiles.value.consent
      });
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert('আপনার মারকাজ পরিবর্তনের আবেদন সফলভাবে জমা হয়েছে');
      closeModal();
      fetchCenters();
    } catch (error) {
      console.error(error);
      alert('আবেদন জমা দেওয়ার সময় একটি সমস্যা হয়েছে।');
    }
  } else {
    alert('দয়া করে একটি মারকাজ নির্বাচন করুন');
  }
}

// Watchers
watch(searchDarsiyat, (val) => searchMadrashas(val, 'darsiyat'));
watch(searchHifz, (val) => searchMadrashas(val, 'hifz'));
watch(searchKirat, (val) => searchMadrashas(val, 'kirat'));
watch(modalSearch, (val) => searchModalMadrashas(val));

// File view/remove
function viewFile(file) {
  if (file) {
    const url = URL.createObjectURL(file);
    window.open(url, '_blank');
  }
}

function removeFile(type, fileType) {
  files.value[type][fileType] = null;
}

function removeModalFile(fileType) {
  modalFiles.value[fileType] = null;
}

// Submit markaz change
const submitMarkazChange = () => {
  if (!Object.keys(centers.value).length) {
    if (!selectedType.value) {
      toaster.error('দয়া করে একটি মারকাজ টাইপ নির্বাচন করুন');
      return;
    }

    let askingMadrasha = '';
    let selectedMadrashaId = '';

    if (selectedType.value === 'darsiyat') {
      askingMadrasha = searchDarsiyat.value;
      selectedMadrashaId = searchResults.value.selectedDarsiyat?.id?.toString() || '';
    } else if (selectedType.value === 'hifz') {
      askingMadrasha = searchHifz.value;
      selectedMadrashaId = searchResults.value.selectedHifz?.id?.toString() || '';
    } else if (selectedType.value === 'kirat') {
      askingMadrasha = searchKirat.value;
      selectedMadrashaId = searchResults.value.selectedKirat?.id?.toString() || '';
    }

    if (!askingMadrasha) {
      toaster.error('দয়া করে একটি কাঙ্খিত মারকাজ নির্বাচন করুন');
      return;
    }

    if (!files.value[selectedType.value].noc || !files.value[selectedType.value].consent) {
      toaster.error('দয়া করে সকল প্রয়োজনীয় ফাইল আপলোড করুন');
      return;
    }

    markazForm.markaz_type = selectedType.value;
    markazForm.asking_madrasha = askingMadrasha;
    markazForm.markaz_id = selectedMadrashaId;
    markazForm.onapotti_potro = files.value[selectedType.value].noc;
    markazForm.shommoti_potro = files.value[selectedType.value].consent;

    markazForm.post('/markaz-exchange', {
      onSuccess: (res) => {
        toaster.success(res.data?.message || 'আবেদন সফলভাবে জমা হয়েছে');
        resetForm();
      },
      onError: (err) => {
        console.error(err);
        toaster.error('আবেদন জমা দেওয়ার সময় একটি সমস্যা হয়েছে।');
      },
      forceFormData: true
    });
  } else {
    toaster.info('বর্তমান মারকাজ পরিবর্তন করতে "পরিবর্তন করুন" বাটনে ক্লিক করুন।');
  }
};

// Reset form
const resetForm = () => {
  searchDarsiyat.value = '';
  searchHifz.value = '';
  searchKirat.value = '';
  selectedType.value = '';
  searchResults.value.selectedDarsiyat = null;
  searchResults.value.selectedHifz = null;
  searchResults.value.selectedKirat = null;
  files.value = {
    darsiyat: { noc: null, consent: null },
    hifz: { noc: null, consent: null },
    kirat: { noc: null, consent: null }
  };
  fetchCenters();
};
</script>


<template>
  <AdminLayout>
    <div
    style="font-family: 'SolaimanLipi', sans-serif;"

    class="py-12">
      <div class="sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
          <div class="p-6 bg-white border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-800 mb-6">মারকাজ পরিবর্তন</h2>

            <!-- Centers Information -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-gray-700 mb-3">বর্তমান মারকাজসমূহ</h3>
              <div class="space-y-3">
                <div v-if="centers.darsiyat" class="flex justify-between items-center bg-gray-50 p-3 rounded-md">
                  <span class="text-gray-800">
                    <span class="font-semibold">দরসিয়াত:</span><br> {{ centers.darsiyat }}
                  </span>
                  <button @click="openModal('darsiyat')" class="px-3 py-1 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition">
                    পরিবর্তন করুন
                  </button>
                </div>
                <div v-if="centers.hifz" class="flex justify-between items-center bg-gray-50 p-3 rounded-md">
                  <span class="text-gray-800">
                    <span class="font-semibold">হিফজ:</span><br> {{ centers.hifz }}
                  </span>
                  <button @click="openModal('hifz')" class="px-3 py-1 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition">
                    পরিবর্তন করুন
                  </button>
                </div>
                <div v-if="centers.kirat" class="flex justify-between items-center bg-gray-50 p-3 rounded-md">
                  <span class="text-gray-800">
                    <span class="font-semibold">কিরাত:</span><br> {{ centers.kirat }}
                  </span>
                  <button @click="openModal('kirat')" class="px-3 py-1 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition">
                    পরিবর্তন করুন
                  </button>
                </div>
                <div v-if="!Object.keys(centers).length" class="text-gray-500 italic">
                  <div class="mb-4">কোন মারকাজ পাওয়া যায়নি</div>
                  <!-- Radio buttons for users without any markaz -->
                  <div class="space-y-2">
                    <div class="flex items-center">
                      <input id="darsiyat-radio" type="radio" v-model="selectedType" value="darsiyat" class="w-4 h-4 text-indigo-600 focus:ring-indigo-500">
                      <label for="darsiyat-radio" class="ml-2 text-gray-700">দারসিয়াত মারকাজ</label>
                    </div>
                    <div class="flex items-center">
                      <input id="hifz-radio" type="radio" v-model="selectedType" value="hifz" class="w-4 h-4 text-indigo-600 focus:ring-indigo-500">
                      <label for="hifz-radio" class="ml-2 text-gray-700">হিফজ মারকাজ</label>
                    </div>
                    <div class="flex items-center">
                      <input id="kirat-radio" type="radio" v-model="selectedType" value="kirat" class="w-4 h-4 text-indigo-600 focus:ring-indigo-500">
                      <label for="kirat-radio" class="ml-2 text-gray-700">কিরাত মারকাজ</label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Desired Centers by Type -->
            <div class="space-y-6">
              <!-- Darsiyat Section -->
              <div v-if="!centers.darsiyat || selectedType === 'darsiyat'" class="border border-gray-200 rounded-md p-4">
                <h3 class="text-lg font-medium text-gray-700 mb-3">কাঙ্খিত দারসিয়াত মারকাজ</h3>
                <div class="relative mb-4">
                  <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                  </div>
                  <input
                    type="text"
                    placeholder="দারসিয়াত মাদরাসা সার্চ করুন..."
                    class="w-full pl-10 px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    v-model="searchDarsiyat"
                  >
                  <!-- Dropdown results -->
                  <div v-if="searchDarsiyat && searchResults.darsiyat.length" class="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg">
                    <ul class="max-h-60 overflow-y-auto">
                      <li v-for="(result, index) in searchResults.darsiyat" :key="index"
                          class="px-4 py-2 hover:bg-gray-50 cursor-pointer"
                          @click="selectCenter('darsiyat', result)">
                        {{ result.name }} ({{ result.ElhaqNo }})
                      </li>
                    </ul>
                  </div>
                </div>

                <!-- Attachments for Darsiyat -->
                <div class="space-y-4">
                  <div class="relative">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      বর্তমান মারকাজ অনাপত্তিপত্র
                    </label>
                    <input
                      type="file"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      @change="handleFileChange($event, 'darsiyat', 'noc')"
                      v-if="!files.darsiyat.noc"
                    />
                    <div v-if="!files.darsiyat.noc" class="flex items-center justify-center w-full px-4 py-2 bg-white border-2 border-dashed border-gray-300 rounded-md hover:border-indigo-500">
                      <svg class="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                      </svg>
                      <span class="text-gray-600">ফাইল আপলোড করুন</span>
                    </div>
                    <!-- ফাইল আপলোড হলে দেখাবে -->
                    <div v-else class="flex items-center justify-between w-full px-4 py-2 bg-white border border-gray-300 rounded-md">
                      <div class="flex items-center">
                        <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        <span class="text-gray-700 truncate">{{ files.darsiyat.noc.name }}</span>
                      </div>
                      <div class="flex space-x-2">
                        <button type="button" @click="viewFile(files.darsiyat.noc)" class="text-blue-500 hover:text-blue-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                        </button>
                        <button type="button" @click="removeFile('darsiyat', 'noc')" class="text-red-500 hover:text-red-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>

                  <div class="relative">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      কাঙ্খিত মারকাজ সম্মতিপত্র
                    </label>
                    <input
                      type="file"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      @change="handleFileChange($event, 'darsiyat', 'consent')"
                      v-if="!files.darsiyat.consent"
                    />
                    <div v-if="!files.darsiyat.consent" class="flex items-center justify-center w-full px-4 py-2 bg-white border-2 border-dashed border-gray-300 rounded-md hover:border-indigo-500">
                      <svg class="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                      </svg>
                      <span class="text-gray-600">ফাইল আপলোড করুন</span>
                    </div>
                    <!-- ফাইল আপলোড হলে দেখাবে -->
                    <div v-else class="flex items-center justify-between w-full px-4 py-2 bg-white border border-gray-300 rounded-md">
                      <div class="flex items-center">
                        <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        <span class="text-gray-700 truncate">{{ files.darsiyat.consent.name }}</span>
                      </div>
                      <div class="flex space-x-2">
                        <button type="button" @click="viewFile(files.darsiyat.consent)" class="text-blue-500 hover:text-blue-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                        </button>
                        <button type="button" @click="removeFile('darsiyat', 'consent')" class="text-red-500 hover:text-red-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Selected Darsiyat Center -->
                <div v-if="searchResults.selectedDarsiyat" class="mt-4 p-3 bg-gray-50 rounded-md">
                  <h4 class="font-medium text-gray-700 mb-2">নির্বাচিত মারকাজ</h4>
                  <p class="text-gray-800">{{ searchResults.selectedDarsiyat.name }}</p>
                  <p class="text-gray-600 text-sm">ইলহাক নং: {{ searchResults.selectedDarsiyat.ElhaqNo }}</p>
                </div>
              </div>

              <!-- Hifz Section -->
              <div v-if="!centers.hifz || selectedType === 'hifz'" class="border border-gray-200 rounded-md p-4">
                <h3 class="text-lg font-medium text-gray-700 mb-3">কাঙ্খিত হিফজ মারকাজ</h3>
                <div class="relative mb-4">
                  <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                  </div>
                  <input
                    type="text"
                    placeholder="হিফজ মাদরাসা সার্চ করুন..."
                    class="w-full pl-10 px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    v-model="searchHifz"
                  >
                  <!-- Dropdown results -->
                  <div v-if="searchHifz && searchResults.hifz.length" class="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg">
                    <ul class="max-h-60 overflow-y-auto">
                      <li v-for="(result, index) in searchResults.hifz" :key="index"
                          class="px-4 py-2 hover:bg-gray-50 cursor-pointer"
                          @click="selectCenter('hifz', result)">
                        {{ result.name }} ({{ result.ElhaqNo }})
                      </li>
                    </ul>
                  </div>
                </div>

                <!-- Attachments for Hifz -->
                <div class="space-y-4">
                  <div class="relative">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      বর্তমান মারকাজ অনাপত্তিপত্র
                    </label>
                    <input
                      type="file"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      @change="handleFileChange($event, 'hifz', 'noc')"
                      v-if="!files.hifz.noc"
                    />
                    <div v-if="!files.hifz.noc" class="flex items-center justify-center w-full px-4 py-2 bg-white border-2 border-dashed border-gray-300 rounded-md hover:border-indigo-500">
                      <svg class="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                      </svg>
                      <span class="text-gray-600">ফাইল আপলোড করুন</span>
                    </div>
                    <!-- ফাইল আপলোড হলে দেখাবে -->
                    <div v-else class="flex items-center justify-between w-full px-4 py-2 bg-white border border-gray-300 rounded-md">
                      <div class="flex items-center">
                        <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        <span class="text-gray-700 truncate">{{ files.hifz.noc.name }}</span>
                      </div>
                      <div class="flex space-x-2">
                        <button type="button" @click="viewFile(files.hifz.noc)" class="text-blue-500 hover:text-blue-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                        </button>
                        <button type="button" @click="removeFile('hifz', 'noc')" class="text-red-500 hover:text-red-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>

                  <div class="relative">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      কাঙ্খিত মারকাজ সম্মতিপত্র
                    </label>
                    <input
                      type="file"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      @change="handleFileChange($event, 'hifz', 'consent')"
                      v-if="!files.hifz.consent"
                    />
                    <div v-if="!files.hifz.consent" class="flex items-center justify-center w-full px-4 py-2 bg-white border-2 border-dashed border-gray-300 rounded-md hover:border-indigo-500">
                      <svg class="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                      </svg>
                      <span class="text-gray-600">ফাইল আপলোড করুন</span>
                    </div>
                    <!-- ফাইল আপলোড হলে দেখাবে -->
                    <div v-else class="flex items-center justify-between w-full px-4 py-2 bg-white border border-gray-300 rounded-md">
                      <div class="flex items-center">
                        <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        <span class="text-gray-700 truncate">{{ files.hifz.consent.name }}</span>
                      </div>
                      <div class="flex space-x-2">
                        <button type="button" @click="viewFile(files.hifz.consent)" class="text-blue-500 hover:text-blue-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                        </button>
                        <button type="button" @click="removeFile('hifz', 'consent')" class="text-red-500 hover:text-red-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Selected Hifz Center -->
                <div v-if="searchResults.selectedHifz" class="mt-4 p-3 bg-gray-50 rounded-md">
                  <h4 class="font-medium text-gray-700 mb-2">নির্বাচিত মারকাজ</h4>
                  <p class="text-gray-800">{{ searchResults.selectedHifz.name }}</p>
                  <p class="text-gray-600 text-sm">ইলহাক নং: {{ searchResults.selectedHifz.ElhaqNo }}</p>
                </div>
              </div>

              <!-- Kirat Section -->
              <div v-if="!centers.kirat || selectedType === 'kirat'" class="border border-gray-200 rounded-md p-4">
                <h3 class="text-lg font-medium text-gray-700 mb-3">কাঙ্খিত কিরাত মারকাজ</h3>
                <div class="relative mb-4">
                  <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                  </div>
                  <input
                    type="text"
                    placeholder="কিরাত মাদরাসা সার্চ করুন..."
                    class="w-full pl-10 px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    v-model="searchKirat"
                  >
                  <!-- Dropdown results -->
                  <div v-if="searchKirat && searchResults.kirat.length" class="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg">
                    <ul class="max-h-60 overflow-y-auto">
                      <li v-for="(result, index) in searchResults.kirat" :key="index"
                          class="px-4 py-2 hover:bg-gray-50 cursor-pointer"
                          @click="selectCenter('kirat', result)">
                        {{ result.name }} ({{ result.ElhaqNo }})
                      </li>
                    </ul>
                  </div>
                </div>

                <!-- Attachments for Kirat -->
                <div class="space-y-4">
                  <div class="relative">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      বর্তমান মারকাজ অনাপত্তিপত্র
                    </label>
                    <input
                      type="file"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      @change="handleFileChange($event, 'kirat', 'noc')"
                      v-if="!files.kirat.noc"
                    />
                    <div v-if="!files.kirat.noc" class="flex items-center justify-center w-full px-4 py-2 bg-white border-2 border-dashed border-gray-300 rounded-md hover:border-indigo-500">
                      <svg class="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                      </svg>
                      <span class="text-gray-600">ফাইল আপলোড করুন</span>
                    </div>
                    <!-- ফাইল আপলোড হলে দেখাবে -->
                    <div v-else class="flex items-center justify-between w-full px-4 py-2 bg-white border border-gray-300 rounded-md">
                      <div class="flex items-center">
                        <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        <span class="text-gray-700 truncate">{{ files.kirat.noc.name }}</span>
                      </div>
                      <div class="flex space-x-2">
                        <button type="button" @click="viewFile(files.kirat.noc)" class="text-blue-500 hover:text-blue-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 616 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                        </button>
                        <button type="button" @click="removeFile('kirat', 'noc')" class="text-red-500 hover:text-red-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>

                  <div class="relative">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      কাঙ্খিত মারকাজ সম্মতিপত্র
                    </label>
                    <input
                      type="file"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      @change="handleFileChange($event, 'kirat', 'consent')"
                      v-if="!files.kirat.consent"
                    />
                    <div v-if="!files.kirat.consent" class="flex items-center justify-center w-full px-4 py-2 bg-white border-2 border-dashed border-gray-300 rounded-md hover:border-indigo-500">
                      <svg class="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                      </svg>
                      <span class="text-gray-600">ফাইল আপলোড করুন</span>
                    </div>
                    <!-- ফাইল আপলোড হলে দেখাবে -->
                    <div v-else class="flex items-center justify-between w-full px-4 py-2 bg-white border border-gray-300 rounded-md">
                      <div class="flex items-center">
                        <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        <span class="text-gray-700 truncate">{{ files.kirat.consent.name }}</span>
                      </div>
                      <div class="flex space-x-2">
                        <button type="button" @click="viewFile(files.kirat.consent)" class="text-blue-500 hover:text-blue-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                        </button>
                        <button type="button" @click="removeFile('kirat', 'consent')" class="text-red-500 hover:text-red-700">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Selected Kirat Center -->
                <div v-if="searchResults.selectedKirat" class="mt-4 p-3 bg-gray-50 rounded-md">
                  <h4 class="font-medium text-gray-700 mb-2">নির্বাচিত মারকাজ</h4>
                  <p class="text-gray-800">{{ searchResults.selectedKirat.name }}</p>
                  <p class="text-gray-600 text-sm">ইলহাক নং: {{ searchResults.selectedKirat.ElhaqNo }}</p>
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="mt-8">
              <button
                @click="submitMarkazChange"
                class="w-full px-4 py-2 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition"
              >
                আবেদন জমা দিন
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for changing markaz -->
    <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <!-- Background overlay -->
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>

        <!-- Modal panel -->
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  {{ modalTitle }}
                </h3>
                <div class="mt-4">
                  <!-- Search input -->
                  <div class="relative mb-4">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                      </svg>
                    </div>
                    <input
                      type="text"
                      placeholder="মাদরাসা সার্চ করুন..."
                      class="w-full pl-10 px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                      v-model="modalSearch"
                    >
                    <!-- Dropdown results -->
                    <div v-if="modalSearch && modalSearchResults.length" class="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg">
                      <ul class="max-h-60 overflow-y-auto">
                        <li v-for="(result, index) in modalSearchResults" :key="index"
                            class="px-4 py-2 hover:bg-gray-50 cursor-pointer"
                            @click="selectModalCenter(result)">
                          {{ result.name }} ({{ result.ElhaqNo }})
                        </li>
                      </ul>
                    </div>
                  </div>

                  <!-- Selected Center -->
                  <div v-if="selectedModalCenterData" class="mb-4 p-3 bg-gray-50 rounded-md">
                    <h4 class="font-medium text-gray-700 mb-2">নির্বাচিত মারকাজ</h4>
                    <p class="text-gray-800">{{ selectedModalCenterData.name }}</p>
                    <p class="text-gray-600 text-sm">ইলহাক নং: {{ selectedModalCenterData.ElhaqNo }}</p>
                  </div>

                  <!-- File uploads -->
                  <div class="space-y-4">
                    <div class="relative">
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        বর্তমান মারকাজ অনাপত্তিপত্র
                      </label>
                      <input
                        type="file"
                        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        @change="handleModalFileChange($event, 'noc')"
                        v-if="!modalFiles.noc"
                      />
                      <div v-if="!modalFiles.noc" class="flex items-center justify-center w-full px-4 py-2 bg-white border-2 border-dashed border-gray-300 rounded-md hover:border-indigo-500">
                        <svg class="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                        <span class="text-gray-600">ফাইল আপলোড করুন</span>
                      </div>
                      <!-- File preview -->
                      <div v-else class="flex items-center justify-between w-full px-4 py-2 bg-white border border-gray-300 rounded-md">
                        <div class="flex items-center">
                          <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                          </svg>
                          <span class="text-gray-700 truncate">{{ modalFiles.noc.name }}</span>
                        </div>
                        <div class="flex space-x-2">
                          <button type="button" @click="viewFile(modalFiles.noc)" class="text-blue-500 hover:text-blue-700">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                          </button>
                          <button type="button" @click="removeModalFile('noc')" class="text-red-500 hover:text-red-700">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="relative">
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        কাঙ্খিত মারকাজ সম্মতিপত্র
                      </label>
                      <input
                        type="file"
                        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        @change="handleModalFileChange($event, 'consent')"
                        v-if="!modalFiles.consent"
                      />
                      <div v-if="!modalFiles.consent" class="flex items-center justify-center w-full px-4 py-2 bg-white border-2 border-dashed border-gray-300 rounded-md hover:border-indigo-500">
                        <svg class="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                        <span class="text-gray-600">ফাইল আপলোড করুন</span>
                      </div>
                      <!-- File preview -->
                      <div v-else class="flex items-center justify-between w-full px-4 py-2 bg-white border border-gray-300 rounded-md">
                        <div class="flex items-center">
                          <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                          </svg>
                          <span class="text-gray-700 truncate">{{ modalFiles.consent.name }}</span>
                        </div>
                        <div class="flex space-x-2">
                          <button type="button" @click="viewFile(modalFiles.consent)" class="text-blue-500 hover:text-blue-700">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 616 0z"></path>
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                          </button>
                          <button type="button" @click="removeModalFile('consent')" class="text-red-500 hover:text-red-700">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="saveModalChanges" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm">
              সাবমিট করুন
            </button>
            <button @click="closeModal" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              বাতিল করুন
            </button>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<style scoped>
/* Add any component-specific styles here */
</style>

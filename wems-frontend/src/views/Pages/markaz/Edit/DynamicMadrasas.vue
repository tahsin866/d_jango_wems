<template>
  <div class="mb-6">
    <h3 class="text-xl font-bold text-gray-900 mb-6 flex items-center">
      <i class="fas fa-list-alt mr-2 text-indigo-400"></i>
      আবেদনকৃত মাদরাসায় পরীক্ষা দিতে ইচ্ছুক মাদরাসার তালিকা ও তথ্য
    </h3>
    <div class="space-y-6">
      <div
        v-for="(row, index) in rows"
        :key="index"
        class="bg-white rounded border border-gray-300 shadow mb-4"
      >
        <div class="p-6 border-b border-gray-200">
          <div class="mb-4 w-full">
            <label class="block font-bold text-sm text-gray-700 mb-2">
              <i class="fas fa-search mr-1 text-indigo-400"></i>
              মাদরাসা নির্বাচন করুন <span class="text-red-500">*</span>
            </label>
            <!-- Classic adminLTE search input with dropdown (no PrimeVue) -->
            <div class="relative">
              <input
                type="text"
                v-model="row.searchQuery"
                @input="searchMadrasas({query: row.searchQuery}, index)"
                @focus="preloadSuggestions(index)"
                placeholder="মাদরাসার নাম বা ইলহাক নম্বর দিয়ে খুঁজুন"
                class="w-full px-3 py-2 border border-gray-400 rounded focus:border-indigo-500 focus:ring-indigo-500 shadow text-gray-800 font-bold"
                autocomplete="off"
              />
              <!-- Suggestions dropdown -->
              <div v-if="getSuggestions(index).length && row.searchQuery" class="absolute z-50 left-0 top-full w-full bg-white border border-gray-300 rounded shadow mt-1 max-h-60 overflow-y-auto">
                <div
                  v-for="option in getSuggestions(index)"
                  :key="option.id"
                  @mousedown.prevent="handleMadrasaSelect({ value: option }, row, index)"
                  class="px-4 py-2 cursor-pointer hover:bg-indigo-50 text-sm font-medium flex items-center"
                >
                  <span>{{ option.name }}</span>
                  <span v-if="option.elhaqno" class="ml-2 text-xs text-gray-500">(ইলহাক: {{ option.elhaqno }})</span>
                </div>
                <div v-if="getSuggestions(index).length === 0" class="p-2 text-gray-500">কোন মাদরাসা পাওয়া যায়নি</div>
              </div>
            </div>
            <div v-if="!row.madrasa_id" class="text-sm text-red-500 mt-1">মাদরাসা নির্বাচন করুন</div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Darsiyat Fields -->
            <template v-if="showDarsiyatFields">
              <div class="flex flex-col">
                <label class="block font-bold text-sm text-gray-700 mb-2">ফযীলত <span class="text-red-500">*</span></label>
                <input
                  type="number"
                  v-model="row.fazilat"
                  @input="emitUpdate(row, index)"
                  min="0"
                  placeholder="ছাত্র সংখ্যা লিখুন"
                  class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
                />
                <p v-if="isRequiredFieldEmpty(row, 'fazilat')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
              </div>
              <div class="flex flex-col">
                <label class="block font-bold text-sm text-gray-700 mb-2">সানাবিয়া ‍উলইয়া <span class="text-red-500">*</span></label>
                <input
                  type="number"
                  v-model="row.sanabiya_ulya"
                  @input="emitUpdate(row, index)"
                  min="0"
                  placeholder="ছাত্র সংখ্যা লিখুন"
                  class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
                />
                <p v-if="isRequiredFieldEmpty(row, 'sanabiya_ulya')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
              </div>
              <div class="flex flex-col">
                <label class="block font-bold text-sm text-gray-700 mb-2">সানাবিয়া <span class="text-red-500">*</span></label>
                <input
                  type="number"
                  v-model="row.sanabiya"
                  @input="emitUpdate(row, index)"
                  min="0"
                  placeholder="ছাত্র সংখ্যা লিখুন"
                  class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
                />
                <p v-if="isRequiredFieldEmpty(row, 'sanabiya')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
              </div>
              <div class="flex flex-col">
                <label class="block font-bold text-sm text-gray-700 mb-2">মুতাওয়াসসিতা <span class="text-red-500">*</span></label>
                <input
                  type="number"
                  v-model="row.mutawassita"
                  @input="emitUpdate(row, index)"
                  min="0"
                  placeholder="ছাত্র সংখ্যা লিখুন"
                  class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
                />
                <p v-if="isRequiredFieldEmpty(row, 'mutawassita')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
              </div>
              <div class="flex flex-col">
                <label class="block font-bold text-sm text-gray-700 mb-2">ইবতেদাইয়্যাহ <span class="text-red-500">*</span></label>
                <input
                  type="number"
                  v-model="row.ibtedaiyyah"
                  @input="emitUpdate(row, index)"
                  min="0"
                  placeholder="ছাত্র সংখ্যা লিখুন"
                  class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
                />
                <p v-if="isRequiredFieldEmpty(row, 'ibtedaiyyah')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
              </div>
            </template>
            <!-- Hifzul Quran Field -->
            <div v-if="showHifzField" class="flex flex-col">
              <label class="block font-bold text-sm text-gray-700 mb-2">হিফজুল কোরান <span class="text-red-500">*</span></label>
              <input
                type="number"
                v-model="row.hifzul_quran"
                @input="emitUpdate(row, index)"
                min="0"
                placeholder="ছাত্র সংখ্যা লিখুন"
                class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
              />
              <p v-if="isRequiredFieldEmpty(row, 'hifzul_quran')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
            </div>
            <!-- Kirat Field -->
            <div v-if="showKiratField" class="flex flex-col">
              <label class="block font-bold text-sm text-gray-700 mb-2">ইলমুল কিরআত <span class="text-red-500">*</span></label>
              <input
                type="number"
                v-model="row.qirat"
                @input="emitUpdate(row, index)"
                min="0"
                placeholder="ছাত্র সংখ্যা লিখুন"
                class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
              />
              <p v-if="isRequiredFieldEmpty(row, 'qirat')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
            </div>
            <div v-if="rows.length > 1" class="flex items-end">
              <button
                @click="emit('remove-row', index)"
                type="button"
                class="bg-red-100 hover:bg-red-200 text-red-700 font-bold px-4 py-2 rounded border border-red-300 w-full text-xs flex items-center justify-center"
              >
                <i class="fas fa-trash mr-1"></i> সারি মুছুন
              </button>
            </div>
          </div>

          <!-- File Uploads for NOC & Resolution -->
          <div class="mt-6">
            <h3 class="text-lg font-bold text-gray-900 mb-4 flex items-center">
              <i class="fas fa-file-alt mr-2 text-indigo-400"></i>
              প্রয়োজনীয় ডকুমেন্টস <span class="text-red-500">*</span>
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="border border-gray-300 rounded p-4 bg-gray-50 shadow">
                <div class="flex items-center justify-between mb-2">
                  <label class="block font-bold text-sm text-gray-700">পূর্বের মাদরাসার অনাপত্তিপত্র <span class="text-red-500">*</span></label>
                  <div v-if="row.files.nocPreview" class="flex items-center space-x-2">
                    <a :href="row.files.nocPreview" target="_blank" class="inline-flex items-center px-2 py-1 bg-indigo-50 border border-indigo-200 rounded text-xs text-indigo-700 font-bold">প্রিভিউ</a>
                    <button
                      @click="removeFile('noc', index)"
                      type="button"
                      class="bg-red-100 hover:bg-red-200 text-red-700 font-bold px-3 py-1 rounded border border-red-300 ml-1 text-xs flex items-center"
                    >
                      <i class="fas fa-times mr-1"></i> মুছুন
                    </button>
                  </div>
                </div>
                <input
                  type="file"
                  accept="application/pdf,image/*"
                  @change="e => handleFileSelect(e, 'noc', index)"
                  class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded px-2 py-2"
                />
                <div v-if="!row.files.noc && row.madrasa_id" class="text-sm text-red-500 mt-1">অনাপত্তিপত্র আপলোড করুন</div>
                <div v-if="row.files.nocPreview" class="mt-4">
                  <div class="border rounded bg-white p-2">
                    <div class="flex justify-between items-center mb-2">
                      <span class="text-xs font-bold text-gray-500">প্রিভিউ</span>
                    </div>
                    <img
                      v-if="isImageFile(row.files.noc)"
                      :src="row.files.nocPreview"
                      class="max-h-32 mx-auto object-contain"
                    />
                    <div v-else class="flex items-center justify-center h-32 bg-gray-50 border rounded">
                      <i class="fas fa-file-pdf text-red-500 text-2xl mr-2"></i>
                      <span class="text-xs text-gray-600">PDF ফাইল</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="border border-gray-300 rounded p-4 bg-gray-50 shadow">
                <div class="flex items-center justify-between mb-2">
                  <label class="block font-bold text-sm text-gray-700">বর্তমান মাদরাসার সম্মতিপত্র <span class="text-red-500">*</span></label>
                  <div v-if="row.files.resolutionPreview" class="flex items-center space-x-2">
                    <a :href="row.files.resolutionPreview" target="_blank" class="inline-flex items-center px-2 py-1 bg-indigo-50 border border-indigo-200 rounded text-xs text-indigo-700 font-bold">প্রিভিউ</a>
                    <button
                      @click="removeFile('resolution', index)"
                      type="button"
                      class="bg-red-100 hover:bg-red-200 text-red-700 font-bold px-3 py-1 rounded border border-red-300 ml-1 text-xs flex items-center"
                    >
                      <i class="fas fa-times mr-1"></i> মুছুন
                    </button>
                  </div>
                </div>
                <input
                  type="file"
                  accept="application/pdf,image/*"
                  @change="e => handleFileSelect(e, 'resolution', index)"
                  class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded px-2 py-2"
                />
                <div v-if="!row.files.resolution && row.madrasa_id" class="text-sm text-red-500 mt-1">সম্মতিপত্র আপলোড করুন</div>
                <div v-if="row.files.resolutionPreview" class="mt-4">
                  <div class="border rounded bg-white p-2">
                    <div class="flex justify-between items-center mb-2">
                      <span class="text-xs font-bold text-gray-500">প্রিভিউ</span>
                    </div>
                    <img
                      v-if="isImageFile(row.files.resolution)"
                      :src="row.files.resolutionPreview"
                      class="max-h-32 mx-auto object-contain"
                    />
                    <div v-else class="flex items-center justify-center h-32 bg-gray-50 border rounded">
                      <i class="fas fa-file-pdf text-red-500 text-2xl mr-2"></i>
                      <span class="text-xs text-gray-600">PDF ফাইল</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Add New Row Button -->
      <div>
        <button
          @click="emit('add-row')"
          type="button"
          class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-3 rounded shadow flex items-center"
        >
          <i class="fas fa-plus mr-2"></i> নতুন সারি যোগ করুন
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// Types as before
export interface MadrashaType {
  id?: number | string;
  name?: string;
  elhaqno?: string | number;
}
export interface RowType {
  id?: number | null;
  searchQuery?: string;
  madrasa_id?: number | string | null;
  fazilat?: number | null;
  sanabiya_ulya?: number | null;
  sanabiya?: number | null;
  mutawassita?: number | null;
  ibtedaiyyah?: number | null;
  hifzul_quran?: number | null;
  qirat?: number | null;
  selectedMadrasha?: MadrashaType | null;
  isOpen?: boolean;
  files: {
    noc?: File | null;
    nocPreview?: string | null;
    resolution?: File | null;
    resolutionPreview?: string | null;
  };
}

const props = defineProps<{
  rows: RowType[];
  madrashas: MadrashaType[];
  filteredOptions?: (row: RowType) => MadrashaType[];
  markazType: string;
}>();

const emit = defineEmits<{
  (e: 'add-row'): void;
  (e: 'remove-row', index: number): void;
  (e: 'file-upload', file: File, type: 'noc' | 'resolution', index: number): void;
  (e: 'remove-file', type: 'noc' | 'resolution', index: number): void;
  (e: 'select-option', madrasha: MadrashaType, row: RowType): void;
  (e: 'update-row', row: RowType, index: number): void;
}>();

const showDarsiyatFields = computed(() => props.markazType === 'দরসিয়াত');
const showHifzField = computed(() => props.markazType === 'তাহফিজুল কোরআন');
const showKiratField = computed(() => props.markazType === 'কিরাআত');

const suggestionCache = ref<{ [key: number]: MadrashaType[] }>({});
const isLoading = ref<{ [key: number]: boolean }>({});

async function searchMadrasas(event: any, index: number) {
  const query = (event?.query ?? '').toString().trim();
  if (!query) {
    suggestionCache.value[index] = [];
    return;
  }
  isLoading.value[index] = true;
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/markaz/search-madrasa/?elhaq=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    const suggestions: MadrashaType[] = Array.isArray(data) ? data.map((item: any) => ({
      id: item.id || '',
      name: item.mname || '',
      elhaqno: item.elhaqno ? item.elhaqno.toString() : null
    })).filter(item => item.name) : [];
    suggestionCache.value[index] = suggestions;
  } catch (error) {
    console.error('Search error:', error);
    suggestionCache.value[index] = [];
  } finally {
    isLoading.value[index] = false;
  }
}
function getSuggestions(index: number): MadrashaType[] {
  if (props.filteredOptions) {
    return props.filteredOptions(props.rows[index]);
  }
  return suggestionCache.value[index] || [];
}
function preloadSuggestions(index: number) {
  suggestionCache.value[index] = [];
}
function handleMadrasaSelect(evt: any, row: RowType, index: number) {
  const selectedMadrasha = evt.value as MadrashaType;
  row.searchQuery = selectedMadrasha.name || '';
  row.madrasa_id = selectedMadrasha.id;
  row.madrasa_Name = selectedMadrasha.name || '';
  row.selectedMadrasha = { ...selectedMadrasha, name: selectedMadrasha.name || '' };
  suggestionCache.value[index] = [];
  emit('select-option', { ...selectedMadrasha, name: selectedMadrasha.name || '' }, row);
  emit('update-row', row, index);
}
function handleFileSelect(event: any, type: 'noc' | 'resolution', index: number) {
  let file: File | null = null;
  if (event instanceof File) file = event;
  else if (event?.files?.length > 0) file = event.files[0];
  else if (event?.target?.files?.length > 0) file = event.target.files[0];
  else if (event?.originalEvent?.target?.files?.length > 0) file = event.originalEvent.target.files[0];
  if (file) {
    emit('file-upload', file, type, index);
    emit('update-row', props.rows[index], index);
  }
}
function removeFile(type: 'noc' | 'resolution', index: number) {
  emit('remove-file', type, index);
  emit('update-row', props.rows[index], index);
}
function emitUpdate(row: RowType, index: number) {
  emit('update-row', row, index);
}
type RequiredFieldName = 'fazilat' | 'sanabiya_ulya' | 'sanabiya' | 'mutawassita' | 'ibtedaiyyah' | 'hifzul_quran' | 'qirat';
function isRequiredFieldEmpty(row: RowType, field: RequiredFieldName): boolean {
  if (!row.madrasa_id) return false;
  const markazType = props.markazType;
  const value = (row as any)[field];
  if (markazType === 'দরসিয়াত') {
    const required: RequiredFieldName[] = ['fazilat', 'sanabiya_ulya', 'sanabiya', 'mutawassita', 'ibtedaiyyah'];
    if (required.includes(field)) {
      return !value || value === 0;
    }
  }
  if (markazType === 'তাহফিজুল কোরআন' && field === 'hifzul_quran') {
    return !value || value === 0;
  }
  if (markazType === 'কিরাআত' && field === 'qirat') {
    return !value || value === 0;
  }
  return false;
}
function isImageFile(file: any) {
  if (!file) return false;
  return ['image/jpeg', 'image/png', 'image/jpg'].includes(file.type);
}
</script>

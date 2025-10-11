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
            <!-- Search Type Toggle -->
            <div class="mb-2 flex items-center space-x-4">
              <label class="flex items-center cursor-pointer">
                <input
                  type="radio"
                  :value="true"
                  v-model="row.exactSearch"
                  class="mr-2 text-indigo-600 focus:ring-indigo-500"
                  @change="() => {suggestionCache.value[index] = []; if (row.searchQuery.trim()) debouncedSearchMadrasas({query: row.searchQuery}, index, row.exactSearch);}"
                />
                <span class="text-sm font-medium text-gray-700">সঠিক মিলান (Exact)</span>
              </label>
              <label class="flex items-center cursor-pointer">
                <input
                  type="radio"
                  :value="false"
                  v-model="row.exactSearch"
                  class="mr-2 text-indigo-600 focus:ring-indigo-500"
                  @change="() => {suggestionCache.value[index] = []; if (row.searchQuery.trim()) debouncedSearchMadrasas({query: row.searchQuery}, index, row.exactSearch);}"
                />
                <span class="text-sm font-medium text-gray-700">আংশিক মিলান (Partial)</span>
              </label>
              <span class="text-xs text-gray-500" v-if="row.exactSearch">
                <i class="fas fa-info-circle mr-1"></i>ইলহাক নম্বর সঠিকভাবে খুঁজুন
              </span>
              <span class="text-xs text-gray-500" v-else>
                <i class="fas fa-info-circle mr-1"></i>ইলহাক নম্বরের অংশ দিয়ে খুঁজুন
              </span>
            </div>
            <!-- Classic adminLTE search input with dropdown (no PrimeVue) -->
            <div class="relative">
              <div class="flex items-center">
                <input
                  type="text"
                  v-model="row.searchQuery"
                  @input="debouncedSearchMadrasas({query: row.searchQuery}, index, row.exactSearch)"
                  @focus="() => { preloadSuggestions(index); if (row.madrasa_id) { row.madrasa_id = null; } }"
                  :placeholder="row.exactSearch ? 'ইলহাক নম্বর সঠিকভাবে লিখুন' : 'ইলহাক নম্বরের অংশ দিয়ে খুঁজুন'"
                  :class="[
                    'flex-1 px-3 py-2 border rounded focus:border-indigo-500 focus:ring-indigo-500 shadow font-bold autocomplete-off',
                    row.madrasa_id ? 'bg-green-50 border-green-300 text-green-800' : 'border-gray-400 text-gray-800'
                  ]"
                  autocomplete="off"
                />
                <div v-if="row.madrasa_id" class="absolute right-2 text-green-600">
                  <i class="fas fa-check-circle"></i>
                </div>
              </div>
              <!-- Suggestions dropdown -->
              <div v-if="getSuggestions(index).length && !row.madrasa_id" class="absolute z-50 left-0 top-full w-full bg-white border border-gray-300 rounded shadow mt-1 max-h-60 overflow-y-auto">
                <!-- Loading indicator -->
                <div v-if="isLoading[index] && !row.madrasa_id" class="p-3 text-sm text-gray-600 border-b">
                  <div class="flex items-center justify-center">
                    <i class="fas fa-spinner fa-spin mr-2 text-indigo-500"></i>
                    <span>{{ row.exactSearch ? 'সঠিক মিলান খোঁজা হচ্ছে...' : 'আংশিক মিলান খোঁজা হচ্ছে...' }}</span>
                  </div>
                </div>
                <!-- Search status indicator -->
                <div v-else-if="row.searchQuery && getSuggestions(index).length === 0 && !row.madrasa_id" class="p-3 text-sm text-gray-600 border-b">
                  <div class="flex items-center">
                    <i class="fas fa-search mr-2" :class="row.exactSearch ? 'text-green-500' : 'text-blue-500'"></i>
                    <span>{{ row.exactSearch ? 'সঠিক মিলানে কোন ফলাফল পাওয়া যায়নি' : 'আংশিক মিলানে কোন ফলাফল পাওয়া যায়নি' }}</span>
                  </div>
                  <div class="text-xs text-gray-500 mt-1">
                    {{ row.exactSearch ? 'ইলহাক নম্বরটি সঠিকভাবে লিখুন' : 'ইলহাক নম্বরের আরেকটি অংশ চেষ্টা করুন' }}
                  </div>
                </div>
                <div
                  v-for="option in getSuggestions(index)"
                  :key="option.id"
                  @mousedown.prevent="handleMadrasaSelect({ value: option }, row, index)"
                  class="px-4 py-2 cursor-pointer hover:bg-indigo-50 text-sm font-medium flex items-center border-b last:border-b-0"
                >
                  <div class="flex items-center flex-1">
                    <i class="fas fa-school mr-2 text-indigo-400"></i>
                    <div class="flex-1">
                      <div class="font-medium">{{ option.name }}</div>
                      <div v-if="option.elhaqno" class="text-xs text-gray-500 mt-1">ইলহাক: {{ option.elhaqno }}</div>
                    </div>
                  </div>
                  <div class="flex flex-col items-end">
                    <div v-if="row.exactSearch && option.elhaqno && option.elhaqno.toString().toLowerCase() === row.searchQuery.toLowerCase()" class="mb-1">
                      <span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                        <i class="fas fa-check mr-1"></i>সঠিক মিল
                      </span>
                    </div>
                    <div class="text-xs text-gray-400">
                      {{ row.exactSearch ? 'Exact' : 'Partial' }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="!row.madrasa_id" class="text-sm text-red-500 mt-1 flex items-center">
              <i class="fas fa-exclamation-triangle mr-1"></i>
              অনুগ্রহ করে একটি মাদরাসা নির্বাচন করুন
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Darsiyat Fields -->
            <template v-if="showDarsiyatFields">
              <div class="flex flex-col">
                <label class="block font-bold text-sm text-gray-700 mb-2">ফযীলত <span class="text-red-500">*</span></label>
                <input
                  type="number"
                  v-model="row.fazilat"
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
                      @click="emit('remove-file', 'noc', index)"
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
                      @click="emit('remove-file', 'resolution', index)"
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

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  rows: Array,
  madrashas: Array,
  filteredOptions: Function,
  markazType: String
})

const emit = defineEmits([
  'add-row',
  'remove-row',
  'file-upload',
  'remove-file',
  'select-option'
])

const showDarsiyatFields = computed(() => props.markazType === 'দরসিয়াত')
const showHifzField = computed(() => props.markazType === 'তাহফিজুল কোরআন')
const showKiratField = computed(() => props.markazType === 'কিরাআত')

const suggestionCache = ref({})
const isLoading = ref({})
const abortControllers = ref({})

function debounce(func, delay) {
  let timeoutId
  return function (...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func.apply(this, args), delay)
  }
}

async function searchMadrasas(event, index, exactMatch = true) {
  const query = (event?.query ?? '').toString().trim()

  if (abortControllers.value[index]) {
    abortControllers.value[index].abort()
  }

  if (!query) {
    suggestionCache.value[index] = []
    isLoading.value[index] = false
    return
  }

  isLoading.value[index] = true
  const controller = new AbortController()
  abortControllers.value[index] = controller

  try {
    const exactParam = exactMatch ? 'true' : 'false'
    const response = await fetch(`http://127.0.0.1:8000/api/markaz/search-madrasa/?elhaq=${encodeURIComponent(query)}&exact=${exactParam}`, {
      signal: controller.signal
    })

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

    const data = await response.json()
    const suggestions = Array.isArray(data)
      ? data.map(item => ({
          id: item.school_id || '',
          name: item.mname || '',
          elhaqno: item.elhaqno ? item.elhaqno.toString() : null
        })).filter(item => item.name)
      : []

    if (!controller.signal.aborted) {
      suggestionCache.value[index] = suggestions
    }
  } catch (error) {
    if (error.name !== 'AbortError') {
      if (!controller.signal.aborted) {
        suggestionCache.value[index] = []
      }
    }
  } finally {
    if (!controller.signal.aborted) {
      isLoading.value[index] = false
    }
    delete abortControllers.value[index]
  }
}

const debouncedSearchMadrasas = debounce(searchMadrasas, 300)
function getSuggestions(index) {
  return suggestionCache.value[index] || []
}
function preloadSuggestions(index) {
  suggestionCache.value[index] = []
}
function handleMadrasaSelect(evt, row, index) {
  const selectedMadrasha = evt.value
  row.searchQuery = selectedMadrasha.name || ''
  row.madrasa_id = selectedMadrasha.id
  row.selectedMadrasha = { ...selectedMadrasha, name: selectedMadrasha.name || '' }
  suggestionCache.value[index] = []
  if (abortControllers.value[index]) {
    abortControllers.value[index].abort()
    delete abortControllers.value[index]
  }
  emit('select-option', { ...selectedMadrasha, name: selectedMadrasha.name || '' }, row)
}
function handleFileSelect(event, type, index) {
  let file = null
  if (event instanceof File) file = event
  else if (event?.files?.length > 0) file = event.files[0]
  else if (event?.target?.files?.length > 0) file = event.target.files[0]
  else if (event?.originalEvent?.target?.files?.length > 0) file = event.originalEvent.target.files[0]
  if (file) emit('file-upload', file, type, index)
}
function isRequiredFieldEmpty(row, field) {
  if (!row.madrasa_id) return false
  const markazType = props.markazType
  const value = row[field]
  if (markazType === 'দরসিয়াত') {
    const required = ['fazilat', 'sanabiya_ulya', 'sanabiya', 'mutawassita', 'ibtedaiyyah']
    if (required.includes(field)) {
      return !value || value === 0
    }
  }
  if (markazType === 'তাহফিজুল কোরআন' && field === 'hifzul_quran') {
    return !value || value === 0
  }
  if (markazType === 'কিরাআত' && field === 'qirat') {
    return !value || value === 0
  }
  return false
}
function isImageFile(file) {
  if (!file) return false
  return ['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)
}
</script>

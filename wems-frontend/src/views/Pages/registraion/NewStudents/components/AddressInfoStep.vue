<script setup>
import { ref, watch, defineEmits, defineProps, onMounted, computed } from 'vue'
import InputText from 'primevue/inputtext'
import axios from 'axios'

const emit = defineEmits(['update:modelValue', 'prev', 'next'])
const props = defineProps({
  modelValue: Object,
  boardOptions: Array,
  form: Object
})

// Debug: Log board options when component receives them
watch(() => props.boardOptions, (newVal) => {
  console.log('AddressInfoStep received boardOptions:', newVal)
}, { immediate: true })

// Fallback board options if parent doesn't provide
const fallbackBoardOptions = [
  { id: 1, name: 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ', value: 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ' },
  { id: 2, name: 'বেফাকুল মাদারিসিল কওমিয়া গওহরডাঙ্গা বাংলাদেশ', value: 'বেফাকুল মাদারিসিল কওমিয়া গওহরডাঙ্গা বাংলাদেশ' },
  { id: 3, name: 'আযাদ দ্বীনি এদারায়ে তালীম বাংলাদেশ', value: 'আযাদ দ্বীনি এদারায়ে তালীম বাংলাদেশ' },
  { id: 4, name: 'তানযীমুল মাদারিসিদ দ্বীনিয়া বাংলাদেশ', value: 'তানযীমুল মাদারিসিদ দ্বীনিয়া বাংলাদেশ' },
  { id: 5, name: 'জাতীয় দ্বীনি মাদরাসা শিক্ষাবোর্ড বাংলাদেশ', value: 'জাতীয় দ্বীনি মাদরাসা শিক্ষাবোর্ড বাংলাদেশ' },
  { id: 6, name: 'আঞ্জুমানে ইত্তেহাদুল মাদারিস বাংলাদেশ', value: 'আঞ্জুমানে ইত্তেহাদুল মাদারিস বাংলাদেশ' }
]

// Computed property for board options with fallback
const availableBoardOptions = computed(() => {
  return props.boardOptions && props.boardOptions.length > 0 ? props.boardOptions : fallbackBoardOptions
})

// Local reactive copies for v-model
const localForm = ref({
  board_name: '',
  board_year: ''
})

// Watch for changes and emit updates
watch(localForm, (newVal) => {
  emit('update:modelValue', { ...props.modelValue, ...newVal })
}, { deep: true })

// Watch for external changes to modelValue
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    localForm.value.board_name = newVal.board_name || ''
    localForm.value.board_year = newVal.board_year || ''
  }
}, { immediate: true })

const divisions = ref([])
const districts = ref([])
const thanas = ref([])

const addressFilters = ref({
  division: '',
  district: '',
  Thana: ''
})

// Board year options
const years = [
  { label: '২০২৫', value: '2025' },
  { label: '২০২৪', value: '2024' },
  { label: '২০২৩', value: '2023' },
  { label: '২০২২', value: '2022' },
  { label: '২০২১', value: '2021' },
  { label: '২০২০', value: '2020' },
  { label: '২০১৯', value: '2019' },
  { label: '২০১৮', value: '2018' },
  { label: '২০১৭', value: '2017' },
  { label: '২০১৬', value: '2016' },
  { label: '২০১৫', value: '2015' },
  { label: '২০১৪', value: '2014' },
  { label: '২০১৩', value: '2013' },
  { label: '২০১২', value: '2012' },
  { label: '২০১১', value: '2011' }
]


const isNonBefaqBoard = ref(false)
watch(() => localForm.value.board_name, (val) => {
  isNonBefaqBoard.value = !!val && val !== 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ'
})

onMounted(async () => {
  await loadDivisions()
})

const loadDivisions = async () => {
  try {
    const response = await axios.get('/api/admin/madrasha/divisions/')
    divisions.value = response.data.results || response.data
    return true
  } catch {
    return false
  }
}

const handleDivisionChange = async () => {
  addressFilters.value.district = ''
  addressFilters.value.Thana = ''
  districts.value = []
  thanas.value = []
  if (!addressFilters.value.division) return
  try {
    const response = await axios.get(`/api/admin/madrasha/districts/?did=${addressFilters.value.division}`)
    districts.value = response.data.results || response.data
  } catch {
    // Handle error silently
  }
}

const handleDistrictChange = async () => {
  addressFilters.value.Thana = ''
  thanas.value = []
  if (!addressFilters.value.district) return
  try {
    const response = await axios.get(`/api/admin/madrasha/thanas/?district_id=${addressFilters.value.district}`)
    thanas.value = response.data.results || response.data
    thanas.value = response.data
  } catch {
    // Handle error silently
  }
}

// File attachment for non-Befaq board
const handleExtraAttachment = (event) => {
  const file = event.target.files[0]
  const updatedForm = { ...props.modelValue, extraAttachment: file }
  emit('update:modelValue', updatedForm)
}

// Update modelValue when address fields are changed
watch(addressFilters, () => {
  const updatedForm = { ...props.modelValue }

  if (addressFilters.value.division) {
    const selectedDivision = divisions.value.find(d => d.did == addressFilters.value.division)
    if (selectedDivision) {
      updatedForm.division_name = selectedDivision.division
      updatedForm.division_id = selectedDivision.did
    }
  }
  if (addressFilters.value.district) {
    const selectedDistrict = districts.value.find(d => d.desid == addressFilters.value.district)
    if (selectedDistrict) {
      updatedForm.district_name = selectedDistrict.district
      updatedForm.district_id = selectedDistrict.desid
    }
  }
  if (addressFilters.value.Thana) {
    const selectedThana = thanas.value.find(t => t.thana_id == addressFilters.value.Thana)
    if (selectedThana) {
      updatedForm.thana_name = selectedThana.thana
      updatedForm.thana_id = selectedThana.thana_id
    }
  }
  emit('update:modelValue', updatedForm)
}, { deep: true })</script>

<template>
  <div>
    <div
      style="font-family: 'SolaimanLipi', sans-serif;"
      class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-6">
      <div class="p-6 bg-white border-b border-gray-200">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight mb-4">প্রয়োজনীয় তথ্য</h2>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">পরীক্ষার্থীর ধরন</label>
            <InputText value="নিয়মিত" disabled class="w-full mt-1 bg-gray-100" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">বোর্ড</label>
            <!-- Debug info -->
            <!-- <div class="text-xs text-gray-500 mb-1">
              Board Options Count: {{ availableBoardOptions.length }}
            </div> -->
            <select
              v-model="localForm.board_name"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-gray-50"
            >
              <option value="">বোর্ড নির্বাচন করুন</option>
              <option v-for="board in availableBoardOptions" :key="board.id" :value="board.value">
                {{ board.name }}
              </option>
            </select>
          </div>
        </div>
        <!-- Non Befaq Board হলে বছর ফিল্ড দেখাও -->
        <div v-if="isNonBefaqBoard" class="mt-6">
          <label class="block font-medium text-sm text-gray-700">বছর নির্বাচন করুন</label>
          <select
            v-model="localForm.board_year"
            class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-gray-50"
          >
            <option value="">বছর নির্বাচন করুন</option>
            <option v-for="year in years" :key="year.value" :value="year.value">
              {{ year.label }}
            </option>
          </select>
        </div>
        <!-- Non Befaq Board হলে এটাচমেন্ট ফিল্ড দেখাও -->
        <div v-if="isNonBefaqBoard" class="mt-6">
          <label class="block font-medium text-sm text-gray-700">অতিরিক্ত সংযুক্তি (Non-Befaq বোর্ডের জন্য)</label>
          <input type="file" @change="handleExtraAttachment" class="w-full mt-1" />
        </div>
      </div>
    </div>

    <!-- ঠিকানা -->
    <div class="bg-white border border-gray-200 rounded-sm shadow-md">
      <div class="bg-gradient-to-r from-gray-700 to-gray-600 px-6 py-4 relative">
        <div class="flex justify-between items-center relative z-10">
          <div class="flex gap-4 items-center">
            <div class="p-2 rounded-sm bg-white bg-opacity-20 backdrop-blur-sm">
              <i class="text-2xl text-white fa-home"></i>
            </div>
            <h5 class="text-white text-xl font-bold tracking-wide">
              ঠিকানার তথ্য
            </h5>
          </div>
        </div>
      </div>
      <div class="p-6 bg-gray-50 overflow-visible">
        <div class="grid grid-cols-1 gap-6 overflow-visible">
          <!-- Address Section -->
          <label class="block text-base font-medium text-gray-700 mb-1">বিভাগ</label>
          <select
            v-model="addressFilters.division"
            :disabled="!divisions.length"
            @change="handleDivisionChange"
            class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 bg-gray-50"
          >
            <option value="">সকল বিভাগ</option>
            <option v-for="division in divisions" :key="division.did" :value="division.did">{{ division.division }}</option>
          </select>
          <span v-if="!divisions.length" class="text-md text-gray-500">Loading divisions...</span>

          <label class="block text-base font-medium text-gray-700 mb-1 mt-4">জেলা</label>
          <select
            v-model="addressFilters.district"
            :disabled="!addressFilters.division || !districts.length"
            @change="handleDistrictChange"
            class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 bg-gray-50"
          >
            <option value="">সকল জেলা</option>
            <option v-for="district in districts" :key="district.desid" :value="district.desid">
              {{ district.district }}
            </option>
          </select>
          <span v-if="addressFilters.division && !districts.length" class="text-md text-gray-500">Loading districts...</span>
          <span v-else-if="!addressFilters.division && divisions.length > 0" class="text-md text-gray-500">বিভাগ নির্বাচন করুন</span>

          <label class="block text-base font-medium text-gray-700 mb-1 mt-4">থানা/উপজিলা</label>
          <select
            v-model="addressFilters.Thana"
            :disabled="!addressFilters.district || !thanas.length"
            class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 bg-gray-50"
          >
            <option value="">সকল থানা</option>
            <option v-for="thana in thanas" :key="thana.thana_id" :value="thana.thana_id">{{ thana.thana }}</option>
          </select>
          <span v-if="addressFilters.district && !thanas.length" class="text-md text-gray-500">Loading thanas...</span>
          <span v-else-if="!addressFilters.district && districts.length > 0" class="text-md text-gray-500">জেলা নির্বাচন করুন</span>
        </div>
      </div>
    </div>
    <div class="flex justify-between mt-6">
      <button type="button" @click="emit('prev')" class="inline-flex items-center px-4 py-2 bg-gray-300 border border-transparent rounded-md font-semibold text-xs text-gray-800 uppercase tracking-widest hover:bg-gray-400">
        আগের ধাপ
      </button>
      <button type="button" @click="emit('next')" class="inline-flex items-center px-4 py-2 bg-gray-800 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-gray-700">
        পরবর্তী ধাপ
      </button>
    </div>
  </div>
</template>

<style scoped>
.transition-colors {
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}
.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.rounded-sm {
  border-radius: 0.125rem;
}
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
/* Custom select styling */
select {
  background-image: none;
  max-height: none !important;
  overflow-y: visible !important;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

/* Browser-specific dropdown fixes */
select::-ms-expand {
  display: none;
}

/* Fix dropdown options visibility */
select option {
  padding: 8px 12px;
  background-color: white;
  color: #374151;
  border: none;
  font-size: 16px;
  line-height: 1.5;
}

select option:hover {
  background-color: #f3f4f6;
}

select option:checked {
  background-color: #e5e7eb;
  font-weight: 600;
}

/* Ensure dropdown appears above other elements */
.relative select {
  position: relative;
  z-index: 50;
}

/* Fix for dropdown size and visibility */
select {
  min-height: 48px;
  line-height: 1.5;
}

/* Container overflow fixes */
.overflow-visible {
  overflow: visible !important;
}

/* Ensure proper stacking context */
.relative.overflow-visible {
  z-index: 1;
}

.relative.overflow-visible:focus-within {
  z-index: 10;
}

/* Disabled state improvements */
select:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
</style>

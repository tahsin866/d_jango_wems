<template>
<<<<<<< HEAD
  <Fieldset legend="ঠিকানার তথ্য" :pt="{
    legend: { className: 'text-xl font-bold text-white bg-gradient-to-r from-gray-700 to-gray-600 px-6 py-4 rounded-t' },
    content: { className: 'p-6 bg-gray-50 overflow-visible' }
  }">
    <template #legend>
      <div class="flex gap-4 items-center">
        <div class="p-2 rounded-sm bg-white bg-opacity-20 backdrop-blur-sm">
          <i class="text-2xl text-white fa-home"></i>
        </div>
        <span class="text-white text-xl font-bold tracking-wide">ঠিকানার তথ্য</span>
      </div>
    </template>

    <div class="grid grid-cols-1 gap-6 overflow-visible">
      <!-- বিভাগ -->
      <div>
        <label for="division" class="block text-base font-medium text-gray-700 mb-2">বিভাগ</label>
        <Dropdown
          id="division"
          v-model="localAddress.division"
          :options="divisions"
          optionLabel="Division"
          optionValue="id"
          placeholder="সকল বিভাগ"
          :disabled="addressLoading.divisions"
          :loading="addressLoading.divisions"
          class="w-full"
          :pt="{
            root: { class: 'w-full' },
            input: { class: 'w-full bg-gray-50 border-gray-300' },
            list: { class: 'z-50' }
          }"
          @change="onDivisionChange"
        />
        <small v-if="addressLoading.divisions" class="text-md text-gray-500 block mt-1">Loading divisions...</small>
      </div>

      <!-- জেলা -->
      <div>
        <label for="district" class="block text-base font-medium text-gray-700 mb-2">জেলা</label>
        <Dropdown
          id="district"
          v-model="localAddress.district"
          :options="districts"
          optionLabel="District"
          optionValue="DesID"
          placeholder="সকল জেলা"
          :disabled="addressLoading.districts || (!localAddress.division && divisions.length > 0)"
          :loading="addressLoading.districts"
          class="w-full"
          :pt="{
            root: { class: 'w-full' },
            input: { class: 'w-full bg-gray-50 border-gray-300' },
            list: { class: 'z-50' }
          }"
          @change="onDistrictChange"
        />
        <small v-if="addressLoading.districts" class="text-md text-gray-500 block mt-1">Loading districts...</small>
        <small v-else-if="!localAddress.division && divisions.length > 0" class="text-md text-gray-500 block mt-1">বিভাগ নির্বাচন করুন</small>
      </div>

      <!-- থানা/উপজিলা -->
      <div>
        <label for="thana" class="block text-base font-medium text-gray-700 mb-2">থানা/উপজিলা</label>
        <Dropdown
          id="thana"
          v-model="localAddress.Thana"
          :options="thanas"
          optionLabel="Thana"
          optionValue="Thana_ID"
          placeholder="সকল থানা"
          :disabled="addressLoading.thanas || (!localAddress.district && districts.length > 0)"
          :loading="addressLoading.thanas"
          class="w-full"
          :pt="{
            root: { class: 'w-full' },
            input: { class: 'w-full bg-gray-50 border-gray-300' },
            list: { class: 'z-50' }
          }"
          @change="onThanaChange"
        />
        <small v-if="addressLoading.thanas" class="text-md text-gray-500 block mt-1">Loading thanas...</small>
        <small v-else-if="!localAddress.district && districts.length > 0" class="text-md text-gray-500 block mt-1">জেলা নির্বাচন করুন</small>
      </div>
    </div>
  </Fieldset>
=======
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
          :value="localAddress.division"
          :disabled="addressLoading.divisions"
          @change="onDivisionChange($event)"
          class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 bg-gray-50"
        >
          <option value="">সকল বিভাগ</option>
          <option v-for="division in divisions" :key="division.id" :value="division.id">{{ division.Division }}</option>
        </select>
        <span v-if="addressLoading.divisions" class="text-md text-gray-500">Loading divisions...</span>

        <label class="block text-base font-medium text-gray-700 mb-1 mt-4">জেলা</label>
        <select
          :value="localAddress.district"
          :disabled="addressLoading.districts || (!localAddress.division && divisions.length > 0)"
          @change="onDistrictChange($event)"
          class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 bg-gray-50"
        >
          <option value="">সকল জেলা</option>
          <option v-for="district in districts" :key="district.DesID" :value="district.DesID">
            {{ district.District }}
          </option>
        </select>
        <span v-if="addressLoading.districts" class="text-md text-gray-500">Loading districts...</span>
        <span v-else-if="!localAddress.division && divisions.length > 0" class="text-md text-gray-500">বিভাগ নির্বাচন করুন</span>

        <label class="block text-base font-medium text-gray-700 mb-1 mt-4">থানা/উপজিলা</label>
        <select
          :value="localAddress.Thana"
          :disabled="addressLoading.thanas || (!localAddress.district && districts.length > 0)"
          @change="onThanaChange($event)"
          class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 bg-gray-50"
        >
          <option value="">সকল থানা</option>
          <option v-for="thana in thanas" :key="thana.Thana_ID" :value="thana.Thana_ID">{{ thana.Thana }}</option>
        </select>
        <span v-if="addressLoading.thanas" class="text-md text-gray-500">Loading thanas...</span>
        <span v-else-if="!localAddress.district && districts.length > 0" class="text-md text-gray-500">জেলা নির্বাচন করুন</span>
      </div>
    </div>
  </div>
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
</template>

<script setup>
import { reactive, watch, computed } from 'vue'
<<<<<<< HEAD
import Dropdown from 'primevue/dropdown'
import Fieldset from 'primevue/fieldset'
=======
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01

// Props
const props = defineProps({
  divisions: Array,
  districts: Array,
  thanas: Array,
  addressFilters: Object,
  studentInfoForm: Object
})

// Emits
const emit = defineEmits(['update:addressFilters'])

// Computed props
const divisions = computed(() => props.divisions ?? [])
const districts = computed(() => props.districts ?? [])
const thanas = computed(() => props.thanas ?? [])
const addressLoading = computed(() => ({
  divisions: false,
  districts: false,
  thanas: false
}))

// Local address state
const localAddress = reactive({
  division: props.addressFilters?.division ?? '',
  district: props.addressFilters?.district ?? '',
  Thana: props.addressFilters?.Thana ?? ''
})

// Sync local state if props change
watch(() => props.addressFilters, (v) => {
  if (!v) return
  localAddress.division = v.division ?? ''
  localAddress.district = v.district ?? ''
  localAddress.Thana = v.Thana ?? ''
}, { deep: true, immediate: true })

<<<<<<< HEAD
// Emit updates when local address changes
watch(localAddress, () => {
  emit('update:addressFilters', { ...localAddress })
}, { deep: true })

// Event handlers
function onDivisionChange(event) {
  // Clear dependent fields when division changes
=======
// Event handlers
function onDivisionChange(event) {
  const value = event.target.value
  localAddress.division = value
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
  localAddress.district = ''
  localAddress.Thana = ''
  emit('update:addressFilters', { ...localAddress })
}

function onDistrictChange(event) {
<<<<<<< HEAD
  // Clear dependent field when district changes
=======
  const value = event.target.value
  localAddress.district = value
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
  localAddress.Thana = ''
  emit('update:addressFilters', { ...localAddress })
}

function onThanaChange(event) {
<<<<<<< HEAD
  // Just emit the updated filters
=======
  const value = event.target.value
  localAddress.Thana = value
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
  emit('update:addressFilters', { ...localAddress })
}
</script>

<style scoped>
<<<<<<< HEAD
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* Ensure proper z-index for dropdown visibility */
:deep(.p-dropdown-list) {
  z-index: 1000 !important;
}

/* Container overflow fixes for dropdown visibility */
.overflow-visible {
  overflow: visible !important;
}
=======
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
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
</style>

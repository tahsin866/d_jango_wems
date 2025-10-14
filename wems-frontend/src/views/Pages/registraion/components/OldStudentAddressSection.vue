<template>
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
</template>

<script setup>
import { reactive, watch, computed } from 'vue'
import Dropdown from 'primevue/dropdown'
import Fieldset from 'primevue/fieldset'

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

// Emit updates when local address changes
watch(localAddress, () => {
  emit('update:addressFilters', { ...localAddress })
}, { deep: true })

// Event handlers
function onDivisionChange(event) {
  // Clear dependent fields when division changes
  localAddress.district = ''
  localAddress.Thana = ''
  emit('update:addressFilters', { ...localAddress })
}

function onDistrictChange(event) {
  // Clear dependent field when district changes
  localAddress.Thana = ''
  emit('update:addressFilters', { ...localAddress })
}

function onThanaChange(event) {
  // Just emit the updated filters
  emit('update:addressFilters', { ...localAddress })
}
</script>

<style scoped>
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
</style>

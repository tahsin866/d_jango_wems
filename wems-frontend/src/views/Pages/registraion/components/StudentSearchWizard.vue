<script setup lang="ts">
import { ref, watch } from 'vue';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';

const props = defineProps(['filters']);
const emit = defineEmits(['update:filters']);
const localFilters = ref(JSON.parse(JSON.stringify(props.filters)));

watch(localFilters, (newVal) => emit('update:filters', newVal), { deep: true });

const marhalOptions = [
  { name: 'ফযীলত', value: 'ফযীলত' },
  { name: 'সানাবিয়া উলিয়া', value: 'সানাবিয়া উলিয়া' },
  { name: 'সানাবিয়া', value: 'সানাবিয়া' },
  { name: 'মুতাওয়াসসিতা', value: 'মুতাওয়াসসিতা' },
  { name: 'ইবতিদাইয়া', value: 'ইবতিদাইয়া' },
  { name: 'তাহফিজুল কুরআন', value: 'তাহফিজুল কুরআন' },
  { name: 'ইলমুত তাজবীদ ওয়াল কিরাআত', value: 'ইলমুত তাজবীদ ওয়াল কিরাআত' },
];

const studentTypeOptions = [
  { name: 'নিয়মিত', value: 'নিয়মিত' },
  { name: 'অনিয়মিত অন্যান্য', value: 'অনিয়মিত অন্যান্য' },
  { name: 'মানউন্নয়ন', value: 'মানউন্নয়ন' },
  { name: 'অনিয়মিত যেমনী', value: 'অনিয়মিত যেমনী' }
];

const paymentStatusOptions = [
  { name: 'পরিশোধিত', value: 'পরিশোধিত' },
  { name: 'অপরিশোধিত', value: 'অপরিশোধিত' }
];

const applicationStatusOptions = [
  { name: 'বোর্ড দাখিল', value: 'বোর্ড দাখিল' },
  { name: 'বোর্ড ফেরত', value: 'বোর্ড ফেরত' },
  { name: 'অনুমোদন', value: 'অনুমোদন' },
  { name: 'পেন্ডিং', value: 'পেন্ডিং' }
];

const resetSearch = () => {
  Object.keys(localFilters.value).forEach(k => localFilters.value[k].value = null)
}
</script>

<template>
  <div
  style="font-family: 'SolaimanLipi', sans-serif;"
  class="overflow-hidden rounded-sm shadow-lg bg-gray-100 mb-8 border border-gray-300">
    <!-- Header -->
    <div class="p-5 bg-gray-800 border-b border-gray-700 flex flex-col md:flex-row md:items-center md:justify-between gap-2">
      <div class="flex items-center gap-3">
        <span class="inline-flex items-center justify-center rounded-sm h-9 w-9 bg-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-300" viewBox="0 0 20 20" fill="currentColor">
            <path d="M9 9a2 2 0 114 0 2 2 0 01-4 0z" />
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a4 4 0 00-3.446 6.032l-2.261 2.26a1 1 0 101.414 1.415l2.261-2.261A4 4 0 1011 5z" clip-rule="evenodd" />
          </svg>
        </span>
        <h3 class="text-gray-100 text-2xl font-bold tracking-tight">সার্চ উইজার্ড</h3>
      </div>
      <div class="flex gap-2 flex-wrap justify-end">
        <button
          class="inline-flex items-center px-4 py-2 bg-gray-700 border border-gray-600 rounded-sm font-semibold text-xs text-gray-100 uppercase tracking-widest shadow hover:bg-gray-600 transition"
        >
          <i class="pi pi-user-plus mr-2" /> নিবন্ধন করুন
        </button>
        <button
          class="inline-flex items-center px-4 py-2 bg-gray-600 border border-gray-500 rounded-sm font-semibold text-xs text-gray-100 uppercase tracking-widest shadow hover:bg-gray-500 transition"
        >
          <i class="pi pi-file-import mr-2" /> ইম্পোর্ট করুন
        </button>
      </div>
    </div>
    <!-- Filters -->
    <div class="p-7 bg-gray-100">
      <div class="grid grid-cols-1 md:grid-cols-5 gap-5 mb-4">
        <div>
          <label class="block text-xs font-semibold text-gray-700 mb-2">সার্চ করুন</label>
          <InputText
            v-model="localFilters['global'].value"
            placeholder="নাম, রেজি নং, মাদরাসা..."
            class="pl-3 pr-4 py-2 border-gray-300 focus:ring-gray-500 focus:border-gray-500 block w-full shadow-sm sm:text-sm border rounded-sm bg-white"
          />
        </div>
        <div>
          <label class="block text-xs font-semibold text-gray-700 mb-2">মারহালা</label>
          <Dropdown
            v-model="localFilters.current_class.value"
            :options="marhalOptions"
            placeholder="সিলেক্ট করুন"
            optionLabel="name"
            optionValue="value"
            class="w-full"
            dropdownIcon="pi pi-chevron-down"
            panelClass="z-[60]"
          />
        </div>
        <div>
          <label class="block text-xs font-semibold text-gray-700 mb-2">পরীক্ষার্থীর ধরন</label>
          <Dropdown
            v-model="localFilters.student_type.value"
            :options="studentTypeOptions"
            placeholder="সিলেক্ট করুন"
            optionLabel="name"
            optionValue="value"
            class="w-full"
            dropdownIcon="pi pi-chevron-down"
            panelClass="z-[60]"
          />
        </div>
        <div>
          <label class="block text-xs font-semibold text-gray-700 mb-2">পেমেন্ট স্ট্যাটাস</label>
          <Dropdown
            v-model="localFilters.payment_status.value"
            :options="paymentStatusOptions"
            placeholder="সিলেক্ট করুন"
            optionLabel="name"
            optionValue="value"
            class="w-full"
            dropdownIcon="pi pi-chevron-down"
            panelClass="z-[60]"
          />
        </div>
        <div>
          <label class="block text-xs font-semibold text-gray-700 mb-2">আবেদন অবস্থা</label>
          <Dropdown
            v-model="localFilters.status.value"
            :options="applicationStatusOptions"
            placeholder="সিলেক্ট করুন"
            optionLabel="name"
            optionValue="value"
            class="w-full"
            dropdownIcon="pi pi-chevron-down"
            panelClass="z-[60]"
          />
        </div>
      </div>
      <div class="flex flex-col sm:flex-row justify-end gap-2 mt-2">
        <button
          class="inline-flex items-center px-5 py-2 bg-gray-700 border border-gray-600 rounded-sm font-semibold text-xs text-gray-100 uppercase tracking-widest shadow hover:bg-gray-600 transition"
        >
          <i class="pi pi-search mr-2" /> সার্চ করুন
        </button>
        <button
          @click="resetSearch"
          class="inline-flex items-center px-5 py-2 bg-gray-200 border border-gray-300 rounded-sm font-semibold text-xs text-gray-700 uppercase tracking-widest shadow hover:bg-gray-300 transition"
        >
          <i class="pi pi-refresh mr-2" /> রিসেট
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Make PrimeVue dropdown panel go above dialogs if needed */
:deep(.p-dropdown-panel) {
  z-index: 60 !important;
}
</style>

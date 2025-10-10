<script setup lang="ts">
import { ref, watch } from 'vue';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';

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
  class="overflow-hidden rounded-sm shadow-xl bg-white mb-8 border border-gray-200">
    <!-- Header -->
    <div class="p-4 bg-gray-800 border-b border-gray-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div class="flex items-center gap-4">
        <span class="inline-flex items-center justify-center rounded-sm h-12 w-12 bg-gray-800 bg-opacity-50 backdrop-blur">
          <i class="pi pi-search text-white text-xl"></i>
        </span>
        <div>
          <h3 class="text-white text-2xl font-bold tracking-tight">সার্চ উইজার্ড</h3>
          <p class="text-blue-100 text-sm mt-1">শিক্ষার্থী অনুসন্ধান এবং ফিল্টার করুন</p>
        </div>
      </div>
      <div class="flex gap-3 flex-wrap justify-end">
        <Button
          label="নিবন্ধন করুন"
          icon="pi pi-user-plus"
          iconPos="left"
          class="p-button-outlined p-button-sm bg-white bg-opacity-20 text-white border-white hover:bg-opacity-30"
        />
        <Button
          label="ইম্পোর্ট করুন"
          icon="pi pi-file-import"
          iconPos="left"
          class="p-button-outlined p-button-sm bg-white bg-opacity-20 text-white border-white hover:bg-opacity-30"
        />
      </div>
    </div>
    <!-- Filters -->
    <div class="p-6 bg-gray-50">
      <div class="mb-6">
        <h4 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <i class="pi pi-filter text-blue-600"></i>
          অনুসন্ধান ফিল্টার
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">সার্চ করুন</label>
            <IconField class="w-full">
              <InputIcon class="text-gray-400">
                <i class="pi pi-search" />
              </InputIcon>
              <InputText
                v-model="localFilters['global'].value"
                placeholder="নাম, রেজি নং, মাদরাসা..."
                class="w-full"
              />
            </IconField>
          </div>
        <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">মারহালা</label>
            <Dropdown
              v-model="localFilters.current_class.value"
              :options="marhalOptions"
              placeholder="সিলেক্ট করুন"
              optionLabel="name"
              optionValue="value"
              class="w-full"
              :showClear="true"
              panelClass="z-[60]"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">পরীক্ষার্থীর ধরন</label>
            <Dropdown
              v-model="localFilters.student_type.value"
              :options="studentTypeOptions"
              placeholder="সিলেক্ট করুন"
              optionLabel="name"
              optionValue="value"
              class="w-full"
              :showClear="true"
              panelClass="z-[60]"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">পেমেন্ট স্ট্যাটাস</label>
            <Dropdown
              v-model="localFilters.payment_status.value"
              :options="paymentStatusOptions"
              placeholder="সিলেক্ট করুন"
              optionLabel="name"
              optionValue="value"
              class="w-full"
              :showClear="true"
              panelClass="z-[60]"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">আবেদন অবস্থা</label>
            <Dropdown
              v-model="localFilters.status.value"
              :options="applicationStatusOptions"
              placeholder="সিলেক্ট করুন"
              optionLabel="name"
              optionValue="value"
              class="w-full"
              :showClear="true"
              panelClass="z-[60]"
            />
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row justify-end gap-3 mt-6 pt-6 border-t border-gray-200">
        <Button
          label="সার্চ করুন"
          icon="pi pi-search"
          iconPos="left"
          class="p-button-sm bg-blue-600 text-white hover:bg-blue-700"
        />
        <Button
          label="রিসেট"
          icon="pi pi-refresh"
          iconPos="left"
          @click="resetSearch"
          class="p-button-outlined p-button-sm border-gray-300 text-gray-700 hover:bg-gray-50"
        />
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

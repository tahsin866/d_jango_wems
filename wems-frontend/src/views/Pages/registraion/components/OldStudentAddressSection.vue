<template>
  <div class="bg-white border border-gray-200 rounded-sm shadow-md overflow-hidden">
    <div class="bg-gradient-to-r from-gray-700 to-gray-600 px-6 py-4 relative">
      <div class="flex justify-between items-center relative z-10">
        <div class="flex gap-4 items-center">
          <div class="p-2 rounded-sm bg-white bg-opacity-20 backdrop-blur-sm">
            <i class="text-2xl text-white" :class="addressType === 'present' ? 'fa-map-marker-alt' : 'fa-home'"></i>
          </div>
          <h5 class="text-white text-xl font-bold tracking-wide">
            {{ addressType === 'present' ? 'বর্তমান ঠিকানা' : 'স্থায়ী ঠিকানা' }}
          </h5>
        </div>

        <div class="flex items-center space-x-3">
          <span class="text-white font-medium">বর্তমান</span>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="isPermanent" class="sr-only peer">
            <div class="w-12 h-6 bg-gray-300 peer-focus:ring-2 peer-focus:ring-gray-400 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gray-700"></div>
          </label>
          <span class="text-white font-medium">স্থায়ী</span>
        </div>
      </div>
    </div>

    <div class="p-6 bg-gray-50">
      <div class="grid grid-cols-1 gap-6">
        <div class="relative">
          <label class="flex text-gray-700 text-lg font-semibold gap-2 items-center mb-2">
            <i class="fas fa-map-marked-alt" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            বিভাগ
          </label>
          <div class="relative">
            <select
              v-model="currentAddress.division"
              @change="onDivisionChange"
              class="bg-white border border-gray-300 rounded-sm w-full block focus:ring-gray-500 focus:ring-2 px-4 py-3 shadow-sm transition-colors appearance-none"
            >
              <option value="">সকল</option>
              <option v-for="division in divisions" :key="division.id" :value="String(division.id)">
                {{ division.Division }}
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>
        </div>

        <div class="relative">
          <label class="flex text-gray-700 text-lg font-semibold gap-2 items-center mb-2">
            <i class="fas fa-city" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            জেলা
          </label>
          <div class="relative">
            <select
              v-model="currentAddress.district"
              @change="onDistrictChange"
              :disabled="!currentAddress.division"
              class="bg-white border border-gray-300 rounded-sm w-full block focus:ring-gray-500 focus:ring-2 px-4 py-3 shadow-sm transition-colors appearance-none disabled:bg-gray-100 disabled:opacity-70"
            >
              <option value="">সকল</option>
              <option v-for="district in currentDistricts" :key="district.DesID" :value="String(district.DesID)">
                {{ district.District }}
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>
        </div>

        <div class="relative">
          <label class="flex text-gray-700 text-lg font-semibold gap-2 items-center mb-2">
            <i class="fas fa-location-dot" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            থানা/উপজেলা
          </label>
          <div class="relative">
            <select
              v-model="currentAddress.Thana"
              @change="onThanaChange"
              :disabled="!currentAddress.district"
              class="bg-white border border-gray-300 rounded-sm w-full block focus:ring-gray-500 focus:ring-2 px-4 py-3 shadow-sm transition-colors appearance-none disabled:bg-gray-100 disabled:opacity-70"
            >
              <option value="">সকল</option>
              <option v-for="thana in currentThanas" :key="thana.Thana_ID" :value="String(thana.Thana_ID)">
                {{ thana.Thana }}
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed, ref } from 'vue';

type Division = { id: string | number; Division: string };
type District = { DesID: string | number; District: string };
type Thana = { Thana_ID: string | number; Thana: string };
type Filters = { division?: string; district?: string; Thana?: string };
type StudentInfo = Record<string, any>;

const props = defineProps<{
  divisions?: Division[];
  presentFilters?: Filters;
  presentDistricts?: District[];
  presentThanas?: Thana[];
  permanentFilters?: Filters;
  districts?: District[];
  thanas?: Thana[];
  studentInfoForm?: StudentInfo;
}>();

const emit = defineEmits<{
  (e: 'present-division-change'): void;
  (e: 'present-district-change'): void;
  (e: 'permanent-division-change'): void;
  (e: 'permanent-district-change'): void;
  (e: 'update:studentInfoForm', payload: StudentInfo): void;
}>();

// Toggle between present and permanent address
const isPermanent = ref(false);
const addressType = computed(() => isPermanent.value ? 'permanent' : 'present');

// Local reactive copies to avoid mutating props directly
const localPresent = reactive<Filters>({
  division: props.presentFilters?.division ?? '',
  district: props.presentFilters?.district ?? '',
  Thana: props.presentFilters?.Thana ?? ''
});

const localPermanent = reactive<Filters>({
  division: props.permanentFilters?.division ?? '',
  district: props.permanentFilters?.district ?? '',
  Thana: props.permanentFilters?.Thana ?? ''
});

// Current address data based on toggle
const currentAddress = computed(() => isPermanent.value ? localPermanent : localPresent);
const currentDistricts = computed(() => isPermanent.value ? props.districts : props.presentDistricts);
const currentThanas = computed(() => isPermanent.value ? props.thanas : props.presentThanas);

// Sync when parent updates props
watch(
  () => props.presentFilters,
  (v) => {
    if (!v) return;
    localPresent.division = v.division ?? '';
    localPresent.district = v.district ?? '';
    localPresent.Thana = v.Thana ?? '';
  },
  { deep: true, immediate: true }
);

watch(
  () => props.permanentFilters,
  (v) => {
    if (!v) return;
    localPermanent.division = v.division ?? '';
    localPermanent.district = v.district ?? '';
    localPermanent.Thana = v.Thana ?? '';
  },
  { deep: true, immediate: true }
);

// Helpers to build updated studentInfoForm and emit it back to parent
const emitUpdatedStudentInfoForPresent = () => {
  const updated: StudentInfo = { ...(props.studentInfoForm ?? {}) };

  // division
  const selDiv = (props.divisions ?? []).find((d) => String(d.id) === String(localPresent.division));
  if (selDiv) {
    updated.present_division_name = selDiv.Division;
    updated.presernt_DID = String(selDiv.id);
  } else {
    updated.present_division_name = '';
    updated.presernt_DID = '';
  }

  // district
  const selDistrict = (props.presentDistricts ?? []).find((d) => String(d.DesID) === String(localPresent.district));
  if (selDistrict) {
    updated.present_district_name = selDistrict.District;
    updated.present_desId = String(selDistrict.DesID);
  } else {
    updated.present_district_name = '';
    updated.present_desId = '';
  }

  // thana
  const selThana = (props.presentThanas ?? []).find((t) => String(t.Thana_ID) === String(localPresent.Thana));
  if (selThana) {
    updated.present_thana_name = selThana.Thana;
    updated.present_TID = String(selThana.Thana_ID);
  } else {
    updated.present_thana_name = '';
    updated.present_TID = '';
  }

  emit('update:studentInfoForm', updated);
};

const emitUpdatedStudentInfoForPermanent = () => {
  const updated: StudentInfo = { ...(props.studentInfoForm ?? {}) };

  // division
  const selDiv = (props.divisions ?? []).find((d) => String(d.id) === String(localPermanent.division));
  if (selDiv) {
    updated.parmanent_division_name = selDiv.Division;
    updated.parmanent_DID = String(selDiv.id);
  } else {
    updated.parmanent_division_name = '';
    updated.parmanent_DID = '';
  }

  // district
  const selDistrict = (props.districts ?? []).find((d) => String(d.DesID) === String(localPermanent.district));
  if (selDistrict) {
    updated.parmanent_district_name = selDistrict.District;
    updated.parmanent_desId = String(selDistrict.DesID);
  } else {
    updated.parmanent_district_name = '';
    updated.parmanent_desId = '';
  }

  // thana
  const selThana = (props.thanas ?? []).find((t) => String(t.Thana_ID) === String(localPermanent.Thana));
  if (selThana) {
    updated.parmanent_thana_name = selThana.Thana;
    updated.parmanent_TID = String(selThana.Thana_ID);
  } else {
    updated.parmanent_thana_name = '';
    updated.parmanent_TID = '';
  }

  emit('update:studentInfoForm', updated);
};

// Event handlers called from selects
const onDivisionChange = () => {
  // reset dependent selects
  currentAddress.value.district = '';
  currentAddress.value.Thana = '';

  // notify parent to load districts
  if (isPermanent.value) {
    emit('permanent-division-change');
    emitUpdatedStudentInfoForPermanent();
  } else {
    emit('present-division-change');
    emitUpdatedStudentInfoForPresent();
  }
};

const onDistrictChange = () => {
  // reset thana
  currentAddress.value.Thana = '';

  if (isPermanent.value) {
    emit('permanent-district-change');
    emitUpdatedStudentInfoForPermanent();
  } else {
    emit('present-district-change');
    emitUpdatedStudentInfoForPresent();
  }
};

const onThanaChange = () => {
  if (isPermanent.value) {
    emitUpdatedStudentInfoForPermanent();
  } else {
    emitUpdatedStudentInfoForPresent();
  }
};
</script>

<style scoped>
/* Professional styling enhancements */
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
}

/* Disabled state improvements */
select:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

/* Toggle switch styling */
.peer:checked ~ .peer-checked\:after\:translate-x-full {
  transform: translateX(100%);
}

.peer:checked ~ .peer-checked\:bg-gray-700 {
  background-color: #374151;
}
</style>

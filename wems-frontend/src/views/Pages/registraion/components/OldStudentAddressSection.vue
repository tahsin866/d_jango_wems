<template>
  <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
    <!-- Present Address -->
    <div class="bg-white border border-emerald-100 rounded-md shadow">
      <div class="bg-gradient-to-r rounded-t-md from-emerald-800 overflow-hidden px-6 py-3 relative to-emerald-600">
        <div class="flex gap-3 items-center relative z-10">
          <i class="text-2xl text-white fa-map-marker-alt fas"></i>
          <h5 class="text-white text-xl">বর্তমান ঠিকানা</h5>
        </div>
      </div>
      <div class="bg-opacity-5 bg-white p-6">
        <div class="grid grid-cols-1 gap-4">
          <div class="relative">
            <label class="flex text-emerald-700 text-lg font-medium gap-2 items-center mb-1">বিভাগ</label>
            <div class="relative">
              <select
                v-model="localPresent.division"
                @change="onPresentDivisionChange"
                class="bg-white border border-gray-200 rounded-sm w-full block focus:ring-[#2d6a4f] focus:ring-2 px-4 py-2"
              >
                <option value="">সকল</option>
                <option v-for="division in divisions" :key="division.id" :value="String(division.id)">
                  {{ division.Division }}
                </option>
              </select>
            </div>
          </div>

          <div class="relative">
            <label class="flex text-emerald-700 text-lg font-medium gap-2 items-center mb-1">জেলা</label>
            <div class="relative">
              <select
                v-model="localPresent.district"
                @change="onPresentDistrictChange"
                :disabled="!localPresent.division"
                class="bg-white border border-gray-200 rounded-sm w-full block focus:ring-[#2d6a4f] focus:ring-2 px-4 py-2"
              >
                <option value="">সকল</option>
                <option v-for="district in presentDistricts" :key="district.DesID" :value="String(district.DesID)">
                  {{ district.District }}
                </option>
              </select>
            </div>
          </div>

          <div class="relative">
            <label class="flex text-emerald-700 text-lg font-medium gap-2 items-center mb-1">থানা/উপজেলা</label>
            <div class="relative">
              <select
                v-model="localPresent.Thana"
                @change="onPresentThanaChange"
                :disabled="!localPresent.district"
                class="bg-white border border-gray-200 rounded-sm w-full block focus:ring-[#2d6a4f] focus:ring-2 px-4 py-2"
              >
                <option value="">সকল</option>
                <option v-for="thana in presentThanas" :key="thana.Thana_ID" :value="String(thana.Thana_ID)">
                  {{ thana.Thana }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Permanent Address -->
    <div class="bg-white border border-emerald-100 rounded-md shadow">
      <div class="bg-gradient-to-r rounded-t-md from-emerald-800 overflow-hidden px-6 py-3 relative to-emerald-600">
        <div class="flex gap-3 items-center relative z-10">
          <i class="text-2xl text-white fa-home fas"></i>
          <h5 class="text-white text-xl">স্থায়ী ঠিকানা</h5>
        </div>
      </div>
      <div class="bg-opacity-5 bg-white p-6">
        <div class="grid grid-cols-1 gap-4">
          <div class="relative">
            <label class="flex text-emerald-700 text-lg font-medium gap-2 items-center mb-1">বিভাগ</label>
            <div class="relative">
              <select
                v-model="localPermanent.division"
                @change="onPermanentDivisionChange"
                class="bg-white border border-gray-200 rounded-sm w-full block focus:ring-[#2d6a4f] focus:ring-2 px-4 py-2"
              >
                <option value="">সকল</option>
                <option v-for="division in divisions" :key="division.id" :value="String(division.id)">
                  {{ division.Division }}
                </option>
              </select>
            </div>
          </div>

          <div class="relative">
            <label class="flex text-emerald-700 text-lg font-medium gap-2 items-center mb-1">জেলা</label>
            <div class="relative">
              <select
                v-model="localPermanent.district"
                @change="onPermanentDistrictChange"
                :disabled="!localPermanent.division"
                class="bg-white border border-gray-200 rounded-sm w-full block focus:ring-[#2d6a4f] focus:ring-2 px-4 py-2"
              >
                <option value="">সকল</option>
                <option v-for="district in districts" :key="district.DesID" :value="String(district.DesID)">
                  {{ district.District }}
                </option>
              </select>
            </div>
          </div>

          <div class="relative">
            <label class="flex text-emerald-700 text-lg font-medium gap-2 items-center mb-1">থানা/উপজেলা</label>
            <div class="relative">
              <select
                v-model="localPermanent.Thana"
                @change="onPermanentThanaChange"
                :disabled="!localPermanent.district"
                class="bg-white border border-gray-200 rounded-sm w-full block focus:ring-[#2d6a4f] focus:ring-2 px-4 py-2"
              >
                <option value="">সকল</option>
                <option v-for="thana in thanas" :key="thana.Thana_ID" :value="String(thana.Thana_ID)">
                  {{ thana.Thana }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue';

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
const onPresentDivisionChange = () => {
  // reset dependent selects
  localPresent.district = '';
  localPresent.Thana = '';

  // notify parent to load districts
  emit('present-division-change');
  // update studentInfo form fields and inform parent
  emitUpdatedStudentInfoForPresent();
};

const onPresentDistrictChange = () => {
  // reset thana
  localPresent.Thana = '';
  emit('present-district-change');
  emitUpdatedStudentInfoForPresent();
};

const onPresentThanaChange = () => {
  // just update studentInfo
  emitUpdatedStudentInfoForPresent();
};

const onPermanentDivisionChange = () => {
  localPermanent.district = '';
  localPermanent.Thana = '';
  emit('permanent-division-change');
  emitUpdatedStudentInfoForPermanent();
};

const onPermanentDistrictChange = () => {
  localPermanent.Thana = '';
  emit('permanent-district-change');
  emitUpdatedStudentInfoForPermanent();
};

const onPermanentThanaChange = () => {
  emitUpdatedStudentInfoForPermanent();
};
</script>

<style scoped>
/* All styling via Tailwind utility classes in template */
</style>

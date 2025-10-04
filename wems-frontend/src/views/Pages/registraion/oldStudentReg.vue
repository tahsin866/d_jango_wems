<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="mx-auto px-4 py-3 sm:px-6 lg:px-8"
    :class="[!isDark ? 'bg-gray-50 text-gray-200' : 'bg-gray-900 text-gray-200']"
  >
    <div class="rounded-sm mt-5 overflow-hidden"
      :class="[!isDark ? 'bg-white' : 'bg-gray-800']">
      <!-- Stepper Header -->
      <div class="flex flex-col sm:flex-row justify-between items-center px-8 pt-8 pb-4"
        :class="[!isDark ? 'bg-gray-800' : 'bg-gray-900']">
        <div class="flex items-center gap-4">
          <i class="fa-solid fa-user-graduate text-3xl text-gray-300"></i>
          <h2 class="text-2xl font-bold text-gray-200 tracking-wide">ছাত্র তথ্য সম্পাদনা</h2>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="px-8 pt-4">
        <div class="flex items-center gap-2 mb-2">
          <template v-for="(tab, idx) in tabs" :key="tab">
            <div class="flex flex-col items-center">
              <div
                :class="[
                  'w-8 h-8 flex items-center justify-center rounded-full text-base font-bold transition-all duration-300 shadow',
                  currentTab === idx ? 'bg-gray-600 text-white scale-110 shadow-lg ring-2 ring-gray-500' :
                    idx < currentTab ? 'bg-gray-500 text-white' :
                    'bg-gray-300 text-gray-600',
                  isDark && (currentTab === idx || idx < currentTab) ? 'bg-gray-700 text-white' : ''
                ]"
              >{{ idx + 1 }}</div>
              <span class="mt-1 text-xs font-medium"
                :class="currentTab === idx
                  ? isDark ? 'text-gray-300' : 'text-gray-700'
                  : isDark ? 'text-gray-500' : 'text-gray-500'
              ">{{ tab }}</span>
            </div>
            <template v-if="idx < tabs.length - 1">
              <div class="w-6 h-1 rounded"
                :class="isDark ? 'bg-gray-600' : 'bg-gray-500'"></div>
            </template>
          </template>
        </div>
        <div class="w-full h-1 bg-gray-200 rounded relative mb-2"
          :class="isDark ? 'bg-gray-700' : ''">
          <div
            class="h-1 bg-gray-600 rounded transition-all duration-300"
            :class="isDark ? 'bg-gray-500' : ''"
            :style="{ width: ((currentTab + 1) / tabs.length * 100) + '%' }"
          ></div>
        </div>
      </div>

      <form @submit.prevent="submitStudentInfo" class="p-8 space-y-8 rounded-b-2xl">
        <!-- Animated Tab Content -->
        <transition
          enter-active-class="transition duration-500 ease-out"
          enter-from-class="opacity-0 transform translate-y-8"
          enter-to-class="opacity-100 transform translate-y-0"
          leave-active-class="transition duration-300 ease-in"
          leave-from-class="opacity-100 transform translate-y-0"
          leave-to-class="opacity-0 transform -translate-y-8"
          mode="out-in"
        >
          <div :key="currentTab" class="min-h-[400px]">
            <!-- Tab 1: Personal Info -->
            <div v-if="currentTab === 0" class="fade-in">
              <OldStudentPersonalInfo v-model="studentInfoForm" />
            </div>

            <div v-if="currentTab === 1" class="fade-in">
              <OldStudentAddressSection
                :divisions="divisions"
                :addressFilters="addressFilters"
                :districts="districts"
                :thanas="thanas"
                @update:addressFilters="onUpdateAddressFilters"
                v-model:studentInfoForm="studentInfoForm"
              />
            </div>
            <!-- Tab 4: Attachments -->
            <div v-if="currentTab === 2" class="fade-in">
              <OldStudentAttachments
                :studentPhoto="studentPhoto"
                :studentPhotoPreview="studentPhotoPreview"
                :nidAttachment="nidAttachment"
                :nidAttachmentPreview="nidAttachmentPreview"
                @file-upload="handleFileUpload"
                @remove-file="removeFile"
              />
            </div>
            <!-- Tab 5: Review & Submit -->
            <div v-if="currentTab === 3" class="fade-in">
              <div
                class="text-xl font-semibold mb-3 flex items-center gap-2"
                :class="isDark ? 'text-gray-300' : 'text-gray-700'"
              >
                <i class="fa-solid fa-circle-check text-2xl text-gray-500"></i> তথ্য যাচাই ও সংরক্ষণ
              </div>
              <div class="mb-3"
                :class="isDark ? 'text-gray-400' : 'text-gray-600'"
              >
                অনুগ্রহ করে পূর্বের সকল তথ্য যাচাই করুন। চাইলে আগের ধাপে ফিরে তথ্য পরিবর্তন করতে পারেন।
              </div>
              <div class="rounded-lg border border-dashed p-4"
                :class="isDark ? 'border-gray-600 bg-gray-700 text-gray-300' : 'border-gray-300 bg-gray-100 text-gray-700'"
              >
                <i class="fa-solid fa-info-circle mr-2 text-gray-500"></i>
                সকল তথ্য সঠিক থাকলে <b>সংরক্ষণ করুন</b> বাটনে ক্লিক করুন।
              </div>
            </div>
          </div>
        </transition>

        <!-- Navigation Buttons -->
        <div class="flex justify-between items-center mt-8">
          <button
            type="button"
            class="flex items-center gap-2 px-6 py-2 rounded-md font-medium transition-colors"
            :class="[isDark ? 'text-gray-300 bg-gray-700 hover:bg-gray-600' : 'text-gray-700 bg-gray-200 hover:bg-gray-300']"
            @click="prevTab"
            :disabled="currentTab === 0"
          >
            <i class="fa-solid fa-arrow-left"></i> পূর্বের ধাপ
          </button>
          <div class="flex gap-2">
            <button
              v-if="currentTab < tabs.length - 1"
              type="button"
              class="flex items-center gap-2 px-8 py-2 rounded-md font-bold shadow transition-colors"
              :class="[isDark ? 'bg-gray-700 text-white hover:bg-gray-600' : 'bg-gray-600 text-white hover:bg-gray-500']"
              @click="nextTab"
            >
              পরবর্তী ধাপ <i class="fa-solid fa-arrow-right"></i>
            </button>
            <button
              v-else
              type="submit"
              class="flex items-center gap-2 px-10 py-2 rounded-md font-bold shadow transition-colors"
              :class="[isDark ? 'bg-gray-600 text-white hover:bg-gray-500' : 'bg-gray-500 text-white hover:bg-gray-400']"
            >
              <i class="fa-solid fa-cloud-upload-alt"></i> সংরক্ষণ করুন
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
// TypeScript type for secure token system
type SearchResult = {
  secure_token?: string;
  student_basic?: {
    cid?: string | number;
    srtype?: string;
    students_type?: string;
    exam_id?: string | number;
    madrasha_id?: string | number;
    marhala_id?: string | number;
    ip_address?: string;
    created_at?: string;
    updated_at?: string;
    student_name_bn?: string;
    father_name_bn?: string;
    date_of_birth?: string;
    roll_no?: number;
    reg_no?: number;
    year?: number;
    // add other fields as needed
  };
  student_results?: {
    mid?: string;
    srtype?: number;
    subjects?: Array<{
      result_type?: string;
      [key: string]: string | number | undefined;
    }>;
    [key: string]: string | number | Array<unknown> | undefined;
  };
  // add other properties as needed
};

import { watch, ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

const searchResult = ref<SearchResult | null>(null);

// Register event handler for address filter updates
async function onUpdateAddressFilters(filters: { division?: string; district?: string; Thana?: string }) {
  const prev = { ...addressFilters.value };
  addressFilters.value = {
    division: filters.division ?? '',
    district: filters.district ?? '',
    Thana: filters.Thana ?? ''
  };
  // If division changed, reload districts and reset thana
  if (addressFilters.value.division !== prev.division) {
    await handleDivisionChange();
  }
  // District changes are handled by the watcher to load thanas
}
import OldStudentPersonalInfo from '@/views/Pages/registraion/components/OldStudentPersonalInfo.vue';
import OldStudentAddressSection from '@/views/Pages/registraion/components/OldStudentAddressSection.vue';
import OldStudentAttachments from '@/views/Pages/registraion/components/OldStudentAttachments.vue';

defineProps({
  roll: String,
  reg_id: String,
  CID: String,
  modelValue: Object
});

// Dark mode detection
const isDark = computed(() => {
  return document.documentElement.classList.contains('dark');
});

// Local state & forms

function useForm<T extends Record<string, unknown>>(arg0: T) {
  return ref({ ...arg0 });
}

const studentInfoForm = useForm({
  name_bn: '',
  name_en: '',
  name_ar: '',
  father_name_bn: '',
  father_name_en: '',
  father_name_ar: '',
  mother_name_bn: '',
  mother_name_en: '',
  mother_name_ar: '',
  BRN_no: '',
  NID_no: '',
  past_Roll: '',
  past_reg_id: '',
  madrasha_name: '',
  markaz_name: '',
  passing_year: '',
  class: '',
  Division: '',
  Date_of_birth: '',
  current_madrasha: '',
  current_markaz: '',
  student_type: '',
  current_class: '',
  exam_books_name: '',
  mobile_no: '',
  user_name: '',
  user_id: '',
  markaz_id: '',
  NID_attach: '',
  marhala_id: '',
  division_name: '',
  DID: '',
  district_name: '',
  desId: '',
  thana_name: '',
  TID: '',
  student_image: '',
  irregular_sub: null,
});

// File Attachments
const studentPhoto = ref<File | null>(null);
const studentPhotoPreview = ref<string | null>(null);
const nidAttachment = ref<File | null>(null);
const nidAttachmentPreview = ref<string | null>(null);

// Address Data
type Division = { id: string; Division: string };
type District = { DesID: string; District: string };
type Thana = { Thana_ID: string; Thana: string };

const divisions = ref<Division[]>([]);
const districts = ref<District[]>([]);
const thanas = ref<Thana[]>([]);

const addressFilters = ref({ division: '', district: '', Thana: '' });

// Watch for district change to load thanas
watch(() => addressFilters.value.district, async (newDistrict, oldDistrict) => {
  if (newDistrict && newDistrict !== oldDistrict) {
    await handleDistrictChange();
  }
});

const tabs = [
  'ব্যক্তিগত তথ্য',
  'ঠিকানা',
  'সংযুক্তি',
  'শেষ ধাপ'
];
const currentTab = ref(0);
const loading = ref(true);
const fadeIn = ref(false);

// --- Fake data sources ---

// Real API functions
const fetchDivisions = async () => {
  const response = await fetch('/api/admin/madrasha/divisions/');
  if (!response.ok) return [];
  const data = await response.json();
  return (data.results || []).map((item: { did: string; division: string }) => ({ id: String(item.did), Division: item.division }));
};
const fetchDistricts = async (divisionId: string) => {
  const url = divisionId ? `/api/admin/madrasha/districts/?did=${divisionId}` : '/api/admin/madrasha/districts/';
  const response = await fetch(url);
  if (!response.ok) return [];
  const data = await response.json();
  return (data.results || []).map((item: { desid: string; district: string }) => ({ DesID: String(item.desid), District: item.district }));
};
const fetchThanas = async (districtId: string) => {
  const url = districtId ? `/api/admin/madrasha/thanas/?district_id=${districtId}` : '/api/admin/madrasha/thanas/';
  const response = await fetch(url);
  if (!response.ok) return [];
  const data = await response.json();
  return (data.results || []).map((item: { thana_id: string; thana: string }) => ({ Thana_ID: String(item.thana_id), Thana: item.thana }));
};

const nextTab = () => {
  if (currentTab.value < tabs.length - 1) currentTab.value++;
};
const prevTab = () => {
  if (currentTab.value > 0) currentTab.value--;
};

onMounted(async () => {
  // Load search result from sessionStorage if available
  try {
    const storedSearchResult = sessionStorage.getItem('oldStudentSearchResult');
    if (storedSearchResult) {
      searchResult.value = JSON.parse(storedSearchResult);
      console.log('Loaded search result from sessionStorage:', searchResult.value);
    }
  } catch (e) {
    console.warn('Could not load search result from sessionStorage:', e);
  }

  // Prefill from sessionStorage (preferred) to avoid showing data in URL
  try {
    const stored = sessionStorage.getItem('oldRegPrefill');
    if (stored) {
      const payload = JSON.parse(stored) as Partial<{ name_bn: string; father_name_bn: string; Date_of_birth: string }>;
      if (payload.name_bn) studentInfoForm.value.name_bn = payload.name_bn;
      if (payload.father_name_bn) studentInfoForm.value.father_name_bn = payload.father_name_bn;
      if (payload.Date_of_birth) studentInfoForm.value.Date_of_birth = payload.Date_of_birth;
      sessionStorage.removeItem('oldRegPrefill');
    } else {
      // Fallback: Prefill from query params if provided
      const route = useRoute();
      const q = route.query as Record<string, string | string[]>;
      const getQ = (key: string) => {
        const v = q[key];
        return Array.isArray(v) ? v[0] : (v ?? '');
      };
      const qbName = getQ('name_bn');
      const qfName = getQ('father_name_bn');
      const qDob = getQ('Date_of_birth');
      if (qbName) studentInfoForm.value.name_bn = qbName as string;
      if (qfName) studentInfoForm.value.father_name_bn = qfName as string;
      if (qDob) studentInfoForm.value.Date_of_birth = qDob as string;
    }
  } catch {}

  divisions.value = await fetchDivisions();
  if (addressFilters.value.division) {
    districts.value = await fetchDistricts(addressFilters.value.division);
  }
  if (addressFilters.value.district) {
    thanas.value = await fetchThanas(addressFilters.value.district);
  }
  setTimeout(() => {
    fadeIn.value = true;
    loading.value = false;
  }, 120);
});

const handleFileUpload = (event: Event, type: string) => {
  const input = event.target as HTMLInputElement;
  const file = input?.files?.[0] ?? null;
  if (!file) return;
  if (type === 'studentPhoto') {
    studentPhoto.value = file;
    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      studentPhotoPreview.value = (e.target?.result as string | null) ?? null;
    };
    reader.readAsDataURL(file);
  } else if (type === 'nidAttachment') {
    nidAttachment.value = file;
    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      nidAttachmentPreview.value = (e.target?.result as string | null) ?? null;
    };
    reader.readAsDataURL(file);
  }
};

const removeFile = (type: string) => {
  if (type === 'studentPhoto') {
    studentPhoto.value = null;
    studentPhotoPreview.value = null;
  } else if (type === 'nidAttachment') {
    nidAttachment.value = null;
    nidAttachmentPreview.value = null;
  }
};

const handleDivisionChange = async () => {
  addressFilters.value.district = '';
  addressFilters.value.Thana = '';
  districts.value = [];
  thanas.value = [];
  if (!addressFilters.value.division) return;
  districts.value = await fetchDistricts(addressFilters.value.division);
};
const handleDistrictChange = async () => {
  addressFilters.value.Thana = '';
  thanas.value = [];
  if (!addressFilters.value.district) return;
  thanas.value = await fetchThanas(addressFilters.value.district);
};

const updateFormData = () => {
  if (addressFilters.value.division) {
    const sel = divisions.value.find(d => d.id == addressFilters.value.division);
    if (sel) { studentInfoForm.value.division_name = sel.Division; studentInfoForm.value.DID = sel.id; }
  }
  if (addressFilters.value.district) {
    const sel = districts.value.find(d => d.DesID == addressFilters.value.district);
    if (sel) { studentInfoForm.value.district_name = sel.District; studentInfoForm.value.desId = sel.DesID; }
  }
  if (addressFilters.value.Thana) {
    const sel = thanas.value.find(t => t.Thana_ID == addressFilters.value.Thana);
    if (sel) { studentInfoForm.value.thana_name = sel.Thana; studentInfoForm.value.TID = sel.Thana_ID; }
  }
};

// Declare searchResult as a ref to avoid type errors

const submitStudentInfo = async () => {
  updateFormData();
  // Build payload for backend
  const personal = {
    student_name_bn: studentInfoForm.value.name_bn,
    student_name_ar: studentInfoForm.value.name_ar,
    student_name_en: studentInfoForm.value.name_en,
    father_name_bn: studentInfoForm.value.father_name_bn,
    father_name_ar: studentInfoForm.value.father_name_ar,
    father_name_en: studentInfoForm.value.father_name_en,
    mother_name_bn: studentInfoForm.value.mother_name_bn,
    mother_name_ar: studentInfoForm.value.mother_name_ar,
    mother_name_en: studentInfoForm.value.mother_name_en,
    date_of_birth: studentInfoForm.value.Date_of_birth,
    roll_no: studentInfoForm.value.past_Roll,
    marhala_id: studentInfoForm.value.marhala_id || searchResult.value?.student_basic?.marhala_id,
    mobile: studentInfoForm.value.mobile_no,
    // Merge fields from search result
    cid: searchResult.value?.student_basic?.cid ?? studentInfoForm.value.marhala_id,
    srtype: searchResult.value?.student_basic?.srtype ?? null,
  // Always use students_type from searchResult (not from form)
  students_type: searchResult.value?.student_basic?.students_type ?? '',
    exam_id: searchResult.value?.student_basic?.exam_id ?? null,
    madrasha_id: searchResult.value?.student_basic?.madrasha_id ?? null,
    irregular_sub: (studentInfoForm.value.irregular_sub === '' || studentInfoForm.value.irregular_sub === null)
      ? null
      : Number(studentInfoForm.value.irregular_sub),
    ip_address: searchResult.value?.student_basic?.ip_address ?? '127.0.0.1',
    created_at: searchResult.value?.student_basic?.created_at ?? new Date().toISOString(),
    updated_at: searchResult.value?.student_basic?.updated_at ?? new Date().toISOString(),
    // add other fields as needed
  };
  const address = {
    division: studentInfoForm.value.division_name,
    did: studentInfoForm.value.DID ? Number(studentInfoForm.value.DID) : null,
    district: studentInfoForm.value.district_name,
    desid: studentInfoForm.value.desId ? Number(studentInfoForm.value.desId) : null,
    thana: studentInfoForm.value.thana_name,
    thana_id: studentInfoForm.value.TID ? Number(studentInfoForm.value.TID) : null,
    birth_certificate_no: studentInfoForm.value.BRN_no,
    nid_no: studentInfoForm.value.NID_no,
    nid_photo: studentInfoForm.value.NID_attach,
  };
  const attachments = {
    birth_no: studentInfoForm.value.BRN_no,
    birth_attach: studentPhotoPreview.value || '',
    nid_no: studentInfoForm.value.NID_no,
    nid_attach: nidAttachmentPreview.value || '',
  };

  loading.value = true;

  // Debug logging
  console.log('=== SUBMITTING REGISTRATION DATA ===');
  console.log('Personal:', personal);
  console.log('Personal students_type:', personal.students_type);
  console.log('SearchResult students_type:', searchResult.value?.student_basic?.students_type);
  console.log('Address:', address);
  console.log('Attachments:', attachments);
  console.log('Search Result:', searchResult.value);
  console.log('=====================================');

  try {
    const res = await fetch('/api/admin/registration/oldstudent/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ personal, address, attachments, search_result: searchResult.value })
    });
    let result = null;
    try {
      result = await res.json();
    } catch {
      // If response is not JSON, show raw text (likely HTML error page)
      const text = await res.text();
      loading.value = false;
      window.alert('সংরক্ষণ ব্যর্থ: ' + text.slice(0, 300)); // Show first 300 chars
      return;
    }
    loading.value = false;
    if (res.ok && result.success) {
      window.alert('ছাত্রের তথ্য সফলভাবে সংরক্ষণ করা হয়েছে! রেজিস্ট্রেশন নম্বর: ' + result.reg_no);
      // Optionally reset form or redirect
    } else {
      window.alert('সংরক্ষণ ব্যর্থ: ' + (result.message || 'Unknown error'));
    }
  } catch (err) {
    loading.value = false;
    window.alert('সংরক্ষণ ব্যর্থ: ' + (err instanceof Error ? err.message : String(err)));
  }
};
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

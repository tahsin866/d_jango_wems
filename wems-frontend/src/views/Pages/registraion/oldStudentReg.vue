<template>
  <AdminLayout>
    <div
      style="font-family: 'SolaimanLipi', sans-serif;"
      class="mx-auto px-4 py-5 sm:px-6 lg:px-8"
      :class="[!isDark ? 'bg-gray-50' : 'dark:bg-slate-900 text-gray-200']"
    >
      <div class="rounded-md mt-5 overflow-hidden"
        :class="[!isDark ? 'bg-white' : 'dark:bg-slate-800']">
        <!-- Stepper Header -->
        <div class="flex flex-col sm:flex-row justify-between items-center px-8 pt-8 pb-4"
          :class="[!isDark ? 'bg-emerald-700' : 'dark:bg-emerald-800']">
          <div class="flex items-center gap-4">
            <i class="fa-solid fa-user-graduate text-3xl text-white"></i>
            <h2 class="text-2xl font-bold text-white tracking-wide">ছাত্র তথ্য সম্পাদনা</h2>
          </div>
          <div class="mt-4 sm:mt-0">
            <span class="inline-block bg-white/10 text-white text-xs rounded-full px-3 py-1 font-semibold tracking-wider">Advanced Edit Mode</span>
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
                    currentTab === idx ? 'bg-emerald-500 text-white scale-110 shadow-lg ring-2 ring-emerald-700' :
                      idx < currentTab ? 'bg-emerald-300 text-white' :
                      'bg-gray-200 text-gray-400',
                    isDark && (currentTab === idx || idx < currentTab) ? 'dark:bg-emerald-700 dark:text-white' : ''
                  ]"
                >{{ idx + 1 }}</div>
                <span class="mt-1 text-xs font-medium"
                  :class="currentTab === idx
                    ? isDark ? 'dark:text-emerald-300' : 'text-emerald-700'
                    : isDark ? 'dark:text-gray-400' : 'text-gray-400'"
                >{{ tab }}</span>
              </div>
              <template v-if="idx < tabs.length - 1">
                <div class="w-6 h-1 rounded"
                  :class="isDark ? 'dark:bg-emerald-700' : 'bg-gradient-to-r from-emerald-400 to-cyan-400'"></div>
              </template>
            </template>
          </div>
          <div class="w-full h-1 bg-gray-200 dark:bg-slate-700 rounded relative mb-2">
            <div
              class="h-1 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded transition-all duration-300 dark:bg-emerald-700"
              :style="{ width: ((currentTab + 1) / tabs.length * 100) + '%' }"
            ></div>
          </div>
        </div>

        <form @submit.prevent="submitStudentInfo" class="p-8 space-y-8 rounded-b-2xl">
          <!-- Animated Tab Content (Tailwind-only transition classes) -->
          <transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="opacity-0 transform translate-y-6 scale-95"
            enter-to-class="opacity-100 transform translate-y-0 scale-100"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100 transform translate-y-0 scale-100"
            leave-to-class="opacity-0 transform translate-y-6 scale-95"
            mode="out-in"
          >
            <div :key="currentTab">
              <!-- Tab 1: Personal Info -->
              <div v-if="currentTab === 0">
                <OldStudentPersonalInfo v-model="studentInfoForm" />
              </div>
              <!-- Tab 2: Past & Current Exam Info -->
              <div v-if="currentTab === 1">
                <OldStudentExamInfo
                  :pastExamForm="pastExamForm"
                  :currentExamForm="currentExamForm"
                />
              </div>
              <!-- Tab 3: Address Section -->
              <div v-if="currentTab === 2">
                <OldStudentAddressSection
                  :divisions="divisions"
                  :presentFilters="presentFilters"
                  :presentDistricts="presentDistricts"
                  :presentThanas="presentThanas"
                  :permanentFilters="permanentFilters"
                  :districts="districts"
                  :thanas="thanas"
                  @present-division-change="presentHandleDivisionChange"
                  @present-district-change="presentHandleDistrictChange"
                  @permanent-division-change="handleDivisionChange"
                  @permanent-district-change="handleDistrictChange"
                  v-model:studentInfoForm="studentInfoForm"
                />
              </div>
              <!-- Tab 4: Attachments -->
              <div v-if="currentTab === 3">
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
              <div v-if="currentTab === 4">
                <div
                  class="text-xl font-semibold mb-3 flex items-center gap-2"
                  :class="isDark ? 'dark:text-emerald-300' : 'text-emerald-700'"
                >
                  <i class="fa-solid fa-circle-check text-2xl"
                    :class="isDark ? 'dark:text-cyan-300' : 'text-cyan-700'"></i> তথ্য যাচাই ও সংরক্ষণ
                </div>
                <div class="mb-3"
                  :class="isDark ? 'dark:text-gray-300' : 'text-gray-700'">
                  অনুগ্রহ করে পূর্বের সকল তথ্য যাচাই করুন। চাইলে আগের ধাপে ফিরে তথ্য পরিবর্তন করতে পারেন।
                </div>
                <div class="rounded-lg border border-dashed p-4"
                  :class="isDark ? 'dark:border-emerald-700 dark:bg-emerald-900 text-emerald-300' : 'border-emerald-200 bg-emerald-50 text-emerald-800'">
                  <i class="fa-solid fa-info-circle mr-2"></i>
                  সকল তথ্য সঠিক থাকলে <b>সংরক্ষণ করুন</b> বাটনে ক্লিক করুন।
                </div>
              </div>
            </div>
          </transition>

          <!-- Navigation Buttons -->
          <div class="flex justify-between items-center mt-8">
            <button
              type="button"
              class="flex items-center gap-2 px-6 py-2 rounded-md font-semibold"
              :class="[isDark ? 'dark:text-gray-200 dark:bg-slate-700 dark:hover:bg-slate-600' : 'text-gray-700 bg-gray-100 hover:bg-gray-200']"
              @click="prevTab"
              :disabled="currentTab === 0"
            >
              <i class="fa-solid fa-arrow-left"></i> পূর্বের ধাপ
            </button>
            <div class="flex gap-2">
              <button
                v-if="currentTab < tabs.length - 1"
                type="button"
                class="flex items-center gap-2 px-8 py-2 rounded-md font-bold shadow"
                :class="[isDark ? 'dark:bg-emerald-800 dark:text-white dark:hover:bg-emerald-900' : 'bg-emerald-600 text-white hover:bg-emerald-700']"
                @click="nextTab"
              >
                পরবর্তী ধাপ <i class="fa-solid fa-arrow-right"></i>
              </button>
              <button
                v-else
                type="submit"
                class="flex items-center gap-2 px-10 py-2 rounded-md font-bold shadow"
                :class="[isDark ? 'dark:bg-cyan-800 dark:text-white dark:hover:bg-cyan-900' : 'bg-cyan-700 text-white hover:bg-cyan-800']"
              >
                <i class="fa-solid fa-cloud-upload-alt"></i> সংরক্ষণ করুন
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import AdminLayout from '@/components/layout/AdminLayout.vue';
import { ref, onMounted, computed } from 'vue';

import OldStudentPersonalInfo from '@/views/Pages/registraion/components/OldStudentPersonalInfo.vue';
import OldStudentExamInfo from '@/views/Pages/registraion/components/OldStudentExamInfo.vue';
import OldStudentAddressSection from '@/views/Pages/registraion/components/OldStudentAddressSection.vue';
import OldStudentAttachments from '@/views/Pages/registraion/components/OldStudentAttachments.vue';

defineProps({
  roll: String,
  reg_id: String,
  CID: String,
  modelValue: Object
});

// Dark mode detection (via Tailwind's .dark class or custom logic)
const isDark = computed(() => {
  return document.documentElement.classList.contains('dark');
});

// Local state & forms (useForm kept for compatibility but submission is faked)
const pastExamForm = useForm({
  Name: '',
  Father: '',
  Mother: '',
  DateofBirth: '',
  Roll: '',
  reg_id: '',
  CID: '',
  Madrasha: '',
  Markaj: '',
  Class: '',
  Division: ''
});

const currentExamForm = useForm({
  Madrasha: '',
  Markaj: '',
  Class: '',
  student_type: '',
  marhalaId: '',
  irregular_subjects: ''
});

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
  present_division_name: '',
  presernt_DID: '',
  present_district_name: '',
  present_desId: '',
  present_thana_name: '',
  present_TID: '',
  parmanent_division_name: '',
  parmanent_DID: '',
  parmanent_district_name: '',
  parmanent_desId: '',
  parmanent_thana_name: '',
  parmanent_TID: '',
  student_image: '',
});

// File Attachments (fake previews)
const studentPhoto = ref<File | null>(null);
const studentPhotoPreview = ref<string | null>(null);
const nidAttachment = ref<File | null>(null);
const nidAttachmentPreview = ref<string | null>(null);

// Address Data (fake)
type Division = { id: string; Division: string };
type District = { DesID: string; District: string };
type Thana = { Thana_ID: string; Thana: string };

const divisions = ref<Division[]>([]);
const presentDistricts = ref<District[]>([]);
const presentThanas = ref<Thana[]>([]);
const districts = ref<District[]>([]);
const thanas = ref<Thana[]>([]);

const presentFilters = ref({ division: '', district: '', Thana: '' });
const permanentFilters = ref({ division: '', district: '', Thana: '' });

const tabs = [
  'ব্যক্তিগত তথ্য',
  'পরীক্ষার তথ্য',
  'ঠিকানা',
  'সংযুক্তি',
  'শেষ ধাপ'
];
const currentTab = ref(0);
const loading = ref(true);
const fadeIn = ref(false);
const showError = ref(false);
const errorMessage = ref('');

// --- Fake data sources ---
const FAKE_DIVISIONS = [
  { id: '1', Division: 'ঢাকা' },
  { id: '2', Division: 'চট্টগ্রাম' },
  { id: '3', Division: 'রাজশাহী' }
];
const FAKE_DISTRICTS: { [key: string]: { DesID: string; District: string }[] } = {
  '1': [{ DesID: '11', District: 'ঢাকা জেলা' }, { DesID: '12', District: 'গাজীপুর' }],
  '2': [{ DesID: '21', District: 'চট্টগ্রাম জেলা' }],
  '3': [{ DesID: '31', District: 'রাজশাহী জেলা' }]
};
const FAKE_THANAS: { [key: string]: { Thana_ID: string; Thana: string }[] } = {
  '11': [{ Thana_ID: '111', Thana: 'ঢাকা থানা়-১' }, { Thana_ID: '112', Thana: 'ঢাকা থানা়-২' }],
  '12': [{ Thana_ID: '121', Thana: 'গাজীপুর থানা়' }],
  '21': [{ Thana_ID: '211', Thana: 'চট্টগ্রাম থানা়' }],
  '31': [{ Thana_ID: '311', Thana: 'রাজশাহী থানা়' }]
};

const FAKE_STUDENT = {
  pastExam: {
    Name: 'রফিকুল ইসলাম',
    Father: 'আবুল হাসান',
    Mother: 'আকতারুন্নেসা',
    DateofBirth: '2008-02-14',
    Roll: '101',
    reg_id: 'REG-2025-101',
    Madrasha: 'আব্দুল্লাহ মাদরাসা',
    Markaj: 'মারকায-১',
    Class: '8',
    Division: 'জায়্যিদ',
    years: '2025'
  },
  currentExam: {
    Madrasha: 'আব্দুল্লাহ মাদরাসা',
    Markaj: 'মারকায-১',
    Class: '8',
    student_type: 'নিয়মিত',
    marhalaId: '2',
    irregular_subjects: 'নাহ'
  },
  studentInfo: {
    present_division_name: 'ঢাকা',
    presernt_DID: '1',
    present_district_name: 'ঢাকা জেলা',
    present_des_id: '11',
    present_thana_name: 'ঢাকা থানা়-১',
    present_TID: '111',
    parmanent_division_name: 'চট্টগ্রাম',
    parmanent_DID: '2',
    parmanent_district_name: 'চট্টগ্রাম জেলা',
    parmanent_desId: '21',
    parmanent_thana_name: 'চট্টগ্রাম থানা়',
    parmanent_TID: '211'
  }
};

const fakeFetchStudentForEdit = async () => {
  await new Promise((r) => setTimeout(r, 200));
  return FAKE_STUDENT;
};

const fakeFetchDivisions = async () => {
  await new Promise((r) => setTimeout(r, 120));
  return FAKE_DIVISIONS;
};
const fakeFetchDistricts = async (divisionId: string) => {
  await new Promise((r) => setTimeout(r, 120));
  return FAKE_DISTRICTS[divisionId] ?? [];
};
const fakeFetchThanas = async (districtId: string) => {
  await new Promise((r) => setTimeout(r, 120));
  return FAKE_THANAS[districtId] ?? [];
};

const nextTab = () => {
  if (currentTab.value < tabs.length - 1) currentTab.value++;
};
const prevTab = () => {
  if (currentTab.value > 0) currentTab.value--;
};

onMounted(async () => {
  try {
    const response = await fakeFetchStudentForEdit();
    if (response.pastExam) {
      Object.assign(pastExamForm, response.pastExam);
      studentInfoForm.value.name_bn = response.pastExam.Name || '';
      studentInfoForm.value.father_name_bn = response.pastExam.Father || '';
      studentInfoForm.value.mother_name_bn = response.pastExam.Mother || '';
      studentInfoForm.value.past_Roll = response.pastExam.Roll || '';
      studentInfoForm.value.past_reg_id = response.pastExam.reg_id || '';
      studentInfoForm.value.madrasha_name = response.pastExam.Madrasha || '';
      studentInfoForm.value.markaz_name = response.pastExam.Markaj || '';
      studentInfoForm.value.passing_year = response.pastExam.years || '';
      studentInfoForm.value.class = response.pastExam.Class || '';
      studentInfoForm.value.Division = response.pastExam.Division || '';
      studentInfoForm.value.Date_of_birth = response.pastExam.DateofBirth || '';
    }

    if (response.currentExam) {
      Object.assign(currentExamForm, response.currentExam);
      studentInfoForm.value.current_madrasha = response.currentExam.Madrasha || '';
      studentInfoForm.value.current_markaz = response.currentExam.Markaj || '';
      studentInfoForm.value.student_type = response.currentExam.student_type || '';
      studentInfoForm.value.exam_books_name = response.currentExam.irregular_subjects || '';
    }

    if (response.studentInfo) {
      studentInfoForm.value.present_division_name = response.studentInfo.present_division_name || '';
      studentInfoForm.value.presernt_DID = response.studentInfo.presernt_DID || '';
      studentInfoForm.value.present_district_name = response.studentInfo.present_district_name || '';
      studentInfoForm.value.present_desId = response.studentInfo.present_des_id || '';
      studentInfoForm.value.present_thana_name = response.studentInfo.present_thana_name || '';
      studentInfoForm.value.present_TID = response.studentInfo.present_TID || '';
      studentInfoForm.value.parmanent_division_name = response.studentInfo.parmanent_division_name || '';
      studentInfoForm.value.parmanent_DID = response.studentInfo.parmanent_DID || '';
      studentInfoForm.value.parmanent_district_name = response.studentInfo.parmanent_district_name || '';
      studentInfoForm.value.parmanent_desId = response.studentInfo.parmanent_desId || '';
      studentInfoForm.value.parmanent_thana_name = response.studentInfo.parmanent_thana_name || '';
      studentInfoForm.value.parmanent_TID = response.studentInfo.parmanent_TID || '';
      presentFilters.value.division = response.studentInfo.presernt_DID || '';
      presentFilters.value.district = response.studentInfo.present_des_id || '';
      presentFilters.value.Thana = response.studentInfo.present_TID || '';
      permanentFilters.value.division = response.studentInfo.parmanent_DID || '';
      permanentFilters.value.district = response.studentInfo.parmanent_desId || '';
      permanentFilters.value.Thana = response.studentInfo.parmanent_TID || '';
    }
  } catch (err) {
    showError.value = true;
    errorMessage.value = 'ছাত্রের তথ্য লোড করতে সমস্যা হয়েছে (ফেক মোড)।';
    console.error(err);
  }
  divisions.value = await fakeFetchDivisions();

  if (presentFilters.value.division) {
    presentDistricts.value = await fakeFetchDistricts(presentFilters.value.division);
  }
  if (presentFilters.value.district) {
    presentThanas.value = await fakeFetchThanas(presentFilters.value.district);
  }

  if (permanentFilters.value.division) {
    districts.value = await fakeFetchDistricts(permanentFilters.value.division);
  }
  if (permanentFilters.value.district) {
    thanas.value = await fakeFetchThanas(permanentFilters.value.district);
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

const presentHandleDivisionChange = async () => {
  presentFilters.value.district = '';
  presentFilters.value.Thana = '';
  presentDistricts.value = [];
  presentThanas.value = [];
  if (!presentFilters.value.division) return;
  presentDistricts.value = await fakeFetchDistricts(presentFilters.value.division);
};
const presentHandleDistrictChange = async () => {
  presentFilters.value.Thana = '';
  presentThanas.value = [];
  if (!presentFilters.value.district) return;
  presentThanas.value = await fakeFetchThanas(presentFilters.value.district);
};
const handleDivisionChange = async () => {
  permanentFilters.value.district = '';
  permanentFilters.value.Thana = '';
  districts.value = [];
  thanas.value = [];
  if (!permanentFilters.value.division) return;
  districts.value = await fakeFetchDistricts(permanentFilters.value.division);
};
const handleDistrictChange = async () => {
  permanentFilters.value.Thana = '';
  thanas.value = [];
  if (!permanentFilters.value.district) return;
  thanas.value = await fakeFetchThanas(permanentFilters.value.district);
};

const updateFormData = () => {
  if (presentFilters.value.division) {
    const sel = divisions.value.find(d => d.id == presentFilters.value.division);
    if (sel) { studentInfoForm.value.present_division_name = sel.Division; studentInfoForm.value.presernt_DID = sel.id; }
  }
  if (presentFilters.value.district) {
    const sel = presentDistricts.value.find(d => d.DesID == presentFilters.value.district);
    if (sel) { studentInfoForm.value.present_district_name = sel.District; studentInfoForm.value.present_desId = sel.DesID; }
  }
  if (presentFilters.value.Thana) {
    const sel = presentThanas.value.find(t => t.Thana_ID == presentFilters.value.Thana);
    if (sel) { studentInfoForm.value.present_thana_name = sel.Thana; studentInfoForm.value.present_TID = sel.Thana_ID; }
  }
  if (permanentFilters.value.division) {
    const sel = divisions.value.find(d => d.id == permanentFilters.value.division);
    if (sel) { studentInfoForm.value.parmanent_division_name = sel.Division; studentInfoForm.value.parmanent_DID = sel.id; }
  }
  if (permanentFilters.value.district) {
    const sel = districts.value.find(d => d.DesID == permanentFilters.value.district);
    if (sel) { studentInfoForm.value.parmanent_district_name = sel.District; studentInfoForm.value.parmanent_desId = sel.DesID; }
  }
  if (permanentFilters.value.Thana) {
    const sel = thanas.value.find(t => t.Thana_ID == permanentFilters.value.Thana);
    if (sel) { studentInfoForm.value.parmanent_thana_name = sel.Thana; studentInfoForm.value.parmanent_TID = sel.Thana_ID; }
  }
};

const submitStudentInfo = async () => {
  updateFormData();
  if (studentPhotoPreview.value) studentInfoForm.value.student_image = studentPhotoPreview.value;
  if (nidAttachmentPreview.value) studentInfoForm.value.NID_attach = nidAttachmentPreview.value;

  loading.value = true;
  await new Promise((r) => setTimeout(r, 600));
  loading.value = false;
  window.alert('ফেক মোড: ছাত্রের তথ্য সফলভাবে সংরক্ষণ করা হয়েছে (ডেমো)');
};

function useForm<T extends Record<string, unknown>>(arg0: T) {
  return ref({ ...arg0 });
}
</script>

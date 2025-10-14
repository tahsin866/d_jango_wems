<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="mx-auto px-4 py-3 sm:px-6 lg:px-8"
    :class="[!isDark ? 'bg-gray-50 text-gray-200' : 'bg-gray-900 text-gray-200']"
  >
    <div class="rounded-sm mt-5 overflow-hidden"
      :class="[!isDark ? 'bg-white' : 'bg-gray-800']">
      <!-- Stepper Header -->
      <Panel
        :class="[!isDark ? 'bg-gray-800' : 'bg-gray-900']"
        :toggleable="false"
      >
        <template #header>
          <div class="flex items-center gap-4">
            <i class="fa-solid fa-user-graduate text-3xl text-gray-300"></i>
            <h2 class="text-2xl font-bold text-gray-200 tracking-wide">ছাত্র তথ্য সম্পাদনা</h2>
          </div>
        </template>
      </Panel>

      <!-- Progress Bar -->
      <div class="px-8 pt-4">
        <ProgressBar
          :value="(currentTab + 1) / tabs.length * 100"
          :class="isDark ? 'bg-gray-700' : ''"
        ></ProgressBar>

        <Steps v-model:activeStep="currentTab" :model="stepItems" :readonly="true" class="mt-4">
          <template #item="{item, index}">
            <div class="flex flex-col items-center">
              <div
                :class="[
                  'w-8 h-8 flex items-center justify-center rounded-full text-base font-bold transition-all duration-300 shadow',
                  currentTab === index ? 'bg-gray-600 text-white scale-110 shadow-lg ring-2 ring-gray-500' :
                    index < currentTab ? 'bg-gray-500 text-white' :
                    'bg-gray-300 text-gray-600',
                  isDark && (currentTab === index || index < currentTab) ? 'bg-gray-700 text-white' : ''
                ]"
              >{{ index + 1 }}</div>
              <span class="mt-1 text-xs font-medium"
                :class="currentTab === index
                  ? isDark ? 'text-gray-300' : 'text-gray-700'
                  : isDark ? 'text-gray-500' : 'text-gray-500'
              ">{{ item.label }}</span>
            </div>
          </template>
        </Steps>
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
              <Panel header="ব্যক্তিগত তথ্য" :toggleable="false">
                <OldStudentPersonalInfo v-model="studentInfoForm" />
              </Panel>
            </div>

            <div v-if="currentTab === 1" class="fade-in">
              <Panel header="ঠিকানা" :toggleable="false">
                <OldStudentAddressSection
                  :divisions="divisions"
                  :addressFilters="addressFilters"
                  :districts="districts"
                  :thanas="thanas"
                  @update:addressFilters="onUpdateAddressFilters"
                  v-model:studentInfoForm="studentInfoForm"
                />
              </Panel>
            </div>
            <!-- Tab 4: Attachments -->
            <div v-if="currentTab === 2" class="fade-in">
              <Panel header="সংযুক্তি" :toggleable="false">
                <OldStudentAttachments
                  :studentPhoto="studentPhoto"
                  :studentPhotoPreview="studentPhotoPreview"
                  :nidAttachment="nidAttachment"
                  :nidAttachmentPreview="nidAttachmentPreview"
                  @file-upload="handleFileUpload"
                  @remove-file="removeFile"
                />
              </Panel>
            </div>
            <!-- Tab 5: Review & Submit -->
            <div v-if="currentTab === 3" class="fade-in">
              <Panel header="শেষ ধাপ" :toggleable="false">
                <div class="flex items-center gap-2 mb-3">
                  <i class="fa-solid fa-circle-check text-2xl text-gray-500"></i>
                  <span class="text-xl font-semibold" :class="isDark ? 'text-gray-300' : 'text-gray-700'">
                    তথ্য যাচাই ও সংরক্ষণ
                  </span>
                </div>
                <div class="mb-3" :class="isDark ? 'text-gray-400' : 'text-gray-600'">
                  অনুগ্রহ করে পূর্বের সকল তথ্য যাচাই করুন। চাইলে আগের ধাপে ফিরে তথ্য পরিবর্তন করতে পারেন।
                </div>
                <Message severity="info" :closable="false">
                  <i class="fa-solid fa-info-circle mr-2"></i>
                  সকল তথ্য সঠিক থাকলে <b>সংরক্ষণ করুন</b> বাটনে ক্লিক করুন।
                </Message>
              </Panel>
            </div>
          </div>
        </transition>

        <!-- Navigation Buttons -->
        <div class="flex justify-between items-center mt-8">
          <Button
            type="button"
            :label="'পূর্বের ধাপ'"
            icon="fa-solid fa-arrow-left"
            iconPos="left"
            :disabled="currentTab === 0"
            @click="prevTab"
            :class="[isDark ? 'p-button-outlined' : '']"
          />
          <div class="flex gap-2">
            <Button
              v-if="currentTab < tabs.length - 1"
              type="button"
              :label="'পরবর্তী ধাপ'"
              icon="fa-solid fa-arrow-right"
              iconPos="right"
              @click="nextTab"
              :class="[isDark ? 'p-button-outlined' : '']"
            />
            <Button
              v-else
              type="submit"
              :label="'সংরক্ষণ করুন'"
              icon="fa-solid fa-cloud-upload-alt"
              iconPos="left"
              :class="[isDark ? 'p-button-outlined' : '']"
            />
          </div>
        </div>
      </form>
    </div>
  </div>

  </template>

<script setup>
import { watch, ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getCurrentUserId } from '@/stores/userProfile'
import { useToast } from 'primevue/usetoast'

import Button from 'primevue/button'
import Panel from 'primevue/panel'
import ProgressBar from 'primevue/progressbar'
import Steps from 'primevue/steps'
import Message from 'primevue/message'

import OldStudentPersonalInfo from '@/views/Pages/registraion/components/OldStudentPersonalInfo.vue'
import OldStudentAddressSection from '@/views/Pages/registraion/components/OldStudentAddressSection.vue'
import OldStudentAttachments from '@/views/Pages/registraion/components/OldStudentAttachments.vue'

defineProps({
  roll: String,
  reg_id: String,
  CID: String,
  modelValue: Object
})

// Toast setup
const toast = useToast()

// Dark mode detection
const isDark = computed(() => {
  return document.documentElement.classList.contains('dark')
})

// Step items for Steps
const stepItems = computed(() => {
  return tabs.map((tab, index) => ({
    label: tab,
    command: () => { currentTab.value = index }
  }))
})

// Local state & forms
function useForm(obj) {
  return ref({ ...obj })
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
})

// File Attachments
const studentPhoto = ref(null)
const studentPhotoPreview = ref(null)
const nidAttachment = ref(null)
const nidAttachmentPreview = ref(null)

// Address Data
const divisions = ref([])
const districts = ref([])
const thanas = ref([])

const addressFilters = ref({ division: '', district: '', Thana: '' })

// Watch for district change to load thanas
watch(() => addressFilters.value.district, async (newDistrict, oldDistrict) => {
  if (newDistrict && newDistrict !== oldDistrict) {
    await handleDistrictChange()
  }
})

const tabs = [
  'ব্যক্তিগত তথ্য',
  'ঠিকানা',
  'সংযুক্তি',
  'শেষ ধাপ'
]
const currentTab = ref(0)
const loading = ref(true)
const fadeIn = ref(false)

// Flash message system using PrimeVue Toast
const showFlashMessage = (message, type = 'success', options = {}) => {
  const titles = {
    success: 'সফলভাবে সম্পন্ন হয়েছে',
    error: 'সমস্যা হয়েছে',
    warning: 'সতর্কতা',
    info: 'তথ্য'
  }

  toast.add({
    severity: type,
    summary: options.title || titles[type],
    detail: message,
    life: options.duration || 5000,
    closable: options.showCloseButton !== false
  })
}

// Real API functions
const fetchDivisions = async () => {
  const response = await fetch('/api/admin/madrasha/divisions/')
  if (!response.ok) return []
  const data = await response.json()
  return (data.results || []).map(item => ({ id: String(item.did), Division: item.division }))
}
const fetchDistricts = async (divisionId) => {
  const url = divisionId ? `/api/admin/madrasha/districts/?did=${divisionId}` : '/api/admin/madrasha/districts/'
  const response = await fetch(url)
  if (!response.ok) return []
  const data = await response.json()
  return (data.results || []).map(item => ({ DesID: String(item.desid), District: item.district }))
}
const fetchThanas = async (districtId) => {
  const url = districtId ? `/api/admin/madrasha/thanas/?district_id=${districtId}` : '/api/admin/madrasha/thanas/'
  const response = await fetch(url)
  if (!response.ok) return []
  const data = await response.json()
  return (data.results || []).map(item => ({ Thana_ID: String(item.thana_id), Thana: item.thana }))
}

const nextTab = () => {
  if (currentTab.value < tabs.length - 1) currentTab.value++
}
const prevTab = () => {
  if (currentTab.value > 0) currentTab.value--
}

const searchResult = ref(null)

onMounted(async () => {
  // REDIS CACHE SYSTEM: Load session key first, then fallback
  let sessionKey = null

  try {
    const storedSession = sessionStorage.getItem('oldStudentRedisSession')
    if (storedSession) {
      const sessionData = JSON.parse(storedSession)
      if (sessionData.session_key) {
        sessionKey = sessionData.session_key
        searchResult.value = { session_key: sessionKey }
        if (sessionData.student_preview) {
          studentInfoForm.value.name_bn = sessionData.student_preview.student_name_bn || ''
          studentInfoForm.value.father_name_bn = sessionData.student_preview.father_name_bn || ''
        }
      }
    }
  } catch (e) {
    console.warn('Could not load Redis session from sessionStorage:', e)
  }

  // Fallback: Load old search result if no Redis session
  if (!sessionKey) {
    try {
      const storedSearchResult = sessionStorage.getItem('oldStudentSearchResult')
      if (storedSearchResult) {
        searchResult.value = JSON.parse(storedSearchResult)
      }
    } catch (e) {
      console.warn('Could not load search result from sessionStorage:', e)
    }
  }

  // Prefill from sessionStorage (preferred) to avoid showing data in URL
  try {
    const stored = sessionStorage.getItem('oldRegPrefill')
    if (stored) {
      const payload = JSON.parse(stored)
      if (payload.name_bn) studentInfoForm.value.name_bn = payload.name_bn
      if (payload.father_name_bn) studentInfoForm.value.father_name_bn = payload.father_name_bn
      if (payload.Date_of_birth) studentInfoForm.value.Date_of_birth = payload.Date_of_birth
      sessionStorage.removeItem('oldRegPrefill')
    } else {
      // Fallback: Prefill from query params if provided
      const route = useRoute()
      const q = route.query
      const getQ = key => {
        const v = q[key]
        return Array.isArray(v) ? v[0] : (v ?? '')
      }
      const qbName = getQ('name_bn')
      const qfName = getQ('father_name_bn')
      const qDob = getQ('Date_of_birth')
      if (qbName) studentInfoForm.value.name_bn = qbName
      if (qfName) studentInfoForm.value.father_name_bn = qfName
      if (qDob) studentInfoForm.value.Date_of_birth = qDob
    }
  } catch {}

  divisions.value = await fetchDivisions()
  if (addressFilters.value.division) {
    districts.value = await fetchDistricts(addressFilters.value.division)
  }
  if (addressFilters.value.district) {
    thanas.value = await fetchThanas(addressFilters.value.district)
  }
  setTimeout(() => {
    fadeIn.value = true
    loading.value = false
  }, 120)
})

const handleFileUpload = (event, type) => {
  const input = event.target
  const file = input?.files?.[0] ?? null
  if (!file) return

  try {
    if (type === 'studentPhoto') {
      studentPhoto.value = file
      const reader = new FileReader()
      reader.onload = (e) => {
        studentPhotoPreview.value = (e.target?.result ?? null)
      }
      reader.readAsDataURL(file)
      showFlashMessage(`ছাত্রের ছবি আপলোড সফল হয়েছে: ${file.name}`, 'success')
    } else if (type === 'nidAttachment') {
      nidAttachment.value = file
      const reader = new FileReader()
      reader.onload = (e) => {
        nidAttachmentPreview.value = (e.target?.result ?? null)
      }
      reader.readAsDataURL(file)
      showFlashMessage(`এনআইডি সংযুক্তি আপলোড সফল হয়েছে: ${file.name}`, 'success')
    }
  } catch  {
    showFlashMessage('ফাইল আপলোডে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
  }
}

const removeFile = (type) => {
  const fileName = type === 'studentPhoto' ? 'ছাত্রের ছবি' : 'এনআইডি সংযুক্তি'
  if (type === 'studentPhoto') {
    studentPhoto.value = null
    studentPhotoPreview.value = null
  } else if (type === 'nidAttachment') {
    nidAttachment.value = null
    nidAttachmentPreview.value = null
  }
  showFlashMessage(`${fileName} সরিয়ে ফেলা হয়েছে`, 'success')
}

const handleDivisionChange = async () => {
  try {
    addressFilters.value.district = ''
    addressFilters.value.Thana = ''
    districts.value = []
    thanas.value = []
    if (!addressFilters.value.division) return
    districts.value = await fetchDistricts(addressFilters.value.division)
    showFlashMessage('বিভাগ নির্বাচন করা হয়েছে, জেলা লোড হয়েছে', 'success')
  } catch  {
    showFlashMessage('জেলা লোড করতে সমস্যা হয়েছে', 'error')
  }
}
const handleDistrictChange = async () => {
  try {
    addressFilters.value.Thana = ''
    thanas.value = []
    if (!addressFilters.value.district) return
    thanas.value = await fetchThanas(addressFilters.value.district)
    showFlashMessage('জেলা নির্বাচন করা হয়েছে, থানা লোড হয়েছে', 'success')
  } catch  {
    showFlashMessage('থানা লোড করতে সমস্যা হয়েছে', 'error')
  }
}

const updateFormData = () => {
  if (addressFilters.value.division) {
    const sel = divisions.value.find(d => d.id == addressFilters.value.division)
    if (sel) { studentInfoForm.value.division_name = sel.Division; studentInfoForm.value.DID = sel.id }
  }
  if (addressFilters.value.district) {
    const sel = districts.value.find(d => d.DesID == addressFilters.value.district)
    if (sel) { studentInfoForm.value.district_name = sel.District; studentInfoForm.value.desId = sel.DesID }
  }
  if (addressFilters.value.Thana) {
    const sel = thanas.value.find(t => t.Thana_ID == addressFilters.value.Thana)
    if (sel) { studentInfoForm.value.thana_name = sel.Thana; studentInfoForm.value.TID = sel.Thana_ID }
  }
}

const submitStudentInfo = async () => {
  updateFormData()
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
    cid: searchResult.value?.student_basic?.cid ?? studentInfoForm.value.marhala_id,
    srtype: searchResult.value?.student_basic?.srtype ?? null,
    students_type: searchResult.value?.student_basic?.students_type ?? '',
    exam_id: searchResult.value?.student_basic?.exam_id ?? null,
    madrasha_id: searchResult.value?.student_basic?.madrasha_id ?? null,
    irregular_sub: (studentInfoForm.value.irregular_sub === '' || studentInfoForm.value.irregular_sub === null)
      ? null
      : Number(studentInfoForm.value.irregular_sub),
    ip_address: searchResult.value?.student_basic?.ip_address ?? '127.0.0.1',
    created_at: searchResult.value?.student_basic?.created_at ?? new Date().toISOString(),
    updated_at: searchResult.value?.student_basic?.updated_at ?? new Date().toISOString(),
  }
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
  }
  const attachments = {
    birth_no: studentInfoForm.value.BRN_no,
    birth_attach: studentPhotoPreview.value || '',
    nid_no: studentInfoForm.value.NID_no,
    nid_attach: nidAttachmentPreview.value || '',
  }

  loading.value = true

  const currentUserId = getCurrentUserId()
  try {
    const res = await fetch('/api/admin/registration/oldstudent/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_key: searchResult.value?.session_key,
        user_id: currentUserId,
        personal,
        address,
        attachments,
        search_result: searchResult.value?.session_key ? undefined : searchResult.value
      })
    })
    let result = null
    try {
      result = await res.json()
    } catch {
      const text = await res.text()
      loading.value = false
      showFlashMessage('সংরক্ষণ ব্যর্থ: ' + text.slice(0, 300), 'error')
      return
    }
    loading.value = false
    if (res.ok && result.success) {
      const marhalaInfo = `marhala_id: ${result.marhala_id} (${result.marhala_id_source})`
      const madrashaInfo = `madrasha_id: ${result.madrasha_id} (${result.madrasha_id_source})`
      const mappingInfo = ` (${marhalaInfo}, ${madrashaInfo})`

      showFlashMessage(`ছাত্রের তথ্য সফলভাবে সংরক্ষণ করা হয়েছে! রেজিস্ট্রেশন নম্বর: ${result.reg_no}${mappingInfo}`, 'success')
    } else {
      let errorMessage = result.message || result.error || 'Unknown error'
      if (result.code === 'REG_NO_OUT_OF_RANGE') {
        errorMessage = `রেজিস্ট্রেশন নম্বর সমস্যা: ${result.error}. অনুগ্রহ করে আবার চেষ্টা করুন।`
      } else if (result.code === 'DUPLICATE_REGISTRATION') {
        errorMessage = `ডুপ্লিকেট রেজিস্ট্রেশন: এই রেজিস্ট্রেশন নম্বরটি ইতিমধ্যে বিদ্যমান (${result.reg_no})`
      }
      showFlashMessage('সংরক্ষণ ব্যর্থ: ' + errorMessage, 'error')
    }
  } catch (err) {
    loading.value = false
    showFlashMessage('সংরক্ষণ ব্যর্থ: ' + (err instanceof Error ? err.message : String(err)), 'error')
  }
}

// Address filter event handler
async function onUpdateAddressFilters(filters) {
  const prev = { ...addressFilters.value }
  addressFilters.value = {
    division: filters.division ?? '',
    district: filters.district ?? '',
    Thana: filters.Thana ?? ''
  }
  if (addressFilters.value.division !== prev.division) {
    await handleDivisionChange()
  }
}
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

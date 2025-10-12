<script setup>
import { ref, onMounted, reactive,watch } from 'vue'
import { useRoute } from 'vue-router'

import PersonalInfo from '@/views/Pages/registraion/NewStudents/components/PersonalInfoStep.vue'
import AddressInfo from '@/views/Pages/registraion/NewStudents/components/AddressInfoStep.vue'
import AttachmentsInfo from '@/views/Pages/registraion/NewStudents/components/AttachmentsInfo.vue'

import axios from 'axios'

const props = defineProps({
  roll: String,
  reg_id: String,
  CID: String,
  modelValue: Object
})

const route = useRoute()

// Simple toast notification state
const toastMessage = ref('')
const toastType = ref('') // 'success' or 'error'
const showToast = ref(false)

// Simple toast function
const showToastMessage = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true

  // Auto hide after 5 seconds
  setTimeout(() => {
    showToast.value = false
  }, 5000)
}

const currentStep = ref(1)
const examName = ref('')
const marhalaName = ref('')
const currentMarhalaId = ref(null)
const boardOptions = ref([])

// Watch boardOptions changes
watch(boardOptions, (newVal) => {
  console.log('boardOptions changed:', newVal)
  console.log('boardOptions length:', newVal.length)
}, { deep: true })

// Main form state (using reactive instead of useForm)
const studentInfoForm = reactive({
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
  madrasha_id: '',
  class: '',
  Division: '',
  Date_of_birth: '',
  current_madrasha: '',
  current_markaz: '',
  student_type: '',
  current_class: '',
  exam_books_name: '',
  mobile_no: '',
  board_name: '',
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
  NID_attach: null,
  markaz_id: ''
})

// File refs for attachments
const studentPhotoFile = ref(null)
const birthCertificateFile = ref(null)
const marksheetFile = ref(null)

// Load board options from API
const loadBoardOptions = async () => {
  try {
    console.log('Starting to load board options...')
    const response = await axios.get('/api/admin/registration/boards/options/')
    boardOptions.value = response.data
    console.log('Board options loaded:', response.data)
    console.log('boardOptions.value:', boardOptions.value)
  } catch (error) {
    console.error('Error loading board options:', error)
    // Fallback to static options if API fails
    boardOptions.value = [
      { id: 1, name: 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ', value: 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ' },
      { id: 2, name: 'বেফাকুল মাদারিসিল কওমিয়া গওহরডাঙ্গা বাংলাদেশ', value: 'বেফাকুল মাদারিসিল কওমিয়া গওহরডাঙ্গা বাংলাদেশ' },
      { id: 3, name: 'আযাদ দ্বীনি এদারায়ে তালীম বাংলাদেশ', value: 'আযাদ দ্বীনি এদারায়ে তালীম বাংলাদেশ' },
      { id: 4, name: 'তানযীমুল মাদারিসিদ দ্বীনিয়া বাংলাদেশ', value: 'তানযীমুল মাদারিসিদ দ্বীনিয়া বাংলাদেশ' },
      { id: 5, name: 'জাতীয় দ্বীনি মাদরাসা শিক্ষাবোর্ড বাংলাদেশ', value: 'জাতীয় দ্বীনি মাদরাসা শিক্ষাবোর্ড বাংলাদেশ' },
      { id: 6, name: 'আঞ্জুমানে ইত্তেহাদুল মাদারিস বাংলাদেশ', value: 'আঞ্জুমানে ইত্তেহাদুল মাদারিস বাংলাদেশ' }
    ]
    console.log('Using fallback board options:', boardOptions.value)
  }
}

onMounted(async () => {
  const marhalaId = route.params.marhalaId
  currentMarhalaId.value = marhalaId

  try {
    // Fetch marhala info
    const marhalaResponse = await axios.get(`/api/student-registration/${marhalaId}`)
    examName.value = marhalaResponse.data.examName
    marhalaName.value = marhalaResponse.data.marhalaName
    studentInfoForm.current_class = marhalaResponse.data.marhalaName
    studentInfoForm.marhala_id = marhalaId

    // Fetch board options
    await loadBoardOptions()
  } catch (error) {
    console.error("Error fetching data:", error)
  }
})

// Load board options from API


// Step navigation
const gotoStep = (step) => {
  currentStep.value = step
}

// Data update from children
const updatePersonalInfo = (info) => {
  Object.assign(studentInfoForm, info)
}
const updateAddressInfo = (info) => {
  Object.assign(studentInfoForm, info)
}
const updateAttachments = (files) => {
  studentPhotoFile.value = files.studentPhoto
  birthCertificateFile.value = files.birthCertificate
  marksheetFile.value = files.marksheet
}

// Submit main form
const submitStudentInfo = async () => {
  try {
    // Prepare data for new student registration API
    const registrationData = {
      // Personal info
      student_name_bn: studentInfoForm.name_bn || '',
      student_name_ar: studentInfoForm.name_ar || '',
      student_name_en: studentInfoForm.name_en || '',
      father_name_bn: studentInfoForm.father_name_bn || '',
      father_name_ar: studentInfoForm.father_name_ar || '',
      father_name_en: studentInfoForm.father_name_en || '',
      mother_name_bn: studentInfoForm.mother_name_bn || '',
      mother_name_ar: studentInfoForm.mother_name_ar || '',
      mother_name_en: studentInfoForm.mother_name_en || '',
      date_of_birth: studentInfoForm.Date_of_birth || null,
      mobile: studentInfoForm.mobile_no || '',

      // Board info (new fields)
      board_name: studentInfoForm.board_name || '',
      board_id: getBoardIdFromName(studentInfoForm.board_name),
      irregular_year: studentInfoForm.board_year || '',

      // IDs
      marhala_id: currentMarhalaId.value,
      madrasha_id: studentInfoForm.madrasha_id || null,
      markaz_id: studentInfoForm.markaz_id || null,

      // Address (using IDs)
      division_id: studentInfoForm.presernt_DID || '',
      district_id: studentInfoForm.present_desId || '',
      thana_id: studentInfoForm.present_TID || '',

      // Attachments
      birth_no: studentInfoForm.BRN_no || '',
      birth_attach: studentInfoForm.NID_attach || '',
      nid_no: studentInfoForm.NID_no || '',
      nid_attach: studentInfoForm.NID_attach || '',
      marksheet: marksheetFile.value || '',
      student_image: studentPhotoFile.value || '',
    }

    console.log('Submitting registration data:', registrationData)

    // Submit to new student registration API
    const response = await axios.post('/api/admin/registration/newstudent/register/', registrationData, {
      headers: {
        'Content-Type': 'application/json'
      }
    })

    console.log('Registration response:', response.data)

    // Success message
    showToastMessage(`ছাত্রের তথ্য সফলভাবে সংরক্ষণ করা হয়েছে! রেজিস্ট্রেশন নং: ${response.data.reg_no}`, 'success')

  } catch (error) {
    // Error message
    showToastMessage('ছাত্রের তথ্য সংরক্ষণ করতে সমস্যা হয়েছে', 'error')
    console.error('Error saving student information:', error)
  }
}

// Helper function to get board_id from board_name
const getBoardIdFromName = (boardName) => {
  if (!boardName || !boardOptions.value) return null
  const board = boardOptions.value.find(b => b.name === boardName || b.value === boardName)
  return board ? board.id : null
}
</script>

<template>
  <!-- Toast Notification -->
  <div v-if="showToast"
       :class="[
         'fixed top-4 left-4 z-50 p-4 rounded-md shadow-lg max-w-sm',
         toastType === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
       ]">
    <div class="flex items-center justify-between">
      <span>{{ toastMessage }}</span>
      <button @click="showToast = false" class="ml-4 text-white hover:text-gray-200">
        ✕
      </button>
    </div>
  </div>

  <div
  style="font-family: 'SolaimanLipi', sans-serif;"

  class="py-12">
      <div class="sm:px-6 lg:px-8">
        <!-- Step indicator -->
        <div class="mb-6">
          <ul class="flex border-b">
            <li class="mr-1 -mb-px" :class="{ 'border-b-2 border-indigo-500': currentStep === 1 }">
              <a @click="gotoStep(1)" class="bg-white inline-block py-2 px-4 font-medium cursor-pointer"
                 :class="currentStep === 1 ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-800'">
                ব্যক্তিগত তথ্য
              </a>
            </li>
            <li class="mr-1" :class="{ 'border-b-2 border-indigo-500': currentStep === 2 }">
              <a @click="gotoStep(2)" class="bg-white inline-block py-2 px-4 font-medium cursor-pointer"
                 :class="currentStep === 2 ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-800'">
                প্রয়োজনীয় তথ্য ও ঠিকানা
              </a>
            </li>
            <li class="mr-1" :class="{ 'border-b-2 border-indigo-500': currentStep === 3 }">
              <a @click="gotoStep(3)" class="bg-white inline-block py-2 px-4 font-medium cursor-pointer"
                 :class="currentStep === 3 ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-800'">
                সংযুক্তি
              </a>
            </li>
          </ul>
        </div>

        <PersonalInfo
          v-if="currentStep === 1"
          :marhalaName="marhalaName"
          v-model="studentInfoForm"
          @next="gotoStep(2)"
        />

        <AddressInfo
          v-if="currentStep === 2"
          :form="studentInfoForm"
          :boardOptions="boardOptions"
          v-model="studentInfoForm"
          @prev="gotoStep(1)"
          @next="gotoStep(3)"
        />

        <AttachmentsInfo
          v-if="currentStep === 3"
          :form="studentInfoForm"
          :boardOptions="boardOptions"
          @prev="gotoStep(2)"
          @submit="submitStudentInfo"
          @update-files="updateAttachments"
        />
      </div>
    </div>

</template>

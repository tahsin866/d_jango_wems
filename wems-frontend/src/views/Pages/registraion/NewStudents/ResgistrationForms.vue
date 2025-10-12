<script setup>
import { ref, onMounted, reactive,watch } from 'vue'
import { useRoute } from 'vue-router'
import { getCurrentUserId } from '@/stores/userProfile'

import PersonalInfo from '@/views/Pages/registraion/NewStudents/components/PersonalInfoStep.vue'
import AddressInfo from '@/views/Pages/registraion/NewStudents/components/AddressInfoStep.vue'
import AttachmentsInfo from '@/views/Pages/registraion/NewStudents/components/AttachmentsInfo.vue'

import axios from 'axios'

defineProps({
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
  // Personal info (matches model fields)
  student_name_bn: '',
  student_name_ar: '',
  student_name_en: '',
  father_name_bn: '',
  father_name_ar: '',
  father_name_en: '',
  mother_name_bn: '',
  mother_name_ar: '',
  mother_name_en: '',
  date_of_birth: '',
  mobile: '',

  // Document numbers
  birth_no: '',
  nid_no: '',

  // IDs
  marhala_id: '',
  madrasha_id: '',
  markaz_id: '',
  exam_id: '',

  // Board info (NEW FIELDS)
  board_id: '',
  irregular_year: '',
  board_name: '', // For UI binding
  board_year: '',  // For UI binding

  // Address info
  division_id: '',
  district_id: '',
  thana_id: '',

  // Files
  student_image: null,
  marksheet: null,

  // Additional fields for compatibility
  roll_no: '',
  reg_no: '',
  year: '',
  status: 'active',
  students_type: '',
  is_old: 0
})

// Watch for address and board changes in studentInfoForm (after initialization)
watch(() => [studentInfoForm.division_id, studentInfoForm.district_id, studentInfoForm.thana_id, studentInfoForm.board_name, studentInfoForm.board_year], (newValues) => {
  console.log('📍 Parent received address/board data:', {
    division_id: newValues[0],
    district_id: newValues[1],
    thana_id: newValues[2],
    board_name: newValues[3],
    board_year: newValues[4]
  })

  // Update board_id when board_name changes
  if (newValues[3]) {
    studentInfoForm.board_id = getBoardIdFromName(newValues[3])
  }

  // Update irregular_year when board_year changes
  if (newValues[4]) {
    studentInfoForm.irregular_year = newValues[4]
  }
}, { deep: true })// File refs for attachments
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
const updateAttachments = (files) => {
  studentPhotoFile.value = files.studentPhoto
  birthCertificateFile.value = files.birthCertificate
  marksheetFile.value = files.marksheet
}

// Submit main form
const submitStudentInfo = async () => {
  try {
    console.log('Current studentInfoForm before submit:', studentInfoForm)
    console.log('Files - Photo:', studentPhotoFile.value, 'Marksheet:', marksheetFile.value)

    // Create FormData for file uploads
    const formData = new FormData()

    // Personal info
    formData.append('student_name_bn', studentInfoForm.student_name_bn || '')
    formData.append('student_name_ar', studentInfoForm.student_name_ar || '')
    formData.append('student_name_en', studentInfoForm.student_name_en || '')
    formData.append('father_name_bn', studentInfoForm.father_name_bn || '')
    formData.append('father_name_ar', studentInfoForm.father_name_ar || '')
    formData.append('father_name_en', studentInfoForm.father_name_en || '')
    formData.append('mother_name_bn', studentInfoForm.mother_name_bn || '')
    formData.append('mother_name_ar', studentInfoForm.mother_name_ar || '')
    formData.append('mother_name_en', studentInfoForm.mother_name_en || '')

    // Date format conversion to YYYY-MM-DD
    let formattedDate = ''
    if (studentInfoForm.date_of_birth) {
      const date = new Date(studentInfoForm.date_of_birth)
      formattedDate = date.toISOString().split('T')[0] // YYYY-MM-DD format
    }
    formData.append('date_of_birth', formattedDate)
    formData.append('mobile', studentInfoForm.mobile || '')

    // Board info (using board_id and irregular_year from model)
    formData.append('board_id', studentInfoForm.board_id || getBoardIdFromName(studentInfoForm.board_name) || '')
    formData.append('irregular_year', studentInfoForm.irregular_year || studentInfoForm.board_year || '')

    // IDs - marhala_id from route, madrasha_id and markaz_id will be auto-detected by backend
    formData.append('marhala_id', currentMarhalaId.value || '')

    // Get actual user_id from session like OldStudent
    const currentUserId = getCurrentUserId()
    formData.append('user_id', currentUserId || '1') // Use actual user session or fallback to 1
    // Remove madrasha_id and markaz_id - they will be auto-detected from user session

    // Address (using IDs from AddressInfoStep)
    console.log('Address fields to submit:')
    console.log('division_id:', studentInfoForm.division_id)
    console.log('district_id:', studentInfoForm.district_id)
    console.log('thana_id:', studentInfoForm.thana_id)
    console.log('board_name:', studentInfoForm.board_name)
    console.log('board_year:', studentInfoForm.board_year)

    formData.append('division_id', studentInfoForm.division_id || '')
    formData.append('district_id', studentInfoForm.district_id || '')
    formData.append('thana_id', studentInfoForm.thana_id || '')

    // Document numbers
    formData.append('birth_no', studentInfoForm.birth_no || '')
    formData.append('nid_no', studentInfoForm.nid_no || '')
    formData.append('birth_attach', '')
    formData.append('nid_attach', '')

    // File attachments
    if (studentPhotoFile.value) {
      formData.append('student_image', studentPhotoFile.value)
    }
    if (marksheetFile.value) {
      formData.append('marksheet', marksheetFile.value)
    }

    console.log('Submitting FormData with files...')

    // Debug FormData contents
    for (let [key, value] of formData.entries()) {
      console.log(`FormData ${key}:`, value)
    }

    // Submit to new student registration API
    const response = await axios.post('/api/admin/registration/newstudent/register/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    console.log('Registration response:', response.data)

    // Success message
    showToastMessage(`ছাত্রের তথ্য সফলভাবে সংরক্ষণ করা হয়েছে! রেজিস্ট্রেশন নং: ${response.data.reg_no}`, 'success')

  } catch (error) {
    // Error message
    showToastMessage('ছাত্রের তথ্য সংরক্ষণ করতে সমস্যা হয়েছে', 'error')
    console.error('Error saving student information:', error)
    if (error.response) {
      console.error('Error response:', error.response.data)
    }
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

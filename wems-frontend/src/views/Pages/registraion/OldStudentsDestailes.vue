<template>
  <div
  style="font-family: 'SolaimanLipi', sans-serif;"

  class="bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center min-h-screen">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Loading student information...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
        <div class="flex items-center">
          <svg class="h-6 w-6 text-red-400 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h3 class="text-md font-semibold text-red-800">Error loading student data</h3>
            <p class="mt-1 text-md text-red-700">{{ error }}</p>
            <button @click="fetchStudentData(route.params.id)" class="mt-2 text-md text-red-600 underline hover:text-red-800">
              Try again
            </button>
          </div>
        </div>
      </div>

      <!-- Student Data -->
      <div v-else class="bg-white shadow-lg rounded-lg overflow-hidden">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-4">
          <div class="flex items-center justify-between">
            <h1 class="text-2xl font-bold text-white">Student Information</h1>
            <div class="flex items-center space-x-2">
              <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                {{ studentData.status || 'Active' }}
              </span>
              <span v-if="studentData.is_old" class="bg-amber-100 text-amber-800 text-xs font-semibold px-2.5 py-0.5 rounded">
       পুরাতন ছাত্র
              </span>
            </div>
          </div>
        </div>

        <!-- Student Photo and Basic Info -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex flex-col sm:flex-row items-center sm:items-start space-y-4 sm:space-y-0 sm:space-x-6">
            <!-- Student Photo -->
            <div class="flex-shrink-0">
              <img
                :src="studentData.photo || '/placeholder-avatar.png'"
                alt="Student Photo"
                class="h-32 w-32 rounded-full object-cover border-4 border-gray-200"
              >
            </div>

            <!-- Basic Information -->
            <div class="flex-1 text-center sm:text-left">
              <h2 class="text-2xl font-bold text-gray-900">{{ studentData.student_name_bn }}</h2>
              <h3 class="text-lg text-gray-600">{{ studentData.student_name_en }}</h3>
              <h4 class="text-lg text-gray-600" dir="rtl">{{ studentData.student_name_ar }}</h4>

              <div class="mt-3 flex flex-wrap justify-center sm:justify-start gap-2">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-md font-semibold bg-blue-100 text-blue-800">
                  রোন নম্বর: {{ studentData.roll_no }}
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-md font-semibold bg-green-100 text-green-800">
                  রেজিস্ট্রেশন নম্বর: {{ studentData.reg_no }}
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-md font-semibold bg-purple-100 text-purple-800">
                  শিক্ষাবর্ষ: {{ studentData.year }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed Information Tabs -->
        <div class="bg-white">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-4 px-6 border-b-2 font-semibold text-md'
                ]"
              >
                {{ tab.name }}
              </button>
            </nav>
          </div>

          <!-- Tab Content -->
          <div class="p-6">
            <!-- Personal Information Tab -->
            <div v-if="activeTab === 'personal'" class="space-y-6">
              <h3 class="text-lg font-semibold text-gray-900">ব্যক্তিগত তথ্য</h3>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">ছা্ত্রের তথ্য</h4>
                  <dl class="mt-2 space-y-2">
                    <div class="flex justify-between">
                      <dt class="text-md
                      text-gray-600">জন্ম-তারিখ:</dt>
                      <dd class="text-md text-gray-900">{{ formatDate(studentData.date_of_birth) }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">মোবাইল:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.mobile }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">পরীক্ষার্থীর ধরণ:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.students_type }}</dd>
                    </div>
                  </dl>
                </div>

                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">পিতার ইনফরমেশন</h4>
                  <dl class="mt-2 space-y-2">
                    <div>
                      <dt class="text-md font-semibold text-gray-600">পিতার নাম (বাংলা):</dt>
                      <dd class="text-md text-gray-900">{{ studentData.father_name_bn }}</dd>
                    </div>
                    <div>
                      <dt class="text-md font-semibold text-gray-600">পিতার নাম (ইংরেজি):</dt>
                      <dd class="text-md text-gray-900">{{ studentData.father_name_ar }}</dd>
                    </div>
                    <div>
                      <dt class="text-md font-semibold text-gray-600">পিতার নাম (আরবি):</dt>
                      <dd class="text-md text-gray-900" dir="rtl">{{ studentData.father_name_ar }}</dd>
                    </div>
                  </dl>
                </div>

                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">মাতার ইনফরমেশন</h4>
                  <dl class="mt-2 space-y-2">
                    <div>
                      <dt class="text-md font-semibold text-gray-600">Name (BN):</dt>
                      <dd class="text-md text-gray-900">{{ studentData.mother_name_bn }}</dd>
                    </div>
                    <div>
                      <dt class="text-md font-semibold text-gray-600">Name (EN):</dt>
                      <dd class="text-md text-gray-900">{{ studentData.mother_name_en }}</dd>
                    </div>
                    <div>
                      <dt class="text-md font-semibold text-gray-600">Name (AR):</dt>
                      <dd class="text-md text-gray-900" dir="rtl">{{ studentData.mother_name_ar }}</dd>
                    </div>
                  </dl>
                </div>

                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">সিস্টেম ইনফরমেশন</h4>
                  <dl class="mt-2 space-y-2">
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">আইপি এড্রেস:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.ip_address }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Created:</dt>
                      <dd class="text-md text-gray-900">{{ formatDateTime(studentData.created_at) }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Updated:</dt>
                      <dd class="text-md text-gray-900">{{ formatDateTime(studentData.updated_at) }}</dd>
                    </div>
                  </dl>
                </div>
              </div>
            </div>

            <!-- Academic Information Tab -->
            <div v-if="activeTab === 'academic'" class="space-y-6">
              <h3 class="text-lg font-semibold text-gray-900">Academic Information</h3>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">Enrollment Details</h4>
                  <dl class="mt-2 space-y-2">
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Marhala ID:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.marhala_id }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">CID:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.cid }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Srtype:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.srtype }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Exam ID:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.exam_id }}</dd>
                    </div>
                  </dl>
                </div>

                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">Institution Details</h4>
                  <dl class="mt-2 space-y-2">
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Madrasha ID:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.madrasha_id }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Markaz ID:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.markaz_id }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Hijri Year:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.hijri_year }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Bangla Year:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.bangla_year }}</dd>
                    </div>
                  </dl>
                </div>

                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">Academic Status</h4>
                  <dl class="mt-2 space-y-2">
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Status:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.status }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Is Old Student:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.is_old ? 'Yes' : 'No' }}</dd>
                    </div>
                    <div class="flex justify-between">
                      <dt class="text-md font-semibold text-gray-600">Irregular Subjects:</dt>
                      <dd class="text-md text-gray-900">{{ studentData.irregular_sub }}</dd>
                    </div>
                  </dl>
                </div>
              </div>
            </div>

            <!-- NEW: Address & Documents Tab -->
            <div v-if="activeTab === 'address'" class="space-y-6">
              <h3 class="text-lg font-semibold text-gray-900">Address & Documents</h3>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Address Information -->
                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">Contact Address</h4>
                  <dl class="mt-2 space-y-2">
                    <div>
                      <dt class="text-md font-semibold text-gray-600">Division:</dt>
                      <dd class="text-md text-gray-900">{{ studentAddressData.division || 'N/A' }}</dd>
                    </div>
                    <div>
                      <dt class="text-md font-semibold text-gray-600">District:</dt>
                      <dd class="text-md text-gray-900">{{ studentAddressData.district || 'N/A' }}</dd>
                    </div>
                    <div>
                      <dt class="text-md font-semibold text-gray-600">Thana:</dt>
                      <dd class="text-md text-gray-900">{{ studentAddressData.thana || 'N/A' }}</dd>
                    </div>
                    <div>
                      <dt class="text-md font-semibold text-gray-600">Post Office:</dt>
                      <dd class="text-md text-gray-900">{{ studentAddressData.post_office || 'N/A' }}</dd>
                    </div>
                  </dl>
                </div>

                <!-- Document Information -->
                <div>
                  <h4 class="text-md font-semibold text-gray-500 uppercase tracking-wider">Documents & Photos</h4>
                  <div class="mt-2 space-y-4">
                    <!-- Passport -->
                    <div>
                      <dt class="text-md font-semibold text-gray-600">Passport Photo:</dt>
                      <dd class="mt-1">
                        <img
                          v-if="studentAddressData.passport_photo"
                          :src="studentAddressData.passport_photo"
                          alt="Passport Photo"
                          class="h-24 w-24 rounded-lg border border-gray-300 object-cover"
                        >
                        <span v-else class="text-md text-gray-500">No photo available</span>
                      </dd>
                    </div>

                    <!-- Birth Certificate -->
                    <div>
                      <dt class="text-md font-semibold text-gray-600">Birth Certificate No:</dt>
                      <dd class="text-md text-gray-900">{{ studentAddressData.birth_certificate_no || 'N/A' }}</dd>
                      <dt class="text-md font-semibold text-gray-600 mt-2">Birth Certificate Photo:</dt>
                      <dd class="mt-1">
                        <img
                          v-if="studentAddressData.birth_certificate_photo"
                          :src="studentAddressData.birth_certificate_photo"
                          alt="Birth Certificate"
                          class="h-24 w-24 rounded-lg border border-gray-300 object-cover"
                        >
                        <span v-else class="text-md text-gray-500">No photo available</span>
                      </dd>
                    </div>

                    <!-- NID -->
                    <div>
                      <dt class="text-md font-semibold text-gray-600">NID No:</dt>
                      <dd class="text-md text-gray-900">{{ studentAddressData.nid_no || 'N/A' }}</dd>
                      <dt class="text-md font-semibold text-gray-600 mt-2">NID Photo:</dt>
                      <dd class="mt-1">
                        <img
                          v-if="studentAddressData.nid_photo"
                          :src="studentAddressData.nid_photo"
                          alt="NID Photo"
                          class="h-24 w-24 rounded-lg border border-gray-300 object-cover"
                        >
                        <span v-else class="text-md text-gray-500">No photo available</span>
                      </dd>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Actions Tab -->
            <div v-if="activeTab === 'actions'" class="space-y-6">
              <h3 class="text-lg font-semibold text-gray-900">Actions</h3>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button @click="editStudent" class="inline-flex justify-center items-center px-4 py-2 border border-transparent shadow-sm text-md font-semibold rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                  Edit Student
                </button>

                <button @click="downloadPDF" class="inline-flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-md font-semibold rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clip-rule="evenodd" />
                  </svg>
                  Download PDF
                </button>

                <button @click="printCertificate" class="inline-flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-md font-semibold rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                    <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 1 1 0 000 2H6a2 2 0 100 4h2a2 2 0 100 4h2a1 1 0 100 2 2 2 0 01-2 2H6a2 2 0 01-2-2V5z" clip-rule="evenodd" />
                  </svg>
                  Print Certificate
                </button>

                <button @click="deleteRecord" class="inline-flex justify-center items-center px-4 py-2 border border-red-300 shadow-sm text-md font-semibold rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                  <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  Delete Record
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

// Reactive state
const route = useRoute()
const activeTab = ref('personal')
const loading = ref(true)
const error = ref(null)

const tabs = ref([
  { id: 'personal', name: 'Personal Information' },
  { id: 'academic', name: 'Academic Information' },
  { id: 'address', name: 'Address & Documents' },
  { id: 'actions', name: 'Actions' }
])

// Student data as reactive object
const studentData = reactive({})

// Student Address data as reactive object
const studentAddressData = reactive({})


// Methods
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return 'N/A'
  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Date(dateTimeString).toLocaleString(undefined, options)
}

// Action methods
const editStudent = () => {
  console.log('Edit student:', studentData.id)
  // Navigate to edit page or open modal
}

const downloadPDF = () => {
  console.log('Download PDF for student:', studentData.id)
  // Implement PDF download logic
}

const printCertificate = () => {
  console.log('Print certificate for student:', studentData.id)
  // Implement print logic
}

const deleteRecord = () => {
  if (confirm('Are you sure you want to delete this student record?')) {
    console.log('Delete student:', studentData.id)
    // Implement delete logic
  }
}

// Fetch combined student data from API
const fetchStudentData = async (studentId) => {
  try {
    loading.value = true
    error.value = null

    // Get user ID from localStorage or wherever it's stored
    const userId = localStorage.getItem('user_id') || null

    // Fetch combined student data using the new API endpoint
    const response = await axios.get(`/api/registration/${studentId}/`, {
      params: { user_id: userId }
    })

    if (response.data.success) {
      const data = response.data.data

      // Update student data with all fields from the first table
      Object.assign(studentData, {
        id: data.id,
        photo: data.photo,
        student_name_bn: data.student_name_bn,
        student_name_ar: data.student_name_ar,
        student_name_en: data.student_name_en,
        father_name_bn: data.father_name_bn,
        father_name_ar: data.father_name_ar,
        father_name_en: data.father_name_en,
        mother_name_bn: data.mother_name_bn,
        mother_name_ar: data.mother_name_ar,
        mother_name_en: data.mother_name_en,
        roll_no: data.roll_no,
        reg_no: data.reg_no,
        year: data.year,
        date_of_birth: data.date_of_birth,
        mobile: data.mobile,
        status: data.status,
        ip_address: data.ip_address,
        created_at: data.created_at,
        updated_at: data.updated_at,
        marhala_id: data.marhala_id,
        cid: data.cid,
        srtype: data.srtype,
        hijri_year: data.hijri_year,
        bangla_year: data.bangla_year,
        students_type: data.students_type,
        exam_id: data.exam_id,
        madrasha_id: data.madrasha_id,
        markaz_id: data.markaz_id,
        is_old: data.is_old,
        irregular_sub: data.irregular_sub
      })

      // Update address data with fields from the second table
      Object.assign(studentAddressData, {
        division: data.division,
        district: data.district,
        thana: data.thana,
        post_office: data.post_office,
        passport_photo: data.passport_photo,
        birth_certificate_no: data.birth_certificate_no,
        birth_certificate_photo: data.birth_certificate_photo,
        nid_no: data.nid_no,
        nid_photo: data.nid_photo
      })
    } else {
      error.value = response.data.error || 'Failed to fetch student data'
    }
  } catch (err) {
    console.error('Error fetching student data:', err)
    error.value = err.response?.data?.error || 'Failed to fetch student data'
  } finally {
    loading.value = false
  }
}

// Lifecycle hook
onMounted(() => {
  const studentId = route.params.id
  if (studentId) {
    fetchStudentData(studentId)
  } else {
    error.value = 'No student ID provided'
    loading.value = false
  }
})
</script>

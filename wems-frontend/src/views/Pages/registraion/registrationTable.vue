<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import StudentStatsCards from '@/views/Pages/registraion/components/StudentStatsCards.vue'
import StudentSearchWizard from '@/views/Pages/registraion/components/StudentSearchWizard.vue'
import StudentsDataTable from '@/views/Pages/registraion/components/StudentsDataTable.vue'
import { getCurrentUserId } from '@/stores/userProfile'

const students = ref([])
const loading = ref(true)
const error = ref(null)

const filters = ref({
  global: { value: null },
  id: { value: null },
  name_bn: { value: null },
  father_name_bn: { value: null },
  current_madrasha: { value: null },
  exam_name_Bn: { value: null },
  current_class: { value: null },
  Date_of_birth: { value: null },
  student_type: { value: null },
  payment_status: { value: null },
  status: { value: null },
  marhala: { value: null }
})

const studentStats = ref({
  totalStudents: 0,
  boardSubmittedStudents: 0,
  approvedStudents: 0,
  boardReturnedStudents: 0
})

const fetchData = async () => {
  try {
    loading.value = true

    const currentUserId = getCurrentUserId()
    const [studentsRes, statsRes] = await Promise.all([
      axios.get('/api/admin/registration/students/', {
        params: currentUserId ? { user_id: currentUserId } : {}
      }),
      axios.get('/api/admin/registration/students/statistics/', {
        params: currentUserId ? { user_id: currentUserId } : {}
      })
    ])

    const studentsData = studentsRes.data.success ? studentsRes.data.data : studentsRes.data
    const statsData = statsRes.data.success ? statsRes.data.data : statsRes.data

    students.value = studentsData.map(student => ({
      ...student,
      showMenu: false
    }))
    studentStats.value = statsData
  } catch  {
    error.value = 'ডাটা লোড করতে সমস্যা হয়েছে।'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
const refresh = () => fetchData()
</script>

<template>
  <div class="p-4 mt-5 mx-auto">
    <StudentStatsCards :studentStats="studentStats" />
    <StudentSearchWizard v-model:filters="filters" />
    <StudentsDataTable
      :students="students"
      :filters="filters"
      :loading="loading"
      @update:filters="val => {
        Object.keys(val).forEach(key => {
          filters.value[key] = val[key]
        })
      }"
      @refresh="refresh"
    />
  </div>
</template>

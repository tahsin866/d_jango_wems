<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import StudentStatsCards from '@/views/Pages/registraion/components/StudentStatsCards.vue'
import StudentSearchWizard from '@/views/Pages/registraion/components/StudentSearchWizard.vue'
import StudentsDataTable from '@/views/Pages/registraion/components/StudentsDataTable.vue'

const students = ref([]);
const loading = ref(true);
const error = ref<string | null>(null);
interface FilterField {
  value: string | number | null;
}

interface Filters {
  global: FilterField;
  id: FilterField;
  name_bn: FilterField;
  father_name_bn: FilterField;
  current_madrasha: FilterField;
  exam_name_Bn: FilterField;
  current_class: FilterField;
  Date_of_birth: FilterField;
  student_type: FilterField;
  payment_status: FilterField;
  status: FilterField;
  marhala: FilterField;
}

const filters = ref<Filters>({
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
});
const studentStats = ref({
  totalStudents: 0,
  boardSubmittedStudents: 0,
  approvedStudents: 0,
  boardReturnedStudents: 0
});

const fetchData = async () => {
  try {
    loading.value = true;
    const [studentsRes, statsRes] = await Promise.all([
      axios.get('/api/students-registration'),
      axios.get('/api/dashboard/student-stats')
    ]);
    students.value = studentsRes.data.map(student => ({
      ...student,
      showMenu: false
    }));
    studentStats.value = statsRes.data;
  } catch (err) {
    console.error(err);
    error.value = 'ডাটা লোড করতে সমস্যা হয়েছে।';
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);

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
      const filterKey = key as keyof Filters;
      if ((filters.value as Filters)[filterKey]) {
        (filters.value as Filters)[filterKey].value = val[filterKey].value;
      }
    });
  }"
  @refresh="refresh"
/>
    </div>

</template>

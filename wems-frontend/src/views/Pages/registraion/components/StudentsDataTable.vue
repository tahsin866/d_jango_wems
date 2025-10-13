<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="students-data-table bg-white rounded-sm shadow-md border border-gray-200">
    <!-- Clean toolbar with actions and search -->
    <div class="bg-white border-b border-gray-100">
      <!-- Title Section -->
      <div class="px-6 pt-6 pb-4">
        <h2 class="text-xl font-bold text-gray-900 mb-1 flex items-center">
          <i class="pi pi-users mr-2 text-blue-600"></i>
          শিক্ষার্থী তালিকা
        </h2>
        <p class="text-sm text-gray-500">মোট {{ studentsData.length }} জন শিক্ষার্থী</p>
      </div>

      <!-- Toolbar -->
      <div class="px-6 pb-6">
        <Toolbar class="bg-transparent border-0 p-0">
          <template #start>
            <div class="flex items-center gap-3">
              <Button
                icon="pi pi-plus"
                @click="expandAll"
                class="bg-blue-500 hover:bg-blue-600 text-white border-0 rounded-md px-3 py-2 transition-colors"
                v-tooltip="'Expand All'"
              />
              <Button
                icon="pi pi-minus"
                @click="collapseAll"
                class="bg-gray-500 hover:bg-gray-600 text-white border-0 rounded-md px-3 py-2 transition-colors"
                v-tooltip="'Collapse All'"
              />
              <Button
                icon="pi pi-download"
                @click="exportCSV"
                class="bg-green-500 hover:bg-green-600 text-white border-0 rounded-md px-3 py-2 transition-colors"
                v-tooltip="'CSV ডাউনলোড'"
              />
              <Button
                icon="pi pi-send"
                @click="submitAllApplications"
                class="bg-indigo-500 hover:bg-indigo-600 text-white border-0 rounded-md px-3 py-2 transition-colors"
                v-tooltip="'সব দাখিল করুন'"
              />
            </div>
          </template>

          <template #center>
            <div class="flex items-center gap-3">
              <IconField class="w-80">
                <InputIcon class="text-gray-400">
                  <i class="pi pi-search" />
                </InputIcon>
                <InputText
                  v-model="tableFilters['global'].value"
                  placeholder="শিক্ষার্থী অনুসন্ধান করুন..."
                  class="w-full border-gray-300 rounded-md focus:border-blue-500 focus:ring-blue-500"
                />
              </IconField>
            </div>
          </template>

          <template #end>
            <div class="flex items-center gap-3">
              <Button
                icon="pi pi-user-plus"
                label="নতুন নিবন্ধন"
                @click="navigateToNewRegistration"
                class="bg-purple-500 hover:bg-purple-600 text-white border-0 rounded-md px-4 py-2 transition-colors"
                v-tooltip="'নতুন শিক্ষার্থী নিবন্ধন করুন'"
              />
              <Button
                :label="useScrollMode ? 'পেজ ভিউ' : 'স্ক্রল ভিউ'"
                icon="pi pi-list"
                @click="toggleViewMode"
                class="bg-gray-100 hover:bg-gray-200 text-gray-700 border-0 rounded-md px-4 py-2 transition-colors"
                v-tooltip="'View Mode Toggle'"
              />
              <SplitButton
                label="আরও"
                :model="toolbarItems"
                class="bg-gray-100 hover:bg-gray-200 text-gray-700 border-0 rounded-md py-2 px-4"
                size="small"
              />
            </div>
          </template>
        </Toolbar>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <span class="ml-3 text-gray-600">লোড হচ্ছে...</span>
    </div>

    <!-- PrimeVue DataTable -->
    <div v-else class="card border border-surface-200 dark:border-surface-700 rounded-md" style="height: calc(100vh - 300px);">
      <div class="overflow-hidden">
        <DataTable
          v-model:expandedRows="expandedRows"
          v-model:editingRows="editingRows"
          v-model:filters="tableFilters"
          :value="displayStudents"
          dataKey="id"
          editMode="row"
          @rowExpand="onRowExpand"
          @rowCollapse="onRowCollapse"
          @row-edit-save="onRowEditSave"
          tableStyle="min-width: 60rem"
          :scrollable="true"
          scrollHeight="calc(100vh - 400px)"
          :paginator="!useScrollMode"
          :rows="rowsPerPage"
          :rowsPerPageOptions="[10, 25, 50, 100]"
          :paginatorTemplate="'FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown'"
          :currentPageReportTemplate="`মোট {totalRecords} টি রেকর্ডের মধ্যে {first} থেকে {last} দেখানো হচ্ছে`"
          :pageLinkSize="10"
          filterDisplay="menu"
          :globalFilterFields="['name_bn', 'father_name_bn', 'current_madrasha']"
          :pt="{
            table: { style: 'min-width: 60rem' },
            column: {
              bodycell: ({ state }) => ({
                style:  state['d_editing']&&'padding-top: 0.75rem; padding-bottom: 0.75rem'
              })
            },
            rowEditorInitButton: {
              class: 'w-8 h-8 rounded-md text-white bg-blue-500 border-0 mr-1'
            },
            rowEditorSaveButton: {
              class: 'w-8 h-8 rounded-md text-white bg-green-500 border-0 mr-1'
            },
            rowEditorCancelButton: {
              class: 'w-8 h-8 rounded-md text-white bg-red-500 border-0'
            }
          }"
        >

          <Column expander style="width: 5rem" />
          <Column field="id" header="রেজিস্ট্রেশন নং" sortable />
          <Column field="student_image" header="ছবি">
            <template #body="slotProps">
              <div class="flex items-center">
                <div v-if="slotProps.data.student_image" class="h-10 w-10 rounded-full overflow-hidden">
                  <img :src="slotProps.data.student_image" :alt="slotProps.data.name_bn" class="h-full w-full object-cover">
                </div>
                <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                  <i class="pi pi-user text-gray-400"></i>
                </div>
              </div>
            </template>
          </Column>
          <Column field="name_bn" header="নাম" sortable>
            <template #editor="{ data, field }">
              <InputText v-model="data[field]" fluid />
            </template>
          </Column>
          <Column field="father_name_bn" header="পিতার নাম" sortable>
            <template #editor="{ data, field }">
              <InputText v-model="data[field]" fluid />
            </template>
          </Column>
          <Column field="current_madrasha" header="মাদরাসার নাম" sortable>
            <template #editor="{ data, field }">
              <InputText v-model="data[field]" fluid />
            </template>
          </Column>
          <Column field="exam_name_Bn" header="পরীক্ষার নাম" sortable>
            <template #editor="{ data, field }">
              <InputText v-model="data[field]" fluid />
            </template>
          </Column>
          <Column field="current_class" header="মারহালা" sortable filterField="current_class" :showFilterMenu="false">
            <template #editor="{ data, field }">
              <InputText v-model="data[field]" fluid />
            </template>
            <template #filter="{ filterModel, filterCallback }">
              <Select v-model="filterModel.value" @change="filterCallback()" :options="classOptions" optionLabel="label" optionValue="value" placeholder="মারহালা নির্বাচন করুন" style="min-width: 12rem" :showClear="true" />
            </template>
          </Column>
          <Column field="Date_of_birth" header="জন্ম-তারিখ" sortable>
            <template #editor="{ data, field }">
              <InputText v-model="data[field]" fluid />
            </template>
          </Column>
          <Column field="student_type" header="পরীক্ষার্থীর ধরন" sortable filterField="student_type" :showFilterMenu="false">
            <template #editor="{ data, field }">
              <Select v-model="data[field]" :options="studentTypes" optionLabel="label" optionValue="value" placeholder="ধরন নির্বাচন করুন" fluid />
            </template>
            <template #filter="{ filterModel, filterCallback }">
              <Select v-model="filterModel.value" @change="filterCallback()" :options="studentTypes" optionLabel="label" optionValue="value" placeholder="ধরন নির্বাচন করুন" style="min-width: 12rem" :showClear="true" />
            </template>
          </Column>
          <Column field="payment_status" header="পেমেন্ট স্ট্যাটাস" filterField="is_paid" :showFilterMenu="false">
            <template #body="slotProps">
              <Tag
                :value="slotProps.data.is_paid ? 'পরিশোধিত' : 'অপরিশোধিত'"
                :severity="slotProps.data.is_paid ? 'success' : 'danger'"
              />
            </template>
            <template #filter="{ filterModel, filterCallback }">
              <Select v-model="filterModel.value" @change="filterCallback()" :options="paymentStatusOptions" optionLabel="label" optionValue="value" placeholder="পেমেন্ট স্ট্যাটাস" style="min-width: 12rem" :showClear="true">
                <template #option="slotProps">
                  <Tag :value="slotProps.option.label" :severity="slotProps.option.value ? 'success' : 'danger'" />
                </template>
              </Select>
            </template>
          </Column>
          <Column field="status" header="আবেদন অবস্থা" filterField="status" :showFilterMenu="false">
            <template #editor="{ data, field }">
              <Select v-model="data[field]" :options="statuses" optionLabel="label" optionValue="value" placeholder="স্ট্যাটাস নির্বাচন করুন" fluid>
                <template #option="slotProps">
                  <Tag :value="slotProps.option.label" :severity="getStatusSeverity(slotProps.option.value)" />
                </template>
              </Select>
            </template>
            <template #body="slotProps">
              <Tag
                :value="getStatusInBangla(slotProps.data.status)"
                :severity="getStatusSeverity(slotProps.data.status)"
              />
            </template>
            <template #filter="{ filterModel, filterCallback }">
              <Select v-model="filterModel.value" @change="filterCallback()" :options="statuses" optionLabel="label" optionValue="value" placeholder="আবেদন অবস্থা" style="min-width: 12rem" :showClear="true">
                <template #option="slotProps">
                  <Tag :value="slotProps.option.label" :severity="getStatusSeverity(slotProps.option.value)" />
                </template>
              </Select>
            </template>
          </Column>
          <Column :rowEditor="true" style="width: 10%; min-width: 8rem" bodyStyle="text-align:center"></Column>
          <Column header="করনীয়">
            <template #body="slotProps">
              <SplitButton
                :model="getDropdownItems(slotProps.data)"
                label="বিস্তারিত"
                icon="pi pi-eye"
                size="small"
                class="py-2"
                @click="viewStudent(slotProps.data.id)"
              />
            </template>
          </Column>

          <template #expansion="slotProps">
            <div class="p-4">
              <h5 class="text-lg font-semibold mb-4">সাম্প্রতিক কার্যক্রম - {{ slotProps.data.name_bn }}</h5>
              <DataTable
                v-model:editingRows="editingActivityRows"
                :value="slotProps.data.activities || []"
                editMode="row"
                @row-edit-save="(event) => onActivityRowEditSave(event, slotProps.data.id)"
                dataKey="id"
                :pt="{
                  table: { style: 'min-width: 40rem' },
                  column: {
                    bodycell: ({ state }) => ({
                      style:  state['d_editing']&&'padding-top: 0.75rem; padding-bottom: 0.75rem'
                    })
                  },
                  rowEditorInitButton: {
                    class: 'w-8 h-8 rounded-md text-white bg-blue-500 border-0 mr-1'
                  },
                  rowEditorSaveButton: {
                    class: 'w-8 h-8 rounded-md text-white bg-green-500 border-0 mr-1'
                  },
                  rowEditorCancelButton: {
                    class: 'w-8 h-8 rounded-md text-white bg-red-500 border-0'
                  }
                }"
              >
                <Column field="date" header="তারিখ" sortable>
                  <template #editor="{ data, field }">
                    <InputText v-model="data[field]" fluid />
                  </template>
                </Column>
                <Column field="activity" header="কার্যক্রম" sortable>
                  <template #editor="{ data, field }">
                    <InputText v-model="data[field]" fluid />
                  </template>
                </Column>
                <Column field="status" header="অবস্থা" sortable>
                  <template #editor="{ data, field }">
                    <Select v-model="data[field]" :options="activityStatuses" optionLabel="label" optionValue="value" placeholder="অবস্থা নির্বাচন করুন" fluid>
                      <template #option="slotProps">
                        <Tag :value="slotProps.option.label" :severity="getStudentActivitySeverity(slotProps.option.value)" />
                      </template>
                    </Select>
                  </template>
                  <template #body="slotProps">
                    <Tag
                      :value="slotProps.data.status"
                      :severity="getStudentActivitySeverity(slotProps.data.status)"
                    />
                  </template>
                </Column>
                <Column field="action" header="পদক্ষেপ" sortable>
                  <template #editor="{ data, field }">
                    <InputText v-model="data[field]" fluid />
                  </template>
                  <template #body="slotProps">
                    <Button
                      icon="pi pi-search"
                      size="small"
                      variant="text"
                      @click="handleActivityAction(slotProps.data.action)"
                    />
                  </template>
                </Column>
                <Column :rowEditor="true" style="width: 10%; min-width: 8rem" bodyStyle="text-align:center"></Column>
              </DataTable>
            </div>
          </template>

          <template #empty>
            <div class="text-center py-8">
              <i class="pi pi-inbox text-4xl text-gray-400 mb-3"></i>
              <p class="text-gray-600">কোন শিক্ষার্থী পাওয়া যায়নি</p>
            </div>
          </template>
        </DataTable>
      </div>
    </div>

    <!-- Confirmation Dialog -->
    <div v-if="confirmDialog.show" class="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50">
      <div class="bg-white rounded-sm p-6 max-w-md w-full mx-4 shadow-xl border border-gray-200">
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900">{{ confirmDialog.header }}</h3>
          <p class="mt-2 text-gray-600">{{ confirmDialog.message }}</p>
        </div>
        <div class="flex justify-end space-x-3">
          <button
            @click="confirmDialog.show = false"
            class="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            বাতিল
          </button>
          <button
            @click="confirmDialog.accept && confirmDialog.accept()"
            :class="[
              'px-4 py-2 text-white rounded-md transition-colors',
              confirmDialog.type === 'delete'
                ? 'bg-red-600 hover:bg-red-700'
                : 'bg-blue-600 hover:bg-blue-700'
            ]"
          >
            {{ confirmDialog.type === 'delete' ? 'মুছে ফেলুন' : 'নিশ্চিত করুন' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import SplitButton from 'primevue/splitbutton'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Toolbar from 'primevue/toolbar'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import { FilterMatchMode } from '@primevue/core/api'
import 'primeicons/primeicons.css'
import StudentService from '@/services/studentService'
import router from '@/router'
import { getCurrentUserId } from '@/stores/userProfile'

// Props/Emits
const props = defineProps({
  students: Array,
  filters: Object,
  loading: Boolean
})
const emit = defineEmits(['refresh', 'update:filters'])

// Reactive data
const studentsData = ref([])
const error = ref(null)
// const loading = ref(false)
const scrollHeight = ref('400px')

// Load students from API
const loadStudents = async () => {
  // loading.value = true // Using parent prop for loading
  error.value = null

  try {
    const currentUserId = getCurrentUserId()
    const students = await StudentService.getStudents({
      user_id: currentUserId || undefined
    })

    studentsData.value = students
  } catch (err) {
    // Show API error
    error.value = err instanceof Error ? err.message : 'Failed to load students'
    toast.add({
      severity: 'error',
      summary: 'API Error',
      detail: error.value,
      life: 5000
    })
  }
  // finally {
  //   loading.value = false
  // }
}

// Calculate scroll height based on window size
const calculateScrollHeight = () => {
  const windowHeight = window.innerHeight
  const headerHeight = 200
  const footerHeight = 100
  const availableHeight = windowHeight - headerHeight - footerHeight
  scrollHeight.value = Math.max(400, availableHeight) + 'px'
}

onMounted(() => {
  loadStudents()
  calculateScrollHeight()
  window.addEventListener('resize', calculateScrollHeight)
})

onUnmounted(() => {
  window.removeEventListener('resize', calculateScrollHeight)
})

// Filters
const localFilters = ref({ ...(props.filters ?? {}) })
watch(() => props.filters, (val) => { localFilters.value = { ...(val ?? {}) } }, { deep: true })
watch(localFilters, (val) => { emit('update:filters', val) }, { deep: true })

const toast = useToast()
const deleteId = ref(null)

// Row editing
const editingRows = ref([])
const editingActivityRows = ref([])
const statuses = ref([
  { label: 'বোর্ড দাখিল', value: 'submitted' },
  { label: 'অনুমোদিত', value: 'approved' },
  { label: 'বোর্ড ফেরত', value: 'returned' },
  { label: 'পেন্ডিং', value: 'pending' }
])

const studentTypes = ref([
  { label: 'নিয়মিত', value: 'নিয়মিত' },
  { label: 'অনিয়মিত', value: 'অনিয়মিত' }
])

const activityStatuses = ref([
  { label: 'সম্পন্ন', value: 'Completed' },
  { label: 'পেন্ডিং', value: 'Pending' },
  { label: 'পরিশোধিত', value: 'Paid' },
  { label: 'অপরিশোধিত', value: 'Unpaid' },
  { label: 'যাচাইকৃত', value: 'Verified' },
  { label: 'অনুমোদিত', value: 'Approved' }
])

const classOptions = ref([
  { label: '১ম', value: '১ম' },
  { label: '২য়', value: '২য়' },
  { label: '৩য়', value: '৩য়' },
  { label: '৪র্থ', value: '৪র্থ' },
  { label: '৫ম', value: '৫ম' },
  { label: '৬ষ্ঠ', value: '৬ষ্ঠ' },
  { label: '৭ম', value: '৭ম' },
  { label: '৮ম', value: '৮ম' },
  { label: '৯ম', value: '৯ম' },
  { label: '১০ম', value: '১০ম' }
])

const paymentStatusOptions = ref([
  { label: 'পরিশোধিত', value: true },
  { label: 'অপরিশোধিত', value: false }
])

const tableFilters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name_bn: { value: null, matchMode: FilterMatchMode.CONTAINS },
  current_class: { value: null, matchMode: FilterMatchMode.EQUALS },
  student_type: { value: null, matchMode: FilterMatchMode.EQUALS },
  is_paid: { value: null, matchMode: FilterMatchMode.EQUALS },
  status: { value: null, matchMode: FilterMatchMode.EQUALS }
})

const toolbarItems = ref([
  {
    label: 'CSV ডাউনলোড',
    icon: 'pi pi-download',
    command: () => exportCSV()
  },
  {
    label: 'সব দাখিল করুন',
    icon: 'pi pi-send',
    command: () => submitAllApplications()
  },
  {
    separator: true
  },
  {
    label: 'Expand All',
    icon: 'pi pi-plus',
    command: () => expandAll()
  },
  {
    label: 'Collapse All',
    icon: 'pi pi-minus',
    command: () => collapseAll()
  }
])

const getStatusInBangla = (status) => {
  switch (status) {
    case 'submitted': return 'বোর্ড দাখিল'
    case 'approved': return 'অনুমোদিত'
    case 'returned': return 'বোর্ড ফেরত'
    case 'pending': return 'পেন্ডিং'
    default: return 'পেন্ডিং'
  }
}

const confirmDialog = ref({ show: false, type: '', header: '', message: '', accept: null })

// Used in template: openSubmitConfirm, openDeleteConfirm
// Used in template: openDeleteConfirm
const openDeleteConfirm = (event, id) => {
  deleteId.value = id
  confirmDialog.value = {
    show: true,
    type: 'delete',
    header: 'সতর্কীকরণ!',
    message: 'আপনি কি নিশ্চিত যে এই আবেদনটি মুছে ফেলতে চান? এই কাজটি অপরিবর্তনীয়!',
    accept: () => { deleteStudent(); confirmDialog.value.show = false }
  }
}
const getDropdownItems = (data) => [
  { label: 'এডিট', icon: 'pi pi-pencil', command: () => data?.id && editStudent(data.id) },
  { label: 'বিস্তারিত দেখুন', icon: 'pi pi-info-circle', command: () => data?.id && viewStudent(data.id) },
  { separator: true },
  { label: 'মুছে ফেলুন', icon: 'pi pi-trash', command: () => data?.id && openDeleteConfirm(new Event('click'), data.id) }
]

const editStudent = (id) => {
  router.push(`/students/edit/${id}`)
}
const viewStudent = (id) => {
  router.push(`/user/registration/detail/${id}`)
}

const submitAllApplications = () => {
  confirmDialog.value = {
    show: true,
    type: 'submitall',
    header: 'নিশ্চিতকরণ',
    message: 'আপনি কি নিশ্চিত যে আপনি সমস্ত আবেদন বোর্ডে দাখিল করতে চান?',
    accept: () => {
      toast.add({ severity: 'info', summary: 'প্রক্রিয়াকরণ', detail: 'আপনার সমস্ত আবেদন বোর্ডে দাখিল করা হচ্ছে...', life: 3000 })

      StudentService.submitAllApplications()
        .then(() => {
          toast.add({ severity: 'success', summary: 'সফল', detail: 'সকল আবেদন সফলভাবে বোর্ডে দাখিল হয়েছে', life: 5000 })
          emit('refresh')
        })
        .catch((err) => {
          const msg = err && err.message ? `সকল আবেদন দাখিল করতে ব্যর্থ হয়েছে: ${err.message}` : 'সকল আবেদন দাখিল করতে ব্যর্থ হয়েছে'
          toast.add({ severity: 'error', summary: 'ত্রুটি', detail: msg, life: 5000 })
        })

      confirmDialog.value.show = false
    }
  }
}

const exportCSV = () => {
  // displayedColumns and paginatedStudents must be defined in your actual code
  // If not, you need to implement them appropriately
  // This is a placeholder to avoid "never read" errors
  if (!displayedColumns?.value || !paginatedStudents?.value) return
  const header = displayedColumns.value.map(col => col.label).join(',')
  const rows = paginatedStudents.value.map(student => displayedColumns.value.map(col => {
    if (col.field === 'student_image') return student.student_image ? 'Yes' : 'No'
    if (col.field === 'actions') return ''
    return `"${(student[col.field] ?? '').toString().replace(/"/g, '""')}"`
  }).join(','))
  const csvContent = [header, ...rows].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', 'students.csv')
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const expandedRows = ref({})

const onRowExpand = (event) => {
  toast.add({
    severity: 'info',
    summary: 'Student Expanded',
    detail: `${event.data.name_bn} details expanded`,
    life: 2000
  })
}

const onRowCollapse = (event) => {
  toast.add({
    severity: 'success',
    summary: 'Student Collapsed',
    detail: `${event.data.name_bn} details collapsed`,
    life: 2000
  })
}

const expandAll = () => {
  expandedRows.value = displayStudents.value.reduce((acc, student) => {
    acc[student.id] = true
    return acc
  }, {})
  toast.add({
    severity: 'success',
    summary: 'All Expanded',
    detail: 'All student rows expanded',
    life: 2000
  })
}

const collapseAll = () => {
  expandedRows.value = {}
  toast.add({
    severity: 'success',
    summary: 'All Collapsed',
    detail: 'All student rows collapsed',
    life: 2000
  })
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'approved': return 'success'
    case 'submitted': return 'info'
    case 'returned': return 'warning'
    case 'pending': return 'secondary'
    default: return 'secondary'
  }
}

const getStudentActivitySeverity = (status) => {
  switch (status.toLowerCase()) {
    case 'completed':
    case 'paid':
    case 'verified':
    case 'approved':
      return 'success'
    case 'pending':
    case 'unpaid':
      return 'warning'
    default:
      return 'secondary'
  }
}

const handleActivityAction = (action) => {
  toast.add({
    severity: 'info',
    summary: 'Activity Action',
    detail: `Action: ${action}`,
    life: 2000
  })
}

const useScrollMode = ref(false)
const toggleViewMode = () => {
  useScrollMode.value = !useScrollMode.value
}

const rowsPerPage = ref(10)
const displayStudents = computed(() => props.students || studentsData.value)

// To avoid "never read" error, provide default for displayedColumns and paginatedStudents if not present
const displayedColumns = ref([
  { label: 'রেজিস্ট্রেশন নং', field: 'id' },
  { label: 'নাম', field: 'name_bn' },
  { label: 'পিতার নাম', field: 'father_name_bn' },
  { label: 'মাদরাসার নাম', field: 'current_madrasha' },
  { label: 'পরীক্ষার নাম', field: 'exam_name_Bn' },
  { label: 'মারহালা', field: 'current_class' },
  { label: 'জন্ম-তারিখ', field: 'Date_of_birth' },
  { label: 'পরীক্ষার্থীর ধরন', field: 'student_type' },
  { label: 'পেমেন্ট স্ট্যাটাস', field: 'payment_status' },
  { label: 'আবেদন অবস্থা', field: 'status' },
  { label: 'ছবি', field: 'student_image' },
  { label: 'actions', field: 'actions' }
])
const paginatedStudents = computed(() => displayStudents.value.slice(0, rowsPerPage.value))
</script>

<style scoped>
.students-data-table {
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  border-radius: 0.5rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.table-container {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.table-wrapper {
  overflow-x: auto;
  flex: 1;
}

.table-wrapper.scrollable-mode {
  overflow-y: auto;
  max-height: 60vh;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Custom scrollbar for table */
.table-wrapper::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.table-wrapper::-webkit-scrollbar-corner {
  background: #f1f5f9;
}

/* AdminLTE style buttons */
button {
  font-weight: 500;
  border-radius: 0.375rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

button:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Table styling */
table {
  border-collapse: separate;
  border-spacing: 0;
}

thead th {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

tbody tr {
  transition: background-color 0.15s ease-in-out;
}

tbody tr:hover {
  background-color: #f9fafb;
}

/* Dropdown styling */
.relative .absolute {
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Modal styling */
.fixed {
  backdrop-filter: blur(2px);
}

/* Status badges */
.inline-flex {
  font-weight: 600;
  letter-spacing: 0.025em;
}

/* Split button styling */
:deep(.p-splitbutton) {
  height: auto;
  min-height: 2.5rem;
}

:deep(.p-splitbutton .p-button) {
  height: auto;
  min-height: 2.5rem;
  font-size: 0.875rem;
  padding: 0.5rem 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.p-splitbutton .p-splitbutton-dropdown) {
  min-height: 2.5rem;
  padding: 0 0.5rem;
}

:deep(.p-splitbutton .p-menu) {
  min-width: 10rem;
}

/* Ensure regular buttons have consistent height */
:deep(.p-button) {
  min-height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
}

/* Enhanced pagination styling */
:deep(.p-paginator) {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  padding: 0.75rem 1rem;
  margin-top: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

:deep(.p-paginator .p-paginator-pages) {
  display: flex;
  gap: 0.25rem;
}

:deep(.p-paginator .p-paginator-page) {
  min-width: 2.25rem;
  height: 2.25rem;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
  transition: all 0.2s;
  border-radius: 0.25rem;
  font-weight: 500;
}

:deep(.p-paginator .p-paginator-page:hover) {
  background: #f9fafb;
  border-color: #9ca3af;
}

:deep(.p-paginator .p-paginator-page.p-paginator-page-selected) {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
}

:deep(.p-paginator .p-paginator-first),
:deep(.p-paginator .p-paginator-prev),
:deep(.p-paginator .p-paginator-next),
:deep(.p-paginator .p-paginator-last) {
  min-width: 2.25rem;
  height: 2.25rem;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
  transition: all 0.2s;
  border-radius: 0.25rem;
}

:deep(.p-paginator .p-paginator-first:hover),
:deep(.p-paginator .p-paginator-prev:hover),
:deep(.p-paginator .p-paginator-next:hover),
:deep(.p-paginator .p-paginator-last:hover) {
  background: #f9fafb;
  border-color: #9ca3af;
}

:deep(.p-paginator .p-paginator-current) {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
  padding: 0.5rem 0.75rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

:deep(.p-paginator .p-dropdown) {
  min-width: 4rem;
  height: 2.25rem;
}

:deep(.p-paginator .p-dropdown .p-dropdown-label) {
  padding: 0.25rem 0.5rem;
}

/* Responsive pagination */
@media (max-width: 768px) {
  :deep(.p-paginator) {
    padding: 0.5rem;
    gap: 0.25rem;
  }

  :deep(.p-paginator .p-paginator-page) {
    min-width: 2rem;
    height: 2rem;
    font-size: 0.875rem;
  }

  :deep(.p-paginator .p-paginator-current) {
    font-size: 0.875rem;
    padding: 0.25rem 0.5rem;
  }
}



</style>

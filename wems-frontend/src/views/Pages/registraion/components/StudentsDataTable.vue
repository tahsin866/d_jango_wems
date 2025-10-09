<script lang="ts" setup>
import { ref, watch, computed, defineProps, defineEmits } from 'vue';
import { useToast } from 'primevue/usetoast';
import SplitButton from 'primevue/splitbutton';
import axios from 'axios';

// Type declarations
type Student = {
  id: number;
  student_image?: string;
  name_bn: string;
  father_name_bn: string;
  current_madrasha: string;
  exam_name_Bn: string;
  current_class: string;
  Date_of_birth: string;
  student_type: string;
  payment_status: string;
  is_paid: boolean;
  status: string;
};

type FilterType = Record<string, any>;

type Column = {
  label: string;
  field: keyof Student | 'actions';
  fixed: boolean;
};

// Table columns configuration (user can toggle visibility)
const allColumns: Column[] = [
  { label: 'রেজিস্ট্রেশন নং', field: 'id', fixed: true },
  { label: 'ছবি', field: 'student_image', fixed: false },
  { label: 'নাম', field: 'name_bn', fixed: false },
  { label: 'পিতার নাম', field: 'father_name_bn', fixed: false },
  { label: 'মাদরাসার নাম', field: 'current_madrasha', fixed: false },
  { label: 'পরীক্ষার নাম', field: 'exam_name_Bn', fixed: false },
  { label: 'মারহালা', field: 'current_class', fixed: false },
  { label: 'জন্ম-তারিখ', field: 'Date_of_birth', fixed: false },
  { label: 'পরীক্ষার্থীর ধরন', field: 'student_type', fixed: false },
  { label: 'পেমেন্ট স্ট্যাটাস', field: 'payment_status', fixed: false },
  { label: 'আবেদন অবস্থা', field: 'status', fixed: false },
  { label: 'করনীয়', field: 'actions', fixed: true }
];

// Dummy Data
const dummyStudents: Student[] = [
  {
    id: 101,
    student_image: '',
    name_bn: 'রিফাত হোসেন',
    father_name_bn: 'মোঃ মজিবুর রহমান',
    current_madrasha: 'আলিয়া মাদরাসা',
    exam_name_Bn: 'দাখিল',
    current_class: '৯ম',
    Date_of_birth: '২০০৭-০৪-১৫',
    student_type: 'নিয়মিত',
    payment_status: 'Paid',
    is_paid: true,
    status: 'submitted',
  },
  {
    id: 102,
    student_image: '',
    name_bn: 'জান্নাতুল ফেরদৌস',
    father_name_bn: 'শামসুল আলম',
    current_madrasha: 'কামিল মাদরাসা',
    exam_name_Bn: 'ফাজিল',
    current_class: '১০ম',
    Date_of_birth: '২০০৬-০৮-২২',
    student_type: 'নিয়মিত',
    payment_status: 'Unpaid',
    is_paid: false,
    status: 'pending',
  },
  {
    id: 103,
    student_image: '',
    name_bn: 'সাইফুল ইসলাম',
    father_name_bn: 'আলমগীর হোসেন',
    current_madrasha: 'আলিয়া মাদরাসা',
    exam_name_Bn: 'দাখিল',
    current_class: '৯ম',
    Date_of_birth: '২০০৭-০৯-২৫',
    student_type: 'নিয়মিত',
    payment_status: 'Paid',
    is_paid: true,
    status: 'approved',
  },
];

// Props/Emits
const props = defineProps<{
  students?: Student[];
  filters?: FilterType;
  loading?: boolean;
}>();
const emit = defineEmits<{
  (e: 'refresh'): void,
  (e: 'update:filters', val: FilterType): void
}>();

// Filters
const localFilters = ref<FilterType>({ ...(props.filters ?? {}) });
watch(() => props.filters, (val) => { localFilters.value = { ...(val ?? {}) }; }, { deep: true });
watch(localFilters, (val) => { emit('update:filters', val); }, { deep: true });

// Toast
const toast = useToast();
const submitId = ref<number|null>(null);
const deleteId = ref<number|null>(null);

// Column visibility
const visibleColumns = ref<boolean[]>(allColumns.map(col => col.fixed || true));
const displayedColumns = computed(() =>
  allColumns.filter((col, idx) => col.fixed || visibleColumns.value[idx])
);

// Status in Bangla
const getStatusInBangla = (status?: string): string => {
  switch (status) {
    case 'submitted': return 'বোর্ড দাখিল';
    case 'approved': return 'অনুমোদিত';
    case 'returned': return 'বোর্ড ফেরত';
    case 'pending': return 'পেন্ডিং';
    default: return 'পেন্ডিং';
  }
};

// Confirm dialog logic
const confirmDialog = ref<{show:boolean, type:string, header:string, message:string, accept:Function|null}>({
  show: false, type: '', header: '', message: '', accept: null
});
const openSubmitConfirm = (event: Event, id: number) => {
  submitId.value = id;
  confirmDialog.value = {
    show: true,
    type: 'submit',
    header: 'বোর্ড দাখিল করুন',
    message: 'আপনি কি নিশ্চিত যে এই আবেদনটি সাবমিট করতে চান?',
    accept: () => { submitApplication(); confirmDialog.value.show = false; }
  };
};
const openDeleteConfirm = (event: Event, id: number) => {
  deleteId.value = id;
  confirmDialog.value = {
    show: true,
    type: 'delete',
    header: 'সতর্কীকরণ!',
    message: 'আপনি কি নিশ্চিত যে এই আবেদনটি মুছে ফেলতে চান? এই কাজটি অপরিবর্তনীয়!',
    accept: () => { deleteStudent(); confirmDialog.value.show = false; }
  };
};

// Get dropdown menu items
const getDropdownItems = (data: Student) => [
  { label: 'এডিট', icon: 'pi pi-pencil', command: () => editStudent(data.id) },
  { label: 'বিস্তারিত দেখুন', icon: 'pi pi-info-circle', command: () => viewStudent(data.id) },
  { separator: true },
  { label: 'মুছে ফেলুন', icon: 'pi pi-trash', command: (event: Event) => openDeleteConfirm(event, data.id) }
];

// Navigation functions
const editStudent = (id: number) => {
  toast.add({ severity: 'info', summary: 'এডিট', detail: `${id} ছাত্র এডিট হবে (Demo)`, life: 2000 });
};
const viewStudent = (id: number) => {
  toast.add({ severity: 'info', summary: 'বিস্তারিত', detail: `${id} ছাত্র বিস্তারিত দেখানো হবে (Demo)`, life: 2000 });
};

// Action functions
const submitApplication = () => {
  toast.add({ severity: 'success', summary: 'সফল', detail: 'আবেদন সফলভাবে সাবমিট করা হয়েছে', life: 3000 });
  emit('refresh');
};
const deleteStudent = () => {
  toast.add({ severity: 'success', summary: 'সফল', detail: 'আবেদন সফলভাবে মুছে ফেলা হয়েছে', life: 3000 });
  emit('refresh');
};
const submitAllApplications = () => {
  confirmDialog.value = {
    show: true,
    type: 'submitall',
    header: 'নিশ্চিতকরণ',
    message: 'আপনি কি নিশ্চিত যে আপনি সমস্ত আবেদন বোর্ডে দাখিল করতে চান?',
    accept: () => {
      toast.add({ severity: 'info', summary: 'প্রক্রিয়াকরণ', detail: 'আপনার সমস্ত আবেদন বোর্ডে দাখিল করা হচ্ছে...', life: 3000 });
      setTimeout(() => {
        toast.add({ severity: 'success', summary: 'সফল', detail: 'সকল আবেদন সফলভাবে বোর্ডে দাখিল হয়েছে', life: 5000 });
        emit('refresh');
      }, 1200);
      confirmDialog.value.show = false;
    }
  };cd
};

// CSV Export
const exportCSV = () => {
  const header = displayedColumns.value.map(col => col.label).join(',');
  const rows = paginatedStudents.value.map(student => displayedColumns.value.map(col => {
    if (col.field === 'student_image') return student.student_image ? 'Yes' : 'No';
    if (col.field === 'actions') return '';
    // @ts-ignore
    return `"${(student[col.field] ?? '').toString().replace(/"/g, '""')}"`;
  }).join(','));
  const csvContent = [header, ...rows].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.setAttribute('download', 'students.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Pagination
const page = ref(1);
const rowsPerPage = ref(10);
const studentsData = computed(() => props.students && props.students.length > 0 ? props.students : dummyStudents);
const paginatedStudents = computed<Student[]>(() => {
  const start = (page.value - 1) * rowsPerPage.value;
  const end = start + rowsPerPage.value;
  return studentsData.value.slice(start, end);
});
const totalPages = computed(() => Math.ceil(studentsData.value.length / rowsPerPage.value));
const goToPage = (p: number) => { if (p > 0 && p <= totalPages.value) page.value = p; };
watch(() => studentsData.value, () => { page.value = 1; });

// Column toggler modal
const showColumnToggler = ref(false);
</script>

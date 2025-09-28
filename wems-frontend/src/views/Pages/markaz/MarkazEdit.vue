<script setup lang="ts">
import 'primeicons/primeicons.css';
import { ref, computed, watch, onMounted } from 'vue'
import axios from '@/utils/axios'
import { useRoute, useRouter } from 'vue-router';

// Import your components
import CategorySelect from '@/views/Pages/markaz/Edit/CategorySelect.vue'
import MainMadrasaInfo from '@/views/Pages/markaz/Edit/MainMadrasaInfo.vue'
import DynamicMadrasas from '@/views/Pages/markaz/Edit/DynamicMadrasas.vue'
import RequirementsSection from '@/views/Pages/markaz/Edit/RequirementsSection.vue'
import AttachmentSection from '@/views/Pages/markaz/Edit/AttachmentSection.vue'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Button from 'primevue/button'

const route = useRoute();
const router = useRouter();
const id = route.params.id;
const success = ref(false);
const error = ref('');
const step = ref(0)
const loading = ref(false);
const formErrors = ref<string[]>([]);
const validationErrors = ref<Record<string, string>>({});
const conditionsAgreed = ref(false);

// Dummy user data, replace with actual authentication logic if needed
const user_id = 1;
const user_name = "Demo Madrasha";
const exam_id = "";
const exam_name = "";

const form = ref<{
  user_id: number,
  user_name: string,
  exam_id: string,
  exam_name: string,
  markaz_type: string,
  fazilat: string,
  sanabiya_ulya: string,
  sanabiya: string,
  mutawassita: string,
  ibtedaiyyah: string,
  hifzul_quran: string,
  qirat: string,
  noc_file: File | Blob | null,
  resolution_file: File | Blob | null,
  noc_file_path: string,
  resolution_file_path: string,
  requirements: string,
  muhtamim_consent: File | Blob | null,
  president_consent: File | Blob | null,
  committee_resolution: File | Blob | null,
  associated_madrasas: any[],
  attachments: any[],
  status: string
}>({
  user_id: user_id,
  user_name: user_name,
  exam_id: exam_id,
  exam_name: exam_name,
  markaz_type: "",
  fazilat: '',
  sanabiya_ulya: '',
  sanabiya: '',
  mutawassita: '',
  ibtedaiyyah: '',
  hifzul_quran: '',
  qirat: '',
  noc_file: null,
  resolution_file: null,
  noc_file_path: '',
  resolution_file_path: '',
  requirements: '',
  muhtamim_consent: null,
  president_consent: null,
  committee_resolution: null,
  associated_madrasas: [],
  attachments: [],
  status: ''
})

// Track deleted associated madrasa IDs
const deletedMadrasaIds = ref<number[]>([]);

const rows = ref([{
    id: null, // Add id to track existing records
    fazilat: null,
    sanabiya_ulya: null,
    sanabiya: null,
    mutawassita: null,
    ibtedaiyyah: null,
    hifzul_quran: null,
    qirat: null,
    madrasa_Name: "",
    madrasa_id: "",
    searchQuery: "",
    isOpen: false,
    files: {
        noc: null as File | Blob | null,
        nocPreview: null as string | null,
        resolution: null as File | Blob | null,
        resolutionPreview: null as string | null
    }
}])

const addRow = () => {
    rows.value.push({
        id: null,
        fazilat: null,
        sanabiya_ulya: null,
        sanabiya: null,
        mutawassita: null,
        ibtedaiyyah: null,
        hifzul_quran: null,
        qirat: null,
        madrasa_Name: "",
        madrasa_id: "",
        searchQuery: "",
        isOpen: false,
        files: {
            noc: null,
            nocPreview: null,
            resolution: null,
            resolutionPreview: null
        }
    })
}

const removeRow = (index: number) => {
    if (rows.value.length > 1) {
        const row = rows.value[index];
        if (row.id) {
            deletedMadrasaIds.value.push(row.id);
        }
        rows.value.splice(index, 1);
    }
}


// Watch for changes in rows and update form.value.associated_madrasas
watch(rows, (newRows) => {
  form.value.associated_madrasas = newRows.map(row => ({
    id: row.id,
    madrasa_id: row.madrasa_id,
    madrasa_name: row.madrasa_Name || row.searchQuery,
    fazilat: row.fazilat,
    sanabiya_ulya: row.sanabiya_ulya,
    sanabiya: row.sanabiya,
    mutawassita: row.mutawassita,
    ibtedaiyyah: row.ibtedaiyyah,
    hifzul_quran: row.hifzul_quran,
    qirat: row.qirat,
    noc_file: row.files.noc,
    resolution_file: row.files.resolution,
    noc_file_path: row.files.noc ? row.files.noc.name : (row.noc_file_path || ''),
    resolution_file_path: row.files.resolution ? row.files.resolution.name : (row.resolution_file_path || '')
  }));
}, { deep: true });
function handleAttachmentEdit(e, idx) {
  const file = e.target.files[0];
  if (file) {
    form.value.attachments[idx].new_file = file;
  }
}

const handleFileUpload = (file: any, type: string, index: number) => {
    try {
        if (file instanceof File || file instanceof Blob) {
            if (type === 'noc') {
                rows.value[index].files.noc = file;
                rows.value[index].files.nocPreview = URL.createObjectURL(file);
            } else {
                rows.value[index].files.resolution = file;
                rows.value[index].files.resolutionPreview = URL.createObjectURL(file);
            }
            return;
        }

        let extractedFile = null;

        if (file && file.files && file.files.length > 0) {
            extractedFile = file.files[0];
        } else if (file && file.target && file.target.files && file.target.files.length > 0) {
            extractedFile = file.target.files[0];
        } else if (file && file.originalEvent && file.originalEvent.target &&
                  file.originalEvent.target.files && file.originalEvent.target.files.length > 0) {
            extractedFile = file.originalEvent.target.files[0];
        }

        if (extractedFile) {
            if (type === 'noc') {
                rows.value[index].files.noc = extractedFile;
                rows.value[index].files.nocPreview = URL.createObjectURL(extractedFile);
            } else {
                rows.value[index].files.resolution = extractedFile;
                rows.value[index].files.resolutionPreview = URL.createObjectURL(extractedFile);
            }
        } else {
            console.error('No file found in event:', file);
        }
    } catch (error) {
        console.error('Error in handleFileUpload:', error);
    }
}

const removeFile = (type: string, index: number) => {
    if (type === 'noc') {
        rows.value[index].files.noc = null
        rows.value[index].files.nocPreview = null
    } else {
        rows.value[index].files.resolution = null
        rows.value[index].files.resolutionPreview = null
    }
}

const nocFileForMadrahsa = ref<File | Blob | null>(null)
const nocPreviewForMadrahsa = ref<string | null>(null)
const resolutionFileForMadrahsa = ref(null)
const resolutionPreviewForMadrahsa = ref(null)
const muhtamimFile = ref<File | Blob | null>(null)
const muhtamimPreview = ref<string | null>(null)
const presidentFile = ref<File | Blob | null>(null)
const presidentPreview = ref<string | null>(null)
const committeeFile = ref<File | Blob | null>(null)
const committeePreview = ref<string | null>(null)

const handleFileUploadMumtahin = (event: Event | File | Blob, type: string) => {
  try {
    if (event instanceof File || event instanceof Blob) {
      switch (type) {
        case 'muhtamim':
          muhtamimFile.value = event;
          muhtamimPreview.value = URL.createObjectURL(event);
          break;
        case 'president':
          presidentFile.value = event;
          presidentPreview.value = URL.createObjectURL(event);
          break;
        case 'committee':
          committeeFile.value = event;
          committeePreview.value = URL.createObjectURL(event);
          break;
      }
      return;
    }
    let file: File | null = null;
    const input = event as HTMLInputElement;
    if (input && input.files && input.files.length > 0) {
      file = input.files[0];
    } else if ((event as any).target && (event as any).target.files && (event as any).target.files.length > 0) {
      file = (event as any).target.files[0];
    }

    if (!file) {
      console.error('No file found in event:', event);
      return;
    }

    switch (type) {
      case 'muhtamim':
        muhtamimFile.value = file;
        muhtamimPreview.value = URL.createObjectURL(file);
        break;
      case 'president':
        presidentFile.value = file;
        presidentPreview.value = URL.createObjectURL(file);
        break;
      case 'committee':
        committeeFile.value = file;
        committeePreview.value = URL.createObjectURL(file);
        break;
    }
  } catch (error) {
    console.error('Error in handleFileUploadMumtahin:', error);
  }
}

const removeFileMumtahin = (type: string) => {
    switch (type) {
        case 'muhtamim':
            muhtamimFile.value = null
            muhtamimPreview.value = null
            break
        case 'president':
            presidentFile.value = null
            presidentPreview.value = null
            break
        case 'committee':
            committeeFile.value = null
            committeePreview.value = null
            break
    }
}

const handleFileUploadForMadrahsa = (file: any, type: string) => {
    try {
        if (file instanceof File || file instanceof Blob) {
            if (type === 'noc') {
                form.value.noc_file = file;
                nocFileForMadrahsa.value = file;
                nocPreviewForMadrahsa.value = URL.createObjectURL(file);
            } else {
                form.value.resolution_file = file;
                resolutionFileForMadrahsa.value = file;
                resolutionPreviewForMadrahsa.value = URL.createObjectURL(file);
            }
            return;
        }

        let extractedFile = null;

        if (file && file.files && file.files.length > 0) {
            extractedFile = file.files[0];
        } else if (file && file.target && file.target.files && file.target.files.length > 0) {
            extractedFile = file.target.files[0];
        } else if (file && file.originalEvent && file.originalEvent.target &&
                  file.originalEvent.target.files && file.originalEvent.target.files.length > 0) {
            extractedFile = file.originalEvent.target.files[0];
        }

        if (extractedFile) {
            if (type === 'noc') {
                form.value.noc_file = extractedFile;
                nocFileForMadrahsa.value = extractedFile;
                nocPreviewForMadrahsa.value = URL.createObjectURL(extractedFile);
            } else {
                form.value.resolution_file = extractedFile;
                resolutionFileForMadrahsa.value = extractedFile;
                resolutionPreviewForMadrahsa.value = URL.createObjectURL(extractedFile);
            }
        } else {
            console.error('No file found in event:', file);
        }
    } catch (error) {
        console.error('Error in handleFileUploadForMadrahsa:', error);
    }
}

const removeFileForMadrahsa = (type: string) => {
    if (type === 'noc') {
        nocFileForMadrahsa.value = null
        nocPreviewForMadrahsa.value = null
        form.value.noc_file = null
    } else {
        resolutionFileForMadrahsa.value = null
        resolutionPreviewForMadrahsa.value = null
        form.value.resolution_file = null
    }
}

// Madrasha data from API
interface MadrashaType {
  id?: number | string;
  name?: string;
  ElhaqNo?: string | number;
}

const madrashas = ref<MadrashaType[]>([]);

const filteredOptions = computed(() => (row) => {
  if (!row.searchQuery) return [];
  return madrashas.value.filter(madrasha => {
    const name = (madrasha.name || '').toLowerCase();
    const elhaqNo = (madrasha.elhaqno || '').toString().toLowerCase();
    const searchQuery = row.searchQuery.toLowerCase().trim();
    return name.includes(searchQuery) || elhaqNo.includes(searchQuery);
  });
});


const selectOption = (madrasha: any, row: any) => {
    row.madrasa_Name = madrasha.name;
    row.madrasa_id = madrasha.id;
    row.isOpen = false;
};

watch(() => form.value.markaz_type, (newType) => {
  if (newType === 'দরসিয়াত') {
    form.value.hifzul_quran = '';
    form.value.qirat = '';
  } else if (newType === 'তাহফিজুল কোরআন') {
    form.value.fazilat = '';
    form.value.sanabiya_ulya = '';
    form.value.sanabiya = '';
    form.value.mutawassita = '';
    form.value.ibtedaiyyah = '';
    form.value.qirat = '';
  } else if (newType === 'কিরাআত') {
    form.value.fazilat = '';
    form.value.sanabiya_ulya = '';
    form.value.sanabiya = '';
    form.value.mutawassita = '';
    form.value.ibtedaiyyah = '';
    form.value.hifzul_quran = '';
  }
  rows.value.forEach(row => {
    if (newType === 'দরসিয়াত') {
      row.hifzul_quran = '';
      row.qirat = '';
    } else if (newType === 'তাহফিজুল কোরআন') {
      row.fazilat = '';
      row.sanabiya_ulya = '';
      row.sanabiya = '';
      row.mutawassita = '';
      row.ibtedaiyyah = '';
      row.qirat = '';
    } else if (newType === 'কিরাআত') {
      row.fazilat = '';
      row.sanabiya_ulya = '';
      row.sanabiya = '';
      row.mutawassita = '';
      row.ibtedaiyyah = '';
      row.hifzul_quran = '';
    }
  });
});

const getCurrentDateTime = () => {
    return "2025-07-22 09:17:27";
}

const getCurrentUser = () => {
    return "tahsin866";
}

const stepLabels = [
    { label: "শর্তাবলী", icon: "pi pi-info-circle" },
    { label: "ধরন ও মূল তথ্য", icon: "pi pi-file-edit" },
    { label: "সংযুক্ত মাদ্রাসা", icon: "pi pi-building" },
    { label: "প্রয়োজনীয়তা ও সংযুক্তি", icon: "pi pi-paperclip" }
];

const getStepIcon = (index: number) => {
    return step.value === index ? "pi pi-spin pi-spinner text-gray-700" : "pi pi-circle-fill text-gray-400";
};

// Only ONE declaration for canAccessStep: here always all steps accessible
const canAccessStep = computed(() => ({ 0: true, 1: true, 2: true, 3: true }));

const getStepCompletionPercentage = computed(() => 100);

const handleTabChange = (event: any) => {
    if (event && typeof event.index === 'number') {
        step.value = event.index;
    }
};
const goToNextStep = () => {
    step.value = step.value + 1;
};

onMounted(async () => {
  try {
    const res = await axios.get(`/api/markaz/full-detail/${id}/`);
    if (res.data && res.data.data) {
      const app = res.data.data.markaz_application || {};
      const main = res.data.data.main_madrasa_info || {};
      const associated = res.data.data.associated_madrasas || [];
      const attachments = res.data.data.attachments || [];
      form.value.markaz_type = app.markaz_type || '';
      form.value.requirements = app.requirements || '';
      form.value.exam_id = app.exam || '';
      form.value.user_id = app.user || '';
      form.value.status = app.status || '';
      form.value.fazilat = main.fazilat ?? '';
      form.value.sanabiya_ulya = main.sanabiya_ulya ?? '';
      form.value.sanabiya = main.sanabiya ?? '';
      form.value.mutawassita = main.mutawassita ?? '';
      form.value.ibtedaiyyah = main.ibtedaiyyah ?? '';
      form.value.hifzul_quran = main.hifzul_quran ?? '';
      form.value.qirat = main.qirat ?? '';
      form.value.noc_file_path = main.noc_file_path ?? '';
      form.value.resolution_file_path = main.resolution_file_path ?? '';
      form.value.associated_madrasas = associated.map(row => ({
        ...row,
        fazilat: row.fazilat !== undefined && row.fazilat !== null ? Number(row.fazilat) : null,
        sanabiya_ulya: row.sanabiya_ulya !== undefined && row.sanabiya_ulya !== null ? Number(row.sanabiya_ulya) : null,
        sanabiya: row.sanabiya !== undefined && row.sanabiya !== null ? Number(row.sanabiya) : null,
        mutawassita: row.mutawassita !== undefined && row.mutawassita !== null ? Number(row.mutawassita) : null,
        ibtedaiyyah: row.ibtedaiyyah !== undefined && row.ibtedaiyyah !== null ? Number(row.ibtedaiyyah) : null,
        hifzul_quran: row.hifzul_quran !== undefined && row.hifzul_quran !== null ? Number(row.hifzul_quran) : null,
        qirat: row.qirat !== undefined && row.qirat !== null ? Number(row.qirat) : null
      }));
      form.value.attachments = attachments;
        // Sync rows.value with associated madrasas for DynamicMadrasas.vue
        rows.value = associated.map(row => ({
          id: row.id,
          searchQuery: row.madrasa_name || '', // Use backend-provided madrasa_name
          madrasa_id: row.madrasa_id ?? null,
          fazilat: row.fazilat !== undefined && row.fazilat !== null ? Number(row.fazilat) : null,
          sanabiya_ulya: row.sanabiya_ulya !== undefined && row.sanabiya_ulya !== null ? Number(row.sanabiya_ulya) : null,
          sanabiya: row.sanabiya !== undefined && row.sanabiya !== null ? Number(row.sanabiya) : null,
          mutawassita: row.mutawassita !== undefined && row.mutawassita !== null ? Number(row.mutawassita) : null,
          ibtedaiyyah: row.ibtedaiyyah !== undefined && row.ibtedaiyyah !== null ? Number(row.ibtedaiyyah) : null,
          hifzul_quran: row.hifzul_quran !== undefined && row.hifzul_quran !== null ? Number(row.hifzul_quran) : null,
          qirat: row.qirat !== undefined && row.qirat !== null ? Number(row.qirat) : null,
          selectedMadrasha: null,
          isOpen: false,
          files: {
            noc: null,
            nocPreview: null,
            resolution: null,
            resolutionPreview: null
          }
        }));
    }
  } catch (e) {
    error.value = 'ডাটা লোড করা যায়নি';
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/markaz/search-madrasa/');
    if (response.ok) {
      const data = await response.json();
      madrashas.value = data.map((item: any) => ({
        id: item.id,
        name: item.mname,
        elhaqno: item.elhaqno || item.ElhaqNo || item.elhaq || '',
      }));
    }
  } catch (error) {
    console.error('Failed to fetch madrashas:', error);
  }
});

// In MarkazEdit.vue, update the updateForm function

const updateForm = async () => {
  error.value = '';
  success.value = false;
  loading.value = true;
  try {
    const formData = new FormData();

    // Helper function to safely stringify JSON
    const safeStringify = (obj) => {
      try {
        return JSON.stringify(obj);
      } catch (e) {
        console.error("Error stringifying JSON:", e);
        return "{}";
      }
    };

    // Markaz Application data
    formData.append('markaz_application', safeStringify({
      markaz_type: form.value.markaz_type,
      requirements: form.value.requirements,
      exam: form.value.exam_id,
      user: form.value.user_id,
      status: form.value.status,
    }));

    // Main Madrasa Info
    formData.append('main_madrasa_info', safeStringify({
      fazilat: form.value.fazilat !== '' ? Number(form.value.fazilat) : null,
      sanabiya_ulya: form.value.sanabiya_ulya !== '' ? Number(form.value.sanabiya_ulya) : null,
      sanabiya: form.value.sanabiya !== '' ? Number(form.value.sanabiya) : null,
      mutawassita: form.value.mutawassita !== '' ? Number(form.value.mutawassita) : null,
      ibtedaiyyah: form.value.ibtedaiyyah !== '' ? Number(form.value.ibtedaiyyah) : null,
      hifzul_quran: form.value.hifzul_quran !== '' ? Number(form.value.hifzul_quran) : null,
      qirat: form.value.qirat !== '' ? Number(form.value.qirat) : null,
      noc_file_path: form.value.noc_file_path,
      resolution_file_path: form.value.resolution_file_path,
    }));

    // Associated Madrasas
    const associatedMadrasas = form.value.associated_madrasas.map(row => ({
      id: row.id,
      madrasa_id: row.madrasa_id,
      madrasa_name: row.madrasa_name,
      fazilat: row.fazilat !== '' && row.fazilat !== null ? Number(row.fazilat) : null,
      sanabiya_ulya: row.sanabiya_ulya !== '' && row.sanabiya_ulya !== null ? Number(row.sanabiya_ulya) : null,
      sanabiya: row.sanabiya !== '' && row.sanabiya !== null ? Number(row.sanabiya) : null,
      mutawassita: row.mutawassita !== '' && row.mutawassita !== null ? Number(row.mutawassita) : null,
      ibtedaiyyah: row.ibtedaiyyah !== '' && row.ibtedaiyyah !== null ? Number(row.ibtedaiyyah) : null,
      hifzul_quran: row.hifzul_quran !== '' && row.hifzul_quran !== null ? Number(row.hifzul_quran) : null,
      qirat: row.qirat !== '' && row.qirat !== null ? Number(row.qirat) : null,
      noc_file_path: row.noc_file_path,
      resolution_file_path: row.resolution_file_path
    }));

    formData.append('associated_madrasas', safeStringify(associatedMadrasas));
    formData.append('deleted_madrasa_ids', safeStringify(deletedMadrasaIds.value));

    // Attachments
    formData.append('attachments', safeStringify(form.value.attachments));

    // Files for main madrasa
    if (form.value.noc_file) {
      formData.append('noc_file', form.value.noc_file);
    }
    if (form.value.resolution_file) {
      formData.append('resolution_file', form.value.resolution_file);
    }

    // Files for associated madrasas
    form.value.associated_madrasas.forEach((row) => {
      if (row.noc_file instanceof File) {
        formData.append(`noc_file_${row.id}`, row.noc_file);
      }
      if (row.resolution_file instanceof File) {
        formData.append(`resolution_file_${row.id}`, row.resolution_file);
      }
    });

    // Other attachments
    if (form.value.muhtamim_consent) {
      formData.append('muhtamim_consent', form.value.muhtamim_consent);
    }
    if (form.value.president_consent) {
      formData.append('president_consent', form.value.president_consent);
    }
    if (form.value.committee_resolution) {
      formData.append('committee_resolution', form.value.committee_resolution);
    }

    await axios.put(`/api/markaz/edit/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    success.value = true;
    alert('আপডেট সফল হয়েছে!');
    deletedMadrasaIds.value = [];
  } catch (e) {
    console.error("Update error:", e);
    error.value = e?.response?.data?.error || 'আপডেট ব্যর্থ হয়েছে';
  } finally {
    loading.value = false;
  }
};





</script>

<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="min-h-screen bg-gray-100"
  >
    <!-- AdminLTE Banner/Header -->
    <div class="bg-gray-800 border-b border-gray-900 shadow-lg py-8 px-8 flex flex-col md:flex-row items-center justify-between">
      <div class="flex items-center gap-4">
        <div class="bg-gray-900 p-4 rounded-lg flex items-center justify-center">
          <i class="fas fa-university text-indigo-300 text-3xl"></i>
        </div>
        <div>
          <h1 class="text-2xl md:text-3xl font-extrabold text-white tracking-tight">মারকাযের আবেদন ফরম</h1>
          <p class="text-gray-200 mt-2 font-medium text-base">পরীক্ষা: {{ form.exam_name || 'লোড হচ্ছে...' }}</p>
        </div>
      </div>
      <div class="flex items-center bg-gray-700 rounded-lg px-6 py-3 text-white mt-6 md:mt-0">
        <div class="mr-6 border-r border-gray-500 pr-6">
          <div class="text-sm">তারিখ ও সময়</div>
          <div class="font-bold">{{ getCurrentDateTime() }}</div>
        </div>
        <div>
          <div class="text-sm">ইউজার</div>
          <div class="font-bold">{{ getCurrentUser() }}</div>
        </div>
      </div>
    </div>

    <!-- Progress Tracker -->
    <div class=" mx-auto pt-8 px-4">
      <div class="bg-white border border-gray-300 rounded shadow-lg mb-8">
        <div class="px-8 py-6">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between">
            <h3 class="text-lg font-bold text-gray-700">
              <i class="fas fa-tasks mr-2 text-indigo-400"></i>
              আবেদন অগ্রগতি
            </h3>
            <span class="bg-gray-100 text-gray-800 px-4 py-1 rounded-full text-sm font-bold">
              {{ getStepCompletionPercentage }}% সম্পন্ন
            </span>
          </div>
          <div class="my-4">
            <div class="relative w-full bg-gray-200 rounded-full h-3">
              <div
                class="absolute top-0 left-0 h-3 rounded-full transition-all duration-500"
                :class="getStepCompletionPercentage === 100 ? 'bg-green-500' : 'bg-indigo-500'"
                :style="{ width: getStepCompletionPercentage + '%' }"
              ></div>
            </div>
          </div>
          <div class="hidden md:flex justify-between pt-4">
            <div
              v-for="(stepLabel, index) in stepLabels"
              :key="index"
              class="flex flex-col items-center w-1/4"
              :class="{ 'opacity-50': !canAccessStep[index] && index !== step }"
            >
              <div
                class="flex items-center justify-center h-10 w-10 rounded-full mb-2 border border-gray-300"
                :class="[
                  step === index
                    ? 'bg-indigo-100 text-indigo-700 shadow'
                    : ((index === 0 && isConditionsAccepted) ||
                       (index === 1 && isStep1Valid) ||
                       (index === 2 && isStep2Valid) ||
                       (index === 3 && isStep3Valid))
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-500'
                ]"
              >
                <i :class="[stepLabel.icon, 'text-lg']"></i>
              </div>
              <span class="text-sm font-bold text-gray-700">{{ stepLabel.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Box -->
    <div class=" mx-auto pb-12 px-4">
      <div class="bg-white border border-gray-300 rounded shadow-lg">
        <div class="px-8 py-8">
          <TabView v-model:activeIndex="step" :scrollable="true" @tab-change="handleTabChange">
            <!-- Conditions Tab -->


            <TabPanel :disabled="!canAccessStep[1]">
              <template #header>
                <div class="flex items-center" :class="{ 'opacity-50': !canAccessStep[1] }">
                  <i :class="getStepIcon(1)" class="mr-2"></i>
                  <span class="font-bold">২. ধরন ও মূল তথ্য</span>
                  <i v-if="!canAccessStep[1]" class="fas fa-lock ml-2 text-gray-400"></i>
                </div>
              </template>
              <div>
                <h3 class="text-xl font-bold text-gray-700 mb-6 pb-2 border-b border-gray-200">
                  মারকাযের ধরণ ও মূল তথ্য
                </h3>
                <div class="bg-gray-100 border-l-4 border-indigo-400 p-4 mb-6 rounded-r-md shadow">
                  <div class="flex items-center">
                    <i class="fas fa-info-circle text-indigo-400"></i>
                    <span class="ml-3 text-sm text-gray-800">
                      আপনার মারকাযের ধরণ নির্বাচন করুন এবং প্রয়োজনীয় তথ্য পূরণ করুন। সমস্ত তারকাচিহ্নিত (*) ক্ষেত্র পূরণ করা আবশ্যক।
                    </span>
                  </div>
                </div>
                <div class="bg-white rounded-lg p-5 mb-8 border border-gray-200 shadow">
                  <h4 class="text-lg font-bold text-gray-700 mb-4">মারকায ধরণ নির্বাচন</h4>
                  <CategorySelect
                    :modelValue="form.markaz_type"
                    @update:modelValue="form.markaz_type = $event"
                  />
                </div>
                <div class="bg-white rounded-lg p-5 border border-gray-200 shadow">
                  <h4 class="text-lg font-bold text-gray-700 mb-4">মূল মাদ্রাসার তথ্য</h4>
                  <MainMadrasaInfo
                    :form="form"
                    :nocFile="nocFileForMadrahsa"
                    :nocPreview="nocPreviewForMadrahsa"
                    :resolutionFile="resolutionFileForMadrahsa"
                    :resolutionPreview="resolutionPreviewForMadrahsa"
                    @file-upload="(file, type) => handleFileUploadForMadrahsa(file, type)"
                    @remove-file="removeFileForMadrahsa"
                  />
                </div>
                <div class="flex justify-between p-4 bg-gray-50 rounded-b-lg border-t border-gray-200 mt-6">
                  <Button
                    label="পূর্ববর্তী ধাপ"
                    icon="pi pi-arrow-left"
                    class="p-button-outlined"
                    @click="step = 0"
                  />
                  <Button
                    label="পরবর্তী ধাপ"
                    icon="pi pi-arrow-right"
                    iconPos="right"
                    class="p-button-secondary"
                    @click="goToNextStep"
                  />
                </div>
              </div>
            </TabPanel>

            <TabPanel :disabled="!canAccessStep[2]">
              <template #header>
                <div class="flex items-center" :class="{ 'opacity-50': !canAccessStep[2] }">
                  <i :class="getStepIcon(2)" class="mr-2"></i>
                  <span class="font-bold">৩. সংযুক্ত মাদ্রাসা</span>
                  <i v-if="!canAccessStep[2]" class="fas fa-lock ml-2 text-gray-400"></i>
                </div>
              </template>
              <div>
                <h3 class="text-xl font-bold text-gray-700 mb-6 pb-2 border-b border-gray-200">
                  সংযুক্ত মাদ্রাসার তথ্য
                </h3>
                <div class="bg-gray-100 border-l-4 border-blue-400 p-4 mb-6 rounded-r-md shadow">
                  <div class="flex items-center">
                    <i class="fas fa-exclamation-triangle text-blue-400"></i>
                    <span class="ml-3 text-sm text-gray-800">
                      সংযুক্ত মাদ্রাসা যোগ করতে মাদ্রাসার নাম বা ইলহাক নম্বর দিয়ে অনুসন্ধান করুন। প্রতিটি মাদ্রাসার জন্য প্রয়োজনীয় তথ্য পূরণ করুন।
                    </span>
                  </div>
                </div>
                <div class="bg-white rounded-lg p-5 border border-gray-200 shadow">
                  <div class="flex justify-between items-center mb-4">
                    <h4 class="text-lg font-bold text-gray-700">সংযুক্ত মাদ্রাসা সমূহ</h4>
                    <span class="bg-gray-600 text-white rounded-full px-3 py-1 text-xs font-bold">{{ rows.length }}</span>
                  </div>
                  <DynamicMadrasas
                    :rows="rows"
                    :madrashas="madrashas"
                    :filteredOptions="filteredOptions"
                    :markazType="form.markaz_type"
                    @add-row="addRow"
                    @remove-row="removeRow"
                    @file-upload="handleFileUpload"
                    @remove-file="removeFile"
                    @select-option="selectOption"
                  />
                </div>
                <div class="flex justify-between p-4 bg-gray-50 rounded-b-lg border-t border-gray-200 mt-6">
                  <Button
                    label="পূর্ববর্তী ধাপ"
                    icon="pi pi-arrow-left"
                    class="p-button-outlined"
                    @click="step = 1"
                  />
                  <Button
                    label="পরবর্তী ধাপ"
                    icon="pi pi-arrow-right"
                    iconPos="right"
                    class="p-button-secondary"
                    @click="goToNextStep"
                  />
                </div>
              </div>
            </TabPanel>

            <TabPanel>
              <template #header>
                <div class="flex items-center">
                  <i :class="getStepIcon(3)" class="mr-2"></i>
                  <span class="font-bold">৪. প্রয়োজনীয়তা ও সংযুক্তি</span>
                </div>
              </template>
              <div>
                <h3 class="text-xl font-bold text-gray-700 mb-6 pb-2 border-b border-gray-200">
                  প্রয়োজনীয়তা ও প্রমাণক সংযুক্তি
                </h3>
                <div class="bg-gray-100 border-l-4 border-green-400 p-4 mb-6 rounded-r-md shadow">
                  <div class="flex items-center">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span class="ml-3 text-sm text-gray-800">
                      মারকাজ চাওয়ার প্রয়োজনীয়তা বর্ণনা করুন। ফাইল সংযুক্তি ঐচ্ছিক।
                    </span>
                  </div>
                </div>
                <div class="bg-white rounded-lg p-5 mb-6 border border-gray-200 shadow">
                  <h4 class="text-lg font-bold text-gray-700 mb-4">মারকাজ প্রয়োজনীয়তা <span class="text-red-500">*</span></h4>
                  <RequirementsSection
                    :modelValue="form.requirements"
                    @update:modelValue="form.requirements = $event"
                  />
                  <p class="text-sm text-gray-500 mt-2">
                    এই ক্ষেত্রটি পূরণ করা বাধ্যতামূলক।
                  </p>
                </div>
                <div class="bg-white rounded-lg p-5 border border-gray-200 shadow">
                  <h4 class="text-lg font-bold text-gray-700 mb-4">প্রমাণক সংযুক্তি (ঐচ্ছিক)</h4>
                  <AttachmentSection
                    :muhtamimFile="muhtamimFile"
                    :muhtamimPreview="muhtamimPreview"
                    :presidentFile="presidentFile"
                    :presidentPreview="presidentPreview"
                    :committeeFile="committeeFile"
                    :committeePreview="committeePreview"
                    @file-upload="handleFileUploadMumtahin"
                    @remove-file="removeFileMumtahin"
                  />
                  <div class="mt-4 p-3 bg-gray-100 rounded-md">
                    <p class="text-sm text-gray-600">
                      <i class="fas fa-info-circle mr-2"></i>
                      ফাইল সংযুক্তি ঐচ্ছিক। প্রয়োজনীয়তা ব্যাখ্যা পূরণ করলেই আবেদন জমা দেওয়া যাবে।
                    </p>
                  </div>
                </div>
                <div v-if="formErrors.length > 0" class="p-4 bg-red-50 border border-red-300 rounded-md mb-4">
                  <h4 class="font-bold text-red-700 mb-2">
                    <i class="fas fa-exclamation-circle mr-2"></i>নিম্নলিখিত সমস্যা সমাধান করুন:
                  </h4>
                  <ul class="list-disc pl-5">
                    <li v-for="(error, key) in formErrors" :key="key" class="text-red-700 text-sm">
                      {{ error }}
                    </li>
                  </ul>
                </div>
                <div class="flex justify-between p-4 bg-gray-50 rounded-b-lg border-t border-gray-200 mt-6">
                  <Button
                    label="পূর্ববর্তী ধাপ"
                    icon="pi pi-arrow-left"
                    class="p-button-outlined"
                    @click="step = 2"
                  />
                  <Button
                    label="আপডেট করুন"
                    icon="pi pi-save"
                    iconPos="right"
                    class="p-button-success"
                    :loading="loading"
                    @click="updateForm"
                  />
                </div>
              </div>
            </TabPanel>
          </TabView>
        </div>
      </div>
    </div>
  </div>
</template>

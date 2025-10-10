import { ref, watch } from 'vue';

export function useMarkazApply() {
  // Dark mode
  const darkMode = ref(localStorage.getItem('darkMode') === 'true' || false);
  watch(() => document.documentElement.classList.contains('dark'), (newValue) => {
    darkMode.value = newValue;
  });

  // Step, loading, errors, conditions
  const step = ref(0);
  const loading = ref(false);
  const formErrors = ref([]);
  const validationErrors = ref({});
  const conditionsAgreed = ref(false);

  // System/user info
  const systemDate = '2025-08-10';
  const systemTime = '04:27:27';
  const userLogin = 'tahsin866';
  const user = ref({
    id: 1,
    madrasha_name: 'ডেমো মাদরাসা',
    username: 'tahsin866'
  });
  const exam = ref({
    id: 1,
    exam_name: 'বার্ষিক পরীক্ষা'
  });

  // Form state
  const form = ref({
    user_id: user.value.id,
    user_name: user.value.madrasha_name,
    exam_id: '',
    exam_name: '',
    markaz_type: '',
    fazilat: 0,
    sanabiya_ulya: 0,
    sanabiya: 0,
    mutawassita: 0,
    ibtedaiyyah: 0,
    hifzul_quran: 0,
    qirat: 0,
    noc_file: null as File | Blob | null,
    resolution_file: null as File | Blob | null,
    requirements: '',
    muhtamim_consent: null,
    president_consent: null,
    committee_resolution: null,
    associated_madrasas: []
  });

  // Rows
  type FileType = File | Blob | null;
  type PreviewType = string | null;
  interface Row {
    fazilat: string;
    sanabiya_ulya: string;
    sanabiya: string;
    mutawassita: string;
    ibtedaiyyah: string;
    hifzul_quran: string;
    qirat: string;
    madrasa_Name: string;
    madrasa_id: string | number;
    searchQuery: string;
    isOpen: boolean;
    files: {
      noc: FileType;
      nocPreview: PreviewType;
      resolution: FileType;
      resolutionPreview: PreviewType;
    };
  }
  const rows = ref<Row[]>([
    {
      fazilat: '',
      sanabiya_ulya: '',
      sanabiya: '',
      mutawassita: '',
      ibtedaiyyah: '',
      hifzul_quran: '',
      qirat: '',
      madrasa_Name: '',
      madrasa_id: '',
      searchQuery: '',
      isOpen: false,
      files: {
        noc: null,
        nocPreview: null,
        resolution: null,
        resolutionPreview: null
      }
    }
  ]);

  // Row actions
  const addRow = () => {
    rows.value.push({
      fazilat: '',
      sanabiya_ulya: '',
      sanabiya: '',
      mutawassita: '',
      ibtedaiyyah: '',
      hifzul_quran: '',
      qirat: '',
      madrasa_Name: '',
      madrasa_id: '',
      searchQuery: '',
      isOpen: false,
      files: {
        noc: null,
        nocPreview: null,
        resolution: null,
        resolutionPreview: null
      }
    });
  };

  const removeRow = (index: number) => {
    if (rows.value.length > 1) {
      rows.value.splice(index, 1);
    }
  };

  const handleFileUpload = (file: File | Blob | { files?: FileList; target?: { files?: FileList }; originalEvent?: { target?: { files?: FileList } } }, type: 'noc' | 'resolution', index: number) => {
    let extractedFile: File | Blob | null = null;
    if (file instanceof File || file instanceof Blob) {
      extractedFile = file;
    } else if (file?.files?.length) {
      extractedFile = file.files[0];
    } else if (file?.target?.files?.length) {
      extractedFile = file.target.files[0];
    } else if (file?.originalEvent?.target?.files?.length) {
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
    }
  };

  // File states for Madrasah
  const nocFileForMadrahsa = ref<File | Blob | null>(null);
  const nocPreviewForMadrahsa = ref<string | null>(null);
  const resolutionFileForMadrahsa = ref<File | Blob | null>(null);
  const resolutionPreviewForMadrahsa = ref<string | null>(null);
  // File states for Mumtahin
  const muhtamimFile = ref<File | Blob | null>(null);
  const muhtamimPreview = ref<string | null>(null);
  const presidentFile = ref<File | Blob | null>(null);
  const presidentPreview = ref<string | null>(null);
  const committeeFile = ref<File | Blob | null>(null);
  const committeePreview = ref<string | null>(null);

  // Remove file for DynamicMadrasas
  const removeFile = (type: 'noc' | 'resolution', index: number) => {
    if (type === 'noc') {
      rows.value[index].files.noc = null;
      rows.value[index].files.nocPreview = null;
    } else {
      rows.value[index].files.resolution = null;
      rows.value[index].files.resolutionPreview = null;
    }
  };

  // Mumtahin file upload/remove
  const handleFileUploadMumtahin = (
    event: File | Blob | { files?: FileList; target?: { files?: FileList }; originalEvent?: { target?: { files?: FileList } } },
    type: 'muhtamim' | 'president' | 'committee'
  ) => {
    let file: File | Blob | null = null;
    if (event instanceof File || event instanceof Blob) file = event;
    else if (event?.files && event.files.length > 0) file = event.files[0];
    else if (event?.target?.files && event.target.files.length > 0) file = event.target.files[0];
    else if (event?.originalEvent?.target?.files && event.originalEvent.target.files.length > 0) file = event.originalEvent.target.files[0];
    if (!file) return;
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
  };
  const removeFileMumtahin = (type: 'muhtamim' | 'president' | 'committee') => {
    switch (type) {
      case 'muhtamim':
        muhtamimFile.value = null;
        muhtamimPreview.value = null;
        break;
      case 'president':
        presidentFile.value = null;
        presidentPreview.value = null;
        break;
      case 'committee':
        committeeFile.value = null;
        committeePreview.value = null;
        break;
    }
  };

  // Madrasah file upload/remove
  const handleFileUploadForMadrahsa = (
    file: File | Blob | { files?: FileList; target?: { files?: FileList }; originalEvent?: { target?: { files?: FileList } } },
    type: 'noc' | 'resolution'
  ) => {
    let extractedFile: File | Blob | null = null;
    if (file instanceof File || file instanceof Blob) {
      extractedFile = file;
    } else if (file?.files && file.files.length > 0) extractedFile = file.files[0];
    else if (file?.target?.files && file.target.files.length > 0) extractedFile = file.target.files[0];
    else if (file?.originalEvent?.target?.files && file.originalEvent.target.files.length > 0) extractedFile = file.originalEvent.target.files[0];
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
    }
  };
  const removeFileForMadrahsa = (type: 'noc' | 'resolution') => {
    if (type === 'noc') {
      nocFileForMadrahsa.value = null;
      nocPreviewForMadrahsa.value = null;
      form.value.noc_file = null;
    } else {
      resolutionFileForMadrahsa.value = null;
      resolutionPreviewForMadrahsa.value = null;
      form.value.resolution_file = null;
    }
  };

  // Madrasha search/filter/select
  const madrashas = ref<Array<{ id: number; name: string; ElhaqNo: string }>>([]);
  const filteredOptions = ref<(row: Row) => Array<{ id: number; name: string; ElhaqNo: string }>>();
  filteredOptions.value = (row: Row) => {
    if (!row.searchQuery) return [];
    return madrashas.value.filter((madrasha) => {
      const name = (madrasha.name || '').toLowerCase();
      const elhaqNo = (madrasha.ElhaqNo || '').toString().toLowerCase();
      const searchQuery = row.searchQuery.toLowerCase().trim();
      const normalizedElhaqNo = elhaqNo.replace(/[`']/g, '').replace(/\s+/g, '');
      const normalizedSearchQuery = searchQuery.replace(/[`']/g, '').replace(/\s+/g, '');
      if (normalizedElhaqNo.includes(normalizedSearchQuery)) return true;
      const searchWords = searchQuery.split(' ');
      return searchWords.every((word) => name.includes(word));
    });
  };
  const selectOption = (madrasha: { id: number; name: string; ElhaqNo: string }, row: Row) => {
    row.madrasa_Name = madrasha.name;
    row.madrasa_id = madrasha.id;
    row.searchQuery = `${madrasha.name} (ইলহাক: ${madrasha.ElhaqNo})`;
    row.isOpen = false;
  };

  // Stepper logic
  const handleConditionsAccepted = () => {
    conditionsAgreed.value = true;
  };
  const getCurrentDateTime = () => `${systemDate} ${systemTime}`;
  const getCurrentUser = () => user.value.username;

  // Step completion computations
  const isConditionsAccepted = ref(false);
  watch(conditionsAgreed, (val) => {
    isConditionsAccepted.value = val;
  });
  const isStep1Valid = ref(false);
  const isStep2Valid = ref(false);
  const isStep3Valid = ref(false);
  watch([form, nocFileForMadrahsa, resolutionFileForMadrahsa], () => {
    isStep1Valid.value = !!form.value.markaz_type && (
      (form.value.markaz_type === 'দরসিয়াত' && !!form.value.fazilat && !!form.value.sanabiya_ulya && !!nocFileForMadrahsa.value && !!resolutionFileForMadrahsa.value) ||
      (form.value.markaz_type === 'তাহফিজুল কোরআন' && !!form.value.hifzul_quran && !!nocFileForMadrahsa.value && !!resolutionFileForMadrahsa.value) ||
      (form.value.markaz_type === 'কিরাআত' && !!form.value.qirat && !!nocFileForMadrahsa.value && !!resolutionFileForMadrahsa.value)
    );
  }, { immediate: true });
  watch([rows, form], () => {
    isStep2Valid.value = rows.value.length > 0 && rows.value.every((row) => {
      if (!row.madrasa_id) return false;
      if (!row.files?.noc || !row.files?.resolution) return false;
      if (form.value.markaz_type === 'দরসিয়াত') return row.fazilat && row.sanabiya_ulya;
      if (form.value.markaz_type === 'তাহফিজুল কোরআন') return row.hifzul_quran;
      if (form.value.markaz_type === 'কিরাআত') return row.qirat;
      return false;
    });
  }, { immediate: true });
  watch(form, () => {
    isStep3Valid.value = !!form.value.requirements;
  }, { immediate: true });

  const canAccessStep = ref<Record<number, boolean>>({
    0: true,
    1: false,
    2: false,
    3: false
  });
  watch([isConditionsAccepted, isStep1Valid, isStep2Valid], () => {
    canAccessStep.value = {
      0: true,
      1: !!isConditionsAccepted.value,
      2: !!isConditionsAccepted.value && !!isStep1Valid.value,
      3: !!isConditionsAccepted.value && !!isStep1Valid.value && !!isStep2Valid.value
    };
  }, { immediate: true });

  const getStepCompletionPercentage = ref(0);
  watch([isConditionsAccepted, isStep1Valid, isStep2Valid, isStep3Valid], () => {
    let total = 0;
    if (isConditionsAccepted.value) total += 25;
    if (isStep1Valid.value) total += 25;
    if (isStep2Valid.value) total += 25;
    if (isStep3Valid.value) total += 25;
    getStepCompletionPercentage.value = Math.round(total);
  }, { immediate: true });

  const stepLabels = [
    { label: 'শর্তাবলী', icon: 'pi pi-info-circle' },
    { label: 'ধরন ও মূল তথ্য', icon: 'pi pi-file-edit' },
    { label: 'সংযুক্ত মাদ্রাসা', icon: 'pi pi-building' },
    { label: 'প্রয়োজনীয়তা ও সংযুক্তি', icon: 'pi pi-paperclip' }
  ];
  const getStepIcon = (index: number) => {
    if (index === 0 && isConditionsAccepted.value) return 'pi pi-check-circle text-green-500 dark:text-green-400';
    if (index === 1 && isStep1Valid.value) return 'pi pi-check-circle text-green-500 dark:text-green-400';
    if (index === 2 && isStep2Valid.value) return 'pi pi-check-circle text-green-500 dark:text-green-400';
    if (index === 3 && isStep3Valid.value) return 'pi pi-check-circle text-green-500 dark:text-green-400';
    return step.value === index ? 'pi pi-spin pi-spinner text-blue-500 dark:text-blue-400' : 'pi pi-circle-fill text-gray-400 dark:text-gray-600';
  };

  // Tab change, next step, submit
  interface TabChangeEvent {
    index: number;
    preventDefault: () => void;
  }

  const handleTabChange = (event: TabChangeEvent) => {
    const targetIndex = event.index;
    if (!canAccessStep.value[targetIndex]) {
      event.preventDefault();
      // toast logic should be handled in component
      return;
    }
    step.value = targetIndex;
  };
  const goToNextStep = () => {
    const nextStep = step.value + 1;
    if (canAccessStep.value[nextStep]) step.value = nextStep;
  };
  const submitForm = async () => {
    loading.value = true;
    formErrors.value = [];
    validationErrors.value = {};
    if (!form.value.requirements) {
      loading.value = false;
      // toast logic should be handled in component
      return;
    }
    if (!form.value.markaz_type) {
      loading.value = false;
      // toast logic should be handled in component
      return;
    }
    // Simulate POST
    setTimeout(() => {
      loading.value = false;
      // toast logic should be handled in component
    }, 1500);
  };

  return {
    darkMode,
    step,
    loading,
    formErrors,
    validationErrors,
    conditionsAgreed,
    systemDate,
    systemTime,
    userLogin,
    user,
    exam,
    form,
    rows,
    addRow,
    removeRow,
    handleFileUpload,
    removeFile,
    nocFileForMadrahsa,
    nocPreviewForMadrahsa,
    resolutionFileForMadrahsa,
    resolutionPreviewForMadrahsa,
    muhtamimFile,
    muhtamimPreview,
    presidentFile,
    presidentPreview,
    committeeFile,
    committeePreview,
    handleFileUploadMumtahin,
    removeFileMumtahin,
    handleFileUploadForMadrahsa,
    removeFileForMadrahsa,
    madrashas,
    filteredOptions,
    selectOption,
    handleConditionsAccepted,
    getCurrentDateTime,
    getCurrentUser,
    isConditionsAccepted,
    isStep1Valid,
    isStep2Valid,
    isStep3Valid,
    canAccessStep,
    getStepCompletionPercentage,
    stepLabels,
    getStepIcon,
    handleTabChange,
    goToNextStep,
    submitForm
  };
}

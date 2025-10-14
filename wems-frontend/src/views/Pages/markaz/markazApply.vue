

<script setup>
import 'primeicons/primeicons.css'
import { ref, computed, watch, onMounted } from 'vue'
import axios from 'axios'

import MarkazConditions from '@/views/Pages/markaz/components/MarkazConditions.vue'
import CategorySelect from '@/views/Pages/markaz/components/CategorySelect.vue'
import MainMadrasaInfo from '@/views/Pages/markaz/components/MainMadrasaInfo.vue'
import DynamicMadrasas from '@/views/Pages/markaz/components/DynamicMadrasas.vue'
import RequirementsSection from '@/views/Pages/markaz/components/RequirementsSection.vue'
import AttachmentSection from '@/views/Pages/markaz/components/AttachmentSection.vue'
<<<<<<< HEAD
import FlashMessage from '@/components/ui/FlashMessage.vue'
=======
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Button from 'primevue/button'
// import ProgressBar from 'primevue/progressbar'
// import Card from 'primevue/card'
// import Tooltip from 'primevue/tooltip'
// import Badge from 'primevue/badge'

<<<<<<< HEAD
// Flash message system
const flashMessage = ref({
  show: false,
  message: '',
  type: 'success',
  title: '',
  autoHide: true,
  duration: 5000,
  showCloseButton: true,
  glowEffect: true
})

const showFlashMessage = (message, type = 'success', options = {}) => {
  const titles = {
    success: 'সফলভাবে সম্পন্ন হয়েছে',
    error: 'সমস্যা হয়েছে',
    warning: 'সতর্কতা',
    info: 'তথ্য'
  }

  flashMessage.value = {
    show: true,
    message,
    type,
    title: options.title || titles[type],
    autoHide: options.autoHide !== false,
    duration: options.duration || 5000,
    showCloseButton: options.showCloseButton !== false,
    glowEffect: options.glowEffect !== false
  }
=======
const toast = ref({
  show: false,
  message: '',
  type: 'success'
})

const showToast = (message, type = 'success') => {
  toast.value = {
    show: true,
    message,
    type
  }
  setTimeout(() => {
    toast.value.show = false
  }, 5000)
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
}

const step = ref(0)
const loading = ref(false)
const formErrors = ref([])
const validationErrors = ref({})
const conditionsAgreed = ref(false)

const user_id = 1
const user_name = "Demo Madrasha"
const exam_id = ""
const exam_name = ""

const form = ref({
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
  requirements: '',
  muhtamim_consent: null,
  president_consent: null,
  committee_resolution: null,
  associated_madrasas: []
})

const rows = ref([{
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
  exactSearch: true,
  files: {
    noc: null,
    nocPreview: null,
    resolution: null,
    resolutionPreview: null
  }
}])

const addRow = () => {
  rows.value.push({
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
    exactSearch: true,
    files: {
      noc: null,
      nocPreview: null,
      resolution: null,
      resolutionPreview: null
    }
  })
<<<<<<< HEAD
  showFlashMessage('নতুন সারি যোগ করা হয়েছে', 'success')
=======
  showToast('নতুন সারি যোগ করা হয়েছে', 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
}

const removeRow = (index) => {
  if (rows.value.length > 1) {
    rows.value.splice(index, 1)
<<<<<<< HEAD
    showFlashMessage('সারি সরিয়ে ফেলা হয়েছে', 'success')
  } else {
    showFlashMessage('অন্ততপক্ষে একটি সারি রাখতে হবে', 'error')
=======
    showToast('সারি সরিয়ে ফেলা হয়েছে', 'success')
  } else {
    showToast('অন্ততপক্ষে একটি সারি রাখতে হবে', 'error')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
  }
}

const handleFileUpload = (file, type, index) => {
  try {
    if (file instanceof File || file instanceof Blob) {
      if (type === 'noc') {
        rows.value[index].files.noc = file
        rows.value[index].files.nocPreview = URL.createObjectURL(file)
<<<<<<< HEAD
        showFlashMessage(`অনাপত্তিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
      } else {
        rows.value[index].files.resolution = file
        rows.value[index].files.resolutionPreview = URL.createObjectURL(file)
        showFlashMessage(`সম্মতিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
=======
        showToast(`অনাপত্তিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
      } else {
        rows.value[index].files.resolution = file
        rows.value[index].files.resolutionPreview = URL.createObjectURL(file)
        showToast(`সম্মতিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      }
      return
    }

    let extractedFile = null
    if (file && file.files && file.files.length > 0) {
      extractedFile = file.files[0]
    } else if (file && file.target && file.target.files && file.target.files.length > 0) {
      extractedFile = file.target.files[0]
    } else if (file && file.originalEvent && file.originalEvent.target &&
      file.originalEvent.target.files && file.originalEvent.target.files.length > 0) {
      extractedFile = file.originalEvent.target.files[0]
    }

    if (extractedFile) {
      if (type === 'noc') {
        rows.value[index].files.noc = extractedFile
        rows.value[index].files.nocPreview = URL.createObjectURL(extractedFile)
<<<<<<< HEAD
        showFlashMessage(`অনাপত্তিপত্র আপলোড সফল হয়েছে: ${extractedFile.name}`, 'success')
      } else {
        rows.value[index].files.resolution = extractedFile
        rows.value[index].files.resolutionPreview = URL.createObjectURL(extractedFile)
        showFlashMessage(`সম্মতিপত্র আপলোড সফল হয়েছে: ${extractedFile.name}`, 'success')
      }
    } else {
      showFlashMessage('ফাইল নির্বাচন করা হয়নি। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
    }
  } catch  {
    showFlashMessage('ফাইল আপলোডে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
=======
        showToast(`অনাপত্তিপত্র আপলোড সফল হয়েছে: ${extractedFile.name}`, 'success')
      } else {
        rows.value[index].files.resolution = extractedFile
        rows.value[index].files.resolutionPreview = URL.createObjectURL(extractedFile)
        showToast(`সম্মতিপত্র আপলোড সফল হয়েছে: ${extractedFile.name}`, 'success')
      }
    } else {
      showToast('ফাইল নির্বাচন করা হয়নি। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
    }
  } catch  {
    showToast('ফাইল আপলোডে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
  }
}

const removeFile = (type, index) => {
  const fileName = type === 'noc' ? 'অনাপত্তিপত্র' : 'সম্মতিপত্র'
  if (type === 'noc') {
    rows.value[index].files.noc = null
    rows.value[index].files.nocPreview = null
  } else {
    rows.value[index].files.resolution = null
    rows.value[index].files.resolutionPreview = null
  }
<<<<<<< HEAD
  showFlashMessage(`${fileName} সরিয়ে ফেলা হয়েছে`, 'success')
=======
  showToast(`${fileName} সরিয়ে ফেলা হয়েছে`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
}

const nocFileForMadrahsa = ref(null)
const nocPreviewForMadrahsa = ref(null)
const resolutionFileForMadrahsa = ref(null)
const resolutionPreviewForMadrahsa = ref(null)
const muhtamimFile = ref(null)
const muhtamimPreview = ref(null)
const presidentFile = ref(null)
const presidentPreview = ref(null)
const committeeFile = ref(null)
const committeePreview = ref(null)

const handleFileUploadMumtahin = (event, type) => {
  try {
    if (event instanceof File || event instanceof Blob) {
      switch (type) {
        case 'muhtamim':
          muhtamimFile.value = event
          muhtamimPreview.value = URL.createObjectURL(event)
<<<<<<< HEAD
          showFlashMessage(`মুহতামিমের সম্মতিপত্র আপলোড সফল হয়েছে: ${event.name}`, 'success')
=======
          showToast(`মুহতামিমের সম্মতিপত্র আপলোড সফল হয়েছে: ${event.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
          break
        case 'president':
          presidentFile.value = event
          presidentPreview.value = URL.createObjectURL(event)
<<<<<<< HEAD
          showFlashMessage(`সভাপতির সম্মতিপত্র আপলোড সফল হয়েছে: ${event.name}`, 'success')
=======
          showToast(`সভাপতির সম্মতিপত্র আপলোড সফল হয়েছে: ${event.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
          break
        case 'committee':
          committeeFile.value = event
          committeePreview.value = URL.createObjectURL(event)
<<<<<<< HEAD
          showFlashMessage(`কমিটির প্রস্তাব আপলোড সফল হয়েছে: ${event.name}`, 'success')
=======
          showToast(`কমিটির প্রস্তাব আপলোড সফল হয়েছে: ${event.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
          break
      }
      return
    }

    let file = null
    if (event && event.files && event.files.length > 0) {
      file = event.files[0]
    } else if (event && event.target && event.target.files && event.target.files.length > 0) {
      file = event.target.files[0]
    } else if (event && event.originalEvent && event.originalEvent.target &&
      event.originalEvent.target.files && event.originalEvent.target.files.length > 0) {
      file = event.originalEvent.target.files[0]
    }

    if (!file) {
<<<<<<< HEAD
      showFlashMessage('ফাইল নির্বাচন করা হয়নি। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
=======
      showToast('ফাইল নির্বাচন করা হয়নি। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      return
    }

    switch (type) {
      case 'muhtamim':
        muhtamimFile.value = file
        muhtamimPreview.value = URL.createObjectURL(file)
<<<<<<< HEAD
        showFlashMessage(`মুহতামিমের সম্মতিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
=======
        showToast(`মুহতামিমের সম্মতিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
        break
      case 'president':
        presidentFile.value = file
        presidentPreview.value = URL.createObjectURL(file)
<<<<<<< HEAD
        showFlashMessage(`সভাপতির সম্মতিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
=======
        showToast(`সভাপতির সম্মতিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
        break
      case 'committee':
        committeeFile.value = file
        committeePreview.value = URL.createObjectURL(file)
<<<<<<< HEAD
        showFlashMessage(`কমিটির প্রস্তাব আপলোড সফল হয়েছে: ${file.name}`, 'success')
        break
    }
  } catch {
    showFlashMessage('ফাইল আপলোডে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
=======
        showToast(`কমিটির প্রস্তাব আপলোড সফল হয়েছে: ${file.name}`, 'success')
        break
    }
  } catch {
    showToast('ফাইল আপলোডে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
  }
}

const removeFileMumtahin = (type) => {
  switch (type) {
    case 'muhtamim':
      muhtamimFile.value = null
      muhtamimPreview.value = null
<<<<<<< HEAD
      showFlashMessage('মুহতামিমের সম্মতিপত্র সরিয়ে ফেলা হয়েছে', 'success')
=======
      showToast('মুহতামিমের সম্মতিপত্র সরিয়ে ফেলা হয়েছে', 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      break
    case 'president':
      presidentFile.value = null
      presidentPreview.value = null
<<<<<<< HEAD
      showFlashMessage('সভাপতির সম্মতিপত্র সরিয়ে ফেলা হয়েছে', 'success')
=======
      showToast('সভাপতির সম্মতিপত্র সরিয়ে ফেলা হয়েছে', 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      break
    case 'committee':
      committeeFile.value = null
      committeePreview.value = null
<<<<<<< HEAD
      showFlashMessage('কমিটির প্রস্তাব সরিয়ে ফেলা হয়েছে', 'success')
=======
      showToast('কমিটির প্রস্তাব সরিয়ে ফেলা হয়েছে', 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      break
  }
}

const handleFileUploadForMadrahsa = (file, type) => {
  try {
    if (file instanceof File || file instanceof Blob) {
      if (type === 'noc') {
        form.value.noc_file = file
        nocFileForMadrahsa.value = file
        nocPreviewForMadrahsa.value = URL.createObjectURL(file)
<<<<<<< HEAD
        showFlashMessage(`মূল মাদরাসার অনাপত্তিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
=======
        showToast(`মূল মাদরাসার অনাপত্তিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      } else {
        form.value.resolution_file = file
        resolutionFileForMadrahsa.value = file
        resolutionPreviewForMadrahsa.value = URL.createObjectURL(file)
<<<<<<< HEAD
        showFlashMessage(`মূল মাদরাসার সম্মতিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
=======
        showToast(`মূল মাদরাসার সম্মতিপত্র আপলোড সফল হয়েছে: ${file.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      }
      return
    }

    let extractedFile = null
    if (file && file.files && file.files.length > 0) {
      extractedFile = file.files[0]
    } else if (file && file.target && file.target.files && file.target.files.length > 0) {
      extractedFile = file.target.files[0]
    } else if (file && file.originalEvent && file.originalEvent.target &&
      file.originalEvent.target.files && file.originalEvent.target.files.length > 0) {
      extractedFile = file.originalEvent.target.files[0]
    }

    if (extractedFile) {
      if (type === 'noc') {
        form.value.noc_file = extractedFile
        nocFileForMadrahsa.value = extractedFile
        nocPreviewForMadrahsa.value = URL.createObjectURL(extractedFile)
<<<<<<< HEAD
        showFlashMessage(`মূল মাদরাসার অনাপত্তিপত্র আপলোড সফল হয়েছে: ${extractedFile.name}`, 'success')
=======
        showToast(`মূল মাদরাসার অনাপত্তিপত্র আপলোড সফল হয়েছে: ${extractedFile.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      } else {
        form.value.resolution_file = extractedFile
        resolutionFileForMadrahsa.value = extractedFile
        resolutionPreviewForMadrahsa.value = URL.createObjectURL(extractedFile)
<<<<<<< HEAD
        showFlashMessage(`মূল মাদরাসার সম্মতিপত্র আপলোড সফল হয়েছে: ${extractedFile.name}`, 'success')
      }
    } else {
      showFlashMessage('ফাইল নির্বাচন করা হয়নি। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
    }
  } catch  {
    showFlashMessage('ফাইল আপলোডে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
=======
        showToast(`মূল মাদরাসার সম্মতিপত্র আপলোড সফল হয়েছে: ${extractedFile.name}`, 'success')
      }
    } else {
      showToast('ফাইল নির্বাচন করা হয়নি। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
    }
  } catch  {
    showToast('ফাইল আপলোডে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।', 'error')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
  }
}

const removeFileForMadrahsa = (type) => {
  const fileName = type === 'noc' ? 'মূল মাদরাসার অনাপত্তিপত্র' : 'মূল মাদরাসার সম্মতিপত্র'
  if (type === 'noc') {
    nocFileForMadrahsa.value = null
    nocPreviewForMadrahsa.value = null
    form.value.noc_file = null
  } else {
    resolutionFileForMadrahsa.value = null
    resolutionPreviewForMadrahsa.value = null
    form.value.resolution_file = null
  }
<<<<<<< HEAD
  showFlashMessage(`${fileName} সরিয়ে ফেলা হয়েছে`, 'success')
=======
  showToast(`${fileName} সরিয়ে ফেলা হয়েছে`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
}

const madrashas = ref([])

const filteredOptions = computed(() => (row) => {
  if (!row.searchQuery) return []
  return madrashas.value.filter(madrasha => {
    const name = (madrasha.name || '').toLowerCase()
    const elhaqNo = (madrasha.ElhaqNo || '').toString().toLowerCase()
    const searchQuery = row.searchQuery.toLowerCase().trim()
    const normalizedElhaqNo = elhaqNo.replace(/[`']/g, '').replace(/\s+/g, '')
    const normalizedSearchQuery = searchQuery.replace(/[`']/g, '').replace(/\s+/g, '')
    if (normalizedElhaqNo.includes(normalizedSearchQuery)) return true
    const searchWords = searchQuery.split(' ')
    return searchWords.every(word => name.includes(word))
  })
})

const selectOption = (madrasha, row) => {
  row.madrasa_Name = madrasha.name
  row.madrasa_id = madrasha.id
  row.isOpen = false
<<<<<<< HEAD
  showFlashMessage(`মাদরাসা নির্বাচিত হয়েছে: ${madrasha.name}`, 'success')
=======
  showToast(`মাদরাসা নির্বাচিত হয়েছে: ${madrasha.name}`, 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
}

watch(() => form.value.markaz_type, (newType) => {
  if (newType === 'দরসিয়াত') {
    form.value.hifzul_quran = null
    form.value.qirat = null
  } else if (newType === 'তাহফিজুল কোরআন') {
    form.value.fazilat = null
    form.value.sanabiya_ulya = null
    form.value.sanabiya = null
    form.value.mutawassita = null
    form.value.ibtedaiyyah = null
    form.value.qirat = null
  } else if (newType === 'কিরাআত') {
    form.value.fazilat = null
    form.value.sanabiya_ulya = null
    form.value.sanabiya = null
    form.value.mutawassita = null
    form.value.ibtedaiyyah = null
    form.value.hifzul_quran = null
  }

  rows.value.forEach(row => {
    if (newType === 'দরসিয়াত') {
      row.hifzul_quran = null
      row.qirat = null
    } else if (newType === 'তাহফিজুল কোরআন') {
      row.fazilat = null
      row.sanabiya_ulya = null
      row.sanabiya = null
      row.mutawassita = null
      row.ibtedaiyyah = null
      row.qirat = null
    } else if (newType === 'কিরাআত') {
      row.fazilat = null
      row.sanabiya_ulya = null
      row.sanabiya = null
      row.mutawassita = null
      row.ibtedaiyyah = null
      row.hifzul_quran = null
    }
  })
})

const submitForm = async () => {
  loading.value = true
  formErrors.value = []
  validationErrors.value = {}

  const token = localStorage.getItem('token')
  if (!token) {
    loading.value = false
    formErrors.value = ['আপনি লগইন করে নেই। অনুগ্রহ করে আগে লগইন করুন।']
    return
  }

  if (!form.value.requirements) {
    loading.value = false
    formErrors.value = ['মারকাজ প্রয়োজনীয়তা ব্যাখ্যা করুন']
    return
  }

  if (!form.value.markaz_type) {
    loading.value = false
    formErrors.value = ['মারকাযের স্তর নির্বাচন করুন']
    return
  }

  if (form.value.markaz_type === 'দরসিয়াত') {
    if (form.value.fazilat === null) {
      loading.value = false
      formErrors.value = ['ফাযীলাত ফিল্ড পূরণ করুন']
      return
    }
    if (form.value.sanabiya_ulya === null) {
      loading.value = false
      formErrors.value = ['সানাবিয়া উলইয়া ফিল্ড পূরণ করুন']
      return
    }
  } else if (form.value.markaz_type === 'তাহফিজুল কোরআন') {
    if (form.value.hifzul_quran === null) {
      loading.value = false
      formErrors.value = ['হিফযুল কোরআন ফিল্ড পূরণ করুন']
      return
    }
  } else if (form.value.markaz_type === 'কিরাআত') {
    if (form.value.qirat === null) {
      loading.value = false
      formErrors.value = ['কিরাআত ফিল্ড পূরণ করুন']
      return
    }
  }

  if (!nocFileForMadrahsa.value || !resolutionFileForMadrahsa.value) {
    loading.value = false
    formErrors.value = ['মূল মাদ্রাসার সমস্ত প্রয়োজনীয় ফাইল আপলোড করুন']
    return
  }

  const invalidRows = rows.value.filter(row => {
    if (!row.madrasa_id) return true
    if (!row.files.noc || !row.files.resolution) return true

    function isValidNumber(val) {
      return val !== null && val !== undefined && Number(val) > 0
    }

    if (form.value.markaz_type === 'দরসিয়াত') {
      if (
        !isValidNumber(row.fazilat) ||
        !isValidNumber(row.sanabiya_ulya) ||
        !isValidNumber(row.sanabiya) ||
        !isValidNumber(row.mutawassita) ||
        !isValidNumber(row.ibtedaiyyah)
      ) {
        return true
      }
    } else if (form.value.markaz_type === 'তাহফিজুল কোরআন') {
      if (!isValidNumber(row.hifzul_quran)) {
        return true
      }
    } else if (form.value.markaz_type === 'কিরাআত') {
      if (!isValidNumber(row.qirat)) {
        return true
      }
    }

    return false
  })

  if (invalidRows.length > 0) {
    loading.value = false
    formErrors.value = [`${invalidRows.length}টি সংযুক্ত মাদ্রাসার তথ্য অসম্পূর্ণ`]
    return
  }

  const userId = localStorage.getItem('user_id')
  // const token = localStorage.getItem('token')

  const mainMadrasaInfo = {
    madrasa_id: userId,
    fazilat: form.value.fazilat,
    sanabiya_ulya: form.value.sanabiya_ulya,
    sanabiya: form.value.sanabiya,
    mutawassita: form.value.mutawassita,
    ibtedaiyyah: form.value.ibtedaiyyah,
    hifzul_quran: form.value.hifzul_quran,
    qirat: form.value.qirat,
    noc_file_path: form.value.noc_file ? form.value.noc_file.name : '',
    resolution_file_path: form.value.resolution_file ? form.value.resolution_file.name : ''
  }

  const associatedMadrasas = rows.value.map(row => ({
    madrasa_id: row.madrasa_id,
    fazilat: row.fazilat,
    sanabiya_ulya: row.sanabiya_ulya,
    sanabiya: row.sanabiya,
    mutawassita: row.mutawassita,
    ibtedaiyyah: row.ibtedaiyyah,
    hifzul_quran: row.hifzul_quran,
    qirat: row.qirat,
    noc_file_path: row.files.noc ? row.files.noc.name : '',
    resolution_file_path: row.files.resolution ? row.files.resolution.name : ''
  }))

  const attachments = []
  if (muhtamimFile.value) attachments.push({ type: 'muhtamim_consent', file_path: muhtamimFile.value.name })
  if (presidentFile.value) attachments.push({ type: 'president_consent', file_path: presidentFile.value.name })
  if (committeeFile.value) attachments.push({ type: 'committee_resolution', file_path: committeeFile.value.name })

  const markazApplication = {
    user: userId,
    exam: form.value.exam_id || null,
    markaz_type: form.value.markaz_type,
    requirements: form.value.requirements,
    status: 'pending',
    ip_address: window?.location?.hostname || '',
    printed: false
  }

  const payload = {
    markaz_application: markazApplication,
    main_madrasa_info: mainMadrasaInfo,
    associated_madrasas: associatedMadrasas,
    attachments: attachments
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/markaz/apply/', payload, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    loading.value = false

    if (response.data.success) {
      formErrors.value = []
<<<<<<< HEAD
      showFlashMessage('আপনার আবেদন সফলভাবে জমা হয়েছে! ধন্যবাদ।', 'success')
=======
      showToast('আপনার আবেদন সফলভাবে জমা হয়েছে! ধন্যবাদ।', 'success')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      // Optionally redirect or reset form
      // await router.push('/dashboard')
      // resetForm()
    } else {
      formErrors.value = [response.data.error || 'আবেদন জমা দিতে সমস্যা হয়েছে']
<<<<<<< HEAD
      showFlashMessage(response.data.error || 'আবেদন জমা দিতে সমস্যা হয়েছে', 'error')
=======
      showToast(response.data.error || 'আবেদন জমা দিতে সমস্যা হয়েছে', 'error')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
    }

  } catch (error) {
    loading.value = false
    if (error.response?.status === 401) {
      formErrors.value = ['আপনার লগইন সেশন শেষ হয়ে গেছে। পুনরায় লগইন করুন।']
<<<<<<< HEAD
      showFlashMessage('আপনার লগইন সেশন শেষ হয়ে গেছে। পুনরায় লগইন করুন।', 'error')
=======
      showToast('আপনার লগইন সেশন শেষ হয়ে গেছে। পুনরায় লগইন করুন।', 'error')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('user_type')
      localStorage.removeItem('permissions')
    } else if (error.response?.status === 403) {
      formErrors.value = ['আপনার এই কাজের অনুমতি নেই।']
<<<<<<< HEAD
      showFlashMessage('আপনার এই কাজের অনুমতি নেই।', 'error')
    } else if (error.response?.status >= 500) {
      formErrors.value = ['সার্ভার ত্রুটি। পরে আবার চেষ্টা করুন।']
      showFlashMessage('সার্ভার ত্রুটি হয়েছে। অনুগ্রহ করে কিছুক্ষণ পরে আবার চেষ্টা করুন।', 'error')
    } else if (error.request) {
      formErrors.value = ['নেটওয়ার্ক ত্রুটি। ইন্টারনেট সংযোগ চেক করুন।']
      showFlashMessage('নেটওয়ার্ক ত্রুটি হয়েছে। ইন্টারনেট সংযোগ চেক করুন।', 'error')
    } else {
      formErrors.value = ['আবেদন জমা দিতে সমস্যা হয়েছে: ' + (error.message || 'অজানা সমস্যা')]
      showFlashMessage('আবেদন জমা দিতে সমস্যা হয়েছে: ' + (error.message || 'অজানা সমস্যা'), 'error')
=======
      showToast('আপনার এই কাজের অনুমতি নেই।', 'error')
    } else if (error.response?.status >= 500) {
      formErrors.value = ['সার্ভার ত্রুটি। পরে আবার চেষ্টা করুন।']
      showToast('সার্ভার ত্রুটি হয়েছে। অনুগ্রহ করে কিছুক্ষণ পরে আবার চেষ্টা করুন।', 'error')
    } else if (error.request) {
      formErrors.value = ['নেটওয়ার্ক ত্রুটি। ইন্টারনেট সংযোগ চেক করুন।']
      showToast('নেটওয়ার্ক ত্রুটি হয়েছে। ইন্টারনেট সংযোগ চেক করুন।', 'error')
    } else {
      formErrors.value = ['আবেদন জমা দিতে সমস্যা হয়েছে: ' + (error.message || 'অজানা সমস্যা')]
      showToast('আবেদন জমা দিতে সমস্যা হয়েছে: ' + (error.message || 'অজানা সমস্যা'), 'error')
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01
    }
  }
}

const getCurrentDateTime = () => {
  return "2025-07-22 09:17:27"
}

const getCurrentUser = () => {
  return "tahsin866"
}

const handleConditionsAccepted = () => {
  conditionsAgreed.value = true
}

const isConditionsAccepted = computed(() => {
  return conditionsAgreed.value
})

const isStep1Valid = computed(() => {
  try {
    if (!form.value || !form.value.markaz_type) return false

    if (form.value.markaz_type === 'দরসিয়াত') {
      return form.value.fazilat !== '' && form.value.fazilat !== null &&
             form.value.sanabiya_ulya !== '' && form.value.sanabiya_ulya !== null &&
             !!nocFileForMadrahsa.value && !!resolutionFileForMadrahsa.value
    } else if (form.value.markaz_type === 'তাহফিজুল কোরআন') {
      return form.value.hifzul_quran !== '' && form.value.hifzul_quran !== null &&
             !!nocFileForMadrahsa.value && !!resolutionFileForMadrahsa.value
    } else if (form.value.markaz_type === 'কিরাআত') {
      return form.value.qirat !== '' && form.value.qirat !== null &&
             !!nocFileForMadrahsa.value && !!resolutionFileForMadrahsa.value
    }
    return false
  } catch  {
    return false
  }
})

const isStep2Valid = computed(() => {
  try {
    if (!rows?.value || rows.value.length === 0) return false
    return rows.value.every(row => {
      if (!row.madrasa_id) return false
      if (!row.files?.noc || !row.files?.resolution) return false

      if (form?.value.markaz_type === 'দরসিয়াত') {
        return (row.fazilat !== null && row.fazilat !== undefined) &&
               (row.sanabiya_ulya !== null && row.sanabiya_ulya !== undefined) &&
               (row.sanabiya !== null && row.sanabiya !== undefined) &&
               (row.mutawassita !== null && row.mutawassita !== undefined) &&
               (row.ibtedaiyyah !== null && row.ibtedaiyyah !== undefined)
      } else if (form?.value.markaz_type === 'তাহফিজুল কোরআন') {
        return (row.hifzul_quran !== null && row.hifzul_quran !== undefined)
      } else if (form?.value.markaz_type === 'কিরাআত') {
        return (row.qirat !== null && row.qirat !== undefined)
      }
      return false
    })
  } catch  {
    return false
  }
})

const isStep3Valid = computed(() => {
  try {
    return !!form.value.requirements
  } catch  {
    return false
  }
})

const canAccessStep = computed(() => {
  try {
    return {
      0: true,
      1: !!isConditionsAccepted.value,
      2: (!!isConditionsAccepted.value && !!isStep1Valid.value),
      3: (!!isConditionsAccepted.value && !!isStep1Valid.value && !!isStep2Valid.value)
    }
  } catch  {
    return { 0: true, 1: false, 2: false, 3: false }
  }
})

const getStepCompletionPercentage = computed(() => {
  try {
    let total = 0
    if (isConditionsAccepted?.value) total += 25
    if (isStep1Valid?.value) total += 25
    if (isStep2Valid?.value) total += 25
    if (isStep3Valid?.value) total += 25
    return Math.round(total)
  } catch  {
    return 0
  }
})

const stepLabels = [
  { label: "শর্তাবলী", icon: "pi pi-info-circle" },
  { label: "ধরন ও মূল তথ্য", icon: "pi pi-file-edit" },
  { label: "সংযুক্ত মাদ্রাসা", icon: "pi pi-building" },
  { label: "প্রয়োজনীয়তা ও সংযুক্তি", icon: "pi pi-paperclip" }
]

const getStepIcon = (index) => {
  if (index === 0 && isConditionsAccepted.value) return "pi pi-check-circle text-gray-700"
  if (index === 1 && isStep1Valid.value) return "pi pi-check-circle text-gray-700"
  if (index === 2 && isStep2Valid.value) return "pi pi-check-circle text-gray-700"
  if (index === 3 && isStep3Valid.value) return "pi pi-check-circle text-gray-700"
  return step.value === index ? "pi pi-spin pi-spinner text-gray-700" : "pi pi-circle-fill text-gray-400"
}

const handleTabChange = (event) => {
  if (event && typeof event.index === 'number') {
    step.value = event.index
  }
}

const goToNextStep = () => {
  const nextStep = step.value + 1
  if (canAccessStep.value[nextStep]) {
    step.value = nextStep
  }
}

async function fetchMadrashas() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/markaz/search-madrasa/')
    if (response.ok) {
      const data = await response.json()
      madrashas.value = data.map(item => ({
        id: item.id,
        name: item.mname,
        elhaqno: item.elhaqno || item.ElhaqNo || item.elhaq || ''
      }))
    }
  } catch {
    // fail silent
  }
}

onMounted(() => {
  fetchMadrashas()
})
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
            <TabPanel>
              <template #header>
                <div class="flex items-center">
                  <i :class="getStepIcon(0)" class="mr-2"></i>
                  <span class="font-bold">১. শর্তাবলী</span>
                </div>
              </template>
              <div>
                <MarkazConditions @continue="handleConditionsAccepted" />
                <div v-if="!conditionsAgreed" class="mt-6 p-4 bg-yellow-100 border-l-4 border-yellow-500 rounded-r shadow">
                  <div class="flex items-center">
                    <i class="fas fa-exclamation-triangle text-yellow-600 text-xl"></i>
                    <span class="ml-3 text-sm font-semibold text-yellow-700">
                      শর্তাবলী সম্মত হলে চেকবক্সে টিক দিন এবং পরবর্তী ধাপে যান।
                    </span>
                  </div>
                </div>
                <div class="flex justify-end p-4 bg-gray-50 rounded-b-lg border-t border-gray-200 mt-4">
                  <Button
                    label="পরবর্তী ধাপে যান"
                    icon="pi pi-arrow-right"
                    iconPos="right"
                    class="p-button-secondary"
                    :disabled="!conditionsAgreed"
                    @click="goToNextStep"
                  />
                </div>
              </div>
            </TabPanel>

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
                    label="আবেদন জমা দিন"
                    icon="pi pi-check"
                    iconPos="right"
                    class="p-button-success"
                    :loading="loading"
                    @click="submitForm"
                  />
                </div>
              </div>
            </TabPanel>
          </TabView>
        </div>
      </div>
    </div>
  </div>

<<<<<<< HEAD
  <!-- Flash Message Component -->
  <FlashMessage
    v-if="flashMessage.show"
    :type="flashMessage.type"
    :message="flashMessage.message"
    :title="flashMessage.title"
    :auto-hide="flashMessage.autoHide"
    :duration="flashMessage.duration"
    :show-close-button="flashMessage.showCloseButton"
    :glow-effect="flashMessage.glowEffect"
    @close="flashMessage.show = false"
  />
=======
  <!-- Toast Notification -->
  <transition name="toast-slide">
    <div v-if="toast.show"
         style="font-family: 'SolaimanLipi', sans-serif;"
         class="fixed top-6 right-6 z-50 flex items-start animate-toast-in"
         :class="toast.type === 'success' ? 'success-toast' : 'error-toast'">
      <div class="flex items-center bg-white rounded-lg shadow-xl border-l-4 p-4 min-w-[320px] max-w-md">
        <!-- Icon -->
        <div class="flex-shrink-0 mr-3">
          <div class="w-10 h-10 rounded-full flex items-center justify-center"
               :class="toast.type === 'success' ? 'bg-green-100' : 'bg-red-100'">
            <i :class="toast.type === 'success' ? 'pi pi-check text-green-600' : 'pi pi-times text-red-600'"
               class="text-lg font-bold"></i>
          </div>
        </div>

        <!-- Content -->
        <div class="flex-1">
          <h3 class="font-bold text-sm mb-1"
              :class="toast.type === 'success' ? 'text-green-800' : 'text-red-800'">
            {{ toast.type === 'success' ? 'সফলভাবে সম্পন্ন হয়েছে' : 'সমস্যা হয়েছে' }}
          </h3>
          <p class="text-sm"
             :class="toast.type === 'success' ? 'text-green-700' : 'text-red-700'">
            {{ toast.message }}
          </p>
        </div>

        <!-- Close Button -->
        <button @click="toast.show = false"
                class="flex-shrink-0 ml-3 text-gray-400 hover:text-gray-600 transition-colors">
          <i class="pi pi-times text-lg"></i>
        </button>
      </div>
    </div>
  </transition>
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01

</template>
 <style scoped>
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
  }

<<<<<<< HEAD
  /* Flash message styles are handled by the FlashMessage component */
=======
  /* Toast Animations */
  .toast-slide-enter-active {
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }
  .toast-slide-leave-active {
    transition: all 0.3s ease-in-out;
  }
  .toast-slide-enter-from {
    transform: translateX(100%) scale(0.8);
    opacity: 0;
  }
  .toast-slide-leave-to {
    transform: translateX(100%) scale(0.9);
    opacity: 0;
  }

  /* Toast Styles */
  .success-toast {
    border-left-color: #10b981;
  }
  .success-toast .border-l-4 {
    border-left-color: #10b981 !important;
  }
  .error-toast {
    border-left-color: #ef4444;
  }
  .error-toast .border-l-4 {
    border-left-color: #ef4444 !important;
  }

  /* Custom animation for smooth entrance */
  @keyframes toastSlideIn {
    0% {
      transform: translateX(100%) translateY(-20px);
      opacity: 0;
      filter: blur(4px);
    }
    50% {
      filter: blur(2px);
    }
    100% {
      transform: translateX(0) translateY(0);
      opacity: 1;
      filter: blur(0);
    }
  }

  .animate-toast-in {
    animation: toastSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  /* Hover effects */
  .success-toast:hover .bg-white,
  .error-toast:hover .bg-white {
    transform: translateY(-2px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  /* Pulse animation for success */
  @keyframes successPulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }

  .success-toast .w-10 {
    animation: successPulse 0.6s ease-in-out;
  }

  /* Shake animation for error */
  @keyframes errorShake {
    0%, 100% {
      transform: translateX(0);
    }
    25% {
      transform: translateX(-5px);
    }
    75% {
      transform: translateX(5px);
    }
  }

  .error-toast .w-10 {
    animation: errorShake 0.5s ease-in-out;
  }
>>>>>>> 23df0c6f00d2008386bfdb315ab240eaf25b2d01

  /* Old modal animation (keeping for reference) */
  .animate-modal-open {
    animation: modalOpen 0.3s cubic-bezier(0.4,0,0.2,1);
  }
  @keyframes modalOpen {
    0% {
      transform: scale(0.9) translateY(20px);
      opacity: 0;
    }
    100% {
      transform: scale(1) translateY(0);
      opacity: 1;
    }
  }
  </style>

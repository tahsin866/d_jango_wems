<script setup>
import { ref, defineEmits, defineProps, watch } from 'vue'
import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button'

const emit = defineEmits(['prev', 'submit', 'update-files'])
const props = defineProps({
  form: Object,
  boardOptions: Array
})

const studentPhotoFile = ref(null)
const birthCertificateFile = ref(null)
const marksheetFile = ref(null)
const studentPhotoPreview = ref(null)
const birthCertificatePreview = ref(null)
const marksheetPreview = ref(null)

const handleFileUpload = (event, fileType) => {
  const file = event.files[0]
  if (!file) return
  if (fileType === 'studentPhoto') {
    studentPhotoFile.value = file
    studentPhotoPreview.value = URL.createObjectURL(file)
  } else if (fileType === 'birthCertificate') {
    birthCertificateFile.value = file
    birthCertificatePreview.value = URL.createObjectURL(file)
  } else if (fileType === 'marksheet') {
    marksheetFile.value = file
    marksheetPreview.value = URL.createObjectURL(file)
  }
  emitUpdateFiles()
}

const removeFile = (fileType) => {
  if (fileType === 'studentPhoto') {
    if (studentPhotoPreview.value) URL.revokeObjectURL(studentPhotoPreview.value)
    studentPhotoFile.value = null; studentPhotoPreview.value = null
  }
  if (fileType === 'birthCertificate') {
    if (birthCertificatePreview.value) URL.revokeObjectURL(birthCertificatePreview.value)
    birthCertificateFile.value = null; birthCertificatePreview.value = null
  }
  if (fileType === 'marksheet') {
    if (marksheetPreview.value) URL.revokeObjectURL(marksheetPreview.value)
    marksheetFile.value = null; marksheetPreview.value = null
  }
  emitUpdateFiles()
}
const emitUpdateFiles = () => {
  emit('update-files', {
    studentPhoto: studentPhotoFile.value,
    birthCertificate: birthCertificateFile.value,
    marksheet: marksheetFile.value
  })
}
</script>

<template>
  <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mt-6">
    <div class="p-6 bg-white border-b border-gray-200">
      <h2 class="font-semibold text-xl text-gray-800 leading-tight mb-4">সংযুক্তি</h2>
      <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
        <div class="space-y-3">
          <label class="block font-medium text-sm text-gray-700">ছাত্রের ছবি (পাসপোর্ট সাইজ এবং নীল ব্যাকগ্রাইন্ড হতে হবে)</label>
          <div class="relative">
            <FileUpload mode="basic" :customUpload="true" @uploader="(event) => handleFileUpload(event, 'studentPhoto')" accept="image/*,.pdf" :auto="true" chooseLabel="ফাইল আপলোড করুন" class="w-full" />
            <div v-if="studentPhotoFile" class="flex justify-between items-center mt-2 p-2 bg-gray-50 border border-gray-200 rounded">
              <span class="text-gray-600">{{ studentPhotoFile.name }}</span>
              <div class="flex gap-2">
                <Button v-if="studentPhotoPreview" icon="pi pi-eye" class="p-button-text p-button-sm" @click="() => window.open(studentPhotoPreview, '_blank')" />
                <Button icon="pi pi-trash" class="p-button-text p-button-sm p-button-danger" @click="removeFile('studentPhoto')" />
              </div>
            </div>
          </div>
        </div>
        <div class="space-y-3">
          <label class="block font-medium text-sm text-gray-700">জন্ম নিবন্ধন/এন আইডি সংযুক্তি করুন</label>
          <div class="relative">
            <FileUpload mode="basic" :customUpload="true" @uploader="(event) => handleFileUpload(event, 'birthCertificate')" accept="image/*,.pdf,.doc,.docx" :auto="true" chooseLabel="ফাইল আপলোড করুন" class="w-full" />
            <div v-if="birthCertificateFile" class="flex justify-between items-center mt-2 p-2 bg-gray-50 border border-gray-200 rounded">
              <span class="text-gray-600">{{ birthCertificateFile.name }}</span>
              <div class="flex gap-2">
                <Button v-if="birthCertificatePreview" icon="pi pi-eye" class="p-button-text p-button-sm" @click="() => window.open(birthCertificatePreview, '_blank')" />
                <Button icon="pi pi-trash" class="p-button-text p-button-sm p-button-danger" @click="removeFile('birthCertificate')" />
              </div>
            </div>
          </div>
        </div>
        <div v-if="props.form.board_name && props.form.board_name !== 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ'" class="space-y-3">
          <label class="block font-medium text-sm text-gray-700">মার্কশীট সংযুক্ত করুন</label>
          <div class="relative">
            <FileUpload mode="basic" :customUpload="true" @uploader="(event) => handleFileUpload(event, 'marksheet')" accept="image/*,.pdf,.doc,.docx" :auto="true" chooseLabel="ফাইল আপলোড করুন" class="w-full" />
            <div v-if="marksheetFile" class="flex justify-between items-center mt-2 p-2 bg-gray-50 border border-gray-200 rounded">
              <span class="text-gray-600">{{ marksheetFile.name }}</span>
              <div class="flex gap-2">
                <Button v-if="marksheetPreview" icon="pi pi-eye" class="p-button-text p-button-sm" @click="() => window.open(marksheetPreview, '_blank')" />
                <Button icon="pi pi-trash" class="p-button-text p-button-sm p-button-danger" @click="removeFile('marksheet')" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex justify-between mt-6">

        <Button icon="pi pi-save" label="সংরক্ষণ করুন" class="inline-flex items-center px-4 py-2 bg-gray-800 border border-transparent rounded-md font-semibold text-xs text-white" @click="emit('submit')" />
      </div>
    </div>
  </div>
</template>

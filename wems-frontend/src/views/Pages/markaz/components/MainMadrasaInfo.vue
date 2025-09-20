<script setup lang="ts">
import { defineProps, defineEmits, computed } from 'vue'

const props = defineProps({
    form: {
      type: Object,
      required: true
    },
    nocFile: {
      type: Object,
      default: null
    },
    nocPreview: {
      type: String,
      default: null
    },
    resolutionFile: {
      type: Object,
      default: null
    },
    resolutionPreview: {
      type: String,
      default: null
    },
    errors: {
      type: Object,
      default: () => ({})
    }
})
// ...existing code...
import InputNumber from 'primevue/inputnumber'
import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button'


// Emits
const emit = defineEmits(['file-upload', 'remove-file', 'update:form'])

// Remove localForm, use props.form directly for v-model

// Computed properties to show fields
const showDarsiyatFields = computed(() => props.form.markaz_type === 'দরসিয়াত')
const showHifzField = computed(() => props.form.markaz_type === 'তাহফিজুল কোরআন')
const showKiratField = computed(() => props.form.markaz_type === 'কিরাআত')

// File select handlers
function onNocFileSelect(e: any) {
    if (e?.files?.[0]) {
        emit('file-upload', { files: [e.files[0]] }, 'noc')
    }
}

function onResolutionFileSelect(e: any) {
    if (e?.files?.[0]) {
        emit('file-upload', { files: [e.files[0]] }, 'resolution')
    }
}

// File type helpers
const isImageFile = (file: any) => {
  if (!file) return false;
  return ['image/jpeg', 'image/png', 'image/jpg'].includes(file.type);
};
</script>

<template>
  <div class="bg-white border border-gray-200 shadow-sm rounded-lg mb-8">
    <div class="p-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">আবেদনকৃত মাদরাসার তথ্য</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Darsiyat Fields -->
        <template v-if="showDarsiyatFields">
          <div class="flex flex-col">
            <label class="block font-medium text-sm text-gray-700 mb-1">
              ফযীলত <span class="text-red-500">*</span>
            </label>
            <InputNumber
              v-model="props.form.fazilat"
              placeholder="ছাত্র সংখ্যা লিখুন"
              :min="0"
              showButtons
              buttonLayout="horizontal"
              decrementButtonClass="p-button-secondary"
              incrementButtonClass="p-button-secondary"
              inputClass="w-full h-10 rounded border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500"
              class="w-full"
            />
            <p v-if="props.errors.fazilat" class="text-xs text-red-500 mt-1">{{ props.errors.fazilat }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-medium text-sm text-gray-700 mb-1">
              সানাবিয়া ‍উলইয়া <span class="text-red-500">*</span>
            </label>
            <InputNumber
              v-model="props.form.sanabiya_ulya"
              placeholder="ছাত্র সংখ্যা লিখুন"
              :min="0"
              showButtons
              buttonLayout="horizontal"
              decrementButtonClass="p-button-secondary"
              incrementButtonClass="p-button-secondary"
              inputClass="w-full h-10 rounded border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500"
              class="w-full"
            />
            <p v-if="props.errors.sanabiya_ulya" class="text-xs text-red-500 mt-1">{{ props.errors.sanabiya_ulya }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-medium text-sm text-gray-700 mb-1">
              সানাবিয়া <span class="text-red-500">*</span>
            </label>
            <InputNumber
              v-model="props.form.sanabiya"
              placeholder="ছাত্র সংখ্যা লিখুন"
              :min="0"
              showButtons
              buttonLayout="horizontal"
              decrementButtonClass="p-button-secondary"
              incrementButtonClass="p-button-secondary"
              inputClass="w-full h-10 rounded border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500"
              class="w-full"
            />
            <p v-if="props.errors.sanabiya" class="text-xs text-red-500 mt-1">{{ props.errors.sanabiya }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-medium text-sm text-gray-700 mb-1">
              মুতাওয়াসসিতা <span class="text-red-500">*</span>
            </label>
            <InputNumber
              v-model="props.form.mutawassita"
              placeholder="ছাত্র সংখ্যা লিখুন"
              :min="0"
              showButtons
              buttonLayout="horizontal"
              decrementButtonClass="p-button-secondary"
              incrementButtonClass="p-button-secondary"
              inputClass="w-full h-10 rounded border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500"
              class="w-full"
            />
            <p v-if="props.errors.mutawassita" class="text-xs text-red-500 mt-1">{{ props.errors.mutawassita }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-medium text-sm text-gray-700 mb-1">
                ইবতেদাইয়্যাহ <span class="text-red-500">*</span>
            </label>
        <InputNumber
          v-model="props.form.ibtedaiyyah"
                placeholder="ছাত্র সংখ্যা লিখুন"
                :min="0"
                showButtons
                buttonLayout="horizontal"
                decrementButtonClass="p-button-secondary"
                incrementButtonClass="p-button-secondary"
                inputClass="w-full h-10 rounded border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500"
                class="w-full"
            />
            <p v-if="props.errors.ibtedaiyyah" class="text-xs text-red-500 mt-1">{{ props.errors.ibtedaiyyah }}</p>
          </div>
        </template>
        <!-- Hifzul Quran Field -->
        <div v-if="showHifzField" class="flex flex-col">
          <label class="block font-medium text-sm text-gray-700 mb-1">
            হিফজুল কোরান <span class="text-red-500">*</span>
          </label>
          <InputNumber
            v-model="props.form.hifzul_quran"
            placeholder="ছাত্র সংখ্যা লিখুন"
            :min="0"
            showButtons
            buttonLayout="horizontal"
            decrementButtonClass="p-button-secondary"
            incrementButtonClass="p-button-secondary"
            inputClass="w-full h-10 rounded border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500"
            class="w-full"
          />
          <p v-if="props.errors.hifzul_quran" class="text-xs text-red-500 mt-1">{{ props.errors.hifzul_quran }}</p>
        </div>
        <!-- Kirat Field -->
        <div v-if="showKiratField" class="flex flex-col">
          <label class="block font-medium text-sm text-gray-700 mb-1">
            ইলমুল কিরআত <span class="text-red-500">*</span>
          </label>
          <InputNumber
            v-model="props.form.qirat"
            placeholder="ছাত্র সংখ্যা লিখুন"
            :min="0"
            showButtons
            buttonLayout="horizontal"
            decrementButtonClass="p-button-secondary"
            incrementButtonClass="p-button-secondary"
            inputClass="w-full h-10 rounded border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500"
            class="w-full"
            />
          <p v-if="props.errors.qirat" class="text-xs text-red-500 mt-1">{{ props.errors.qirat }}</p>
        </div>
      </div>
      <!-- File Upload Section -->
      <div class="mt-10">
        <h3 class="text-lg font-semibold text-gray-900 mb-5">
          প্রয়োজনীয় ডকুমেন্টস <span class="text-red-500">*</span>
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- NOC File Upload -->
          <div class="border border-gray-200 rounded-lg p-5 bg-gray-50">
            <div class="flex items-center justify-between mb-3">
              <label class="block font-medium text-sm text-gray-700">
                পূর্বের মাদরাসার অনাপত্তিপত্র <span class="text-red-500">*</span>
              </label>
              <div v-if="props.nocFile" class="flex items-center space-x-2">
                <a
                  :href="props.nocPreview"
                  target="_blank"
                  class="inline-flex items-center px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs text-gray-700"
                >দেখুন</a>
                <Button
                  label="মুছুন"
                  severity="danger"
                  size="small"
                  @click="$emit('remove-file', 'noc')"
                  icon="pi pi-times"
                  class="ml-1"
                />
              </div>
            </div>
            <FileUpload
              mode="basic"
              accept="application/pdf,image/*"
              :auto="true"
              chooseLabel="ফাইল নির্বাচন করুন"
              @select="onNocFileSelect"
              class="w-full"
            />
            <div v-if="!props.nocFile" class="text-xs text-red-500 mt-1">অনাপত্তিপত্র আপলোড করুন</div>
            <div v-if="props.nocPreview" class="mt-4">
              <div class="border rounded bg-white p-2">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-xs font-medium text-gray-500">প্রিভিউ</span>
                </div>
                <img
                  v-if="isImageFile(props.nocFile)"
                  :src="props.nocPreview"
                  class="max-h-32 mx-auto object-contain"
                />
                <div v-else class="flex items-center justify-center h-32 bg-gray-50 border rounded">
                  <i class="pi pi-file-pdf text-red-500 text-2xl mr-2"></i>
                  <span class="text-xs text-gray-600">PDF ফাইল</span>
                </div>
              </div>
            </div>
          </div>
          <!-- Resolution File Upload -->
          <div class="border border-gray-200 rounded-lg p-5 bg-gray-50">
            <div class="flex items-center justify-between mb-3">
              <label class="block font-medium text-sm text-gray-700">
                সম্মতিপত্র <span class="text-red-500">*</span>
              </label>
              <div v-if="props.resolutionFile" class="flex items-center space-x-2">
                <a
                  :href="props.resolutionPreview"
                  target="_blank"
                  class="inline-flex items-center px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs text-gray-700"
                >দেখুন</a>
                <Button
                  label="মুছুন"
                  severity="danger"
                  size="small"
                  @click="$emit('remove-file', 'resolution')"
                  icon="pi pi-times"
                  class="ml-1"
                />
              </div>
            </div>
            <FileUpload
              mode="basic"
              accept="application/pdf,image/*"
              :auto="true"
              chooseLabel="ফাইল নির্বাচন করুন"
              @select="onResolutionFileSelect"
              class="w-full"
            />
            <div v-if="!props.resolutionFile" class="text-xs text-red-500 mt-1">সম্মতিপত্র আপলোড করুন</div>
            <div v-if="props.resolutionPreview" class="mt-4">
              <div class="border rounded bg-white p-2">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-xs font-medium text-gray-500">প্রিভিউ</span>
                </div>
                <img
                  v-if="isImageFile(props.resolutionFile)"
                  :src="props.resolutionPreview"
                  class="max-h-32 mx-auto object-contain"
                />
                <div v-else class="flex items-center justify-center h-32 bg-gray-50 border rounded">
                  <i class="pi pi-file-pdf text-red-500 text-2xl mr-2"></i>
                  <span class="text-xs text-gray-600">PDF ফাইল</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

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
  <div class="bg-white border border-gray-300 shadow-lg rounded mb-8">
    <div class="p-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-8 flex items-center">
        <i class="fas fa-school mr-2 text-indigo-400"></i>
        আবেদনকৃত মাদরাসার তথ্য
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Darsiyat Fields -->
        <template v-if="showDarsiyatFields">
          <div class="flex flex-col">
            <label class="block font-bold text-sm text-gray-700 mb-1">
              ফযীলত <span class="text-red-500">*</span>
            </label>
            <input
              type="number"
              v-model="props.form.fazilat"
              min="0"
              placeholder="ছাত্র সংখ্যা লিখুন"
              class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
            />
            <p v-if="props.errors.fazilat" class="text-xs text-red-500 mt-1">{{ props.errors.fazilat }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-bold text-sm text-gray-700 mb-1">
              সানাবিয়া ‍উলইয়া <span class="text-red-500">*</span>
            </label>
            <input
              type="number"
              v-model="props.form.sanabiya_ulya"
              min="0"
              placeholder="ছাত্র সংখ্যা লিখুন"
              class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
            />
            <p v-if="props.errors.sanabiya_ulya" class="text-xs text-red-500 mt-1">{{ props.errors.sanabiya_ulya }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-bold text-sm text-gray-700 mb-1">
              সানাবিয়া <span class="text-red-500">*</span>
            </label>
            <input
              type="number"
              v-model="props.form.sanabiya"
              min="0"
              placeholder="ছাত্র সংখ্যা লিখুন"
              class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
            />
            <p v-if="props.errors.sanabiya" class="text-xs text-red-500 mt-1">{{ props.errors.sanabiya }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-bold text-sm text-gray-700 mb-1">
              মুতাওয়াসসিতা <span class="text-red-500">*</span>
            </label>
            <input
              type="number"
              v-model="props.form.mutawassita"
              min="0"
              placeholder="ছাত্র সংখ্যা লিখুন"
              class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
            />
            <p v-if="props.errors.mutawassita" class="text-xs text-red-500 mt-1">{{ props.errors.mutawassita }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-bold text-sm text-gray-700 mb-1">
              ইবতেদাইয়্যাহ <span class="text-red-500">*</span>
            </label>
            <input
              type="number"
              v-model="props.form.ibtedaiyyah"
              min="0"
              placeholder="ছাত্র সংখ্যা লিখুন"
              class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
            />
            <p v-if="props.errors.ibtedaiyyah" class="text-xs text-red-500 mt-1">{{ props.errors.ibtedaiyyah }}</p>
          </div>
        </template>
        <!-- Hifzul Quran Field -->
        <div v-if="showHifzField" class="flex flex-col">
          <label class="block font-bold text-sm text-gray-700 mb-1">
            হিফজুল কোরান <span class="text-red-500">*</span>
          </label>
          <input
            type="number"
            v-model="props.form.hifzul_quran"
            min="0"
            placeholder="ছাত্র সংখ্যা লিখুন"
            class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
          />
          <p v-if="props.errors.hifzul_quran" class="text-xs text-red-500 mt-1">{{ props.errors.hifzul_quran }}</p>
        </div>
        <!-- Kirat Field -->
        <div v-if="showKiratField" class="flex flex-col">
          <label class="block font-bold text-sm text-gray-700 mb-1">
            ইলমুল কিরআত <span class="text-red-500">*</span>
          </label>
          <input
            type="number"
            v-model="props.form.qirat"
            min="0"
            placeholder="ছাত্র সংখ্যা লিখুন"
            class="w-full h-10 rounded border border-gray-400 px-3 focus:border-indigo-500 focus:ring-indigo-500 font-bold text-gray-800 bg-gray-50 shadow"
          />
          <p v-if="props.errors.qirat" class="text-xs text-red-500 mt-1">{{ props.errors.qirat }}</p>
        </div>
      </div>
      <!-- File Upload Section -->
      <div class="mt-10">
        <h3 class="text-lg font-bold text-gray-800 mb-5 flex items-center">
          <i class="fas fa-file-alt mr-2 text-indigo-400"></i>
          প্রয়োজনীয় ডকুমেন্টস <span class="text-red-500">*</span>
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- NOC File Upload -->
          <div class="border border-gray-300 rounded-lg p-5 bg-gray-50 shadow">
            <div class="flex items-center justify-between mb-3">
              <label class="block font-bold text-sm text-gray-700">
                পূর্বের মাদরাসার অনাপত্তিপত্র <span class="text-red-500">*</span>
              </label>
              <div v-if="props.nocFile" class="flex items-center space-x-2">
                <a
                  :href="props.nocPreview"
                  target="_blank"
                  class="inline-flex items-center px-2 py-1 bg-indigo-50 border border-indigo-200 rounded text-xs text-indigo-700 font-bold"
                >দেখুন</a>
                <button
                  type="button"
                  @click="$emit('remove-file', 'noc')"
                  class="bg-red-100 hover:bg-red-200 text-red-700 font-bold px-3 py-1 rounded border border-red-300 ml-1 text-xs flex items-center"
                >
                  <i class="fas fa-times mr-1"></i> মুছুন
                </button>
              </div>
            </div>
            <input
              type="file"
              accept="application/pdf,image/*"
              @change="e => $emit('file-upload', e.target, 'noc')"
              class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded px-2 py-2"
            />
            <div v-if="!props.nocFile" class="text-xs text-red-500 mt-1">অনাপত্তিপত্র আপলোড করুন</div>
            <div v-if="props.nocPreview" class="mt-4">
              <div class="border rounded bg-white p-2">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-xs font-bold text-gray-500">প্রিভিউ</span>
                </div>
                <img
                  v-if="isImageFile(props.nocFile)"
                  :src="props.nocPreview"
                  class="max-h-32 mx-auto object-contain"
                />
                <div v-else class="flex items-center justify-center h-32 bg-gray-50 border rounded">
                  <i class="fas fa-file-pdf text-red-500 text-2xl mr-2"></i>
                  <span class="text-xs text-gray-600">PDF ফাইল</span>
                </div>
              </div>
            </div>
          </div>
          <!-- Resolution File Upload -->
          <div class="border border-gray-300 rounded-lg p-5 bg-gray-50 shadow">
            <div class="flex items-center justify-between mb-3">
              <label class="block font-bold text-sm text-gray-700">
                সম্মতিপত্র <span class="text-red-500">*</span>
              </label>
              <div v-if="props.resolutionFile" class="flex items-center space-x-2">
                <a
                  :href="props.resolutionPreview"
                  target="_blank"
                  class="inline-flex items-center px-2 py-1 bg-indigo-50 border border-indigo-200 rounded text-xs text-indigo-700 font-bold"
                >দেখুন</a>
                <button
                  type="button"
                  @click="$emit('remove-file', 'resolution')"
                  class="bg-red-100 hover:bg-red-200 text-red-700 font-bold px-3 py-1 rounded border border-red-300 ml-1 text-xs flex items-center"
                >
                  <i class="fas fa-times mr-1"></i> মুছুন
                </button>
              </div>
            </div>
            <input
              type="file"
              accept="application/pdf,image/*"
              @change="e => $emit('file-upload', e.target, 'resolution')"
              class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded px-2 py-2"
            />
            <div v-if="!props.resolutionFile" class="text-xs text-red-500 mt-1">সম্মতিপত্র আপলোড করুন</div>
            <div v-if="props.resolutionPreview" class="mt-4">
              <div class="border rounded bg-white p-2">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-xs font-bold text-gray-500">প্রিভিউ</span>
                </div>
                <img
                  v-if="isImageFile(props.resolutionFile)"
                  :src="props.resolutionPreview"
                  class="max-h-32 mx-auto object-contain"
                />
                <div v-else class="flex items-center justify-center h-32 bg-gray-50 border rounded">
                  <i class="fas fa-file-pdf text-red-500 text-2xl mr-2"></i>
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


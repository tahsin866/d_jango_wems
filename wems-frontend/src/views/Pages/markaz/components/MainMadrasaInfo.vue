<script setup>
import { computed } from 'vue'

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

defineEmits(['file-upload', 'remove-file', 'update:form'])

const showDarsiyatFields = computed(() => props.form.markaz_type === 'দরসিয়াত')
const showHifzField = computed(() => props.form.markaz_type === 'তাহফিজুল কোরআন')
const showKiratField = computed(() => props.form.markaz_type === 'কিরাআত')



function isImageFile(file) {
  if (!file) return false
  return ['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)
}
</script>

<template>
  <div class="bg-white border border-gray-200 shadow-sm rounded-sm mb-10 overflow-hidden">
    <div class="bg-green-800 to-indigo-900 p-3">
      <h2 class="text-2xl font-bold text-white flex items-center">
        <i class="fas fa-school mr-3 text-blue-200"></i>
        আবেদনকৃত মাদরাসার তথ্য
      </h2>
    </div>
    <div class="p-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <template v-if="showDarsiyatFields">
          <div class="flex flex-col">
            <label class="block font-semibold text-sm text-gray-700 mb-2">
              ফযীলত <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input
                type="number"
                v-model="localForm.value.fazilat"
                min="0"
                placeholder="ছাত্র সংখ্যা লিখুন"
                class="w-full h-12 rounded-sm border border-gray-300 px-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 font-medium text-gray-800 bg-white shadow-sm transition-all duration-200"
              />
            </div>
            <p v-if="props.errors.fazilat" class="text-xs text-red-500 mt-1">{{ props.errors.fazilat }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-semibold text-sm text-gray-700 mb-2">
              সানাবিয়া ‍উলইয়া <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input
                type="number"
                v-model="localForm.value.sanabiya_ulya"
                min="0"
                placeholder="ছাত্র সংখ্যা লিখুন"
                class="w-full h-12 rounded-sm border border-gray-300 px-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 font-medium text-gray-800 bg-white shadow-sm transition-all duration-200"
              />
            </div>
            <p v-if="props.errors.sanabiya_ulya" class="text-xs text-red-500 mt-1">{{ props.errors.sanabiya_ulya }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-semibold text-sm text-gray-700 mb-2">
              সানাবিয়া <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input
                type="number"
                v-model="localForm.value.sanabiya"
                min="0"
                placeholder="ছাত্র সংখ্যা লিখুন"
                class="w-full h-12 rounded-sm border border-gray-300 px-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 font-medium text-gray-800 bg-white shadow-sm transition-all duration-200"
              />
            </div>
            <p v-if="props.errors.sanabiya" class="text-xs text-red-500 mt-1">{{ props.errors.sanabiya }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-semibold text-sm text-gray-700 mb-2">
              মুতাওয়াসসিতা <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input
                type="number"
                v-model="localForm.value.mutawassita"
                min="0"
                placeholder="ছাত্র সংখ্যা লিখুন"
                class="w-full h-12 rounded-sm border border-gray-300 px-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 font-medium text-gray-800 bg-white shadow-sm transition-all duration-200"
              />
            </div>
            <p v-if="props.errors.mutawassita" class="text-xs text-red-500 mt-1">{{ props.errors.mutawassita }}</p>
          </div>
          <div class="flex flex-col">
            <label class="block font-semibold text-sm text-gray-700 mb-2">
              ইবতেদাইয়্যাহ <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input
                type="number"
                v-model="localForm.value.ibtedaiyyah"
                min="0"
                placeholder="ছাত্র সংখ্যা লিখুন"
                class="w-full h-12 rounded-sm border border-gray-300 px-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 font-medium text-gray-800 bg-white shadow-sm transition-all duration-200"
              />
            </div>
            <p v-if="props.errors.ibtedaiyyah" class="text-xs text-red-500 mt-1">{{ props.errors.ibtedaiyyah }}</p>
          </div>
        </template>
        <div v-if="showHifzField" class="flex flex-col">
          <label class="block font-semibold text-sm text-gray-700 mb-2">
            হিফজুল কোরান <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <input
              type="number"
              v-model="localForm.value.hifzul_quran"
              min="0"
              placeholder="ছাত্র সংখ্যা লিখুন"
              class="w-full h-12 rounded-sm border border-gray-300 px-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 font-medium text-gray-800 bg-white shadow-sm transition-all duration-200"
            />
          </div>
          <p v-if="props.errors.hifzul_quran" class="text-xs text-red-500 mt-1">{{ props.errors.hifzul_quran }}</p>
        </div>
        <div v-if="showKiratField" class="flex flex-col">
          <label class="block font-semibold text-sm text-gray-700 mb-2">
            ইলমুল কিরআত <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <input
              type="number"
              v-model="localForm.value.qirat"
              min="0"
              placeholder="ছাত্র সংখ্যা লিখুন"
              class="w-full h-12 rounded-sm border border-gray-300 px-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 font-medium text-gray-800 bg-white shadow-sm transition-all duration-200"
            />
          </div>
          <p v-if="props.errors.qirat" class="text-xs text-red-500 mt-1">{{ props.errors.qirat }}</p>
        </div>
      </div>
      <div class="mt-12">
        <div class="bg-green-800 to-indigo-900 p-3 rounded-t-sm">
          <h3 class="text-lg font-bold text-white flex items-center">
            <i class="fas fa-file-alt mr-3 text-blue-200"></i>
            প্রয়োজনীয় ডকুমেন্টস <span class="text-red-400">*</span>
          </h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 bg-gray-50 rounded-b-lg border border-t-0 border-gray-200">
          <div class="border border-gray-300 rounded-sm p-6 bg-white shadow-md">
            <div class="flex items-center justify-between mb-4">
              <label class="block font-semibold text-sm text-gray-700">
                পূর্বের মাদরাসার অনাপত্তিপত্র <span class="text-red-500">*</span>
              </label>
              <div v-if="props.nocFile" class="flex items-center space-x-2">
                <a
                  :href="props.nocPreview"
                  target="_blank"
                  class="inline-flex items-center px-3 py-1.5 bg-blue-50 border border-blue-200 rounded text-xs text-blue-700 font-semibold hover:bg-blue-100 transition-colors"
                >দেখুন</a>
                <button
                  type="button"
                  @click="$emit('remove-file', 'noc')"
                  class="bg-red-50 hover:bg-red-100 text-red-700 font-semibold px-3 py-1.5 rounded border border-red-200 text-xs flex items-center transition-colors"
                >
                  <i class="fas fa-times mr-1"></i> মুছুন
                </button>
              </div>
            </div>
            <div class="relative">
              <input
                type="file"
                accept="application/pdf,image/*"
                @change="e => $emit('file-upload', e.target, 'noc')"
                class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded-sm px-4 py-3 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200"
              />
            </div>
            <div v-if="!props.nocFile" class="text-xs text-red-500 mt-2">অনাপত্তিপত্র আপলোড করুন</div>
            <div v-if="props.nocPreview" class="mt-5">
              <div class="border rounded-sm bg-gray-50 p-4">
                <div class="flex justify-between items-center mb-3">
                  <span class="text-xs font-semibold text-gray-600 uppercase tracking-wider">প্রিভিউ</span>
                </div>
                <img
                  v-if="isImageFile(props.nocFile)"
                  :src="props.nocPreview"
                  class="max-h-40 mx-auto object-contain rounded-sm shadow-sm"
                />
                <div v-else class="flex items-center justify-center h-40 bg-gray-100 border-2 border-dashed border-gray-300 rounded-sm">
                  <div class="text-center">
                    <i class="fas fa-file-pdf text-red-500 text-3xl mb-2"></i>
                    <p class="text-sm text-gray-600">PDF ফাইল</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="border border-gray-300 rounded-sm p-6 bg-white shadow-md">
            <div class="flex items-center justify-between mb-4">
              <label class="block font-semibold text-sm text-gray-700">
                সম্মতিপত্র <span class="text-red-500">*</span>
              </label>
              <div v-if="props.resolutionFile" class="flex items-center space-x-2">
                <a
                  :href="props.resolutionPreview"
                  target="_blank"
                  class="inline-flex items-center px-3 py-1.5 bg-blue-50 border border-blue-200 rounded text-xs text-blue-700 font-semibold hover:bg-blue-100 transition-colors"
                >দেখুন</a>
                <button
                  type="button"
                  @click="$emit('remove-file', 'resolution')"
                  class="bg-red-50 hover:bg-red-100 text-red-700 font-semibold px-3 py-1.5 rounded border border-red-200 text-xs flex items-center transition-colors"
                >
                  <i class="fas fa-times mr-1"></i> মুছুন
                </button>
              </div>
            </div>
            <div class="relative">
              <input
                type="file"
                accept="application/pdf,image/*"
                @change="e => $emit('file-upload', e.target, 'resolution')"
                class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded-sm px-4 py-3 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200"
              />
            </div>
            <div v-if="!props.resolutionFile" class="text-xs text-red-500 mt-2">সম্মতিপত্র আপলোড করুন</div>
            <div v-if="props.resolutionPreview" class="mt-5">
              <div class="border rounded-sm bg-gray-50 p-4">
                <div class="flex justify-between items-center mb-3">
                  <span class="text-xs font-semibold text-gray-600 uppercase tracking-wider">প্রিভিউ</span>
                </div>
                <img
                  v-if="isImageFile(props.resolutionFile)"
                  :src="props.resolutionPreview"
                  class="max-h-40 mx-auto object-contain rounded-sm shadow-sm"
                />
                <div v-else class="flex items-center justify-center h-40 bg-gray-100 border-2 border-dashed border-gray-300 rounded-sm">
                  <div class="text-center">
                    <i class="fas fa-file-pdf text-red-500 text-3xl mb-2"></i>
                    <p class="text-sm text-gray-600">PDF ফাইল</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

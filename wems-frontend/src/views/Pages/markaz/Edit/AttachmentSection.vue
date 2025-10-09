<template>
  <div class="mb-6">
    <div class="bg-white rounded border border-gray-300 shadow-lg">
      <div class="p-8 border-b border-gray-200">
        <h3 class="text-xl font-bold text-gray-900 mb-6 flex items-center">
          <i class="fas fa-paperclip mr-2 text-indigo-400"></i>
          সংযুক্তি সমূহ
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- মুহতামিমের সম্মতিপত্র -->
          <div class="border border-gray-300 rounded-lg p-6 bg-gray-50 shadow">
            <div class="flex items-center justify-between mb-2">
              <label class="block font-bold text-sm text-gray-700">মুহতামিমের সম্মতিপত্র</label>
              <div v-if="muhtamimPreview" class="flex items-center space-x-2">
                <button
                  type="button"
                  @click="previewFile(muhtamimPreview)"
                  class="bg-indigo-100 hover:bg-indigo-200 text-indigo-700 font-bold px-3 py-1 rounded border border-indigo-300 text-xs flex items-center"
                >
                  <i class="fas fa-eye mr-1"></i> প্রিভিউ
                </button>
                <button
                  type="button"
                  @click="$emit('remove-file', 'muhtamim')"
                  class="bg-red-100 hover:bg-red-200 text-red-700 font-bold px-3 py-1 rounded border border-red-300 text-xs flex items-center"
                >
                  <i class="fas fa-times mr-1"></i> মুছুন
                </button>
              </div>
            </div>
            <input
              type="file"
              accept="application/pdf,image/*"
              @change="e => handleFileSelect(e, 'muhtamim')"
              class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded px-2 py-2"
            />
            <div v-if="muhtamimPreview" class="mt-2 preview-container">
              <div v-if="isPDF(muhtamimPreview)" class="flex items-center text-sm text-gray-700">
                <i class="fas fa-file-pdf text-red-500 mr-2 text-xl"></i>
                <span>PDF দস্তাবেজ আপলোড হয়েছে</span>
              </div>
              <img v-else :src="muhtamimPreview" class="max-h-32 rounded border border-gray-300 mt-2" />
            </div>
          </div>
          <!-- সভাপতির সম্মতিপত্র -->
          <div class="border border-gray-300 rounded-lg p-6 bg-gray-50 shadow">
            <div class="flex items-center justify-between mb-2">
              <label class="block font-bold text-sm text-gray-700">সভাপতির সম্মতিপত্র</label>
              <div v-if="presidentPreview" class="flex items-center space-x-2">
                <button
                  type="button"
                  @click="previewFile(presidentPreview)"
                  class="bg-indigo-100 hover:bg-indigo-200 text-indigo-700 font-bold px-3 py-1 rounded border border-indigo-300 text-xs flex items-center"
                >
                  <i class="fas fa-eye mr-1"></i> প্রিভিউ
                </button>
                <button
                  type="button"
                  @click="$emit('remove-file', 'president')"
                  class="bg-red-100 hover:bg-red-200 text-red-700 font-bold px-3 py-1 rounded border border-red-300 text-xs flex items-center"
                >
                  <i class="fas fa-times mr-1"></i> মুছুন
                </button>
              </div>
            </div>
            <input
              type="file"
              accept="application/pdf,image/*"
              @change="e => handleFileSelect(e, 'president')"
              class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded px-2 py-2"
            />
            <div v-if="presidentPreview" class="mt-2 preview-container">
              <div v-if="isPDF(presidentPreview)" class="flex items-center text-sm text-gray-700">
                <i class="fas fa-file-pdf text-red-500 mr-2 text-xl"></i>
                <span>PDF দস্তাবেজ আপলোড হয়েছে</span>
              </div>
              <img v-else :src="presidentPreview" class="max-h-32 rounded border border-gray-300 mt-2" />
            </div>
          </div>
          <!-- কমিটির সিদ্ধান্ত -->
          <div class="border border-gray-300 rounded-lg p-6 bg-gray-50 shadow">
            <div class="flex items-center justify-between mb-2">
              <label class="block font-bold text-sm text-gray-700">কমিটির সিদ্ধান্ত</label>
              <div v-if="committeePreview" class="flex items-center space-x-2">
                <button
                  type="button"
                  @click="previewFile(committeePreview)"
                  class="bg-indigo-100 hover:bg-indigo-200 text-indigo-700 font-bold px-3 py-1 rounded border border-indigo-300 text-xs flex items-center"
                >
                  <i class="fas fa-eye mr-1"></i> প্রিভিউ
                </button>
                <button
                  type="button"
                  @click="$emit('remove-file', 'committee')"
                  class="bg-red-100 hover:bg-red-200 text-red-700 font-bold px-3 py-1 rounded border border-red-300 text-xs flex items-center"
                >
                  <i class="fas fa-times mr-1"></i> মুছুন
                </button>
              </div>
            </div>
            <input
              type="file"
              accept="application/pdf,image/*"
              @change="e => handleFileSelect(e, 'committee')"
              class="block w-full text-sm text-gray-700 bg-white border border-gray-300 rounded px-2 py-2"
            />
            <div v-if="committeePreview" class="mt-2 preview-container">
              <div v-if="isPDF(committeePreview)" class="flex items-center text-sm text-gray-700">
                <i class="fas fa-file-pdf text-red-500 mr-2 text-xl"></i>
                <span>PDF দস্তাবেজ আপলোড হয়েছে</span>
              </div>
              <img v-else :src="committeePreview" class="max-h-32 rounded border border-gray-300 mt-2" />
            </div>
          </div>
        </div>
        <!-- File Preview Dialog -->
        <div v-if="previewDialogVisible" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
          <div class="bg-white rounded-lg shadow-2xl border border-gray-300 w-full max-w-2xl mx-auto p-6 relative">
            <button
              @click="previewDialogVisible = false"
              class="absolute top-3 right-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-full px-2 py-1"
            ><i class="fas fa-times"></i></button>
            <h3 class="text-lg font-bold text-gray-800 mb-4">{{ previewDialogTitle }}</h3>
            <div v-if="isPDF(previewUrl)">
              <iframe :src="previewUrl" width="100%" height="600px" frameborder="0"></iframe>
            </div>
            <img v-else :src="previewUrl" style="max-width: 100%; max-height: 70vh; margin: 0 auto; display: block" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';

const props = defineProps({
    muhtamimFile: Object,
    muhtamimPreview: String,
    presidentFile: Object,
    presidentPreview: String,
    committeeFile: Object,
    committeePreview: String
});

// For preview dialog
const previewDialogVisible = ref(false);
const previewUrl = ref('');
const previewDialogTitle = ref('ফাইল প্রিভিউ');

const emit = defineEmits(['file-upload', 'remove-file']);

// Detect if URL is a PDF
const isPDF = (url: string) => {
    if (!url) return false;
    return url.toLowerCase().includes('.pdf') || url.startsWith('data:application/pdf');
};

// Open preview dialog
const previewFile = (url: string) => {
    previewUrl.value = url;
    if (isPDF(url)) {
        previewDialogTitle.value = 'PDF দস্তাবেজ প্রিভিউ';
    } else {
        previewDialogTitle.value = 'ছবি প্রিভিউ';
    }
    previewDialogVisible.value = true;
};

// File select handler
const handleFileSelect = (event: any, type: string) => {
    let files: File[] = [];
    if (event && event.target && event.target.files) {
        files = Array.from(event.target.files);
    }
    emit('file-upload', { target: { files } }, type);
};
</script>

<style scoped>
.preview-container {
    transition: all 0.3s ease;
}
</style>

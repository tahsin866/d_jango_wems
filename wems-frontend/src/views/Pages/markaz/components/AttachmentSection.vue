<template>
    <div class="mb-6">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6 bg-white border-b border-gray-200">
                <h3 class="text-lg font-medium text-gray-900 mb-4">সংযুক্তি সমূহ</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- মুহতামিমের সম্মতিপত্র -->
                    <div class="border border-gray-300 rounded-md p-4">
                        <div class="flex items-center justify-between mb-2">
                            <label class="block font-medium text-sm text-gray-700">মুহতামিমের সম্মতিপত্র</label>
                            <div v-if="muhtamimPreview" class="flex items-center space-x-2">
                                <Button label="প্রিভিউ" icon="pi pi-eye" severity="info" size="small" @click="previewFile(muhtamimPreview)" class="p-button-text" />
                                <Button label="মুছুন" icon="pi pi-times" severity="danger" size="small" @click="$emit('remove-file', 'muhtamim')" />
                            </div>
                        </div>
                        <FileUpload mode="basic" accept="application/pdf,image/*" :auto="false" chooseLabel="ফাইল নির্বাচন করুন" @select="(e) => handleFileSelect(e, 'muhtamim')" class="w-full" />
                        <div v-if="muhtamimPreview" class="mt-2 preview-container">
                            <div v-if="isPDF(muhtamimPreview)" class="flex items-center text-sm text-gray-700">
                                <i class="pi pi-file-pdf text-red-500 mr-2 text-xl"></i>
                                <span>PDF দস্তাবেজ আপলোড হয়েছে</span>
                            </div>
                            <img v-else :src="muhtamimPreview" class="max-h-32 rounded border border-gray-300 mt-2" />
                        </div>
                    </div>

                    <!-- সভাপতির সম্মতিপত্র -->
                    <div class="border border-gray-300 rounded-md p-4">
                        <div class="flex items-center justify-between mb-2">
                            <label class="block font-medium text-sm text-gray-700">সভাপতির সম্মতিপত্র</label>
                            <div v-if="presidentPreview" class="flex items-center space-x-2">
                                <Button label="প্রিভিউ" icon="pi pi-eye" severity="info" size="small" @click="previewFile(presidentPreview)" class="p-button-text" />
                                <Button label="মুছুন" icon="pi pi-times" severity="danger" size="small" @click="$emit('remove-file', 'president')" />
                            </div>
                        </div>
                        <FileUpload mode="basic" accept="application/pdf,image/*" :auto="false" chooseLabel="ফাইল নির্বাচন করুন" @select="(e) => handleFileSelect(e, 'president')" class="w-full" />
                        <div v-if="presidentPreview" class="mt-2 preview-container">
                            <div v-if="isPDF(presidentPreview)" class="flex items-center text-sm text-gray-700">
                                <i class="pi pi-file-pdf text-red-500 mr-2 text-xl"></i>
                                <span>PDF দস্তাবেজ আপলোড হয়েছে</span>
                            </div>
                            <img v-else :src="presidentPreview" class="max-h-32 rounded border border-gray-300 mt-2" />
                        </div>
                    </div>

                    <!-- কমিটির সিদ্ধান্ত -->
                    <div class="border border-gray-300 rounded-md p-4">
                        <div class="flex items-center justify-between mb-2">
                            <label class="block font-medium text-sm text-gray-700">কমিটির সিদ্ধান্ত</label>
                            <div v-if="committeePreview" class="flex items-center space-x-2">
                                <Button label="প্রিভিউ" icon="pi pi-eye" severity="info" size="small" @click="previewFile(committeePreview)" class="p-button-text" />
                                <Button label="মুছুন" icon="pi pi-times" severity="danger" size="small" @click="$emit('remove-file', 'committee')" />
                            </div>
                        </div>
                        <FileUpload mode="basic" accept="application/pdf,image/*" :auto="false" chooseLabel="ফাইল নির্বাচন করুন" @select="(e) => handleFileSelect(e, 'committee')" class="w-full" />
                        <div v-if="committeePreview" class="mt-2 preview-container">
                            <div v-if="isPDF(committeePreview)" class="flex items-center text-sm text-gray-700">
                                <i class="pi pi-file-pdf text-red-500 mr-2 text-xl"></i>
                                <span>PDF দস্তাবেজ আপলোড হয়েছে</span>
                            </div>
                            <img v-else :src="committeePreview" class="max-h-32 rounded border border-gray-300 mt-2" />
                        </div>
                    </div>
                </div>

                <!-- File Preview Dialog -->
                <Dialog v-model:visible="previewDialogVisible" :header="previewDialogTitle" :modal="true" :style="{ width: '80vw' }">
                    <div class="preview-dialog-content">
                        <div v-if="isPDF(previewUrl)">
                            <iframe :src="previewUrl" width="100%" height="600px" frameborder="0"></iframe>
                        </div>
                        <img v-else :src="previewUrl" style="max-width: 100%; max-height: 70vh; margin: 0 auto; display: block" />
                    </div>
                </Dialog>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import FileUpload from 'primevue/fileupload';
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

// Handle file selection
const handleFileSelect = (event, type) => {
    try {
        // Check if event has preventDefault method before calling it
        if (event && typeof event.preventDefault === 'function') {
            event.preventDefault();
        }

        // Handle PrimeVue FileUpload event structure
        // PrimeVue FileUpload sends event with files property
        let files = [];

        if (event && event.files) {
            files = Array.isArray(event.files) ? event.files : [event.files];
        } else if (event && event.target && event.target.files) {
            files = Array.from(event.target.files);
        }

        // Keep the same event signature that parent component expects
        const originalEvent = {
            target: {
                files: files
            }
        };

        // Emit the same event as before
        emit('file-upload', originalEvent, type);
    } catch (error) {
        console.error('Error in handleFileSelect:', error);
        // Still emit with empty files to prevent component breaking
        emit('file-upload', { target: { files: [] } }, type);
    }
};

// Detect if URL is a PDF
const isPDF = (url) => {
    if (!url) return false;
    return url.toLowerCase().includes('.pdf') || url.startsWith('data:application/pdf');
};

// Open preview dialog
const previewFile = (url) => {
    previewUrl.value = url;

    // Set dialog title based on file type
    if (isPDF(url)) {
        previewDialogTitle.value = 'PDF দস্তাবেজ প্রিভিউ';
    } else {
        previewDialogTitle.value = 'ছবি প্রিভিউ';
    }

    previewDialogVisible.value = true;
};

// Setup emit to forward events to parent
const emit = defineEmits(['file-upload', 'remove-file']);
</script>

<style scoped>
.preview-container {
    transition: all 0.3s ease;
}

:deep(.p-fileupload-buttonbar) {
    padding: 0;
    background: transparent;
    border: none;
}

:deep(.p-fileupload-content) {
    padding: 0;
    background: transparent;
    border: none;
}

:deep(.p-button.p-fileupload-choose) {
    width: 100%;
}
</style>

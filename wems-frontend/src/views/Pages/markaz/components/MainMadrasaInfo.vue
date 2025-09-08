<script setup lang="ts">
import Button from 'primevue/button';
import FileUpload from 'primevue/fileupload';
import InputNumber from 'primevue/inputnumber';
import { computed, defineEmits, defineProps, ref, watch } from 'vue';
import type { FileUploadSelectEvent } from 'primevue/fileupload';

interface FormType {
    markaz_type?: string;
    fazilat?: number;
    sanabiya_ulya?: number;
    sanabiya?: number;
    mutawassita?: number;
    ibtedaiyyah?: number;
    hifzul_quran?: number;
    qirat?: number;
    // Add other fields if needed
}

interface ErrorsType {
    [key: string]: string;
}

const props = defineProps<{
    form: FormType;
    nocFile?: File | Blob | null;
    nocPreview?: string | null;
    resolutionFile?: File | Blob | null;
    resolutionPreview?: string | null;
    errors?: ErrorsType;
}>();

const emit = defineEmits<{
    (e: 'file-upload', fileWrap: { files: [File] }, type: string): void;
    (e: 'remove-file', type: string): void;
    (e: 'update:form', value: FormType): void;
}>();

const localForm = ref<FormType>({ ...props.form });

watch(
    () => props.form,
    (newVal) => {
        localForm.value = { ...newVal };
    },
    { deep: true }
);

watch(
    localForm,
    (newVal) => {
        emit('update:form', { ...newVal });
    },
    { deep: true }
);

const showDarsiyatFields = computed(() => props.form.markaz_type === 'দরসিয়াত');
const showHifzField = computed(() => props.form.markaz_type === 'তাহফিজুল কোরআন');
const showKiratField = computed(() => props.form.markaz_type === 'কিরাআত');

function onNocFileSelect(e: FileUploadSelectEvent) {
    if (e?.files?.[0]) {
        emit('file-upload', { files: [e.files[0]] }, 'noc');
    }
}

function onResolutionFileSelect(e: FileUploadSelectEvent) {
    if (e?.files?.[0]) {
        emit('file-upload', { files: [e.files[0]] }, 'resolution');
    }
}

// Updated to handle both File and Blob types
const isImageFile = (file?: File | Blob | null): boolean => {
    if (!file) return false;
    return ['image/jpeg', 'image/png', 'image/jpg'].includes(file.type);
};

const currentDateTime = '2025-09-07 08:41:53';
const currentUser = 'tahsin866';

// Updated to handle both File and Blob types
const formatFileSize = (bytes?: number): string => {
    if (!bytes) return '0 KB';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Updated to handle both File and Blob types
const getFileName = (file?: File | Blob | null): string => {
    if (!file) return '';

    // Check if it's a File object (has name property)
    if (file instanceof File && file.name) {
        if (file.name.length > 24) {
            return file.name.substring(0, 12) + '...' + file.name.substring(file.name.length - 8);
        }
        return file.name;
    }

    // If it's a Blob without name, return a default name based on type
    if (file.type.includes('pdf')) {
        return 'document.pdf';
    } else if (file.type.includes('image')) {
        return 'image.' + file.type.split('/')[1];
    }

    return 'file';
};
</script>

<template>
    <div class="text-gray-800 dark:text-gray-100">
        <!-- Section Title -->
        <div class="mb-6">
            <h2 class="text-lg font-medium mb-2 text-gray-800 dark:text-gray-100">আবেদনকৃত মাদরাসার তথ্য</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400">
                মাদরাসার পরীক্ষার্থীর সংখ্যা সঠিকভাবে পূরণ করুন। সকল তারকাচিহ্নিত (*) ক্ষেত্র অবশ্যই পূরণ করতে হবে।
            </p>
        </div>

        <!-- Student Numbers Section -->
        <div class="bg-gray-50 border border-gray-200 dark:bg-slate-700/50 dark:border-slate-600 rounded-lg p-5 mb-6">
            <h3 class="pb-3 mb-4 font-medium text-gray-700 border-b border-gray-200 dark:text-gray-200 dark:border-slate-600">
                <i class="pi pi-users mr-2"></i>পরীক্ষার্থীর সংখ্যা
            </h3>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                <!-- Darsiyat Fields -->
                <div v-if="showDarsiyatFields" class="flex flex-col">
                    <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        ফযীলত <span class="text-red-500">*</span>
                    </label>
                    <InputNumber
                        v-model="localForm.fazilat"
                        placeholder="ছাত্র সংখ্যা লিখুন"
                        :min="0"
                        showButtons
                        buttonLayout="horizontal"
                        :inputClass="'w-full p-2.5 bg-white border-gray-300 text-gray-900 rounded-lg shadow-sm dark:bg-slate-800 dark:border-slate-600 dark:text-white'"
                        decrementButtonClass="p-button-secondary"
                        incrementButtonClass="p-button-secondary"
                        class="w-full"
                    />
                    <p v-if="props.errors?.fazilat" class="text-sm text-red-500 mt-1">{{ props.errors.fazilat }}</p>
                </div>

                <div v-if="showDarsiyatFields" class="flex flex-col">
                    <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        সানাবিয়া ‍উলইয়া <span class="text-red-500">*</span>
                    </label>
                    <InputNumber
                        v-model="localForm.sanabiya_ulya"
                        placeholder="ছাত্র সংখ্যা লিখুন"
                        :min="0"
                        showButtons
                        buttonLayout="horizontal"
                        :inputClass="'w-full p-2.5 bg-white border-gray-300 text-gray-900 rounded-lg shadow-sm dark:bg-slate-800 dark:border-slate-600 dark:text-white'"
                        decrementButtonClass="p-button-secondary"
                        incrementButtonClass="p-button-secondary"
                        class="w-full"
                    />
                    <p v-if="props.errors?.sanabiya_ulya" class="text-sm text-red-500 mt-1">{{ props.errors.sanabiya_ulya }}</p>
                </div>

                <div v-if="showDarsiyatFields" class="flex flex-col">
                    <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        সানাবিয়া <span class="text-red-500">*</span>
                    </label>
                    <InputNumber
                        v-model="localForm.sanabiya"
                        placeholder="ছাত্র সংখ্যা লিখুন"
                        :min="0"
                        showButtons
                        buttonLayout="horizontal"
                        :inputClass="'w-full p-2.5 bg-white border-gray-300 text-gray-900 rounded-lg shadow-sm dark:bg-slate-800 dark:border-slate-600 dark:text-white'"
                        decrementButtonClass="p-button-secondary"
                        incrementButtonClass="p-button-secondary"
                        class="w-full"
                    />
                    <p v-if="props.errors?.sanabiya" class="text-sm text-red-500 mt-1">{{ props.errors.sanabiya }}</p>
                </div>

                <div v-if="showDarsiyatFields" class="flex flex-col">
                    <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        মুতাওয়াসসিতা <span class="text-red-500">*</span>
                    </label>
                    <InputNumber
                        v-model="localForm.mutawassita"
                        placeholder="ছাত্র সংখ্যা লিখুন"
                        :min="0"
                        showButtons
                        buttonLayout="horizontal"
                        :inputClass="'w-full p-2.5 bg-white border-gray-300 text-gray-900 rounded-lg shadow-sm dark:bg-slate-800 dark:border-slate-600 dark:text-white'"
                        decrementButtonClass="p-button-secondary"
                        incrementButtonClass="p-button-secondary"
                        class="w-full"
                    />
                    <p v-if="props.errors?.mutawassita" class="text-sm text-red-500 mt-1">{{ props.errors.mutawassita }}</p>
                </div>

                <div v-if="showDarsiyatFields" class="flex flex-col">
                    <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        ইবতেদাইয়্যাহ <span class="text-red-500">*</span>
                    </label>
                    <InputNumber
                        v-model="localForm.ibtedaiyyah"
                        placeholder="ছাত্র সংখ্যা লিখুন"
                        :min="0"
                        showButtons
                        buttonLayout="horizontal"
                        :inputClass="'w-full p-2.5 bg-white border-gray-300 text-gray-900 rounded-lg shadow-sm dark:bg-slate-800 dark:border-slate-600 dark:text-white'"
                        decrementButtonClass="p-button-secondary"
                        incrementButtonClass="p-button-secondary"
                        class="w-full"
                    />
                    <p v-if="props.errors?.ibtedaiyyah" class="text-sm text-red-500 mt-1">{{ props.errors.ibtedaiyyah }}</p>
                </div>

                <!-- Hifzul Quran Field -->
                <div v-if="showHifzField" class="flex flex-col">
                    <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        হিফজুল কোরান <span class="text-red-500">*</span>
                    </label>
                    <InputNumber
                        v-model="localForm.hifzul_quran"
                        placeholder="ছাত্র সংখ্যা লিখুন"
                        :min="0"
                        showButtons
                        buttonLayout="horizontal"
                        :inputClass="'w-full p-2.5 bg-white border-gray-300 text-gray-900 rounded-lg shadow-sm dark:bg-slate-800 dark:border-slate-600 dark:text-white'"
                        decrementButtonClass="p-button-secondary"
                        incrementButtonClass="p-button-secondary"
                        class="w-full"
                    />
                    <p v-if="props.errors?.hifzul_quran" class="text-sm text-red-500 mt-1">{{ props.errors.hifzul_quran }}</p>
                </div>

                <!-- Kirat Field -->
                <div v-if="showKiratField" class="flex flex-col">
                    <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        ইলমুল কিরআত <span class="text-red-500">*</span>
                    </label>
                    <InputNumber
                        v-model="localForm.qirat"
                        placeholder="ছাত্র সংখ্যা লিখুন"
                        :min="0"
                        showButtons
                        buttonLayout="horizontal"
                        :inputClass="'w-full p-2.5 bg-white border-gray-300 text-gray-900 rounded-lg shadow-sm dark:bg-slate-800 dark:border-slate-600 dark:text-white'"
                        decrementButtonClass="p-button-secondary"
                        incrementButtonClass="p-button-secondary"
                        class="w-full"
                    />
                    <p v-if="props.errors?.qirat" class="text-sm text-red-500 mt-1">{{ props.errors.qirat }}</p>
                </div>
            </div>
        </div>

        <!-- Documents Section -->
        <div class="bg-gray-50 border border-gray-200 dark:bg-slate-700/50 dark:border-slate-600 rounded-lg p-5 mb-6">
            <h3 class="pb-3 mb-4 font-medium text-gray-700 border-b border-gray-200 dark:text-gray-200 dark:border-slate-600">
                <i class="pi pi-file-pdf mr-2"></i>প্রয়োজনীয় ডকুমেন্টস <span class="text-red-500">*</span>
            </h3>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- NOC File Upload -->
                <div class="bg-white border border-gray-300 dark:bg-slate-800 dark:border-slate-600 rounded-lg overflow-hidden">
                    <div class="bg-gray-50 border-b border-gray-200 dark:bg-slate-700 dark:border-slate-600 px-5 py-3 flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-file-export text-lg text-blue-600 dark:text-blue-400"></i>
                            <label class="font-medium text-sm text-gray-700 dark:text-gray-300">
                                পূর্বের মাদরাসার অনাপত্তিপত্র <span class="text-red-500">*</span>
                            </label>
                        </div>
                        <div class="flex items-center gap-2">
                            <span v-if="props.nocFile" class="text-xs font-medium px-2 py-0.5 rounded-full border bg-blue-50 text-blue-700 border-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800">
                                <i class="pi pi-check-circle mr-1"></i>আপলোড করা হয়েছে
                            </span>
                            <span v-else class="text-xs font-medium px-2 py-0.5 rounded-full border bg-yellow-50 text-yellow-700 border-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-300 dark:border-yellow-800">
                                <i class="pi pi-exclamation-triangle mr-1"></i>আপলোড করুন
                            </span>
                        </div>
                    </div>

                    <div class="p-5">
                        <div v-if="props.nocFile" class="mb-4">
                            <!-- File preview area -->
                            <div class="bg-gray-50 border border-gray-200 dark:bg-slate-900/50 dark:border-slate-700 rounded-lg overflow-hidden">
                                <div class="bg-gray-100 border-b border-gray-200 text-gray-500 dark:bg-slate-700 dark:border-slate-600 dark:text-gray-300 px-3 py-2 flex justify-between items-center text-xs font-medium">
                                    <span>{{ getFileName(props.nocFile) }}</span>
                                    <span>{{ formatFileSize(props.nocFile.size) }}</span>
                                </div>
                                <div class="p-3">
                                    <img v-if="isImageFile(props.nocFile)" :src="props.nocPreview"
                                         class="max-h-40 mx-auto object-contain rounded" />
                                    <div v-else class="flex items-center justify-center h-40 rounded bg-gray-50 dark:bg-slate-800">
                                        <div class="flex flex-col items-center gap-2">
                                            <i class="pi pi-file-pdf text-3xl text-red-500 dark:text-red-400"></i>
                                            <span class="text-sm text-gray-600 dark:text-gray-400">PDF ফাইল</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Action buttons -->
                            <div class="mt-3 flex gap-2">
                                <a :href="props.nocPreview || ''" target="_blank" class="flex items-center justify-center gap-1 px-3 py-1.5 rounded-md text-sm font-medium transition-colors bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 shadow-sm dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-gray-200 dark:border-slate-600">
                                    <i class="pi pi-eye"></i> দেখুন
                                </a>
                                <button @click="emit('remove-file', 'noc')" class="flex items-center justify-center gap-1 px-3 py-1.5 rounded-md text-sm font-medium transition-colors bg-red-50 hover:bg-red-100 text-red-700 border border-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 dark:text-red-300 dark:border-red-800">
                                    <i class="pi pi-trash"></i> মুছুন
                                </button>
                            </div>
                        </div>

                        <!-- Upload area -->
                        <div v-if="!props.nocFile" class="flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-6 border-gray-300 bg-gray-50 dark:border-slate-600 dark:bg-slate-800/50">
                            <i class="pi pi-cloud-upload text-4xl mb-2 text-gray-400 dark:text-gray-500"></i>
                            <p class="mb-2 text-sm text-center text-gray-600 dark:text-gray-400">
                                <span class="font-semibold">ফাইল আপলোড করতে ক্লিক করুন</span> অথবা এখানে টেনে আনুন
                            </p>
                            <p class="text-xs text-center mb-4 text-gray-500 dark:text-gray-500">
                                PDF, PNG, JPG (সর্বাধিক 10MB)
                            </p>
                            <FileUpload mode="basic" accept="application/pdf,image/*" :auto="true"
                                chooseLabel="ফাইল নির্বাচন করুন" @select="onNocFileSelect"
                                class="w-full" />
                        </div>

                        <div v-if="!props.nocFile && props.errors?.noc_file" class="mt-2 text-sm text-red-500">{{ props.errors.noc_file }}</div>

                        <!-- Upload metadata info -->
                        <div class="mt-3 rounded-md p-3 text-xs bg-blue-50 border border-blue-100 dark:bg-slate-900/30 dark:border-slate-700">
                            <div class="flex items-center gap-2">
                                <i class="pi pi-info-circle text-blue-600 dark:text-blue-400"></i>
                                <p class="text-gray-700 dark:text-gray-300">
                                    <span class="font-medium">আপলোড তারিখ:</span> {{ currentDateTime }} <span class="mx-1">|</span>
                                    <span class="font-medium">ইউজার:</span> {{ currentUser }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Resolution File Upload -->
                <div class="bg-white border border-gray-300 dark:bg-slate-800 dark:border-slate-600 rounded-lg overflow-hidden">
                    <div class="bg-gray-50 border-b border-gray-200 dark:bg-slate-700 dark:border-slate-600 px-5 py-3 flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-file-export text-lg text-blue-600 dark:text-blue-400"></i>
                            <label class="font-medium text-sm text-gray-700 dark:text-gray-300">
                                সম্মতিপত্র <span class="text-red-500">*</span>
                            </label>
                        </div>
                        <div class="flex items-center gap-2">
                            <span v-if="props.resolutionFile" class="text-xs font-medium px-2 py-0.5 rounded-full border bg-blue-50 text-blue-700 border-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800">
                                <i class="pi pi-check-circle mr-1"></i>আপলোড করা হয়েছে
                            </span>
                            <span v-else class="text-xs font-medium px-2 py-0.5 rounded-full border bg-yellow-50 text-yellow-700 border-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-300 dark:border-yellow-800">
                                <i class="pi pi-exclamation-triangle mr-1"></i>আপলোড করুন
                            </span>
                        </div>
                    </div>

                    <div class="p-5">
                        <div v-if="props.resolutionFile" class="mb-4">
                            <!-- File preview area -->
                            <div class="bg-gray-50 border border-gray-200 dark:bg-slate-900/50 dark:border-slate-700 rounded-lg overflow-hidden">
                                <div class="bg-gray-100 border-b border-gray-200 text-gray-500 dark:bg-slate-700 dark:border-slate-600 dark:text-gray-300 px-3 py-2 flex justify-between items-center text-xs font-medium">
                                    <span>{{ getFileName(props.resolutionFile) }}</span>
                                    <span>{{ formatFileSize(props.resolutionFile.size) }}</span>
                                </div>
                                <div class="p-3">
                                    <img v-if="isImageFile(props.resolutionFile)" :src="props.resolutionPreview"
                                         class="max-h-40 mx-auto object-contain rounded" />
                                    <div v-else class="flex items-center justify-center h-40 rounded bg-gray-50 dark:bg-slate-800">
                                        <div class="flex flex-col items-center gap-2">
                                            <i class="pi pi-file-pdf text-3xl text-red-500 dark:text-red-400"></i>
                                            <span class="text-sm text-gray-600 dark:text-gray-400">PDF ফাইল</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Action buttons -->
                            <div class="mt-3 flex gap-2">
                                <a :href="props.resolutionPreview || ''" target="_blank" class="flex items-center justify-center gap-1 px-3 py-1.5 rounded-md text-sm font-medium transition-colors bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 shadow-sm dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-gray-200 dark:border-slate-600">
                                    <i class="pi pi-eye"></i> দেখুন
                                </a>
                                <button @click="emit('remove-file', 'resolution')" class="flex items-center justify-center gap-1 px-3 py-1.5 rounded-md text-sm font-medium transition-colors bg-red-50 hover:bg-red-100 text-red-700 border border-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 dark:text-red-300 dark:border-red-800">
                                    <i class="pi pi-trash"></i> মুছুন
                                </button>
                            </div>
                        </div>

                        <!-- Upload area -->
                        <div v-if="!props.resolutionFile" class="flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-6 border-gray-300 bg-gray-50 dark:border-slate-600 dark:bg-slate-800/50">
                            <i class="pi pi-cloud-upload text-4xl mb-2 text-gray-400 dark:text-gray-500"></i>
                            <p class="mb-2 text-sm text-center text-gray-600 dark:text-gray-400">
                                <span class="font-semibold">ফাইল আপলোড করতে ক্লিক করুন</span> অথবা এখানে টেনে আনুন
                            </p>
                            <p class="text-xs text-center mb-4 text-gray-500 dark:text-gray-500">
                                PDF, PNG, JPG (সর্বাধিক 10MB)
                            </p>
                            <FileUpload mode="basic" accept="application/pdf,image/*" :auto="true"
                                chooseLabel="ফাইল নির্বাচন করুন" @select="onResolutionFileSelect"
                                class="w-full" />
                        </div>

                        <div v-if="!props.resolutionFile && props.errors?.resolution_file" class="mt-2 text-sm text-red-500">{{ props.errors.resolution_file }}</div>

                        <!-- Upload metadata info -->
                        <div class="mt-3 rounded-md p-3 text-xs bg-blue-50 border border-blue-100 dark:bg-slate-900/30 dark:border-slate-700">
                            <div class="flex items-center gap-2">
                                <i class="pi pi-info-circle text-blue-600 dark:text-blue-400"></i>
                                <p class="text-gray-700 dark:text-gray-300">
                                    <span class="font-medium">আপলোড তারিখ:</span> {{ currentDateTime }} <span class="mx-1">|</span>
                                    <span class="font-medium">ইউজার:</span> {{ currentUser }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

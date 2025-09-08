<template>

      <div
        style="font-family: 'SolaimanLipi', sans-serif;"
        class="min-h-screen bg-gray-50 dark:bg-slate-900 py-10"
      >
        <div class="mx-auto rounded-md  border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden">
          <!-- Page Title Header -->
          <div class="bg-gradient-to-r from-gray-900 to-gray-800 dark:from-slate-900 dark:to-slate-800 shadow-md">
              <div class="px-6 py-6 sm:py-8 flex flex-col md:flex-row justify-between items-center gap-4">
                  <div class="flex items-center mb-4 md:mb-0">
                      <div class="bg-slate-800 text-white p-3.5 rounded-lg shadow mr-5 flex items-center justify-center">
                          <i class="pi pi-building text-2xl" aria-hidden="true"></i>
                      </div>
                      <div>
                          <h1 class="text-3xl font-bold text-white tracking-wide">মারকায আবেদন ফরম</h1>
                          <p class="mt-1 text-slate-300 text-sm">
                              পরীক্ষা: <span class="font-medium">{{ form.exam_name || 'লোড হচ্ছে...' }}</span>
                          </p>
                      </div>
                  </div>
                  <div class="flex flex-col items-end">
                      <div class="bg-gray-900/70 border border-gray-700 rounded-lg px-4 py-2 text-white text-sm">
                          <div class="flex items-center justify-between gap-3">
                              <div class="flex items-center gap-2">
                                  <i class="pi pi-calendar" aria-hidden="true"></i>
                                  <span>{{ getCurrentDateTime() }}</span>
                              </div>
                              <div class="h-4 border-r border-white/30"></div>
                              <div class="flex items-center gap-2">
                                  <i class="pi pi-user" aria-hidden="true"></i>
                                  <span>{{ getCurrentUser() }}</span>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>

          <!-- Progress Tracker -->
          <div class="px-6 pt-8">
              <div class="bg-gray-100 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl p-5 mb-8">
                  <div class="flex flex-col">
                      <div class="flex justify-between items-center mb-3">
                          <h3 class="text-lg font-medium text-gray-700 dark:text-gray-100">আবেদন অগ্রগতি</h3>
                          <span class="px-3 py-1 rounded-full text-sm font-medium bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300 border border-emerald-800">
                              {{ getStepCompletionPercentage }}% সম্পন্ন
                          </span>
                      </div>
                      <div class="bg-gray-200 dark:bg-slate-700 h-2 w-full rounded-full">
                          <div
                              class="h-2 rounded-full transition-all duration-500 ease-out bg-blue-600 dark:bg-blue-500"
                              :style="`width: ${getStepCompletionPercentage}%`"
                          ></div>
                      </div>
                      <div class="hidden md:flex justify-between mt-4">
                          <div
                              v-for="(stepLabel, index) in stepLabels"
                              :key="index"
                              class="flex flex-col items-center w-1/4 transition-all duration-300"
                              :class="{ 'opacity-50': !canAccessStep[index] && index !== step }"
                          >
                              <div
                                  :class="[
                                      'flex items-center justify-center h-10 w-10 rounded-full mb-2',
                                      step === index
                                          ? 'bg-blue-200 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300'
                                          : (index === 0 && isConditionsAccepted) || (index === 1 && isStep1Valid) || (index === 2 && isStep2Valid) || (index === 3 && isStep3Valid)
                                            ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                                            : 'bg-gray-200 text-gray-400 dark:bg-slate-700 dark:text-gray-400'
                                  ]"
                              >
                                  <i :class="[stepLabel.icon, 'text-lg']" aria-hidden="true"></i>
                              </div>
                              <span class="text-sm font-medium text-gray-600 dark:text-gray-300">{{ stepLabel.label }}</span>
                          </div>
                      </div>
                  </div>
              </div>
          </div>

          <!-- Main Content Tabs -->
          <div class="px-6 pb-10">
              <TabView v-model:activeIndex="step" class="custom-tabs" :scrollable="true" @tab-change="handleTabChange">
                  <!-- Conditions Tab -->
                  <TabPanel :value="0">
                      <template #header>
                          <div class="flex items-center">
                              <i :class="getStepIcon(0)" class="mr-2" aria-hidden="true"></i>
                              <span class="font-medium text-gray-700 dark:text-gray-200">১. শর্তাবলী</span>
                          </div>
                      </template>
                      <div class="bg-white dark:bg-slate-800 rounded-xl p-6">
                          <MarkazConditions @continue="handleContinue" />
                      </div>
                  </TabPanel>

                  <!-- Basic Info Tab -->
                  <TabPanel :value="1" :disabled="!canAccessStep[1]">
                      <template #header>
                          <div class="flex items-center" :class="{ 'opacity-50': !canAccessStep[1] }">
                              <i :class="getStepIcon(1)" class="mr-2" aria-hidden="true"></i>
                              <span class="font-medium text-gray-700 dark:text-gray-200">২. ধরন ও মূল তথ্য</span>
                              <i v-if="!canAccessStep[1]" class="pi pi-lock ml-2 text-yellow-500 dark:text-yellow-400" aria-hidden="true"></i>
                          </div>
                      </template>
                      <div class="bg-white dark:bg-slate-800 rounded-xl p-6">
                          <h3 class="text-xl font-bold mb-6 pb-2 border-b text-gray-800 dark:text-gray-100 border-gray-200 dark:border-slate-600">মারকাযের ধরণ ও মূল তথ্য</h3>

                          <div class="bg-blue-50 border-l-4 border-blue-500 dark:bg-blue-900/20 dark:border-blue-700 p-4 mb-6 rounded-r-md">
                              <div class="flex">
                                  <div class="flex-shrink-0">
                                      <i class="pi pi-info-circle text-blue-500 dark:text-blue-400" aria-hidden="true"></i>
                                  </div>
                                  <div class="ml-3">
                                      <p class="text-sm text-blue-700 dark:text-blue-300">নিম্নে আপনার মারকাযের ধরণ নির্বাচন করুন এবং প্রয়োজনীয় তথ্য পূরণ করুন। সমস্ত তারকাচিহ্নিত (*) ক্ষেত্র পূরণ করা আবশ্যক।</p>
                                  </div>
                              </div>
                          </div>

                          <div class="bg-white border border-gray-200 dark:bg-slate-700 dark:border-slate-600 rounded-lg p-5 mb-8 shadow-sm">
                              <h4 class="text-lg font-medium mb-4 text-gray-700 dark:text-gray-100">মারকায ধরণ নির্বাচন</h4>
                              <CategorySelect :modelValue="form.markaz_type" @update:modelValue="form.markaz_type = $event" class="!w-full" />
                          </div>

                          <div class="bg-white border border-gray-200 dark:bg-slate-700 dark:border-slate-600 rounded-lg p-5 shadow-sm">
                              <h4 class="text-lg font-medium mb-4 text-gray-700 dark:text-gray-100">মূল মাদ্রাসার তথ্য</h4>
                              <MainMadrasaInfo
                                  :form="form"
                                  :nocFile="nocFileForMadrahsa ?? undefined"
                                  :nocPreview="nocPreviewForMadrahsa ?? undefined"
                                  :resolutionFile="resolutionFileForMadrahsa ?? undefined"
                                  :resolutionPreview="resolutionPreviewForMadrahsa ?? undefined"
                                  @file-upload="(file, type) => handleFileUploadForMadrahsa(file, type)"
                                  @remove-file="removeFileForMadrahsa"
                                  @nextStep="goToNextStep"
                                  class="!w-full"
                              />
                          </div>

                          <div class="flex justify-between pt-6 mt-6 border-t border-gray-200 dark:border-slate-600">
                              <Button
                                  label="পূর্ববর্তী ধাপ"
                                  icon="pi pi-arrow-left"
                                  class="p-button-outlined"
                                  @click="step = 0"
                              />
                              <!-- 'পরবর্তী ধাপ' button removed; now only in MarkazConditions.vue -->
                          </div>
                      </div>
                  </TabPanel>

                  <!-- Associated Madrasas Tab -->
                  <TabPanel :value="2" :disabled="!canAccessStep[2]">
                      <template #header>
                          <div class="flex items-center" :class="{ 'opacity-50': !canAccessStep[2] }">
                              <i :class="getStepIcon(2)" class="mr-2" aria-hidden="true"></i>
                              <span class="font-medium text-gray-700 dark:text-gray-200">৩. সংযুক্ত মাদ্রাসা</span>
                              <i v-if="!canAccessStep[2]" class="pi pi-lock ml-2 text-yellow-500 dark:text-yellow-400" aria-hidden="true"></i>
                          </div>
                      </template>
                      <div class="bg-white dark:bg-slate-800 rounded-xl p-6">
                          <h3 class="text-xl font-bold mb-6 pb-2 border-b text-gray-800 dark:text-gray-100 border-gray-200 dark:border-slate-600">সংযুক্ত মাদ্রাসার তথ্য</h3>

                          <div class="bg-yellow-50 border-l-4 border-yellow-500 dark:bg-yellow-900/20 dark:border-yellow-700 p-4 mb-6 rounded-r-md">
                              <div class="flex">
                                  <div class="flex-shrink-0">
                                      <i class="pi pi-exclamation-triangle text-yellow-500 dark:text-yellow-400" aria-hidden="true"></i>
                                  </div>
                                  <div class="ml-3">
                                      <p class="text-sm text-yellow-700 dark:text-yellow-300">সংযুক্ত মাদ্রাসা যোগ করতে মাদ্রাসার নাম বা ইলহাক নম্বর দিয়ে অনুসন্ধান করুন। প্রতিটি মাদ্রাসার জন্য প্রয়োজনীয় তথ্য পূরণ করুন।</p>
                                  </div>
                              </div>
                          </div>

                          <div class="bg-white border border-gray-200 dark:bg-slate-700 dark:border-slate-600 rounded-lg p-5 shadow-sm">
                              <div class="flex justify-between items-center mb-4">
                                  <h4 class="text-lg font-medium text-gray-700 dark:text-gray-100">সংযুক্ত মাদ্রাসা সমূহ</h4>
                                  <Badge :value="rows.length" class="bg-blue-600 dark:bg-blue-500"></Badge>
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
                                  class="!w-full"
                              />
                          </div>

                          <div class="flex justify-between pt-6 mt-6 border-t border-gray-200 dark:border-slate-600">
                              <Button
                                  label="পূর্ববর্তী ধাপ"
                                  icon="pi pi-arrow-left"
                                  class="p-button-outlined"
                                  @click="step = 1"
                              />
                              <!-- 'পরবর্তী ধাপ' button removed; now only in MarkazConditions.vue -->
                          </div>
                      </div>
                  </TabPanel>

                  <!-- Requirements and Attachments Tab -->
                  <TabPanel :value="3" :disabled="!canAccessStep[3]">
                      <template #header>
                          <div class="flex items-center" :class="{ 'opacity-50': !canAccessStep[3] }">
                              <i :class="getStepIcon(3)" class="mr-2" aria-hidden="true"></i>
                              <span class="font-medium text-gray-700 dark:text-gray-200">৪. প্রয়োজনীয়তা ও সংযুক্তি</span>
                              <i v-if="!canAccessStep[3]" class="pi pi-lock ml-2 text-yellow-500 dark:text-yellow-400" aria-hidden="true"></i>
                          </div>
                      </template>
                      <div class="bg-white dark:bg-slate-800 rounded-xl p-6">
                          <h3 class="text-xl font-bold mb-6 pb-2 border-b text-gray-800 dark:text-gray-100 border-gray-200 dark:border-slate-600">প্রয়োজনীয়তা ও প্রমাণক সংযুক্তি</h3>

                          <div class="bg-green-50 border-l-4 border-green-500 dark:bg-green-900/20 dark:border-green-700 p-4 mb-6 rounded-r-md">
                              <div class="flex">
                                  <div class="flex-shrink-0">
                                      <i class="pi pi-check-circle text-green-500 dark:text-green-400" aria-hidden="true"></i>
                                  </div>
                                  <div class="ml-3">
                                      <p class="text-sm text-green-700 dark:text-green-300">মারকাজ চাওয়ার প্রয়োজনীয়তা বর্ণনা করুন। প্রয়োজনীয়তা ব্যাখ্যা অবশ্যই পূরণ করুন। ফাইল সংযুক্তি ঐচ্ছিক, তবে যদি থাকে PDF, JPG, বা PNG ফরম্যাটে আপলোড করুন।</p>
                                  </div>
                              </div>
                          </div>

                          <div class="bg-white border border-gray-200 dark:bg-slate-700 dark:border-slate-600 rounded-lg p-5 mb-6 shadow-sm">
                              <h4 class="text-lg font-medium mb-4 text-gray-700 dark:text-gray-100">
                                  মারকাজ প্রয়োজনীয়তা <span class="text-red-500">*</span>
                              </h4>
                              <RequirementsSection :modelValue="form.requirements" @update:modelValue="form.requirements = $event" class="!w-full" />
                              <p class="text-sm mt-2 text-gray-500 dark:text-gray-400">মারকাজ চাওয়ার প্রয়োজনীয়তা বিস্তারিত ব্যাখ্যা করুন। এই ক্ষেত্রটি পূরণ করা বাধ্যতামূলক।</p>
                          </div>

                          <div class="bg-white border border-gray-200 dark:bg-slate-700 dark:border-slate-600 rounded-lg p-5 shadow-sm">
                              <h4 class="text-lg font-medium mb-4 text-gray-700 dark:text-gray-100">প্রমাণক সংযুক্তি (ঐচ্ছিক)</h4>
                              <AttachmentSection
                                  :muhtamimFile="muhtamimFile ?? undefined"
                                  :muhtamimPreview="muhtamimPreview ?? undefined"
                                  :presidentFile="presidentFile ?? undefined"
                                  :presidentPreview="presidentPreview ?? undefined"
                                  :committeeFile="committeeFile ?? undefined"
                                  :committeePreview="committeePreview ?? undefined"
                                  @file-upload="handleFileUploadMumtahin"
                                  @remove-file="removeFileMumtahin"
                                  class="!w-full"
                              />
                              <div class="mt-4 p-3 rounded-md bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-300">
                                  <p class="text-sm">
                                      <i class="pi pi-info-circle mr-1" aria-hidden="true"></i>
                                      ফাইল সংযুক্তি ঐচ্ছিক। প্রয়োজনীয়তা ব্যাখ্যা পূরণ করলেই আবেদন জমা দেওয়া যাবে।
                                  </p>
                              </div>
                          </div>

                          <div v-if="formErrors.length > 0"
                              class="p-4 border rounded-md mt-6 mb-4 bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-700"
                          >
                              <h4 class="font-medium mb-2 text-red-700 dark:text-red-300">
                                  <i class="pi pi-exclamation-circle mr-2" aria-hidden="true"></i>নিম্নলিখিত সমস্যা সমাধান করুন:
                              </h4>
                              <ul class="list-disc pl-5">
                                  <li v-for="(error, key) in formErrors" :key="key" class="text-sm text-red-600 dark:text-red-300">
                                      {{ error }}
                                  </li>
                              </ul>
                          </div>

                          <div class="flex justify-between pt-6 mt-6 border-t border-gray-200 dark:border-slate-600">
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
                                  class="p-button-success p-button-raised shadow-md relative"
                                  :loading="loading"
                                  :disabled="!isStep3Valid || loading"
                                  @click="submitForm"
                              >
                                  <span v-if="!isStep3Valid" class="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2 text-xs rounded py-1 px-2 whitespace-nowrap shadow-lg bg-gray-800 text-white dark:bg-gray-700">
                                      প্রয়োজনীয়তা ব্যাখ্যা পূরণ করুন
                                  </span>
                              </Button>
                          </div>
                      </div>
                  </TabPanel>
              </TabView>
          </div>


        </div>
        <!-- Toast -->
        <Toast position="top-right" />
      </div>

</template>

<script setup lang="ts">

import AttachmentSection from '@/views/Pages/markaz/components/AttachmentSection.vue';
import CategorySelect from '@/views/Pages/markaz/components/CategorySelect.vue';
import DynamicMadrasas from '@/views/Pages/markaz/components/DynamicMadrasas.vue';
import MainMadrasaInfo from '@/views/Pages/markaz/components/MainMadrasaInfo.vue';
import MarkazConditions from '@/views/Pages/markaz/components/MarkazConditions.vue';
import RequirementsSection from '@/views/Pages/markaz/components/RequirementsSection.vue';
import Badge from 'primevue/badge';
import Button from 'primevue/button';
import TabPanel from 'primevue/tabpanel';
import TabView from 'primevue/tabview';
import Toast from 'primevue/toast';
import { useMarkazApply } from '@/composables/markaz/useMarkazApply';


const {
    // darkMode,                 // not needed — rely on Tailwind's dark: classes
    step,
    loading,
    formErrors,
    conditionsAgreed,
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
    submitForm,
    goToNextStep
} = useMarkazApply();

function handleContinue() {
    handleConditionsAccepted();
    goToNextStep();
}
</script>

<style scoped>
/* keep styles minimal — prefer Tailwind utilities; small scrollbars for modern browsers */
:deep(.scrollbar-thin) {
  scrollbar-width: thin;
}
:deep(.scrollbar-thumb-rounded-full::-webkit-scrollbar) {
  height: 8px;
  width: 8px;
}
:deep(.scrollbar-thumb-rounded-full::-webkit-scrollbar-thumb) {
  border-radius: 9999px;
}
</style>

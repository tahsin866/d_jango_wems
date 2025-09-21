<template>
  <div class="mb-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">আবেদনকৃত মাদরাসায় পরীক্ষা দিতে ইচ্ছুক মাদরাসার তালিকা ও তথ্য</h3>
    <div class="space-y-4">
      <div
        v-for="(row, index) in rows"
        :key="index"
        class="bg-white overflow-hidden shadow-sm sm:rounded-lg border border-gray-200"
      >
        <div class="p-6 bg-white border-b border-gray-200">
          <div class="mb-4 w-full">
            <label class="block font-medium text-sm text-gray-700 mb-2">
              মাদরাসা নির্বাচন করুন <span class="text-red-500">*</span>
            </label>
            <AutoComplete
              v-model="row.searchQuery"
              :suggestions="getSuggestions(index)"
              :optionLabel="'name'"
              @complete="(e) => searchMadrasas(e, index)"
              @item-select="(evt) => handleMadrasaSelect(evt, row, index)"
              @focus="() => preloadSuggestions(index)"
              :delay="0"
              :minLength="1"
              :showEmptyMessage="true"
              emptyMessage="কোন মাদরাসা পাওয়া যায়নি"
              placeholder="মাদরাসার নাম বা ইলহাক নম্বর দিয়ে খুঁজুন"
              class="w-full"
            >
              <template #option="{ option }">
                <div>
                  <div class="font-medium">{{ option.name }}</div>
                </div>
              </template>
              <template #empty>
                <div class="p-2 text-gray-500">কোন মাদরাসা পাওয়া যায়নি</div>
              </template>
            </AutoComplete>
            <div v-if="!row.madrasa_id" class="text-sm text-red-500 mt-1">মাদরাসা নির্বাচন করুন</div>
          </div>

          <!-- Student Numbers with InputNumber - Conditional Display Based on Markaz Type -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Darsiyat Fields -->
            <div v-if="showDarsiyatFields" class="flex flex-col">
              <label class="block font-medium text-sm text-gray-700 mb-2"> ফযীলত <span class="text-red-500">*</span> </label>
              <InputNumber
                v-model:number="row.fazilat"
                placeholder="ছাত্র সংখ্যা লিখুন"
                :min="0"
                showButtons
                buttonLayout="horizontal"
                decrementButtonClass="p-button-secondary"
                incrementButtonClass="p-button-secondary"
                inputClass="w-full h-10 rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm"
                class="w-full"
              />
              <div v-if="!row.fazilat && row.madrasa_id" class="text-sm text-red-500 mt-1">ফযীলত ছাত্র সংখ্যা লিখুন</div>
            </div>

            <div v-if="showDarsiyatFields" class="flex flex-col">
              <label class="block font-medium text-sm text-gray-700 mb-2"> সানাবিয়া ‍উলইয়া <span class="text-red-500">*</span> </label>
              <InputNumber
                v-model:number="row.sanabiya_ulya"
                placeholder="ছাত্র সংখ্যা লিখুন"
                :min="0"
                showButtons
                buttonLayout="horizontal"
                decrementButtonClass="p-button-secondary"
                incrementButtonClass="p-button-secondary"
                inputClass="w-full h-10 rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm"
                class="w-full"
              />
              <div v-if="!row.sanabiya_ulya && row.madrasa_id" class="text-sm text-red-500 mt-1">সানাবিয়া ‍উলইয়া ছাত্র সংখ্যা লিখুন</div>
            </div>

            <div v-if="showDarsiyatFields" class="flex flex-col">
              <label class="block font-medium text-sm text-gray-700 mb-2"> সানাবিয়া <span class="text-red-500">*</span> </label>
              <InputNumber
                v-model:number="row.sanabiya"
                placeholder="ছাত্র সংখ্যা লিখুন"
                :min="0"
                showButtons
                buttonLayout="horizontal"
                decrementButtonClass="p-button-secondary"
                incrementButtonClass="p-button-secondary"
                inputClass="w-full h-10 rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm"
                class="w-full"
              />
              <p v-if="isRequiredFieldEmpty(row, 'sanabiya')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
            </div>

            <div v-if="showDarsiyatFields" class="flex flex-col">
              <label class="block font-medium text-sm text-gray-700 mb-2"> মুতাওয়াসসিতা <span class="text-red-500">*</span> </label>
              <InputNumber
                v-model:number="row.mutawassita"
                placeholder="ছাত্র সংখ্যা লিখুন"
                :min="0"
                showButtons
                buttonLayout="horizontal"
                decrementButtonClass="p-button-secondary"
                incrementButtonClass="p-button-secondary"
                inputClass="w-full h-10 rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm"
                class="w-full"
              />
              <p v-if="isRequiredFieldEmpty(row, 'mutawassita')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
            </div>

            <div v-if="showDarsiyatFields" class="flex flex-col">
              <label class="block font-medium text-sm text-gray-700 mb-2"> ইবতেদাইয়্যাহ <span class="text-red-500">*</span> </label>
              <InputNumber
                v-model:number="row.ibtedaiyyah"
                placeholder="ছাত্র সংখ্যা লিখুন"
                :min="0"
                showButtons
                buttonLayout="horizontal"
                decrementButtonClass="p-button-secondary"
                incrementButtonClass="p-button-secondary"
                inputClass="w-full h-10 rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm"
                class="w-full"
              />
              <p v-if="isRequiredFieldEmpty(row, 'ibtedaiyyah')" class="text-sm text-red-500 mt-1">এই ফিল্ডটি পূরণ করা আবশ্যক</p>
            </div>

            <!-- Hifzul Quran Field -->
            <div v-if="showHifzField" class="flex flex-col">
              <label class="block font-medium text-sm text-gray-700 mb-2"> হিফজুল কোরান <span class="text-red-500">*</span> </label>
              <InputNumber
                v-model:number="row.hifzul_quran"
                placeholder="ছাত্র সংখ্যা লিখুন"
                :min="0"
                showButtons
                buttonLayout="horizontal"
                decrementButtonClass="p-button-secondary"
                incrementButtonClass="p-button-secondary"
                inputClass="w-full h-10 rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm"
                class="w-full"
              />
              <div v-if="!row.hifzul_quran && row.madrasa_id" class="text-sm text-red-500 mt-1">হিফজুল কোরান ছাত্র সংখ্যা লিখুন</div>
            </div>

            <!-- Kirat Field -->
            <div v-if="showKiratField" class="flex flex-col">
              <label class="block font-medium text-sm text-gray-700 mb-2"> ইলমুল কিরআত <span class="text-red-500">*</span> </label>
              <InputNumber
                v-model:number="row.qirat"
                placeholder="ছাত্র সংখ্যা লিখুন"
                :min="0"
                showButtons
                buttonLayout="horizontal"
                decrementButtonClass="p-button-secondary"
                incrementButtonClass="p-button-secondary"
                inputClass="w-full h-10 rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm"
                class="w-full"
              />
              <div v-if="!row.qirat && row.madrasa_id" class="text-sm text-red-500 mt-1">ইলমুল কিরআত ছাত্র সংখ্যা লিখুন</div>
            </div>

            <div v-if="rows.length > 1" class="flex items-end">
              <Button @click="() => emit('remove-row', index)" label="সারি মুছুন" icon="pi pi-trash" severity="danger" class="w-full" />
            </div>
          </div>

          <!-- File Uploads for NOC & Resolution -->
          <div class="mt-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">প্রয়োজনীয় ডকুমেন্টস <span class="text-red-500">*</span></h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="border border-gray-300 rounded-md p-4">
                <div class="flex items-center justify-between mb-2">
                  <label class="block font-medium text-sm text-gray-700"> পূর্বের মাদরাসার অনাপত্তিপত্র <span class="text-red-500">*</span> </label>
                  <div v-if="row.files.nocPreview" class="flex items-center space-x-2">
                    <a :href="row.files.nocPreview" target="_blank" class="inline-flex items-center px-2 py-1 bg-gray-100 border border-gray-300 rounded-md text-xs text-gray-700"> প্রিভিউ </a>
                    <Button label="মুছুন" icon="pi pi-times" severity="danger" size="small" @click="() => emit('remove-file', 'noc', index)" class="ml-2" />
                  </div>
                </div>

                <FileUpload
                  mode="basic"
                  accept="application/pdf,image/*"
                  :auto="true"
                  chooseLabel="ফাইল নির্বাচন করুন"
                  @select="(e) => handleFileSelect(e, 'noc', index)"
                  class="w-full"
                />
                <div v-if="!row.files.noc && row.madrasa_id" class="text-sm text-red-500 mt-1">অনাপত্তিপত্র আপলোড করুন</div>
              </div>

              <div class="border border-gray-300 rounded-md p-4">
                <div class="flex items-center justify-between mb-2">
                  <label class="block font-medium text-sm text-gray-700"> বর্তমান মাদরাসার সম্মতিপত্র <span class="text-red-500">*</span> </label>
                  <div v-if="row.files.resolutionPreview" class="flex items-center space-x-2">
                    <a :href="row.files.resolutionPreview" target="_blank" class="inline-flex items-center px-2 py-1 bg-gray-100 border border-gray-300 rounded-md text-xs text-gray-700"> প্রিভিউ </a>
                    <Button label="মুছুন" icon="pi pi-times" severity="danger" size="small" @click="() => emit('remove-file', 'resolution', index)" class="ml-2" />
                  </div>
                </div>

                <FileUpload
                  mode="basic"
                  accept="application/pdf,image/*"
                  :auto="true"
                  chooseLabel="ফাইল নির্বাচন করুন"
                  @select="(e) => handleFileSelect(e, 'resolution', index)"
                  class="w-full"
                />
                <div v-if="!row.files.resolution && row.madrasa_id" class="text-sm text-red-500 mt-1">সম্মতিপত্র আপলোড করুন</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Add New Row Button -->
      <div>
        <Button @click="() => emit('add-row')" label="নতুন সারি যোগ করুন" icon="pi pi-plus" class="p-button-raised p-button-secondary" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, PropType } from 'vue';
import AutoComplete from 'primevue/autocomplete';
import Button from 'primevue/button';
import FileUpload from 'primevue/fileupload';
import InputNumber from 'primevue/inputnumber';

/**
 * Types
 */
export interface MadrashaType {
  id?: number | string;
  name?: string;
  elhaqno?: string | number;
}

export interface RowType {
  searchQuery?: string;
  madrasa_id?: number | string | null;
  fazilat?: number | null;
  sanabiya_ulya?: number | null;
  sanabiya?: number | null;
  mutawassita?: number | null;
  ibtedaiyyah?: number | null;
  hifzul_quran?: number | null;
  qirat?: number | null;
  selectedMadrasha?: MadrashaType | null;
  isOpen?: boolean;
  files: {
    noc?: File | null;
    nocPreview?: string | null;
    resolution?: File | null;
    resolutionPreview?: string | null;
  };
}

const props = defineProps<{
  rows: RowType[];
  madrashas: MadrashaType[];
  filteredOptions?: (row: RowType) => MadrashaType[];
  markazType: string;
}>();

const emit = defineEmits<{
  (e: 'add-row'): void;
  (e: 'remove-row', index: number): void;
  (e: 'file-upload', file: File, type: 'noc' | 'resolution', index: number): void;
  (e: 'remove-file', type: 'noc' | 'resolution', index: number): void;
  (e: 'select-option', madrasha: MadrashaType, row: RowType): void;
}>();

/**
 * Computed helpers for field visibility
 */
const showDarsiyatFields = computed(() => props.markazType === 'দরসিয়াত');
const showHifzField = computed(() => props.markazType === 'তাহফিজুল কোরআন');
const showKiratField = computed(() => props.markazType === 'কিরাআত');

/**
 * Cache suggestions for each row separately
 */
const suggestionCache = ref<{ [key: number]: MadrashaType[] }>({});
const isLoading = ref<{ [key: number]: boolean }>({});

interface AutoCompleteEvent {
  originalEvent?: Event;
  query?: string;
}

/**
 * Search madrasas with API call
 */
async function searchMadrasas(event: AutoCompleteEvent, index: number) {
  const query = (event?.query ?? '').toString().trim();

  // Clear suggestions if query is empty
  if (!query) {
    suggestionCache.value[index] = [];
    return;
  }

  isLoading.value[index] = true;

  try {
    // API call to search
    const response = await fetch(`http://127.0.0.1:8000/api/markaz/search-madrasa/?elhaq=${encodeURIComponent(query)}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Process and format the data - ensure elhaqno is properly handled
    const suggestions: MadrashaType[] = Array.isArray(data) ? data.map((item: any) => {
      const elhaqno = item.elhaqno;

      return {
        id: item.id || '',
        name: item.mname || '',
        // Only set elhaqno if it exists and is not null/undefined/empty
        elhaqno: (elhaqno !== null && elhaqno !== undefined && elhaqno !== '') ? elhaqno.toString() : null
      };
    }).filter(item => item.name) : []; // Filter out items without names

    suggestionCache.value[index] = suggestions;

  } catch (error) {
    console.error('Search error:', error);
    suggestionCache.value[index] = [];
  } finally {
    isLoading.value[index] = false;
  }
}

/**
 * Get cached suggestions for a specific row
 */
function getSuggestions(index: number): MadrashaType[] {
  return suggestionCache.value[index] || [];
}

/**
 * Load initial suggestions on focus
 */
async function preloadSuggestions(index: number) {
  // Don't preload, just clear cache
  suggestionCache.value[index] = [];
}

/**
 * Handle madrasa selection
 */
function handleMadrasaSelect(evt: any, row: RowType, index: number) {
  const selectedMadrasha = evt.value as MadrashaType;
  // Always set only the madrasa name, never any ইলহাক info
  row.searchQuery = selectedMadrasha.name || '';
  row.madrasa_id = selectedMadrasha.id;
  row.selectedMadrasha = {
    ...selectedMadrasha,
    name: selectedMadrasha.name || ''
  };

  // Clear suggestions after selection
  suggestionCache.value[index] = [];

  // Emit the selection event with clean data
  emit('select-option', {
    ...selectedMadrasha,
    name: selectedMadrasha.name || ''
  }, row);

  console.log('Selected madrasha (clean):', { ...selectedMadrasha, name: selectedMadrasha.name || '' });
}

/**
 * File upload handler
 */
function handleFileSelect(event: any, type: 'noc' | 'resolution', index: number) {
  try {
    let file: File | null = null;

    // Extract file from various event formats
    if (event instanceof File) {
      file = event;
    } else if (event?.files?.length > 0) {
      file = event.files[0];
    } else if (event?.target?.files?.length > 0) {
      file = event.target.files[0];
    } else if (event?.originalEvent?.target?.files?.length > 0) {
      file = event.originalEvent.target.files[0];
    }

    if (file) {
      emit('file-upload', file, type, index);
    } else {
      console.warn('No file found in event:', event);
    }
  } catch (error) {
    console.error('File selection error:', error);
  }
}

/**
 * Check if required field is empty
 */
type RequiredFieldName = 'fazilat' | 'sanabiya_ulya' | 'sanabiya' | 'mutawassita' | 'ibtedaiyyah' | 'hifzul_quran' | 'qirat';

function isRequiredFieldEmpty(row: RowType, field: RequiredFieldName): boolean {
  if (!row.madrasa_id) return false;

  const markazType = props.markazType;
  const value = (row as any)[field];

  if (markazType === 'দরসিয়াত') {
    const required: RequiredFieldName[] = ['fazilat', 'sanabiya_ulya', 'sanabiya', 'mutawassita', 'ibtedaiyyah'];
    if (required.includes(field)) {
      return !value || value === 0;
    }
  }

  if (markazType === 'তাহফিজুল কোরআন' && field === 'hifzul_quran') {
    return !value || value === 0;
  }

  if (markazType === 'কিরাআত' && field === 'qirat') {
    return !value || value === 0;
  }

  return false;
}
</script>

<style scoped>
:deep(.p-autocomplete) {
  width: 100%;
}
:deep(.p-autocomplete-input) {
  width: 100%;
  height: 40px;
}
:deep(.p-autocomplete-panel) {
  z-index: 1000;
}
:deep(.p-fileupload-buttonbar) {
  padding: 0;
}
:deep(.p-fileupload-content) {
  padding: 0;
}
</style>

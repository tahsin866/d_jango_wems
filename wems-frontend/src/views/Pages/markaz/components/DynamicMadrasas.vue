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
          <!-- Improved AutoComplete with Immediate Results -->
          <div class="mb-4 w-full">
            <label class="block font-medium text-sm text-gray-700 mb-2">
              মাদরাসা নির্বাচন করুন <span class="text-red-500">*</span>
            </label>

            <AutoComplete
              v-model="row.searchQuery"
              :suggestions="getSuggestions(row, index)"
              :optionLabel="'name'"
              @complete="(e) => searchMadrasas(e, row, index)"
              @item-select="(evt) => {
                const elhaq = evt.value.elhaqno || evt.value.ElhaqNo || '';
                row.searchQuery = elhaq
                  ? `${evt.value.name} (ইলহাক: ${elhaq})`
                  : evt.value.name;
                row.madrasa_id = evt.value.id;
                emit('select-option', evt.value as MadrashaType, row);
              }"
              @focus="() => preloadSuggestions(row)"
              :delay="0"
              :minLength="1"
              :showEmptyMessage="true"
              emptyMessage="কোন মাদরাসা পাওয়া যায়নি"
              placeholder="মাদরাসার নাম বা ইলহাক নম্বর দিয়ে খুঁজুন"
              class="w-full"
            >
              <template #option="{ option }">
                <div>
                  <div class="font-medium">{{ option.name }} <span v-if="option.elhaqno">(ইলহাক: {{ option.elhaqno }})</span></div>
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

/**
 * Props & Emits with types so TS plugins (Volar) can infer correctly
 */
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
 * Computed helpers for field visibility depending on markaz type
 */
const showDarsiyatFields = computed(() => props.markazType === 'দরসিয়াত');
const showHifzField = computed(() => props.markazType === 'তাহফিজুল কোরআন');
const showKiratField = computed(() => props.markazType === 'কিরাআত');

/**
 * Suggestion cache keyed by row object to avoid recomputing suggestions every keystroke
 */
type SuggestionCacheEntry = { suggestions?: MadrashaType[] };
const suggestionCache = ref<{ [key: number]: SuggestionCacheEntry }>({});

/**
 * AutoComplete event shape (from PrimeVue typical payload)
 */
interface AutoCompleteEvent {
  originalEvent?: Event;
  query?: string;
}

/**
 * Search logic for auto-complete (case-insensitive, supports ElhaqNo search)
 */
async function searchMadrasas(event: AutoCompleteEvent, row: RowType, index: number) {
  const query = (event?.query ?? '').toString().trim();

  if (!query) {
    suggestionCache.value[index] = { suggestions: [] };
    row.isOpen = true;
    return;
  }

  try {
    // Fixed URL - include full backend URL
    const response = await fetch(`http://127.0.0.1:8000/api/markaz/search-madrasa/?elhaq=${encodeURIComponent(query)}`);

    if (!response.ok) {
      console.error(`API Error: ${response.status} ${response.statusText}`);
      throw new Error('API error');
    }

    const data = await response.json();
    console.log('API response:', data); // Debug log

    // Only show suggestions if elhaqno exactly matches input
    const suggestions = Array.isArray(data)
      ? data
          .filter((item: any) => (item.elhaqno || '').toLowerCase() === query.toLowerCase())
          .map((item: any) => ({
            name: item.mname,
            elhaqno: item.elhaqno,
            id: item.id ?? item.elhaqno,
          }))
      : [];

    console.log('Mapped suggestions:', suggestions); // Debug log

    suggestionCache.value[index] = { suggestions };
    row.isOpen = true;

  } catch (err) {
    console.error('Search API Error:', err);
    suggestionCache.value[index] = { suggestions: [] };
    row.isOpen = true;
  }
}

/**
 * Return suggestions from cache (or empty array)
 */
function getSuggestions(row: RowType, index: number): MadrashaType[] {
  return suggestionCache.value[index]?.suggestions ?? [];
}

/**
 * On focus, preload first N suggestions
 */
async function preloadSuggestions(row: RowType) {
  // On focus, do not call API with empty query. Just show empty suggestions.
  // Use index-based assignment for cache
  const index = props.rows.findIndex((r: RowType) => r === row);
  suggestionCache.value[index] = { suggestions: [] };
  row.isOpen = true;
}

/**
 * Robust file select handler: extracts a File from the various event shapes PrimeVue/File input may provide
 */
function handleFileSelect(
  event:
    | Event
    | { files?: FileList | File[] }
    | { originalEvent?: Event; files?: FileList | File[] }
    | File
    | Blob,
  type: 'noc' | 'resolution',
  index: number
) {
  try {
    // Direct File/Blob
    if (event instanceof File || event instanceof Blob) {
      emit('file-upload', event as File, type, index);
      return;
    }

    // If it's an object with files property (PrimeVue FileUpload often has event.files)
    if (event && typeof event === 'object') {
      // check event.files as FileList or Array

      const filesCandidate = (event as any).files;
      if (filesCandidate) {
        const file = (filesCandidate instanceof FileList ? filesCandidate[0] : Array.isArray(filesCandidate) ? filesCandidate[0] : null) as File | null;
        if (file) {
          emit('file-upload', file, type, index);
          return;
        }
      }


      const original = (event as any).originalEvent;
      if (original && original.target && (original.target as HTMLInputElement).files) {
        const filelist = (original.target as HTMLInputElement).files!;
        if (filelist.length > 0) {
          emit('file-upload', filelist[0], type, index);
          return;
        }
      }

      // scan for File inside object properties
      for (const key in event as any) {
        const value = (event as any)[key];
        if (value instanceof File) {
          emit('file-upload', value as File, type, index);
          return;
        }
        if (Array.isArray(value) && value.length > 0 && value[0] instanceof File) {
          emit('file-upload', value[0] as File, type, index);
          return;
        }
      }
    }

    // As fallback, try to read target.files from DOM Event
    if (event instanceof Event && event.target) {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        emit('file-upload', target.files[0], type, index);
        return;
      }
    }

    console.warn('No file found in select event', event);
  } catch (err) {
    // keep errors visible for debugging
    // eslint-disable-next-line no-console
    console.error('Error extracting file from event', err);
  }
}

/**
 * Required field names for runtime checking
 */
type RequiredFieldName =
  | 'fazilat'
  | 'sanabiya_ulya'
  | 'sanabiya'
  | 'mutawassita'
  | 'ibtedaiyyah'
  | 'hifzul_quran'
  | 'qirat';

/**
 * Returns true when a required field is empty (used to show validation message)
 */
function isRequiredFieldEmpty(row: RowType, field: RequiredFieldName): boolean {
  if (!row.madrasa_id) return false; // only validate when madrasa selected

  const markazType = props.markazType;

  if (markazType === 'দরসিয়াত') {
    const required: RequiredFieldName[] = ['fazilat', 'sanabiya_ulya', 'sanabiya', 'mutawassita', 'ibtedaiyyah'];
    if (required.includes(field)) {
      const val = (row as any)[field];
      return val === undefined || val === null || val === 0;
    }
  }

  if (markazType === 'তাহফিজুল কোরআন' && field === 'hifzul_quran') {
    const val = row.hifzul_quran;
    return val === undefined || val === null || val === 0;
  }

  if (markazType === 'কিরাআত' && field === 'qirat') {
    const val = row.qirat;
    return val === undefined || val === null || val === 0;
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

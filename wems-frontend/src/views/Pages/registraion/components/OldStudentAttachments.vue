<template>
  <div class="bg-white border border-gray-200 rounded-sm shadow-md">
    <div class="bg-white border border-gray-300 p-6 rounded-sm shadow-sm">
      <div class="flex items-center gap-3 mb-6">
        <div class="p-2 rounded-sm bg-gray-100">
          <i class="fas fa-paperclip text-gray-700"></i>
        </div>
        <h3 class="text-gray-800 text-xl font-bold">সংযুক্তি</h3>
      </div>
      <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
        <!-- Student Photo -->
        <div class="space-y-3">
          <label class="text-gray-700 text-lg block font-medium">
            ছাত্রের ছবি (পাসপোর্ট সাইজ এবং নীল ব্যাকগ্রাইন্ড হতে হবে)
          </label>
          <div class="relative">
            <div
              class="flex bg-gray-50 border-2 border-dashed border-gray-300 justify-between p-4 rounded-sm duration-200 hover:border-gray-500 items-center transition-colors"
              role="status"
              aria-live="polite"
            >
              <span class="text-gray-600">
                {{ studentPhotoName || 'ফাইল আপলোড করুন' }}
              </span>

              <div v-if="studentPhotoPreview" class="flex items-center pointer-events-auto relative space-x-2 z-10">
                <a :href="studentPhotoPreview" target="_blank" rel="noopener" class="text-gray-600 hover:text-gray-800 flex items-center gap-1">
                  <i class="fas fa-eye"></i>
                  <span>প্রিভিউ</span>
                </a>
                <button @click.stop="onRemove('studentPhoto')" type="button" class="text-red-600 hover:text-red-800 flex items-center gap-1">
                  <i class="fas fa-trash-alt"></i>
                  <span>মুছুন</span>
                </button>
              </div>
            </div>

            <input
              aria-label="ছাত্রের ছবি আপলোড করুন"
              type="file"
              @change="e => onFile(e, 'studentPhoto')"
              class="h-full w-full absolute cursor-pointer inset-0 opacity-0 z-0"
              accept="image/*,.pdf,.doc,.docx"
            />
          </div>
        </div>

        <!-- Birth Certificate/NID -->
        <div class="space-y-3">
          <label class="text-gray-700 text-lg block font-medium">
            জন্ম নিবন্ধন/এন আইডি সংযুক্তি করুন
          </label>
          <div class="relative">
            <div
              class="flex bg-gray-50 border-2 border-dashed border-gray-300 justify-between p-4 rounded-sm duration-200 hover:border-gray-500 items-center transition-colors"
              role="status"
              aria-live="polite"
            >
              <span class="text-gray-600">
                {{ nidAttachmentName || 'ফাইল আপলোড করুন' }}
              </span>

              <div v-if="nidAttachmentPreview" class="flex items-center pointer-events-auto relative space-x-2 z-10">
                <a :href="nidAttachmentPreview" target="_blank" rel="noopener" class="text-gray-600 hover:text-gray-800 flex items-center gap-1">
                  <i class="fas fa-eye"></i>
                  <span>প্রিভিউ</span>
                </a>
                <button @click.stop="onRemove('nidAttachment')" type="button" class="text-red-600 hover:text-red-800 flex items-center gap-1">
                  <i class="fas fa-trash-alt"></i>
                  <span>মুছুন</span>
                </button>
              </div>
            </div>

            <input
              aria-label="জন্ম নিবন্ধন/এনআইডি ফাইল আপলোড করুন"
              type="file"
              @change="e => onFile(e, 'nidAttachment')"
              class="h-full w-full absolute cursor-pointer inset-0 opacity-0 z-0"
              accept="image/*,.pdf,.doc,.docx"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  studentPhoto?: File | null;
  studentPhotoPreview?: string | null;
  nidAttachment?: File | null;
  nidAttachmentPreview?: string | null;
}>();

const emit = defineEmits<{
  (e: 'file-upload', event: Event, type: 'studentPhoto' | 'nidAttachment'): void;
  (e: 'remove-file', type: 'studentPhoto' | 'nidAttachment'): void;
}>();

const studentPhotoName = computed(() => {
  return props.studentPhoto?.name ?? '';
});

const nidAttachmentName = computed(() => {
  return props.nidAttachment?.name ?? '';
});

function onFile(e: Event, type: 'studentPhoto' | 'nidAttachment') {
  // forward raw change event to parent so parent can handle File/preview creation
  emit('file-upload', e, type);
}

function onRemove(type: 'studentPhoto' | 'nidAttachment') {
  emit('remove-file', type);
}
</script>

<style scoped>
/* Professional styling enhancements */
.transition-colors {
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.rounded-sm {
  border-radius: 0.125rem;
}

/* Custom focus styles for accessibility */
input:focus {
  outline: none;
}

/* Hover effect for file upload area */
.border-dashed:hover {
  border-style: solid;
}
</style>

<template>
  <div
    class="rounded-sm shadow-md border transition-all duration-300"
    :class="[!isDark ? 'bg-white border-gray-300' : 'dark:bg-slate-800 dark:border-slate-600']"
  >
    <div
      class="bg-gradient-to-r rounded-t-sm overflow-hidden px-6 py-4 relative shadow-sm"
      :class="[!isDark ? 'from-gray-700 to-gray-600' : 'dark:from-gray-900 dark:to-gray-800']"
    >
      <div class="flex gap-4 items-center relative z-10">
        <div class="p-2 rounded-sm bg-white bg-opacity-20 backdrop-blur-sm">
          <i class="text-2xl text-white fa-graduation-cap fas"></i>
        </div>
        <h5 class="text-white text-xl font-bold tracking-wide">বিগত পরীক্ষার তথ্য</h5>
      </div>
    </div>

    <div :class="[!isDark ? 'bg-gray-100' : 'dark:bg-slate-900']" class="p-6">
      <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
        <!-- Madrasha -->
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-school fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            মাদরাসা
          </label>
          <div class="relative">
            <input v-model="localPast.Madrasha" type="text" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>

        <!-- Markaj -->
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-school fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            মারকায
          </label>
          <div class="relative">
            <input v-model="localPast.Markaj" type="text" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>

        <!-- Class -->
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-layer-group fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            শ্রেণী
          </label>
          <div class="relative">
            <input v-model="localPast.Class" type="text" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>

        <!-- Roll Number -->
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-id-card fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            রোল নম্বর
          </label>
          <div class="relative">
            <input v-model="localPast.Roll" type="text" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>

        <!-- Registration ID -->
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-id-card fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            রেজিস্ট্রেশন আইডি
          </label>
          <div class="relative">
            <input v-model="localPast.reg_id" type="text" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>

        <!-- Date of Birth -->
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-calendar-alt fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            জন্ম-তারিখ
          </label>
          <div class="relative">
            <input v-model="localPast.DateofBirth" type="date" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>

        <!-- Result -->
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-trophy fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            ফলাফল
          </label>
          <div class="relative">
            <input v-model="localPast.Division" type="text" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>

        <!-- পরীক্ষার্থীর ধরন -->
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-user-graduate fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            পরীক্ষার্থীর ধরন
          </label>
          <div class="relative">
            <input v-model="localCurrent.student_type" type="text" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>

        <!-- অনিয়মিত হলে পরীক্ষা দিতে হবে এমন কিতাবের নাম -->
        <div class="relative" v-if="localCurrent.student_type === 'অনিয়মিত যেমনী' || localCurrent.student_type === 'অনিয়মিত অন্যান্য'">
          <label :class="[!isDark ? 'text-gray-700' : 'dark:text-gray-300']" class="flex text-lg font-semibold gap-2 items-center mb-2">
            <i class="fa-book fas" :class="[!isDark ? 'text-gray-600' : 'dark:text-gray-400']"></i>
            অনিয়মিত হলে পরীক্ষা দিতে হবে এমন কিতাবের নাম
          </label>
          <div class="relative">
            <input v-model="localCurrent.irregular_subjects" type="text" disabled
              :class="[!isDark ? 'bg-white border border-gray-300 text-gray-700' : 'dark:bg-slate-800 dark:border-slate-700 dark:text-gray-200', 'rounded-sm w-full cursor-not-allowed pl-4 pr-3 py-3 shadow-sm transition-colors']" />
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue';

type PastExamForm = {
  Madrasha?: string;
  Markaj?: string;
  Class?: string;
  Roll?: string;
  reg_id?: string;
  DateofBirth?: string;
  Division?: string;
  [key: string]: any;
};

type CurrentExamForm = {
  student_type?: string;
  irregular_subjects?: string;
  [key: string]: any;
};

const props = defineProps<{
  pastExamForm?: PastExamForm;
  currentExamForm?: CurrentExamForm;
}>();

const isDark = computed(() => document.documentElement.classList.contains('dark'));

// Default dummy data (used if parent doesn't provide props)
const DEFAULT_PAST: PastExamForm = {
  Madrasha: 'আব্দুল্লাহ মাদরাসা',
  Markaj: 'মারকায-১',
  Class: '৮ম',
  Roll: '101',
  reg_id: 'REG-2025-101',
  DateofBirth: '2008-02-14',
  Division: 'জায়্যিদ'
};

const DEFAULT_CURRENT: CurrentExamForm = {
  student_type: 'নিয়মিত',
  irregular_subjects: ''
};

// Create local reactive copies to avoid mutating parent props directly
const localPast = reactive<PastExamForm>({
  Madrasha: props.pastExamForm?.Madrasha ?? DEFAULT_PAST.Madrasha,
  Markaj: props.pastExamForm?.Markaj ?? DEFAULT_PAST.Markaj,
  Class: props.pastExamForm?.Class ?? DEFAULT_PAST.Class,
  Roll: props.pastExamForm?.Roll ?? DEFAULT_PAST.Roll,
  reg_id: props.pastExamForm?.reg_id ?? DEFAULT_PAST.reg_id,
  DateofBirth: props.pastExamForm?.DateofBirth ?? DEFAULT_PAST.DateofBirth,
  Division: props.pastExamForm?.Division ?? DEFAULT_PAST.Division
});

const localCurrent = reactive<CurrentExamForm>({
  student_type: props.currentExamForm?.student_type ?? DEFAULT_CURRENT.student_type,
  irregular_subjects: props.currentExamForm?.irregular_subjects ?? DEFAULT_CURRENT.irregular_subjects
});

// Keep local copies in sync when parent updates props
watch(
  () => props.pastExamForm,
  (v) => {
    if (!v) return;
    Object.assign(localPast, {
      Madrasha: v.Madrasha ?? DEFAULT_PAST.Madrasha,
      Markaj: v.Markaj ?? DEFAULT_PAST.Markaj,
      Class: v.Class ?? DEFAULT_PAST.Class,
      Roll: v.Roll ?? DEFAULT_PAST.Roll,
      reg_id: v.reg_id ?? DEFAULT_PAST.reg_id,
      DateofBirth: v.DateofBirth ?? DEFAULT_PAST.DateofBirth,
      Division: v.Division ?? DEFAULT_PAST.Division
    });
  },
  { deep: true, immediate: true }
);

watch(
  () => props.currentExamForm,
  (v) => {
    if (!v) return;
    Object.assign(localCurrent, {
      student_type: v.student_type ?? DEFAULT_CURRENT.student_type,
      irregular_subjects: v.irregular_subjects ?? DEFAULT_CURRENT.irregular_subjects
    });
  },
  { deep: true, immediate: true }
);
</script>

<style scoped>
/* Professional styling enhancements */
.transition-all {
  transition: all 0.3s ease;
}

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

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* Custom focus styles for accessibility */
input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(107, 114, 128, 0.2);
}

/* Disabled state improvements */
input:disabled {
  opacity: 0.85;
}
</style>

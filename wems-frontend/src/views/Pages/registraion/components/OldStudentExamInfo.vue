<template>
  <div
    class="rounded-lg shadow"
    :class="[!isDark ? 'bg-white' : 'dark:bg-slate-800']"
  >
    <div
      class="bg-gradient-to-r rounded-t-md overflow-hidden px-6 py-3 relative"
      :class="[!isDark ? 'from-emerald-800 to-emerald-600' : 'dark:from-emerald-900 dark:to-emerald-700']"
    >
      <div class="flex gap-3 items-center relative z-10">
        <i class="text-2xl text-white fa-graduation-cap fas"></i>
        <h5 class="text-white text-xl font-arabic">বিগত পরীক্ষার তথ্য</h5>
      </div>
    </div>
    <div :class="[!isDark ? 'bg-opacity-5 bg-white' : 'dark:bg-slate-900 dark:bg-opacity-90']" class="p-6">
      <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
        <!-- Madrasha -->
        <div class="relative">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            <i class="fa-school fas" :class="[!isDark ? 'text-emerald-600' : 'dark:text-emerald-400']"></i>
            মাদরাসা
          </label>
          <input v-model="localPast.Madrasha" type="text" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
        </div>

        <!-- Markaj -->
        <div class="relative">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            <i class="fa-school fas" :class="[!isDark ? 'text-emerald-600' : 'dark:text-emerald-400']"></i>
            মারকায
          </label>
          <input v-model="localPast.Markaj" type="text" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
        </div>

        <!-- Class -->
        <div class="relative">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            <i class="fa-layer-group fas" :class="[!isDark ? 'text-emerald-600' : 'dark:text-emerald-400']"></i>
            শ্রেণী
          </label>
          <input v-model="localPast.Class" type="text" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
        </div>

        <!-- Roll Number -->
        <div class="relative">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            <i class="fa-id-card fas" :class="[!isDark ? 'text-emerald-600' : 'dark:text-emerald-400']"></i>
            রোল নম্বর
          </label>
          <input v-model="localPast.Roll" type="text" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
        </div>

        <!-- Registration ID -->
        <div class="relative">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            <i class="fa-id-card fas" :class="[!isDark ? 'text-emerald-600' : 'dark:text-emerald-400']"></i>
            রেজিস্ট্রেশন আইডি
          </label>
          <input v-model="localPast.reg_id" type="text" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
        </div>

        <!-- Date of Birth -->
        <div class="relative">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            <i class="fa-calendar-alt fas" :class="[!isDark ? 'text-emerald-600' : 'dark:text-emerald-400']"></i>
            জন্ম-তারিখ
          </label>
          <input v-model="localPast.DateofBirth" type="date" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
        </div>

        <!-- Result -->
        <div class="relative">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            <i class="fa-calendar-alt fas" :class="[!isDark ? 'text-emerald-600' : 'dark:text-emerald-400']"></i>
            ফলাফল
          </label>
          <input v-model="localPast.Division" type="text" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
        </div>

        <!-- পরীক্ষার্থীর ধরন -->
        <div class="relative">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            পরীক্ষার্থীর ধরন
          </label>
          <input v-model="localCurrent.student_type" type="text" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
        </div>

        <!-- অনিয়মিত হলে পরীক্ষা দিতে হবে এমন কিতাবের নাম -->
        <div class="relative" v-if="localCurrent.student_type === 'অনিয়মিত যেমনী' || localCurrent.student_type === 'অনিয়মিত অন্যান্য'">
          <label :class="[!isDark ? 'text-emerald-700' : 'dark:text-emerald-300']" class="flex text-lg font-medium gap-2 items-center mb-1">
            অনিয়মিত হলে পরীক্ষা দিতে হবে এমন কিতাবের নাম
          </label>
          <input v-model="localCurrent.irregular_subjects" type="text" disabled
            :class="[!isDark ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'dark:bg-emerald-900 dark:border-emerald-800 dark:text-emerald-200', 'rounded-md w-full cursor-not-allowed pl-4 pr-3 py-2']" />
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
/* Only Tailwind CSS used for styling */
</style>
